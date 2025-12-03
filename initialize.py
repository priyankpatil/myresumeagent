"""
Initialize the resume vector store from PDF files
"""
import os
from dotenv import load_dotenv
import faiss
from resume_agent import ResumeAgent

# Load environment variables from .env file
load_dotenv()

def initialize():
    """Process all PDF files in the resumes folder."""
    resumes_dir = "resumes"
    
    if not os.path.exists(resumes_dir):
        os.makedirs(resumes_dir)
        print(f"Created {resumes_dir} directory. Please add your resume PDF here.")
        return
    
    pdf_files = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {resumes_dir}. Please add your resume PDF.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    
    # Initialize agent
    agent = ResumeAgent()
    
    # Process all PDFs
    all_text = ""
    for pdf_file in pdf_files:
        pdf_path = os.path.join(resumes_dir, pdf_file)
        print(f"\nProcessing {pdf_file}...")
        try:
            text = agent.extract_text_from_pdf(pdf_path)
            all_text += text + "\n\n"
            print(f"✓ Successfully extracted text from {pdf_file}")
        except Exception as e:
            print(f"✗ Error processing {pdf_file}: {e}")
    
    if all_text.strip():
        # Process combined text
        print("\nCreating vector embeddings...")
        chunks = agent.chunk_text(all_text)
        agent.texts = chunks
        
        # Create embeddings (ensure float32 to save memory)
        print(f"Creating embeddings for {len(chunks)} chunks...")
        agent.embeddings = agent.model.encode(chunks, show_progress_bar=True).astype('float32')
        
        # Create FAISS index
        dimension = agent.embeddings.shape[1]
        agent.index = faiss.IndexFlatL2(dimension)
        agent.index.add(agent.embeddings)
        
        # Save the agent state
        os.makedirs("data", exist_ok=True)
        agent.save("data/resume_index.pkl")
        
        print(f"\n✓ Successfully indexed {len(chunks)} text chunks")
        print("✓ Vector store saved to data/resume_index.pkl")
        print("\nYou can now start the server with: python main.py")
    else:
        print("\n✗ No text could be extracted from the PDF files.")

if __name__ == "__main__":
    initialize()

