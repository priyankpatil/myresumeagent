# Steps to Push Code to GitHub

## Prerequisites
- GitHub account (create one at [github.com](https://github.com) if you don't have one)
- Git installed on your machine (check with `git --version`)

## Step-by-Step Instructions

### Step 1: Initialize Git Repository (if not already done)
```bash
cd "/Users/priyankpatil/Documents/Personal Projects/myresumeagent"
git init
```

### Step 2: Verify .gitignore is Working
Make sure your `.env` file (if it exists) won't be committed:
```bash
# Check what will be ignored
git status --ignored
```

### Step 3: Create a GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository name: `myresumeagent` (or any name you prefer)
4. Description: "Resume Q&A Agent powered by Groq LLM"
5. Choose **Public** or **Private**:
   - **Public**: Anyone can see your code (good for portfolio)
   - **Private**: Only you can see it (more secure)
6. **DO NOT** check "Initialize with README" (you already have one)
7. Click **"Create repository"**

### Step 4: Add All Files to Git
```bash
# Add all files (respecting .gitignore)
git add .
```

### Step 5: Check What Will Be Committed
```bash
# Review the files that will be committed
git status
```

**Important**: Make sure you see:
- ✅ `README.md`
- ✅ `resume_agent.py`
- ✅ `main.py`
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ❌ **NO** `.env` file (should be ignored)

### Step 6: Make Your First Commit
```bash
git commit -m "Initial commit: Resume Q&A Agent with Groq LLM integration"
```

### Step 7: Connect to GitHub Repository
After creating the repository on GitHub, you'll see instructions. Use these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/myresumeagent.git

# Or if you prefer SSH (if you have SSH keys set up):
# git remote add origin git@github.com:YOUR_USERNAME/myresumeagent.git
```

### Step 8: Push to GitHub
```bash
# Push to main branch
git branch -M main
git push -u origin main
```

You'll be prompted for your GitHub username and password (or use a Personal Access Token).

### Step 9: Verify on GitHub
1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/myresumeagent`
2. Verify all files are there
3. **Double-check**: Make sure `.env` file is NOT visible (it should be ignored)

## Security Checklist Before Pushing

✅ **No API keys in code files**
✅ **No API keys in README.md** (already fixed)
✅ **`.env` file is in `.gitignore`**
✅ **`.env.local` is in `.gitignore`**

## After Pushing

### For Others to Use Your Code:
They need to:
1. Clone your repository
2. Create their own `.env` file with their Groq API key
3. Run `python initialize.py`
4. Run `python main.py`

### For Deployment (Vercel, etc.):
- Set the `GROQ_API_KEY` environment variable in your hosting platform's settings
- Never commit the actual API key

## Troubleshooting

### If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/myresumeagent.git
```

### If you need to update your API key:
1. Update it in your local `.env` file
2. Never commit it to git
3. If deploying, update it in your hosting platform's environment variables

### If you accidentally committed sensitive data:
```bash
# Remove from git history (use with caution!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
git push --force
```

## Next Steps After Pushing

1. **Add a LICENSE file** (optional but recommended)
2. **Add topics/tags** to your GitHub repo for discoverability
3. **Update README** with screenshots or demo links
4. **Set up GitHub Actions** for CI/CD (optional)

