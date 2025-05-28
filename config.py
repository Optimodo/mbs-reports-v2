import os
from pathlib import Path
import importlib.util
import sys
import pandas as pd

# Base directories
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
CONFIGS_DIR = BASE_DIR / "configs"

# Create directories if they don't exist
for directory in [INPUT_DIR, DATA_DIR, REPORTS_DIR, CONFIGS_DIR]:
    directory.mkdir(exist_ok=True)

# Project detection settings
PROJECT_CODES = {
    'H8499': 'NewMalden',
    'JXXXZ18': 'GreenwichPeninsula',
    'R459': 'OvalBlockB'
}

def detect_project_from_file(file_path):
    """Detect project from the Doc Ref in the Excel file."""
    try:
        # Read just the Doc Ref column (column C) from row 8
        df = pd.read_excel(file_path, usecols="C", skiprows=7, nrows=1)
        if df.empty:
            return None
            
        doc_ref = df.iloc[0, 0]
        if pd.isna(doc_ref):
            return None
            
        # Extract project code (everything before first hyphen)
        project_code = str(doc_ref).split('-')[0]
        
        # Look up project name
        return PROJECT_CODES.get(project_code)
    except Exception as e:
        print(f"Error detecting project from file: {str(e)}")
        return None

def load_project_config(project_name=None, file_path=None):
    """Load project-specific configuration.
    
    Args:
        project_name: Optional project name to load config for
        file_path: Optional file path to detect project from
        
    Returns:
        dict: Project configuration
    """
    # If no project name provided, try to detect from file
    if not project_name and file_path:
        project_name = detect_project_from_file(file_path)
        if project_name:
            print(f"\nDetected project: {project_name}")
    
    # If still no project name, use default
    if not project_name:
        print("\nNo project specified or detected, using default configuration")
        return DEFAULT_SETTINGS
    
    config_file = CONFIGS_DIR / f"{project_name}.py"
    
    if not config_file.exists():
        print(f"Warning: Configuration file for project '{project_name}' not found at {config_file}")
        print("Using default configuration")
        return DEFAULT_SETTINGS
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(project_name, config_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[project_name] = module
    spec.loader.exec_module(module)
    
    return {
        'EXCEL_SETTINGS': module.EXCEL_SETTINGS,
        'CHANGE_DETECTION': module.CHANGE_DETECTION,
        'REPORT_SETTINGS': module.REPORT_SETTINGS,
        'FILE_TYPE_SETTINGS': module.FILE_TYPE_SETTINGS
    }

# Default settings (used if no project is specified)
DEFAULT_SETTINGS = {
    'EXCEL_SETTINGS': {
        "sheet_name": 0,
        "skiprows": 6,
        "usecols": [
            "Status",
            "Doc Ref",
            "Doc Title",
            "Rev",
            "Date (WET)",
            "Last Status Change (WET)",
            "Doc Path",
            "File Type"  # Default file type column
        ]
    },
    'CHANGE_DETECTION': {
        "track_columns": [
            "Status",
            "Doc Ref",
            "Doc Title",
            "Rev",
            "Date (WET)",
            "Last Status Change (WET)"
        ],
        "ignore_columns": [
            "Last Status Change (WET)"
        ]
    },
    'REPORT_SETTINGS': {
        "weekly_summary": True,
        "change_report": True,
        "output_format": "excel",
        "include_charts": True
    },
    'FILE_TYPE_SETTINGS': {
        "column_name": "File Type",  # Default file type column name
        "include_in_summary": True,
        "summary_title": "File Type Summary"
    }
} 