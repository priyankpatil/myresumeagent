# Quick Start Guide

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your resume:**
   - Place your resume PDF in the `resumes/` folder
   - Example: `resumes/my_resume.pdf`

3. **Initialize the index:**
   ```bash
   python initialize.py
   ```
   This will:
   - Extract text from your PDF
   - Create vector embeddings
   - Build a searchable index
   - Save to `data/resume_index.pkl`

4. **Start the server:**
   ```bash
   python main.py
   ```

5. **Open in browser:**
   - Go to http://localhost:8000
   - Start asking questions!

## Example Questions

- "What is your work experience?"
- "What skills do you have?"
- "What is your educational background?"
- "Tell me about your projects"
- "What programming languages do you know?"

## Deployment to Vercel

1. **Prepare the index:**
   ```bash
   python initialize.py
   git add data/resume_index.pkl
   git commit -m "Add resume index"
   ```

2. **Push to GitHub:**
   ```bash
   git push origin main
   ```

3. **Deploy on Vercel:**
   - Go to vercel.com
   - Import your GitHub repository
   - Deploy!

That's it! Your agent will be live at your Vercel URL.

## Troubleshooting

**"Resume index not loaded" error:**
- Make sure you ran `python initialize.py` first
- Check that `data/resume_index.pkl` exists

**Model download is slow:**
- First run downloads ~80MB model
- This is normal and only happens once
- Subsequent runs are instant

**PDF parsing errors:**
- Ensure your PDF is not password-protected
- Try a different PDF if issues persist
- Some PDFs with images may have limited text extraction

