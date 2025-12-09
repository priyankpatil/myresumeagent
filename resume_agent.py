"""
Resume Q&A Agent - Core logic for processing and querying resumes
"""
import os
import pickle
import re
import numpy as np
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import faiss
from pypdf import PdfReader
from groq import Groq


class ResumeAgent:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", groq_model: str = "llama-3.1-8b-instant"):
        """
        Initialize the Resume Agent with a sentence transformer model and Groq LLM.
        
        Args:
            model_name: Hugging Face model name for embeddings
            groq_model: Groq model name for answer generation (default: llama-3.1-8b-instant)
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []
        self.embeddings = None
        
        # Initialize Groq client
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it with your Groq API key.")
        self.groq_client = Groq(api_key=groq_api_key)
        self.groq_model = groq_model
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks for better context.
        
        Args:
            text: Input text
            chunk_size: Size of each chunk in characters
            overlap: Number of characters to overlap between chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        return chunks
    
    def process_resume(self, pdf_path: str) -> Dict:
        """
        Process a resume PDF and create embeddings.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with processed data
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Chunk the text
        chunks = self.chunk_text(text)
        self.texts = chunks
        
        # Create embeddings (ensure float32 to save memory)
        print(f"Creating embeddings for {len(chunks)} chunks...")
        self.embeddings = self.model.encode(chunks, show_progress_bar=True).astype('float32')
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)
        
        return {
            "chunks": len(chunks),
            "text_length": len(text)
        }
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant text chunks based on query.
        
        Args:
            query: User's question
            top_k: Number of top results to return
            
        Returns:
            List of relevant text chunks with scores
        """
        if self.index is None or len(self.texts) == 0:
            return []
        
        # Encode query (ensure float32 to save memory)
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        
        # Ensure query_embedding is 2D (FAISS requires 2D array even for single query)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Ensure query_embedding is contiguous (FAISS requirement)
        query_embedding = np.ascontiguousarray(query_embedding, dtype=np.float32)
        
        # Search - FAISS search signature: search(x, k) where x is query vectors and k is number of results
        # Don't use hasattr() on SWIG-wrapped FAISS objects as it triggers attribute access errors
        try:
            distances, indices = self.index.search(query_embedding, top_k)
        except (TypeError, AttributeError) as e:
            error_msg = str(e)
            # Check if this is a FAISS version mismatch error
            if "missing" in error_msg and "required positional arguments" in error_msg:
                print(f"⚠ FAISS version mismatch detected. Recreating index from embeddings...")
                print(f"Error: {error_msg}")
                # Recreate the index from embeddings (this should work with current FAISS version)
                if self.embeddings is not None and len(self.embeddings) > 0:
                    dimension = self.embeddings.shape[1]
                    self.index = faiss.IndexFlatL2(dimension)
                    self.index.add(self.embeddings)
                    print(f"✓ Index recreated successfully")
                    # Retry the search
                    distances, indices = self.index.search(query_embedding, top_k)
                else:
                    raise ValueError("Cannot recreate index: embeddings are missing or empty")
            else:
                # Re-raise other AttributeError/TypeError
                if isinstance(e, AttributeError):
                    raise AttributeError(f"Index does not have a 'search' method. Index type: {type(self.index)}") from e
                raise
        except Exception as e:
            print(f"FAISS search error: {e}")
            print(f"Query embedding shape: {query_embedding.shape}, dtype: {query_embedding.dtype}")
            print(f"Index type: {type(self.index)}")
            raise
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts) and idx >= 0:  # Check for valid index
                results.append({
                    "text": self.texts[idx],
                    "score": float(distances[0][i]),
                    "rank": i + 1
                })
        
        # Clean up temporary arrays
        del query_embedding, distances, indices
        import gc
        gc.collect()
        
        return results
    
    def answer_question(self, question: str, context_chunks: int = 8) -> str:
        """
        Answer a question about the resume using retrieved context and Groq LLM.
        
        Args:
            question: User's question
            context_chunks: Number of context chunks to use for context
            
        Returns:
            Answer string generated by LLM
        """
        # Enhance search query with synonyms for better retrieval
        question_lower = question.lower()
        enhanced_query = question
        
        # Add relevant keywords based on question type
        if any(word in question_lower for word in ["education", "degree", "university", "school", "college", "gpa", "academic"]):
            enhanced_query = f"{question} education degree university school college GPA academic"
        elif any(word in question_lower for word in ["experience", "work", "job", "position", "role", "employment"]):
            enhanced_query = f"{question} experience work job position role employment"
        elif any(word in question_lower for word in ["skill", "technology", "language", "tool", "proficient", "expertise"]):
            enhanced_query = f"{question} skill technology language tool proficient expertise"
        elif any(word in question_lower for word in ["project", "built", "developed", "created"]):
            enhanced_query = f"{question} project built developed created"
        
        # Search for relevant context
        results = self.search(enhanced_query, top_k=context_chunks)
        
        if not results:
            return "I couldn't find relevant information in the resume. Please try rephrasing your question."
        
        # Build context from top results (remove duplicates)
        seen_texts = set()
        unique_contexts = []
        for r in results:
            text = r["text"].strip()
            if text and text not in seen_texts:
                seen_texts.add(text)
                unique_contexts.append(text)
        
        if not unique_contexts:
            return "I couldn't find relevant information in the resume. Please try rephrasing your question."
        
        # Combine context chunks (limit to prevent memory issues)
        context = "\n\n".join(unique_contexts[:context_chunks])
        
        # Clean up the context (remove excessive whitespace)
        context = re.sub(r'\s+', ' ', context).strip()
        
        # Limit context length to prevent memory issues with LLM (3000 chars max)
        if len(context) > 3000:
            context = context[:3000] + "..."
        
        # Prepare prompt for LLM
        system_prompt = """You are a helpful assistant that answers questions about a resume. 
