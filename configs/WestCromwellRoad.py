"""Configuration for West Cromwell Road project."""

import pandas as pd

PROJECT_TITLE = "West Cromwell Road"

# CSV Settings for West Cromwell Road
CSV_SETTINGS = {
    'encoding': 'utf-8',
    'sep': ',',
    'quotechar': '"',
    'escapechar': '\\',
    'na_values': ['', 'nan', 'NaN', 'NULL'],
    'keep_default_na': True
}

# Column mappings - Now using Excel source (previously CSV)
# Excel has both 'Status' and 'Revision Workflow' columns
# We'll use both: Status for superseded detection, Revision Workflow for main status
COLUMN_MAPPINGS = {
    'Doc Ref': 'Name',                        # Document reference is in Name column
    'Doc Title': 'Description',               # Document title is in Description column  
    'Rev': 'Revision',                        # Revision is in Revision column
    'Status': 'Revision Workflow',            # Primary status from Revision Workflow column
    'Date (WET)': 'Revision Date Modified',   # Date is in Revision Date Modified column
    'Doc Path': 'Full Path'                   # Full folder path for filtering
}

# Excel processing settings
# Using new Excel source with Full Path column
EXCEL_SETTINGS = {
    "sheet_name": 0
    # No skiprows or usecols - load all columns from the Excel file
    # Column mapping will handle transforming to standard format
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
        "Last Status Change (WET)"
    ]
}

# Report settings
REPORT_SETTINGS = {
    "weekly_summary": True,
    "change_report": True,
    "output_format": "excel",
    "include_charts": True
} 

# File type settings
FILE_TYPE_SETTINGS = {
    "enabled": False
}

# Certificate Settings
CERTIFICATE_SETTINGS = {
    'enabled': False,
    'generate_report': False
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': False,
    'generate_report': False
}

# Drawing Settings (for main summary report - all documents in this case)
DRAWING_SETTINGS = {
    'enabled': False  # No file type column, so include all documents
}

# Status Mappings - Maps actual Revision Workflow values to standardized categories
# Note: Now using 'Revision Workflow' column instead of 'Status' column
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A (Approved)',
        'color': '25E82C',  # Green
        'statuses': [
            'EA+DM - Status A',
        ],
        'description': 'Approved documents - ready to proceed'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'Status B',
        ],
        'description': 'Approved documents - ready to proceed'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'QA Rejected',
            'Not Approved'
        ],
        'description': 'Rejected documents requiring revision'
    },
    'Under Review': {
        'display_name': 'Under Review',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Under DC Review',
            'Yes - Proceed to EA Review',
            'Yes - Proceed to Consultant Review',
            'QA Approved'
        ],
        'description': 'Documents currently under review'
    },
    'Other': {
        'display_name': 'Other',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Superseeded',
            'Withdrawn',
            'Ardmore Package Manager'
        ],
        'description': 'Superseeded or Withdrawn documents'
    }
}

# Display order for progression reports
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'Under Review',
    'Other'
]

def map_wcr_status(row):
    """
    Custom status mapping for West Cromwell Road.
    
    Special logic:
    - Documents in '/SS/' folder (superseded) → map to 'Superseeded' status
    - This ensures superseded documents are categorized as 'Other' status
    
    The Excel file has both 'Status' and 'Revision Workflow' columns:
    - 'Status' column shows document state (Superseded, ACTIVE, REVISED, etc.)
    - 'Revision Workflow' column shows workflow status (QA Approved, Not Approved, etc.)
    - 'Full Path' column shows folder location
    
    We use:
    1. Full Path to detect /SS/ folder → set to 'Superseeded'
    2. Otherwise, use Revision Workflow for normal status mapping
    """
    # Get the full path (after column mapping, this will be in 'Doc Path')
    doc_path = row.get('Full Path', '') if pd.notna(row.get('Full Path', '')) else ''
    doc_path = str(doc_path).strip()
    
    # Check if document is in SS (superseded) folder
    # Path format is "/ SS /" with spaces around SS
    if '/ SS /' in doc_path or '/ ss /' in doc_path or '/SS/' in doc_path or '/ss/' in doc_path:
        return 'Superseeded'
    
    # Get the status column value (this will be raw 'Status' from Excel)
    status_raw = row.get('Status', '') if pd.notna(row.get('Status', '')) else ''
    status_raw = str(status_raw).strip()
    
    # If Status column explicitly says Superseded (regardless of folder)
    if status_raw.lower() == 'superseded':
        return 'Superseeded'
    
    # Otherwise, use Revision Workflow column for normal status mapping
    revision_workflow = row.get('Revision Workflow', '') if pd.notna(row.get('Revision Workflow', '')) else ''
    revision_workflow = str(revision_workflow).strip()
    
    # Handle string 'nan' from pandas string conversion
    if revision_workflow.lower() == 'nan':
        revision_workflow = ''
    
    # Return the Revision Workflow value (will be mapped by STATUS_MAPPINGS)
    if revision_workflow:
        return revision_workflow
    
    return 'Other'
