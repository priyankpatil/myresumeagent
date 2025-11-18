# Resume Q&A Agent

A simple Python agent that answers questions about your resume using AI. Deploy for free on Vercel or other platforms.

## Features

- 📄 PDF resume parsing
- 🔍 Semantic search using vector embeddings
- 💬 Natural language Q&A interface powered by Groq LLM
- 🚀 Free deployment on Vercel
- 🎯 Fast AI responses using Groq's free API

## Setup

1. **Get a Groq API Key:**
   - Sign up for a free API key at [console.groq.com](https://console.groq.com/)
   - Copy your API key

2. **Set up environment variable:**
   ```bash
   # On macOS/Linux:
   export GROQ_API_KEY=your-api-key-here
   
   # On Windows:
   set GROQ_API_KEY=your-api-key-here
   
   # Or create a .env file in the project root:
   echo "GROQ_API_KEY=your-api-key-here" > .env
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your resume PDF to the `resumes/` folder**

5. **Initialize the vector store:**
   ```bash
   python initialize.py
   ```

6. **Run locally:**
   ```bash
   python main.py
   ```

7. **Open http://localhost:8000 in your browser**

## Deployment

### Vercel Deployment (Recommended)

**Important:** For Vercel, you need to commit the `data/resume_index.pkl` file since Vercel is serverless and can't run initialization on each request.

1. **Prepare for deployment:**
   ```bash
   # Add your resume PDF to resumes/ folder
   # Run initialization locally
   python initialize.py
   # Commit the generated data/resume_index.pkl file
   git add data/resume_index.pkl
   git commit -m "Add resume index"
   ```

2. **Set environment variable in Vercel:**
   - In your Vercel project settings, go to "Environment Variables"
   - Add `GROQ_API_KEY` with your Groq API key value
   - Make sure to set it for all environments (Production, Preview, Development)

3. **Deploy:**
   - Push to GitHub
   - Go to [vercel.com](https://vercel.com) and sign up/login
   - Click "New Project" and import your GitHub repository
   - Vercel will auto-detect the `vercel.json` configuration
   - Deploy!

4. **Note:** The first deployment will download the sentence-transformers model (~80MB), which may take a few minutes.

### Alternative Free Hosting

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:
- **Render**: Free tier with build-time initialization
- **Railway**: Free tier with $5 monthly credit
- **Fly.io**: Generous free tier

All platforms support this application!

## Usage

1. Place your resume PDF in the `resumes/` folder
2. Run `python initialize.py` to process and index your resume
3. Start the server and ask questions about your resume!

## Project Structure

```
.
├── main.py              # FastAPI application
├── initialize.py        # Initialize vector store from resume
├── resume_agent.py      # Core agent logic
├── vercel.json          # Vercel deployment config
├── requirements.txt     # Python dependencies
├── resumes/             # Place your PDF resume here
└── static/              # Web interface files
```

