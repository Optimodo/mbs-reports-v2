import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Create directories if they don't exist
for directory in [INPUT_DIR, DATA_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# Excel processing settings
EXCEL_SETTINGS = {
    "sheet_name": 0,  # First sheet by default
    "skiprows": 6,    # Skip the first 6 rows
    "usecols": [
        "Status",
        "Type",
        "Doc Ref",
        "Doc Title",
        "Purpose of Issue",
        "Rev",
        "Date (WET)",
        "Last Status Change (WET)",
        "Publisher",
        "Associations",
        "File Name",
        "Doc Path",
        "aMessages",
        "Flag",
        "Secondary File(s)",
        "My Tasks",
        "Task Time"
    ]
}

# Change detection settings
CHANGE_DETECTION = {
    "track_columns": [
        "Status",
        "Doc Ref",
        "Doc Title",
        "Rev",
        "Date (WET)",
        "Last Status Change (WET)"
    ],
    "ignore_columns": [
        "Last Status Change (WET)",
        "Publisher"
    ]
}

# Report settings
REPORT_SETTINGS = {
    "weekly_summary": True,
    "change_report": True,
    "output_format": "excel",  # Options: excel, pdf, html
    "include_charts": True
} 