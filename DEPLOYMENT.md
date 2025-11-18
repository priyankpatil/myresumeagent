# Deployment Guide

## Free Deployment Options

### Option 1: Vercel (Recommended)

Vercel offers free hosting for serverless Python functions.

**Steps:**
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign up/login
3. Click "New Project" and import your GitHub repository
4. Vercel will auto-detect the `vercel.json` configuration
5. Deploy!

**Important Notes:**
- The first deployment will download models (~80MB), which may take a few minutes
- Vercel has a 10-second timeout for free tier, so large PDFs might need optimization
- Consider using Vercel's Pro plan for longer timeouts if needed

**Environment Variables:**
- None required for basic setup
- Optional: Add `PYTHON_VERSION=3.9` if needed

### Option 2: Render

Render offers free tier with some limitations.

**Steps:**
1. Create a `render.yaml` file (see below)
2. Push to GitHub
3. Connect your repo at [render.com](https://render.com)
4. Deploy as a Web Service

**render.yaml:**
```yaml
services:
  - type: web
    name: resume-agent
    env: python
    buildCommand: pip install -r requirements.txt && python initialize.py
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
```

### Option 3: Railway

Railway offers a free tier with $5 credit monthly.

**Steps:**
1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Railway will auto-detect Python and install dependencies
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 4: Fly.io

Fly.io offers free tier with generous limits.

**Steps:**
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Run `fly launch` in your project directory
3. Follow the prompts
4. Deploy with `fly deploy`

## Pre-Deployment Checklist

1. ✅ Add your resume PDF to the `resumes/` folder
2. ✅ Run `python initialize.py` locally to generate the index
3. ✅ Commit the `data/resume_index.pkl` file (or generate it during build)
4. ✅ Test locally with `python main.py`
5. ✅ Push to GitHub

## Build-Time Index Generation

For platforms that rebuild on each deploy, you may want to generate the index during build:

1. Add a build script that runs `python initialize.py`
2. Ensure the `resumes/` folder is committed to git (or use environment variables)
3. The index will be generated during each deployment

## Troubleshooting

### Model Download Issues
- First deployment may fail if model download times out
- Solution: Pre-download models locally and commit them (not recommended due to size)
- Better: Use a smaller model or increase timeout

### Memory Issues
- Free tiers have memory limits
- Solution: Use `all-MiniLM-L6-v2` (already configured) - it's lightweight

### Timeout Issues
- Some platforms have short timeouts
- Solution: Optimize PDF size or use a paid tier

## Cost Optimization

- ✅ Using Hugging Face transformers (free, runs locally)
- ✅ Using FAISS for vector search (free, no API calls)
- ✅ No external API dependencies
- ✅ All processing happens on the server

**Total Cost: $0/month** (on free tiers)

