# Local Environment Setup Guide

## Setting Up Your Groq API Key

The application uses the `GROQ_API_KEY` environment variable to authenticate with Groq's API.

### Option 1: Using a `.env` File (Recommended)

1. **Create a `.env` file** in the project root directory:
   ```bash
   cd /Users/priyankpatil/Documents/Personal\ Projects/myresumeagent
   touch .env
   ```

2. **Add your API key** to the `.env` file:
   ```bash
   echo "GROQ_API_KEY=your-actual-api-key-here" > .env
   ```
   
   Or manually edit the `.env` file and add:
   ```
   GROQ_API_KEY=your-actual-api-key-here
   ```

3. **Verify the file** (the `.env` file is already in `.gitignore`, so it won't be committed):
   ```bash
   cat .env
   ```

4. **Run your application** - the `load_dotenv()` function will automatically load the API key:
   ```bash
   python main.py
   ```

### Option 2: Using Environment Variables (Temporary)

#### On macOS/Linux:
```bash
export GROQ_API_KEY=your-actual-api-key-here
python main.py
```

#### On Windows (Command Prompt):
```cmd
set GROQ_API_KEY=your-actual-api-key-here
python main.py
```

#### On Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="your-actual-api-key-here"
python main.py
```

**Note:** This method only works for the current terminal session. The `.env` file method persists across sessions.

### Getting Your Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `gsk_...`)

### Verifying Your Setup

After setting up the API key, you can verify it's working:

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Check the startup logs** - you should see:
   ```
   Starting up... Pre-loading agent...
   Memory before loading agent: X.XX MB
   Loading ResumeAgent...
   Loading resume index...
   ✓ Loaded resume index from disk
   Memory after loading agent: X.XX MB (+X.XX MB)
   ✓ Agent pre-loaded at startup
   ```

3. **Test the API:**
   ```bash
   curl http://localhost:8000/api/health
   ```
   
   Should return:
   ```json
   {
     "status": "healthy",
     "memory_mb": 229.03,
     "memory_percent": 44.7,
     "agent_loaded": true,
     "agent_ready": true
   }
   ```

### Troubleshooting

**Error: "GROQ_API_KEY environment variable is not set"**
- Make sure your `.env` file exists in the project root
- Check that the file contains: `GROQ_API_KEY=your-key-here`
- Verify there are no extra spaces or quotes around the key
- Make sure `python-dotenv` is installed: `pip install python-dotenv`

**Error: "Agent not initialized"**
- Check that your API key is valid
- Verify the `.env` file is in the same directory as `main.py`
- Try restarting the server after creating/updating the `.env` file

