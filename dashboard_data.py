"""
Dashboard Data Module - Loads and processes resume data from Excel
"""
import os
import pandas as pd
from typing import Dict, Optional, List

# Define the path to the Excel file
DATA_PATH = os.path.join(os.path.dirname(__file__), "resume_data")
FILE_NAME = "resume_data.xlsx"

def load_data():
    """Loads and preprocesses data from the Excel file."""
    try:
        file_path = os.path.join(DATA_PATH, FILE_NAME)
        
        if not os.path.exists(file_path):
            if os.path.exists(FILE_NAME):
                file_path = FILE_NAME
            else:
                print(f"Warning: {FILE_NAME} not found at {DATA_PATH}")
                return None, None, None, None

        # Load Excel Sheets
        candidate = pd.read_excel(file_path, sheet_name='candidate_details')
        resume = pd.read_excel(file_path, sheet_name='resume')
        skills = pd.read_excel(file_path, sheet_name='skills')
        skills_resume = pd.read_excel(file_path, sheet_name='skills_resume')

        # Clean Dates
        resume['date_started'] = pd.to_datetime(resume['date_started'])
        resume['date_ended'] = pd.to_datetime(resume['date_ended']).fillna(pd.Timestamp.today())
        
        # Create display labels
        resume['display_title'] = resume.apply(
            lambda x: x['title'] if pd.notnull(x['title']) else x['education_degree'], axis=1
        )
        resume['display_institution'] = resume['institutution']
        resume['combined_label'] = resume.apply(
            lambda x: f"{x['display_title']} @ {x['display_institution']}", axis=1
        )

        # Merge data for filtering
        skills_linked = pd.merge(skills, skills_resume, on='skill_id', how='left')
        master_df = pd.merge(skills_linked, resume, on='resume_item_id', how='left')
        
        return candidate, resume, skills, master_df

    except Exception as e:
        print(f"Error loading dashboard data: {e}")
        return None, None, None, None

# Load data on module import
candidate_df, resume_df, skills_df, master_df = load_data()

def get_candidate_info() -> Dict:
    """Get candidate header information."""
    if candidate_df is not None and not candidate_df.empty:
        c_name = candidate_df.iloc[0]['full_name']
        c_email = candidate_df.iloc[0]['primary_email']
        c_phone = str(candidate_df.iloc[0]['cell_number'])
        
        # Get LinkedIn and GitHub if available
        c_linkedin = candidate_df.iloc[0].get('linkedin_profile', '')
        c_github = candidate_df.iloc[0].get('github_profile', '')
        
        if resume_df is not None and not resume_df.empty:
            latest_entry = resume_df.sort_values('date_ended', ascending=False).iloc[0]
            c_loc = f"{latest_entry['city']}, {latest_entry['country']}" 
        else:
            c_loc = "Unknown Location"
        
        return {
            "name": c_name,
            "email": c_email,
            "phone": c_phone,
            "location": c_loc,
            "linkedin": c_linkedin if pd.notnull(c_linkedin) else None,
            "github": c_github if pd.notnull(c_github) else None
        }
    return {
        "name": "Candidate Name",
        "email": "Email",
        "phone": "Phone",
        "location": "Location",
        "linkedin": None,
        "github": None
    }

def get_timeline_data(filtered_df: Optional[pd.DataFrame] = None) -> List[Dict]:
    """Get timeline data for the chart."""
    data = filtered_df if filtered_df is not None else resume_df
    if data is None or data.empty:
        return []
    
    data = data.sort_values('date_started')
    return [{
        "start": row['date_started'].strftime('%Y-%m-%d'),
        "end": row['date_ended'].strftime('%Y-%m-%d'),
        "institution": str(row['display_institution']),
        "title": str(row['display_title']),
        "category": str(row['category']),
        "city": str(row.get('city', '')),
        "country": str(row.get('country', '')),
        "label": str(row['combined_label'])
    } for _, row in data.iterrows()]

def get_map_data(filtered_df: Optional[pd.DataFrame] = None) -> List[Dict]:
    """Get map data for the chart."""
    data = filtered_df if filtered_df is not None else resume_df
    if data is None or data.empty:
        return []
    
    loc_data = data[['country', 'city', 'combined_label']].drop_duplicates()
    return [{
        "country": str(row['country']),
        "city": str(row['city']),
        "label": str(row['combined_label'])
    } for _, row in loc_data.iterrows()]

def get_skill_donut_data(filtered_df: Optional[pd.DataFrame] = None) -> List[Dict]:
    """Get skill donut chart data."""
    data = filtered_df if filtered_df is not None else skills_df
    if data is None or data.empty:
        return []
    
    df_grouped = data.groupby('skill_type')['skill'].nunique().reset_index(name='count')
    return [{
        "type": str(row['skill_type']),
        "count": int(row['count'])
    } for _, row in df_grouped.iterrows()]

def get_skill_bar_data(filtered_df: Optional[pd.DataFrame] = None) -> List[Dict]:
    """Get skill bar chart data."""
    data = filtered_df if filtered_df is not None else skills_df
    if data is None or data.empty:
        return []
    
    df_grouped = data.groupby('skill')['years_of_experience'].max().reset_index()
    df_grouped = df_grouped.sort_values('years_of_experience', ascending=True)
    return [{
        "skill": str(row['skill']),
        "years": float(row['years_of_experience'])
    } for _, row in df_grouped.iterrows()]

def filter_by_institution(institution: str) -> Optional[pd.DataFrame]:
    """Filter master_df by institution."""
    if master_df is None:
        return None
    return master_df[master_df['display_institution'] == institution]

def filter_by_skill_type(skill_type: str) -> Optional[pd.DataFrame]:
    """Filter master_df by skill type."""
    if master_df is None:
        return None
    return master_df[master_df['skill_type'] == skill_type]

def filter_by_skill(skill: str) -> Optional[pd.DataFrame]:
    """Filter master_df by specific skill."""
    if master_df is None:
        return None
    return master_df[master_df['skill'] == skill]

