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
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{candidate['name']} - Professional Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #1f2b3e;
            color: #f4f4f4;
            height: 100vh;
            overflow: hidden;
        }}
        .main-container {{
            display: flex;
            height: 100vh;
            width: 100%;
        }}
        .dashboard-section {{
            width: 75%;
            background: #1f2b3e;
            overflow-y: auto;
            padding: 15px;
            border-right: 2px solid #3d4a5c;
        }}
        .agent-section {{
            width: 25%;
            background: #2c3e50;
            display: flex;
            flex-direction: column;
            padding: 15px;
        }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                padding: 20px;
                background: linear-gradient(135deg, rgba(0,183,255,0.1) 0%, rgba(118,75,162,0.1) 100%);
                border-radius: 12px;
                border: 1px solid rgba(0,183,255,0.2);
            }}
            .header h1 {{
                color: #00b7ff;
                font-size: 2.2em;
                margin-bottom: 12px;
                font-weight: 800;
                text-shadow: 0 2px 10px rgba(0,183,255,0.3);
                letter-spacing: 0.5px;
            }}
            .header .contact {{
                color: #e0e0e0;
                font-size: 1em;
                line-height: 1.8;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                align-items: center;
                gap: 15px;
            }}
            .header .contact a {{
                color: #00b7ff;
                text-decoration: none;
                transition: all 0.3s;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }}
            .header .contact a:hover {{
                color: #00d4ff;
                text-shadow: 0 0 8px rgba(0,183,255,0.5);
                transform: translateY(-1px);
            }}
            .header .social-links {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 15px;
                margin-top: 12px;
            }}
            .header .social-links a {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: rgba(0,183,255,0.15);
                border: 2px solid rgba(0,183,255,0.3);
                color: #00b7ff;
                font-size: 1.3em;
                text-decoration: none;
                transition: all 0.3s;
            }}
            .header .social-links a:hover {{
                background: rgba(0,183,255,0.3);
                border-color: #00b7ff;
                transform: translateY(-2px) scale(1.1);
                box-shadow: 0 4px 15px rgba(0,183,255,0.4);
            }}
            .header .divider {{
                color: #3d4a5c;
                margin: 0 8px;
            }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        .dashboard-column {{
            display: flex;
            flex-direction: column;
        }}
        .chart-container {{
            background: rgba(0,0,0,0.2);
            border: 1px solid #3d4a5c;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 15px;
        }}
        .chart-title {{
            color: #f4f4f4;
            font-size: 1.1em;
            margin-bottom: 10px;
            text-align: center;
        }}
        .chart-wrapper {{
            height: 300px;
        }}
        .chart-wrapper.large {{
            height: 400px;
        }}
        .agent-header {{
            color: #00b7ff;
            font-size: 1.3em;
            margin-bottom: 15px;
            text-align: center;
            font-weight: 600;
        }}
        .chat-container {{
            flex: 1;
            border: 1px solid #3d4a5c;
            border-radius: 8px;
            padding: 15px;
            overflow-y: auto;
            background: rgba(0,0,0,0.2);
            margin-bottom: 15px;
            min-height: 200px;
        }}
        .message {{
            margin-bottom: 12px;
            padding: 10px 12px;
            border-radius: 8px;
            max-width: 90%;
            word-wrap: break-word;
            font-size: 0.9em;
        }}
        .user-message {{
            background: #00b7ff;
            color: white;
            margin-left: auto;
            text-align: right;
        }}
        .bot-message {{
            background: #3d4a5c;
            color: #f4f4f4;
        }}
        .input-container {{
            display: flex;
            gap: 8px;
        }}
        input[type="text"] {{
            flex: 1;
            padding: 10px;
            border: 1px solid #3d4a5c;
            border-radius: 6px;
            background: rgba(0,0,0,0.3);
            color: #f4f4f4;
            font-size: 0.9em;
            outline: none;
        }}
        input[type="text"]:focus {{
            border-color: #00b7ff;
        }}
        input[type="text"]::placeholder {{
            color: #a0a0a0;
        }}
        button {{
            padding: 10px 20px;
            background: #00b7ff;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 0.9em;
            cursor: pointer;
            transition: background 0.3s;
        }}
        button:hover {{
            background: #0099cc;
        }}
        button:disabled {{
            background: #555;
            cursor: not-allowed;
        }}
        .loading {{
            display: none;
            text-align: center;
            color: #a0a0a0;
            font-style: italic;
            font-size: 0.85em;
        }}
        .loading.show {{
            display: block;
        }}
        @media (max-width: 1024px) {{
            .dashboard-section {{
                width: 70%;
            }}
            .agent-section {{
                width: 30%;
            }}
        }}
        @media (max-width: 768px) {{
            .main-container {{
                flex-direction: column;
            }}
            .dashboard-section {{
                width: 100%;
                height: 60%;
                border-right: none;
                border-bottom: 2px solid #3d4a5c;
            }}
            .agent-section {{
                width: 100%;
                height: 40%;
            }}
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
            .chart-wrapper {{
                height: 250px;
            }}
            .chart-wrapper.large {{
                height: 300px;
            }}
        }}
        @media (max-width: 480px) {{
            .header h1 {{
                font-size: 1.4em;
            }}
            .header .contact {{
                font-size: 0.8em;
            }}
            .chart-wrapper {{
                height: 200px;
            }}
            .chart-wrapper.large {{
                height: 250px;
            }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="dashboard-section">
            <div class="header">
                <h1>{candidate['name']}</h1>
                <div class="contact">
                    <span>📍 {candidate['location']}</span>
                    <span class="divider">•</span>
                    <span>📞 {candidate['phone']}</span>
                    <span class="divider">•</span>
                    <a href="mailto:{candidate['email']}">✉️ {candidate['email']}</a>
                </div>
                <div class="social-links">
                    {f'<a href="{candidate["linkedin"]}" target="_blank" title="LinkedIn Profile"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>' if candidate.get('linkedin') else ''}
                    {f'<a href="{candidate["github"]}" target="_blank" title="GitHub Profile"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a>' if candidate.get('github') else ''}
                </div>
                <div id="filter-indicator" style="display: none; margin-top: 15px; padding: 10px; background: rgba(0,183,255,0.2); border-radius: 8px; font-size: 0.9em; border: 1px solid rgba(0,183,255,0.3);">
                    <span id="filter-text"></span>
                    <button onclick="clearFilter()" style="margin-left: 10px; padding: 6px 14px; background: #00b7ff; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; transition: all 0.3s;">Clear Filter</button>
                </div>
            </div>
            <div class="dashboard-grid">
                <div class="dashboard-column">
                    <div class="chart-container">
                        <div class="chart-title">🚀 Career Journey</div>
                        <div class="chart-wrapper large" id="timeline-chart"></div>
                    </div>
                    <div class="chart-container">
                        <div class="chart-title">🌍 Global Impact</div>
                        <div class="chart-wrapper" id="map-chart"></div>
                    </div>
                </div>
                <div class="dashboard-column">
                    <div class="chart-container">
                        <div class="chart-title">💡 Skills Arsenal</div>
                        <div class="chart-wrapper" id="donut-chart"></div>
                    </div>
                    <div class="chart-container">
                        <div class="chart-title">⚡ Expertise Levels</div>
                        <div class="chart-wrapper large" id="bar-chart"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="agent-section">
            <div class="agent-header">🤖 AI Agent</div>
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    👋 Hello! Ask me anything about {candidate['name']}'s professional experience:
                    <ul style="margin-top: 8px; padding-left: 20px; font-size: 0.85em;">
                        <li>Work experience?</li>
                        <li>Skills?</li>
                        <li>Education?</li>
                    </ul>
                </div>
            </div>
            <div class="loading" id="loading">Thinking...</div>
            <div class="input-container">
                <input type="text" id="questionInput" placeholder="Ask a question..." onkeypress="handleKeyPress(event)">
                <button onclick="askQuestion()" id="askButton">Ask</button>
            </div>
        </div>
    </div>
    <script>
        let currentFilter = {{ type: null, value: null }};
        
        function clearFilter() {{
            currentFilter = {{ type: null, value: null }};
            const indicator = document.getElementById('filter-indicator');
            if (indicator) {{
                indicator.style.display = 'none';
            }}
            loadDashboardData();
        }}
        
        function updateFilterIndicator() {{
            const indicator = document.getElementById('filter-indicator');
            const filterText = document.getElementById('filter-text');
            if (indicator && filterText) {{
                if (currentFilter.type && currentFilter.value) {{
                    const filterLabels = {{
                        'institution': 'Institution',
                        'skill_type': 'Skill Type',
                        'skill': 'Skill'
                    }};
                    filterText.textContent = `Filtered by: ${{filterLabels[currentFilter.type] || currentFilter.type}}: ${{currentFilter.value}}`;
                    indicator.style.display = 'block';
                }} else {{
                    indicator.style.display = 'none';
                }}
            }}
        }}
        
        function showNoDataMessage(chartId, message) {{
            const chartDiv = document.getElementById(chartId);
            if (chartDiv) {{
                chartDiv.innerHTML = `<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #a0a0a0; text-align: center; padding: 20px; font-size: 0.9em;">${{message}}</div>`;
            }}
        }}
        
        async function loadDashboardData(filterType = null, filterValue = null) {{
            console.log('Loading dashboard data...', filterType, filterValue);
            try {{
                const params = new URLSearchParams();
                if (filterType && filterValue) {{
                    params.append(filterType, filterValue);
                }}
                
                console.log('Fetching data from APIs...');
                const [timelineRes, mapRes, donutRes, barRes] = await Promise.all([
                    fetch(`/api/dashboard/timeline?${{params}}`),
                    fetch(`/api/dashboard/map?${{params}}`),
                    fetch(`/api/dashboard/skills/donut?${{params}}`),
                    fetch(`/api/dashboard/skills/bar?${{params}}`)
                ]);
                
                console.log('API responses:', {{
                    timeline: timelineRes.status,
                    map: mapRes.status,
                    donut: donutRes.status,
                    bar: barRes.status
                }});
                
                const timelineData = await timelineRes.json();
                const mapData = await mapRes.json();
                const donutData = await donutRes.json();
                const barData = await barRes.json();
                
                console.log('Data received:', {{
                    timeline: timelineData.data?.length || 0,
                    map: mapData.data?.length || 0,
                    donut: donutData.data?.length || 0,
                    bar: barData.data?.length || 0
                }});
                
                // Update charts with data (even if empty, let chart functions handle it)
                // Update filter indicator
                updateFilterIndicator();
                
                if (timelineData.data && timelineData.data.length > 0) {{
                    updateTimelineChart(timelineData.data);
                }} else {{
                    showNoDataMessage('timeline-chart', 'No timeline data available.');
                }}
                
                if (mapData.data && mapData.data.length > 0) {{
                    updateMapChart(mapData.data);
                }} else {{
                    showNoDataMessage('map-chart', 'No map data available.');
                }}
                
                if (donutData.data && donutData.data.length > 0) {{
                    updateDonutChart(donutData.data);
                }} else {{
                    showNoDataMessage('donut-chart', 'No skills data available.');
                }}
                
                if (barData.data && barData.data.length > 0) {{
                    updateBarChart(barData.data);
                }} else {{
                    showNoDataMessage('bar-chart', 'No skills data available.');
                }}
            }} catch (error) {{
                console.error('Error loading dashboard data:', error);
                showNoDataMessage('timeline-chart', 'Error: ' + error.message);
                showNoDataMessage('map-chart', 'Error: ' + error.message);
                showNoDataMessage('donut-chart', 'Error: ' + error.message);
                showNoDataMessage('bar-chart', 'Error: ' + error.message);
            }}
        }}
        
        function updateTimelineChart(data) {{
            if (!data || data.length === 0) {{
                showNoDataMessage('timeline-chart', 'No timeline data available.');
                return;
            }}
            
            try {{
                // Sort by start date
                data.sort((a, b) => new Date(a.start) - new Date(b.start));
                const colors = {{'Employment': '#00b7ff', 'Education': '#f95d6a', 'Internship': '#888', 'Other': '#ffa600'}};
                
                // Group by institution
                const institutionGroups = {{}};
                data.forEach((item) => {{
                    if (!institutionGroups[item.institution]) {{
                        institutionGroups[item.institution] = [];
                    }}
                    institutionGroups[item.institution].push(item);
                }});
                
                const institutions = Object.keys(institutionGroups);
                const traces = [];
                const seenCategories = new Set();
                
                // Create horizontal bar chart style timeline
                institutions.forEach((inst, instIdx) => {{
                    const items = institutionGroups[inst];
                    items.forEach((item) => {{
                        const startDate = new Date(item.start);
                        const endDate = new Date(item.end);
                        
                        // Format dates for display
                        const startStr = startDate.toLocaleDateString('en-US', {{ month: 'short', year: 'numeric' }});
                        const endStr = endDate.toLocaleDateString('en-US', {{ month: 'short', year: 'numeric' }});
                        
                        // Store institution in a way that's easily accessible
                        const traceData = {{
                            x: [startDate, endDate],
                            y: [instIdx, instIdx],
                            mode: 'lines',
                            name: item.category,
                            line: {{
                                color: colors[item.category] || '#888',
                                width: 16
                            }},
                            fill: 'toself',
                            fillcolor: colors[item.category] || '#888',
                            opacity: 0.7,
                            customdata: [item.label, item.title, startStr, endStr, item.city, item.country, inst],
                            hovertemplate: '<b>%{{customdata[0]}}</b><br>%{{customdata[1]}}<br>%{{customdata[2]}} to %{{customdata[3]}}<br>%{{customdata[4]}}, %{{customdata[5]}}<extra></extra>',
                            showlegend: !seenCategories.has(item.category),
                            legendgroup: item.category,
                            // Add institution as metadata for easier access
                            meta: {{ institution: inst }}
                        }};
                        
                        traces.push(traceData);
                        
                        seenCategories.add(item.category);
                    }});
                }});
                
                const timelineDiv = document.getElementById('timeline-chart');
                Plotly.newPlot(timelineDiv, traces, {{
                    template: 'plotly_dark',
                    xaxis: {{ 
                        type: 'date',
                        title: '',
                        showgrid: true,
                        gridcolor: 'rgba(255,255,255,0.1)',
                        tickformat: '%Y',
                        dtick: 'M12'  // One tick per year
                    }},
                    yaxis: {{ 
                        title: '',
                        tickmode: 'array',
                        tickvals: institutions.map((_, i) => i),
                        ticktext: institutions,
                        autorange: 'reversed',
                        showgrid: false
                    }},
                    height: 400,
                    margin: {{ l: 150, r: 20, t: 90, b: 50 }},
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    legend: {{ 
                        orientation: 'h',
                        y: 1.3,
                        x: 0.5,
                        xanchor: 'center',
                        yanchor: 'top',
                        font: {{ color: '#f4f4f4', size: 10 }},
                        bgcolor: 'rgba(0,0,0,0.3)',
                        bordercolor: 'rgba(255,255,255,0.2)',
                        borderwidth: 1,
                        itemwidth: 50,
                        tracegroupgap: 15
                    }},
                    clickmode: 'event',
                    hovermode: 'closest'
                }}, {{responsive: true}});
                
                // Setup click handler - wait for chart to be fully rendered
                setTimeout(() => {{
                    // Remove any existing handlers first
                    if (timelineDiv.removeAllListeners) {{
                        timelineDiv.removeAllListeners('plotly_click');
                    }}
                    
                    timelineDiv.on('plotly_click', function(clickData) {{
                        console.log('Timeline clicked:', clickData);
                        if (clickData && clickData.points && clickData.points.length > 0) {{
                            const point = clickData.points[0];
                            console.log('Point data:', point);
                            
                            // Try multiple methods to get institution
                            let institution = null;
                            
                            // Method 1: From customdata (flat array)
                            if (point.customdata && Array.isArray(point.customdata)) {{
                                if (point.customdata.length >= 7) {{
                                    institution = point.customdata[6];
                                }}
                            }}
                            
                            // Method 2: From trace metadata
                            if (!institution && point.fullData && point.fullData.meta) {{
                                institution = point.fullData.meta.institution;
                            }}
                            
                            // Method 3: From y-axis position (most reliable)
                            if (!institution && point.y !== undefined) {{
                                const yValue = Math.round(point.y);
                                console.log('Y value:', yValue, 'Institutions:', institutions);
                                if (yValue >= 0 && yValue < institutions.length) {{
                                    institution = institutions[yValue];
                                }}
                            }}
                            
                            console.log('Final institution from click:', institution);
                            if (institution) {{
                                currentFilter = {{ type: 'institution', value: institution }};
                                updateFilterIndicator();
                                loadDashboardData('institution', institution);
                            }} else {{
                                console.warn('Could not determine institution from click');
                            }}
                        }}
                    }});
                }}, 500);
            }} catch (error) {{
                console.error('Error updating timeline:', error);
                showNoDataMessage('timeline-chart', 'Error rendering timeline chart.');
            }}
        }}
        
        function updateMapChart(data) {{
            if (!data || data.length === 0) {{
                showNoDataMessage('map-chart', 'No map data available.');
                return;
            }}
            
            try {{
                const countryCounts = {{}};
                data.forEach(d => {{
                    countryCounts[d.country] = (countryCounts[d.country] || 0) + 1;
                }});
                
                const countries = Object.keys(countryCounts);
                const counts = Object.values(countryCounts);
                
                if (countries.length === 0) {{
                    showNoDataMessage('map-chart', 'No country data available.');
                    return;
                }}
                
                const trace = {{
                    type: 'choropleth',
                    locationmode: 'country names',
                    locations: countries,
                    z: counts,
                    colorscale: 'Plasma',
                    showscale: false,
                    hovertemplate: '<b>%{{location}}</b><br>Count: %{{z}}<extra></extra>'
                }};
                
                const mapDiv = document.getElementById('map-chart');
                Plotly.newPlot(mapDiv, [trace], {{
                    template: 'plotly_dark',
                    geo: {{
                        bgcolor: 'rgba(0,0,0,0)',
                        showland: true,
                        landcolor: '#2c3e50',
                        showocean: true,
                        oceancolor: '#1f2b3e',
                        showcountries: true,
                        countrycolor: '#444'
                    }},
                    height: 300,
                    margin: {{ l: 0, r: 0, t: 0, b: 0 }},
                    paper_bgcolor: 'rgba(0,0,0,0)'
                }}, {{responsive: true}});
            }} catch (error) {{
                console.error('Error updating map chart:', error);
                showNoDataMessage('map-chart', 'Error rendering map.');
            }}
        }}
        
        function updateDonutChart(data) {{
            if (!data || data.length === 0) {{
                showNoDataMessage('donut-chart', 'No skills data available.');
                return;
            }}
            
            try {{
                // Sort by count for better visualization
                data.sort((a, b) => b.count - a.count);
                
                const colors = ['#00b7ff', '#f95d6a', '#ffa600', '#00d4aa', '#9b59b6', '#e74c3c', '#3498db', '#1abc9c', '#e67e22'];
                
                const trace = {{
                    values: data.map(d => d.count),
                    labels: data.map(d => d.type),
                    type: 'pie',
                    hole: 0.5,
                    marker: {{ 
                        colors: colors.slice(0, data.length),
                        line: {{
                            color: '#1f2b3e',
                            width: 2
                        }}
                    }},
                    textinfo: 'percent',
                    textposition: 'outside',
                    textfont: {{
                        color: '#f4f4f4',
                        size: 12,
                        family: 'Arial, sans-serif'
                    }},
                    hovertemplate: '<b>%{{label}}</b><br>Skills: %{{value}}<br>Percentage: %{{percent}}<extra></extra>',
                    rotation: 0,
                    sort: false  // Keep original order
                }};
                
                const donutDiv = document.getElementById('donut-chart');
                Plotly.newPlot(donutDiv, [trace], {{
                    template: 'plotly_dark',
                    height: 300,
                    margin: {{ l: 20, r: 120, t: 20, b: 20 }},
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    showlegend: true,
                    legend: {{ 
                        y: 0.5,
                        x: 1.02,
                        font: {{ color: '#f4f4f4', size: 9 }},
                        bgcolor: 'rgba(0,0,0,0)',
                        bordercolor: 'rgba(255,255,255,0.1)',
                        borderwidth: 1,
                        tracegroupgap: 5
                    }},
                    clickmode: 'event+select'
                }}, {{responsive: true}});
                
                // Setup click handler
                donutDiv.on('plotly_click', function(data) {{
                    if (data.points && data.points[0]) {{
                        const skillType = data.points[0].label;
                        if (skillType) {{
                            currentFilter = {{ type: 'skill_type', value: skillType }};
                            updateFilterIndicator();
                            loadDashboardData('skill_type', skillType);
                        }}
                    }}
                }});
            }} catch (error) {{
                console.error('Error updating donut chart:', error);
                showNoDataMessage('donut-chart', 'Error rendering chart.');
            }}
        }}
        
        function updateBarChart(data) {{
            if (!data || data.length === 0) {{
                showNoDataMessage('bar-chart', 'No skills data available.');
                return;
            }}
            
            try {{
                // Sort by years for better visualization
                data.sort((a, b) => a.years - b.years);
                
                const trace = {{
                    x: data.map(d => d.years),
                    y: data.map(d => d.skill),
                    type: 'bar',
                    orientation: 'h',
                    marker: {{ color: '#00b7ff' }},
                    text: data.map(d => d.years.toFixed(1) + ' yrs'),
                    textposition: 'outside',
                    hovertemplate: '<b>%{{y}}</b><br>Years: %{{x}}<extra></extra>'
                }};
                
                const barDiv = document.getElementById('bar-chart');
                Plotly.newPlot(barDiv, [trace], {{
                    template: 'plotly_dark',
                    height: 400,
                    margin: {{ l: 120, r: 50, t: 10, b: 10 }},
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    xaxis: {{ 
                        title: 'Years', 
                        showgrid: false,
                        zeroline: false
                    }},
                    yaxis: {{ 
                        title: '', 
                        tickfont: {{ size: 10, color: '#f4f4f4' }},
                        showgrid: false
                    }},
                    clickmode: 'event+select'
                }}, {{responsive: true}});
                
                // Setup click handler
                barDiv.on('plotly_click', function(data) {{
                    if (data.points && data.points[0]) {{
                        const skill = data.points[0].y;
                        if (skill) {{
                            currentFilter = {{ type: 'skill', value: skill }};
                            updateFilterIndicator();
                            loadDashboardData('skill', skill);
                        }}
                    }}
                }});
            }} catch (error) {{
                console.error('Error updating bar chart:', error);
                showNoDataMessage('bar-chart', 'Error rendering chart.');
            }}
        }}
        
        function handleKeyPress(event) {{
            if (event.key === 'Enter') {{
                askQuestion();
            }}
        }}
        
        async function askQuestion() {{
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            const button = document.getElementById('askButton');
            const loading = document.getElementById('loading');
            const chatContainer = document.getElementById('chatContainer');
            
            if (!question) return;
            
            input.disabled = true;
            button.disabled = true;
            loading.classList.add('show');
            
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.textContent = question;
            chatContainer.appendChild(userMsg);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            input.value = '';
            
            try {{
                const response = await fetch('/api/ask', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ question: question }})
                }});
                
                const data = await response.json();
                
                const botMsg = document.createElement('div');
                botMsg.className = 'message bot-message';
                botMsg.textContent = data.answer || 'Sorry, I could not process your question.';
                chatContainer.appendChild(botMsg);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }} catch (error) {{
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message bot-message';
                errorMsg.textContent = 'Error: Could not connect to the server.';
                chatContainer.appendChild(errorMsg);
            }} finally {{
                input.disabled = false;
                button.disabled = false;
                loading.classList.remove('show');
                input.focus();
            }}
        }}
        
        window.addEventListener('DOMContentLoaded', () => {{
            console.log('DOM loaded');
            console.log('Plotly available:', typeof Plotly !== 'undefined');
            console.log('Chart divs exist:', {{
                timeline: !!document.getElementById('timeline-chart'),
                map: !!document.getElementById('map-chart'),
                donut: !!document.getElementById('donut-chart'),
                bar: !!document.getElementById('bar-chart')
            }});
            
            // Wait for Plotly to load
            const checkPlotly = setInterval(() => {{
                if (typeof Plotly !== 'undefined') {{
                    clearInterval(checkPlotly);
                    console.log('Plotly loaded, initializing dashboard...');
                    setTimeout(() => {{
                        loadDashboardData();
                    }}, 200);
                }}
            }}, 100);
            
            // Timeout after 5 seconds
            setTimeout(() => {{
                clearInterval(checkPlotly);
                if (typeof Plotly === 'undefined') {{
                    console.error('Plotly.js failed to load');
                    showNoDataMessage('timeline-chart', 'Plotly.js not loaded. Check internet connection.');
                }}
            }}, 5000);
        }});
    </script>
</body>
</html>"""

@app.get("/api/dashboard/candidate")
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

