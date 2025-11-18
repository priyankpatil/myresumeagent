"""
FastAPI application for Resume Q&A Agent
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from resume_agent import ResumeAgent

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Priyank's Professional AI Agent")

# Initialize agent
agent = None

def load_agent():
    """Load the agent from saved state."""
    global agent
    if agent is None:
        agent = ResumeAgent()
        index_path = "data/resume_index.pkl"
        if os.path.exists(index_path):
            try:
                agent.load(index_path)
                print("✓ Loaded resume index from disk")
            except Exception as e:
                print(f"✗ Error loading index: {e}")
                print("Please run 'python initialize.py' first")
        else:
            print("⚠ No index found. Please run 'python initialize.py' first")
    return agent

# Request/Response models
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    relevant_chunks: list = []

# API Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Priyank's Professional AI Agent</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .chat-container {
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                padding: 20px;
                min-height: 400px;
                max-height: 500px;
                overflow-y: auto;
                margin-bottom: 20px;
                background: #f9f9f9;
            }
            .message {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background: #e0e0e0;
                color: #333;
            }
            .input-container {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                border-color: #667eea;
            }
            button {
                padding: 15px 30px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #5568d3;
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .loading {
                display: none;
                text-align: center;
                color: #666;
                font-style: italic;
            }
            .loading.show {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 Priyank's Professional AI Agent</h1>
            <p class="subtitle">Ask me anything about Priyank's professional experience!</p>
            
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    👋 Hello! I can answer questions about Priyank's professional experience. Try asking:
                    <ul style="margin-top: 10px; padding-left: 20px;">
                        <li>What is Priyank's work experience?</li>
                        <li>What skills does Priyank have?</li>
                        <li>What is Priyank's educational background?</li>
                    </ul>
                </div>
            </div>
            
            <div class="loading" id="loading">Thinking...</div>
            
            <div class="input-container">
                <input type="text" id="questionInput" placeholder="Ask a question about the resume..." onkeypress="handleKeyPress(event)">
                <button onclick="askQuestion()" id="askButton">Ask</button>
            </div>
        </div>
        
        <script>
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    askQuestion();
                }
            }
            
            async function askQuestion() {
                const input = document.getElementById('questionInput');
                const question = input.value.trim();
                const button = document.getElementById('askButton');
                const loading = document.getElementById('loading');
                const chatContainer = document.getElementById('chatContainer');
                
                if (!question) return;
                
                // Disable input and show loading
                input.disabled = true;
                button.disabled = true;
                loading.classList.add('show');
                
                // Add user message
                const userMsg = document.createElement('div');
                userMsg.className = 'message user-message';
                userMsg.textContent = question;
                chatContainer.appendChild(userMsg);
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Clear input
                input.value = '';
                
                try {
                    const response = await fetch('/api/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: question })
                    });
                    
                    const data = await response.json();
                    
                    // Add bot response
                    const botMsg = document.createElement('div');
                    botMsg.className = 'message bot-message';
                    botMsg.textContent = data.answer || 'Sorry, I could not process your question.';
                    chatContainer.appendChild(botMsg);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                } catch (error) {
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'message bot-message';
                    errorMsg.textContent = 'Error: Could not connect to the server.';
                    chatContainer.appendChild(errorMsg);
                } finally {
                    // Re-enable input
                    input.disabled = false;
                    button.disabled = false;
                    loading.classList.remove('show');
                    input.focus();
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Handle question requests."""
    try:
        agent = load_agent()
        
        if agent.index is None or len(agent.texts) == 0:
            raise HTTPException(
                status_code=503,
                detail="Resume index not loaded. Please run 'python initialize.py' first."
            )
        
        answer = agent.answer_question(request.question)
        relevant_chunks = agent.search(request.question, top_k=3)
        
        return QuestionResponse(
            answer=answer,
            relevant_chunks=[chunk["text"] for chunk in relevant_chunks]
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle missing API key or other value errors
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in /api/ask: {error_details}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    agent = load_agent()
    return {
        "status": "healthy",
        "index_loaded": agent.index is not None and len(agent.texts) > 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

