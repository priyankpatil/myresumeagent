"""
FastAPI application for Resume Q&A Agent
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from resume_agent import ResumeAgent
from dashboard_data import (
    get_candidate_info, get_timeline_data, get_map_data,
    get_skill_donut_data, get_skill_bar_data,
    filter_by_institution, filter_by_skill_type, filter_by_skill
)

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Priyank's Professional AI Agent")

# Initialize agent
agent = None

def load_agent():
    """Load the agent from saved state."""
    global agent
    if agent is None:
        try:
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
        except ValueError as e:
            # Handle missing API key gracefully
            print(f"⚠ {str(e)}")
            agent = None
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
    """Serve the main HTML page with dashboard and agent."""
    candidate = get_candidate_info()
    html_content = get_dashboard_html(candidate)
    return HTMLResponse(content=html_content)

def get_dashboard_html(candidate: dict) -> str:
    """Generate the HTML with responsive dashboard and agent."""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        # Fallback: return minimal HTML if template not found
        return f"""<!DOCTYPE html>
<html><head><title>Error</title></head>
<body><h1>Template file not found</h1></body></html>"""
    
    # Replace placeholders in template
    html = template.format(
        candidate_name=candidate.get('name', 'Candidate'),
        candidate_location=candidate.get('location', 'Location'),
        candidate_phone=candidate.get('phone', 'Phone'),
        candidate_email=candidate.get('email', 'Email'),
        linkedin_link=f'<a href="{candidate["linkedin"]}" target="_blank" title="LinkedIn Profile"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>' if candidate.get('linkedin') else '',
        github_link=f'<a href="{candidate["github"]}" target="_blank" title="GitHub Profile"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a>' if candidate.get('github') else ''
    )
    
    return html

async def get_candidate():
    """Get candidate information."""
    return get_candidate_info()

@app.get("/api/dashboard/timeline")
async def get_timeline(
    institution: str = Query(None),
    skill_type: str = Query(None),
    skill: str = Query(None)
):
    """Get timeline data with optional filters."""
    filtered_df = None
    if institution:
        filtered_df = filter_by_institution(institution)
    elif skill_type:
        filtered_df = filter_by_skill_type(skill_type)
    elif skill:
        filtered_df = filter_by_skill(skill)
    return {"data": get_timeline_data(filtered_df)}

@app.get("/api/dashboard/map")
async def get_map(
    institution: str = Query(None),
    skill_type: str = Query(None),
    skill: str = Query(None)
):
    """Get map data with optional filters."""
    filtered_df = None
    if institution:
        filtered_df = filter_by_institution(institution)
    elif skill_type:
        filtered_df = filter_by_skill_type(skill_type)
    elif skill:
        filtered_df = filter_by_skill(skill)
    return {"data": get_map_data(filtered_df)}

@app.get("/api/dashboard/skills/donut")
async def get_skill_donut(
    institution: str = Query(None),
    skill_type: str = Query(None),
    skill: str = Query(None)
):
    """Get skill donut chart data."""
    filtered_df = None
    if institution:
        filtered_df = filter_by_institution(institution)
    elif skill_type:
        filtered_df = filter_by_skill_type(skill_type)
    elif skill:
        filtered_df = filter_by_skill(skill)
    return {"data": get_skill_donut_data(filtered_df)}

@app.get("/api/dashboard/skills/bar")
async def get_skill_bar(
    institution: str = Query(None),
    skill_type: str = Query(None),
    skill: str = Query(None)
):
    """Get skill bar chart data."""
    filtered_df = None
    if institution:
        filtered_df = filter_by_institution(institution)
    elif skill_type:
        filtered_df = filter_by_skill_type(skill_type)
    elif skill:
        filtered_df = filter_by_skill(skill)
    return {"data": get_skill_bar_data(filtered_df)}

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Handle question requests."""
    try:
        agent = load_agent()
        
        if agent is None:
            raise HTTPException(
                status_code=503,
                detail="Agent not initialized. Please set GROQ_API_KEY environment variable."
            )
        
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
        "agent_initialized": agent is not None,
        "index_loaded": agent is not None and agent.index is not None and len(agent.texts) > 0 if agent else False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

