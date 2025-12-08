# 🚀 Professional AI Resume Agent

> **Transform your resume into an interactive, AI-powered professional dashboard**

A beautiful, full-stack web application that combines data visualization, semantic search, and AI to create an engaging professional portfolio. Ask questions about your career journey, explore your global footprint, and showcase your skills—all powered by cutting-edge AI technology.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ What Makes This Special?

This let's you tell your story in a visually pleasing dashboard format. It's a **complete professional storytelling platform** that:

- 📊 **Visualizes Your Career Journey** with interactive, responsive charts
- 🤖 **Answers Questions** about your experience using AI-powered semantic search
- 🌍 **Maps Your Global Impact** across countries and cities
- 💡 **Showcases Your Skills** with beautiful data visualizations
- 📱 **Works Seamlessly** on desktop, tablet, and mobile devices

---

## 🎯 Features

### 📈 Interactive Dashboard

**Career Journey Timeline**
- Gantt-style timeline visualization of your professional journey
- Color-coded by category (Education, Employment, Internship)
- Interactive filtering by institution, skill type, or skill
- Responsive design optimized for all screen sizes

**Global Impact Map**
- Choropleth map showing your professional footprint
- Displays number of cities and work experiences per country
- Highlights your international career journey

**Skills Visualization**
- Donut chart showing skill distribution by type
- Horizontal bar chart displaying years of experience per skill
- Interactive filtering and exploration

**AI-Powered Q&A Agent**
- Ask natural language questions about your resume
- Powered by Groq's fast LLM (Llama 3.1)
- Semantic search using FAISS vector embeddings
- Context-aware responses based on your actual experience

### 🛠️ Technical Highlights