Use only the information provided in the context from the resume. 
Carefully review all the context provided - information may be spread across multiple sections.
If you find relevant information in the context, provide a clear and complete answer directly without prefacing with phrases like "Based on the context" or "According to the resume".
If the context truly doesn't contain enough information to answer the question, say so politely.
Be concise, accurate, and professional in your responses. Answer naturally and conversationally."""
        
        user_prompt = f"""Context from the resume:
{context}

Question: {question}

Please provide a clear and accurate answer."""
        
        try:
            # Generate answer using Groq LLM
            # Use smaller max_tokens to reduce memory usage
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=300  # Reduced from 500 to save memory
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Force cleanup of response object
            del response
            import gc
            gc.collect()
            
            return answer
            
        except Exception as e:
            # Log the error for debugging
            error_msg = str(e)
            print(f"Groq API Error: {error_msg}")
            print(f"Error type: {type(e).__name__}")
            
            # Provide more helpful error message
            if "401" in error_msg or "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
                return f"Authentication error with Groq API. Please check your API key. Error: {error_msg}"
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                return f"Rate limit exceeded. Please try again later. Error: {error_msg}"
            elif "model" in error_msg.lower():
                return f"Model error. The model '{self.groq_model}' may not be available. Error: {error_msg}"
            else:
                # Fallback to simple context return if LLM fails
                return f"I encountered an error while generating an answer: {error_msg}\n\nHere's the relevant information from the resume:\n\n{context[:500]}..."
    
    def save(self, filepath: str):
        """Save the agent state to disk."""
        data = {
            "texts": self.texts,
            "embeddings": self.embeddings,
            "index": self.index
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath: str):
        """Load the agent state from disk."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        self.texts = data["texts"]
        # Convert embeddings to float32 to save memory (if they're float64)
        embeddings = data["embeddings"]
        if embeddings.dtype == np.float64:
            embeddings = embeddings.astype(np.float32)
        self.embeddings = embeddings
        self.index = data["index"]
        
        # Basic validation - just check that index exists
        # Don't try to access any FAISS attributes as SWIG-wrapped objects
        # will throw errors when attributes are accessed via hasattr/getattr
        if self.index is None:
            raise ValueError("Loaded index is None. Index may be corrupted.")
        
        # Note: We don't validate FAISS-specific attributes here because
        # SWIG-wrapped FAISS objects throw errors when accessed via hasattr/getattr.
        # The index will be validated when we actually use it in the search() method.
        
        # Re-initialize Groq client if not already initialized
        if not hasattr(self, 'groq_client') or self.groq_client is None:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY environment variable is not set. Please set it with your Groq API key.")
            self.groq_client = Groq(api_key=groq_api_key)
            if not hasattr(self, 'groq_model'):
                self.groq_model = "llama-3.1-8b-instant"