- **Vector Search**: FAISS-based semantic search for accurate retrieval
- **AI Integration**: Groq API for fast, cost-effective LLM responses
- **Data Management**: Excel-based resume data with structured schemas
- **Memory Optimized**: Efficient memory usage for cloud deployment
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **Modern Stack**: FastAPI, Plotly.js, and modern Python tooling

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/JS)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Dashboard  │  │  Interactive │  │   AI Agent   │   │
│  │    Charts    │  │   Filtering  │  │   Chat UI    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Dashboard    │  │ Resume Agent │  │  Data        │   │
│  │ Data Module  │  │ (FAISS +     │  │  Processing  │   │
│  │              │  │  Groq LLM)   │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Excel Files  │  │ Vector Store │  │  Embeddings  │   │
│  │ (Resume Data)│  │  (FAISS)     │  │  (Sentence   │   │
│  │              │  │              │  │  Transformers)│  │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Groq API key ([Get one free](https://console.groq.com/))
- Your resume data in Excel format (see [Data Structure](#-data-structure))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/myresumeagent.git
   cd myresumeagent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create a .env file
   echo "GROQ_API_KEY=your-groq-api-key-here" > .env
   ```

4. **Prepare your resume data:**
   - Place your resume Excel file in `resume_data/resume_data.xlsx`
   - See [Data Structure](#-data-structure) for the required format

5. **Initialize the vector store:**
   ```bash
   python initialize.py
   ```
   This will:
   - Process your resume data
   - Generate vector embeddings using sentence-transformers
   - Create a FAISS index for semantic search
   - Save the index to `data/resume_index.pkl`

6. **Start the server:**
   ```bash
   python main.py
   ```

7. **Open your browser:**
   Navigate to `http://localhost:8000` and explore your professional dashboard!

---

## 📊 Data Structure

Your resume data should be organized in an Excel file (`resume_data.xlsx`) with the following sheets:

### `candidate_details`
- `full_name`: Your full name
- `primary_email`: Email address
- `cell_number`: Phone number
- `linkedin_profile`: LinkedIn URL (optional)
- `github_profile`: GitHub URL (optional)

### `resume`
- `resume_item_id`: Unique identifier
- `category`: "Education", "Employment", or "Internship"
- `institutution`: Institution/company name
- `title`: Job title or degree
- `education_degree`: Degree name (if education)
- `date_started`: Start date
- `date_ended`: End date (or current date)
- `city`: City name
- `country`: Country name

### `skills`
- `skill_id`: Unique identifier
- `skill`: Skill name
- `skill_type`: Type (e.g., "Technical", "Soft Skills")
- `years_of_experience`: Years of experience

### `skills_resume`
- Links skills to resume items
- `skill_id`: References `skills.skill_id`
- `resume_item_id`: References `resume.resume_item_id`

---

## 🎨 Usage Examples

### Dashboard Interaction

1. **Explore Your Career Journey:**
   - Click on any timeline bar to filter by institution
   - Click on skill types in the donut chart to filter
   - Click on skills in the bar chart to see related experiences
   - Use the "Clear Filter" button to reset

2. **Ask Questions:**
   - "What is your work experience at Amazon?"
   - "What skills do you have in machine learning?"
   - "Tell me about your education background"
   - "What projects have you worked on?"

### API Endpoints

```bash
# Get candidate information
GET /api/dashboard/candidate

# Get timeline data (with optional filters)
GET /api/dashboard/timeline?institution=Amazon
GET /api/dashboard/timeline?skill_type=Technical

# Get map data
GET /api/dashboard/map

# Get skill distributions
GET /api/dashboard/skills/donut
GET /api/dashboard/skills/bar

# Ask a question
POST /api/ask
{
  "question": "What is your experience with Python?"
}

# Health check
GET /api/health
```

---

## 🚢 Deployment

### Render (Recommended)

This project is optimized for Render deployment with memory-efficient configurations.

1. **Create a `render.yaml` file** (already included):
   ```yaml
   services:
     - type: web
       name: resume-agent
       env: python
       buildCommand: pip install -r requirements.txt && python initialize.py
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
   ```

2. **Set environment variables in Render:**
   - `GROQ_API_KEY`: Your Groq API key
   - `TOKENIZERS_PARALLELISM`: `false`

3. **Deploy:**
   - Connect your GitHub repository to Render
   - Render will automatically detect `render.yaml`
   - The build process will initialize the vector store
   - Your app will be live!

**Note:** For Render's free tier (512MB), the app is optimized with:
- Single Uvicorn worker
- Lazy loading of ML models
- Memory-efficient embeddings (float32)
- Aggressive garbage collection

For better performance, consider Render's Standard plan (2GB+).

### Other Platforms

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:
- Vercel (serverless, with size limitations)
- Railway
- Fly.io
- Heroku

---

## 🧪 Testing

### Local Development

```bash
# Run the server
python main.py

# Test the API
curl http://localhost:8000/api/health
```

### Mobile Testing

See [MOBILE_TESTING.md](MOBILE_TESTING.md) for comprehensive mobile testing guide:
- Chrome DevTools mobile emulation
- Real device testing
- Network throttling
- Responsive breakpoint testing

---

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Required. Your Groq API key for LLM responses
- `TOKENIZERS_PARALLELISM`: Set to `false` to avoid warnings

### Memory Optimization

The application includes several memory optimizations:
- Lazy loading of ResumeAgent
- Float32 embeddings (instead of float64)
- Single Uvicorn worker
- Aggressive garbage collection
- Reduced LLM max_tokens

See [MEMORY_OPTIMIZATION.md](MEMORY_OPTIMIZATION.md) for details.

---

## 📁 Project Structure

```
myresumeagent/
├── main.py                 # FastAPI application & routes
├── resume_agent.py         # Core AI agent (FAISS + Groq)
├── dashboard_data.py      # Data processing & API endpoints
├── initialize.py          # Vector store initialization
├── templates/
│   └── dashboard.html     # Frontend dashboard (HTML/JS)
├── resume_data/
│   └── resume_data.xlsx   # Your resume data
├── data/
│   └── resume_index.pkl   # Generated FAISS index
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment config
└── README.md             # This file
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **Groq**: Fast LLM inference
- **Pandas**: Data manipulation
- **PyPDF**: PDF parsing (for future use)

### Frontend
- **Plotly.js**: Interactive charts
- **Vanilla JavaScript**: No framework dependencies
- **Responsive CSS**: Mobile-first design

### Infrastructure
- **Render**: Cloud hosting
- **Python 3.9+**: Runtime

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Groq** for providing fast, free LLM API access
- **FAISS** team for efficient vector search
- **Sentence Transformers** for high-quality embeddings
- **Plotly** for beautiful, interactive visualizations
- **FastAPI** for the excellent web framework

---

## 📧 Contact

**Priyank Patil**
- Email: priyank.patil3@gmail.com

---

## 🎯 Roadmap

- [ ] Support for multiple resume formats (PDF, DOCX)
- [ ] Export dashboard as PDF
- [ ] Multi-language support
- [ ] Advanced analytics and insights
- [ ] Integration with job boards
- [ ] Resume versioning and comparison

---


*Last updated: 7 December 2025*
