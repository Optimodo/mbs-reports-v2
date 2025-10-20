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
            'Not Approved',
            'DM - Status C'
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

# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,
    'file_path': 'WCR Accommodation Schedule 201025.xlsx',
    'read_config': {
        'sheet_name': 0,
        'skiprows': 1,       # Skip row 1, use row 2 as header
        'nrows': 462,        # Rows 3-464 (462 apartments)
        'usecols': 'A:G'     # Columns A through G
    },
    'column_mapping': {
        'apartment': 'Name',             # Column C (e.g., B1.03.001)
        'block': 'Building',             # Column A (e.g., B1)
        'floor': 'Level',                # Column B (already numeric)
        'apartment_type': 'Apt Type',    # Column D
        'bedrooms': 'Beds',              # Column E (already numeric)
        'tenure': 'Tenure'               # Column G
    },
    'apartment_cleaning': {
        'remove_prefix': '',             # Keep apartment numbers as-is (B1.03.001)
        'extract_pattern': None          # Don't extract, keep full string
    },
    'floor_cleaning': {
        'remove_prefix': '',             # Floor is already numeric
        'remove_suffix': '',
        'convert_to_int': True
    }
}

# Accommodation Data (Auto-generated - DO NOT EDIT MANUALLY)
# Run scripts/update_accommodation_data.py to regenerate this section


# Accommodation Data - Auto-generated by update_accommodation_data.py
# Last updated: 2025-10-21
# Source: WCR Accommodation Schedule 201025.xlsx
ACCOMMODATION_DATA = {
    'total_apartments': 462,
    'last_updated': '2025-10-21',
    'source_file': 'WCR Accommodation Schedule 201025.xlsx',
    
    'phases': {
        'Default': {
            'apartment_count': 462,
            'apartments': ['B1.03.001', 'B1.03.002', 'B1.03.003', 'B1.03.004', 'B1.04.001', 'B1.04.002', 'B1.04.003', 'B1.04.004', 'B1.05.001', 'B1.05.002', 'B1.05.003', 'B1.05.004', 'B1.06.001', 'B1.06.002', 'B1.06.003', 'B1.06.004', 'B1.07.001', 'B1.07.002', 'B1.07.003', 'B1.07.004', 'B1.08.001', 'B1.08.002', 'B1.08.003', 'B1.08.004', 'B1.09.001', 'B1.09.002', 'B1.10.001', 'B1.10.002', 'B1.11.001', 'B1.11.002', 'B1.12.001', 'B2.02.001', 'B2.02.002', 'B2.03.001', 'B2.03.002', 'B2.03.003', 'B2.03.004', 'B2.04.001', 'B2.04.002', 'B2.04.003', 'B2.04.004', 'B2.04.005', 'B2.04.006', 'B2.05.001', 'B2.05.002', 'B2.05.003', 'B2.05.004', 'B2.05.005', 'B2.05.006', 'B2.06.001', 'B2.06.002', 'B2.06.003', 'B2.06.004', 'B2.06.005', 'B2.06.006', 'B2.07.001', 'B2.07.002', 'B2.07.003', 'B2.07.004', 'B2.07.005', 'B2.07.006', 'B2.08.001', 'B2.08.002', 'B2.08.003', 'B2.08.004', 'B2.08.005', 'B2.08.006', 'B2.09.001', 'B2.09.002', 'B2.09.003', 'B2.09.004', 'B2.09.005', 'B2.09.006', 'B2.10.001', 'B2.10.002', 'B2.10.003', 'B2.10.004', 'B2.10.005', 'B2.11.001', 'B2.11.002', 'B2.11.003', 'B2.11.004', 'B2.11.005', 'B2.12.001', 'B2.12.002', 'B2.12.003', 'B2.12.004', 'B2.12.005', 'B2.13.001', 'B2.13.002', 'B2.13.003', 'B2.13.004', 'B2.13.005', 'B2.14.001', 'B2.14.002', 'B2.14.003', 'B2.14.004', 'B2.14.005', 'B2.15.001', 'B2.15.002', 'B2.15.003', 'B2.15.004', 'B2.15.005', 'B2.16.001', 'B2.16.002', 'B2.16.003', 'B2.16.004', 'B2.16.005', 'B2.17.001', 'B2.17.002', 'B2.17.003', 'B2.17.004', 'B2.17.005', 'B2.18.001', 'B2.18.002', 'B2.18.003', 'B2.18.004', 'B2.18.005', 'B2.19.001', 'B2.19.002', 'B2.19.003', 'B2.19.004', 'B2.19.005', 'B2.20.001', 'B2.20.002', 'B2.20.003', 'B2.20.004', 'B2.20.005', 'B2.21.001', 'B2.21.002', 'B2.21.003', 'B2.21.004', 'B2.22.001', 'B2.22.002', 'B2.22.003', 'B2.22.004', 'B2.23.001', 'B2.23.002', 'B2.23.003', 'B2.23.004', 'B2.24.001', 'B2.24.002', 'B2.24.003', 'B2.24.004', 'B2.25.001', 'B2.25.002', 'B2.25.003', 'B2.25.004', 'B2.26.001', 'B2.26.002', 'B2.26.003', 'B2.26.004', 'B2.27.001', 'B2.27.002', 'B2.27.002', 'B2.27.004', 'B2.28.001', 'B2.28.002', 'B2.29.001', 'B2.29.002', 'B3.02.001', 'B3.02.002', 'B3.02.003', 'B3.02.004', 'B3.02.005', 'B3.02.006', 'B3.02.007', 'B3.03.001', 'B3.03.002', 'B3.03.003', 'B3.03.004', 'B3.03.005', 'B3.03.006', 'B3.03.007', 'B3.03.008', 'B3.04.001', 'B3.04.002', 'B3.04.003', 'B3.04.004', 'B3.04.005', 'B3.04.006', 'B3.04.007', 'B3.04.008', 'B3.05.001', 'B3.05.002', 'B3.05.003', 'B3.05.004', 'B3.05.005', 'B3.05.006', 'B3.05.007', 'B3.05.008', 'B3.06.001', 'B3.06.002', 'B3.06.003', 'B3.06.004', 'B3.06.005', 'B3.06.006', 'B3.06.007', 'B3.07.001', 'B3.07.002', 'B3.07.003', 'B3.07.004', 'B3.07.005', 'B3.07.006', 'B3.07.007', 'B3.08.001', 'B3.08.002', 'B3.08.003', 'B3.08.004', 'B3.08.005', 'B3.08.006', 'B3.08.007', 'B3.09.001', 'B3.09.002', 'B3.09.003', 'B3.09.004', 'B3.09.005', 'B3.09.006', 'B3.09.007', 'B3.10.001', 'B3.10.002', 'B3.10.003', 'B3.10.004', 'B3.10.005', 'B3.10.006', 'B3.10.007', 'B3.11.001', 'B3.11.002', 'B3.11.003', 'B3.11.004', 'B3.11.005', 'B3.11.006', 'B3.11.007', 'B3.12.001', 'B3.12.002', 'B4.02.001', 'B4.02.002', 'B4.02.003', 'B4.02.004', 'B4.02.005', 'B4.02.006', 'B4.02.007', 'B4.03.001', 'B4.03.002', 'B4.03.003', 'B4.03.004', 'B4.03.005', 'B4.03.006', 'B4.03.007', 'B4.03.008', 'B4.04.001', 'B4.04.002', 'B4.04.003', 'B4.04.004', 'B4.04.005', 'B4.04.006', 'B4.04.007', 'B4.04.008', 'B4.05.001', 'B4.05.002', 'B4.05.003', 'B4.05.004', 'B4.05.005', 'B4.05.006', 'B4.05.007', 'B4.05.008', 'B4.06.001', 'B4.06.002', 'B4.06.003', 'B4.06.004', 'B4.06.005', 'B4.06.006', 'B4.06.007', 'B4.07.001', 'B4.07.002', 'B4.07.003', 'B4.07.004', 'B4.07.005', 'B4.07.006', 'B4.07.007', 'B4.08.001', 'B4.08.002', 'B4.08.003', 'B4.08.004', 'B4.08.005', 'B4.08.006', 'B4.08.007', 'B4.09.001', 'B4.09.002', 'B4.09.003', 'B4.09.004', 'B4.09.005', 'B4.09.006', 'B4.09.007', 'B4.10.001', 'B4.10.002', 'B4.10.003', 'B4.10.004', 'B4.10.005', 'B4.10.006', 'B4.10.007', 'B4.11.001', 'B4.11.002', 'B4.11.003', 'B4.11.004', 'B4.11.005', 'B4.11.006', 'B4.11.007', 'B4.12.001', 'B4.12.002', 'B4.12.003', 'B4.12.004', 'B4.12.005', 'B4.12.006', 'B4.12.007', 'B4.13.001', 'B4.13.002', 'B4.14.001', 'B4.14.002', 'B5.02.001', 'B5.02.002', 'B5.02.003', 'B5.02.004', 'B5.02.005', 'B5.02.006', 'B5.02.007', 'B5.02.008', 'B5.02.009', 'B5.02.010', 'B5.03.001', 'B5.03.002', 'B5.03.003', 'B5.03.004', 'B5.03.005', 'B5.03.006', 'B5.03.007', 'B5.03.008', 'B5.03.009', 'B5.04.001', 'B5.04.002', 'B5.04.003', 'B5.04.004', 'B5.04.005', 'B5.04.006', 'B5.04.007', 'B5.04.008', 'B5.04.009', 'B5.05.001', 'B5.05.002', 'B5.05.003', 'B5.05.004', 'B5.05.005', 'B5.05.006', 'B5.05.007', 'B5.05.008', 'B5.05.009', 'B5.06.001', 'B5.06.002', 'B5.06.003', 'B5.06.004', 'B5.06.005', 'B5.06.006', 'B5.06.007', 'B5.06.008', 'B5.06.009', 'B5.07.001', 'B5.07.002', 'B5.07.003', 'B5.07.004', 'B5.07.005', 'B5.07.006', 'B5.07.007', 'B5.07.008', 'B5.07.009', 'B5.08.001', 'B5.08.002', 'B5.08.003', 'B5.08.004', 'B5.08.005', 'B5.08.006', 'B5.08.007', 'B5.08.008', 'B5.08.009', 'B5.09.001', 'B5.09.002', 'B5.09.003', 'B5.09.004', 'B5.09.005', 'B5.09.006', 'B5.09.007', 'B5.09.008', 'B5.09.009', 'B5.10.001', 'B5.10.002', 'B5.10.003', 'B5.10.004', 'B5.10.005', 'B5.10.006', 'B5.10.007', 'B5.10.008', 'B5.10.009', 'B5.11.001', 'B5.11.002', 'B5.11.003', 'B5.11.004', 'B5.11.005', 'B5.11.006', 'B5.11.007', 'B5.11.008', 'B5.11.009', 'B5.12.001', 'B5.12.002', 'B5.12.003', 'B5.12.004', 'B5.12.005', 'B5.12.006', 'B5.13.001', 'B5.13.002', 'B5.13.003', 'B5.13.004', 'B5.13.005', 'B5.13.006', 'B7. 1.001', 'B7. 1.002', 'B7.00.001', 'B7.00.T01', 'B7.00.T02', 'B7.00.T03', 'B7.00.T04', 'B7.01.001', 'B7.01.003', 'B7.02.001', 'B7.02.002', 'B7.02.003', 'B7.02.004', 'B7.02.005', 'B7.03.001', 'B7.03.002', 'B7.03.003', 'B7.03.004', 'B7.04.001', 'B7.04.002', 'B7.04.003', 'B7.04.004', 'B7.05.001', 'B7.05.002', 'B7.05.003', 'B7.06.001', 'B7.06.002', 'B7.06.003', 'B7.07.001', 'B7.07.002', 'B7.07.003', 'B7.08.001', 'B7.08.002', 'B7.09.001', 'B7.09.002', 'B7.10.001', 'B7.10.002', 'B7.12.001', 'B7.12.002', 'B7.13.001'],
            'blocks': {
                'B1': {
                    'apartment_count': 31,
                    'apartments': ['B1.03.001', 'B1.03.002', 'B1.03.003', 'B1.03.004', 'B1.04.001', 'B1.04.002', 'B1.04.003', 'B1.04.004', 'B1.05.001', 'B1.05.002', 'B1.05.003', 'B1.05.004', 'B1.06.001', 'B1.06.002', 'B1.06.003', 'B1.06.004', 'B1.07.001', 'B1.07.002', 'B1.07.003', 'B1.07.004', 'B1.08.001', 'B1.08.002', 'B1.08.003', 'B1.08.004', 'B1.09.001', 'B1.09.002', 'B1.10.001', 'B1.10.002', 'B1.11.001', 'B1.11.002', 'B1.12.001'],
                    'floors': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                },
                'B2': {
                    'apartment_count': 129,
                    'apartments': ['B2.02.001', 'B2.02.002', 'B2.03.001', 'B2.03.002', 'B2.03.003', 'B2.03.004', 'B2.04.001', 'B2.04.002', 'B2.04.003', 'B2.04.004', 'B2.04.005', 'B2.04.006', 'B2.05.001', 'B2.05.002', 'B2.05.003', 'B2.05.004', 'B2.05.005', 'B2.05.006', 'B2.06.001', 'B2.06.002', 'B2.06.003', 'B2.06.004', 'B2.06.005', 'B2.06.006', 'B2.07.001', 'B2.07.002', 'B2.07.003', 'B2.07.004', 'B2.07.005', 'B2.07.006', 'B2.08.001', 'B2.08.002', 'B2.08.003', 'B2.08.004', 'B2.08.005', 'B2.08.006', 'B2.09.001', 'B2.09.002', 'B2.09.003', 'B2.09.004', 'B2.09.005', 'B2.09.006', 'B2.10.001', 'B2.10.002', 'B2.10.003', 'B2.10.004', 'B2.10.005', 'B2.11.001', 'B2.11.002', 'B2.11.003', 'B2.11.004', 'B2.11.005', 'B2.12.001', 'B2.12.002', 'B2.12.003', 'B2.12.004', 'B2.12.005', 'B2.13.001', 'B2.13.002', 'B2.13.003', 'B2.13.004', 'B2.13.005', 'B2.14.001', 'B2.14.002', 'B2.14.003', 'B2.14.004', 'B2.14.005', 'B2.15.001', 'B2.15.002', 'B2.15.003', 'B2.15.004', 'B2.15.005', 'B2.16.001', 'B2.16.002', 'B2.16.003', 'B2.16.004', 'B2.16.005', 'B2.17.001', 'B2.17.002', 'B2.17.003', 'B2.17.004', 'B2.17.005', 'B2.18.001', 'B2.18.002', 'B2.18.003', 'B2.18.004', 'B2.18.005', 'B2.19.001', 'B2.19.002', 'B2.19.003', 'B2.19.004', 'B2.19.005', 'B2.20.001', 'B2.20.002', 'B2.20.003', 'B2.20.004', 'B2.20.005', 'B2.21.001', 'B2.21.002', 'B2.21.003', 'B2.21.004', 'B2.22.001', 'B2.22.002', 'B2.22.003', 'B2.22.004', 'B2.23.001', 'B2.23.002', 'B2.23.003', 'B2.23.004', 'B2.24.001', 'B2.24.002', 'B2.24.003', 'B2.24.004', 'B2.25.001', 'B2.25.002', 'B2.25.003', 'B2.25.004', 'B2.26.001', 'B2.26.002', 'B2.26.003', 'B2.26.004', 'B2.27.001', 'B2.27.002', 'B2.27.002', 'B2.27.004', 'B2.28.001', 'B2.28.002', 'B2.29.001', 'B2.29.002'],
                    'floors': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
                },
                'B3': {
                    'apartment_count': 75,
                    'apartments': ['B3.02.001', 'B3.02.002', 'B3.02.003', 'B3.02.004', 'B3.02.005', 'B3.02.006', 'B3.02.007', 'B3.03.001', 'B3.03.002', 'B3.03.003', 'B3.03.004', 'B3.03.005', 'B3.03.006', 'B3.03.007', 'B3.03.008', 'B3.04.001', 'B3.04.002', 'B3.04.003', 'B3.04.004', 'B3.04.005', 'B3.04.006', 'B3.04.007', 'B3.04.008', 'B3.05.001', 'B3.05.002', 'B3.05.003', 'B3.05.004', 'B3.05.005', 'B3.05.006', 'B3.05.007', 'B3.05.008', 'B3.06.001', 'B3.06.002', 'B3.06.003', 'B3.06.004', 'B3.06.005', 'B3.06.006', 'B3.06.007', 'B3.07.001', 'B3.07.002', 'B3.07.003', 'B3.07.004', 'B3.07.005', 'B3.07.006', 'B3.07.007', 'B3.08.001', 'B3.08.002', 'B3.08.003', 'B3.08.004', 'B3.08.005', 'B3.08.006', 'B3.08.007', 'B3.09.001', 'B3.09.002', 'B3.09.003', 'B3.09.004', 'B3.09.005', 'B3.09.006', 'B3.09.007', 'B3.10.001', 'B3.10.002', 'B3.10.003', 'B3.10.004', 'B3.10.005', 'B3.10.006', 'B3.10.007', 'B3.11.001', 'B3.11.002', 'B3.11.003', 'B3.11.004', 'B3.11.005', 'B3.11.006', 'B3.11.007', 'B3.12.001', 'B3.12.002'],
                    'floors': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                },
                'B4': {
                    'apartment_count': 84,
                    'apartments': ['B4.02.001', 'B4.02.002', 'B4.02.003', 'B4.02.004', 'B4.02.005', 'B4.02.006', 'B4.02.007', 'B4.03.001', 'B4.03.002', 'B4.03.003', 'B4.03.004', 'B4.03.005', 'B4.03.006', 'B4.03.007', 'B4.03.008', 'B4.04.001', 'B4.04.002', 'B4.04.003', 'B4.04.004', 'B4.04.005', 'B4.04.006', 'B4.04.007', 'B4.04.008', 'B4.05.001', 'B4.05.002', 'B4.05.003', 'B4.05.004', 'B4.05.005', 'B4.05.006', 'B4.05.007', 'B4.05.008', 'B4.06.001', 'B4.06.002', 'B4.06.003', 'B4.06.004', 'B4.06.005', 'B4.06.006', 'B4.06.007', 'B4.07.001', 'B4.07.002', 'B4.07.003', 'B4.07.004', 'B4.07.005', 'B4.07.006', 'B4.07.007', 'B4.08.001', 'B4.08.002', 'B4.08.003', 'B4.08.004', 'B4.08.005', 'B4.08.006', 'B4.08.007', 'B4.09.001', 'B4.09.002', 'B4.09.003', 'B4.09.004', 'B4.09.005', 'B4.09.006', 'B4.09.007', 'B4.10.001', 'B4.10.002', 'B4.10.003', 'B4.10.004', 'B4.10.005', 'B4.10.006', 'B4.10.007', 'B4.11.001', 'B4.11.002', 'B4.11.003', 'B4.11.004', 'B4.11.005', 'B4.11.006', 'B4.11.007', 'B4.12.001', 'B4.12.002', 'B4.12.003', 'B4.12.004', 'B4.12.005', 'B4.12.006', 'B4.12.007', 'B4.13.001', 'B4.13.002', 'B4.14.001', 'B4.14.002'],
                    'floors': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                },
                'B5': {
                    'apartment_count': 103,
                    'apartments': ['B5.02.001', 'B5.02.002', 'B5.02.003', 'B5.02.004', 'B5.02.005', 'B5.02.006', 'B5.02.007', 'B5.02.008', 'B5.02.009', 'B5.02.010', 'B5.03.001', 'B5.03.002', 'B5.03.003', 'B5.03.004', 'B5.03.005', 'B5.03.006', 'B5.03.007', 'B5.03.008', 'B5.03.009', 'B5.04.001', 'B5.04.002', 'B5.04.003', 'B5.04.004', 'B5.04.005', 'B5.04.006', 'B5.04.007', 'B5.04.008', 'B5.04.009', 'B5.05.001', 'B5.05.002', 'B5.05.003', 'B5.05.004', 'B5.05.005', 'B5.05.006', 'B5.05.007', 'B5.05.008', 'B5.05.009', 'B5.06.001', 'B5.06.002', 'B5.06.003', 'B5.06.004', 'B5.06.005', 'B5.06.006', 'B5.06.007', 'B5.06.008', 'B5.06.009', 'B5.07.001', 'B5.07.002', 'B5.07.003', 'B5.07.004', 'B5.07.005', 'B5.07.006', 'B5.07.007', 'B5.07.008', 'B5.07.009', 'B5.08.001', 'B5.08.002', 'B5.08.003', 'B5.08.004', 'B5.08.005', 'B5.08.006', 'B5.08.007', 'B5.08.008', 'B5.08.009', 'B5.09.001', 'B5.09.002', 'B5.09.003', 'B5.09.004', 'B5.09.005', 'B5.09.006', 'B5.09.007', 'B5.09.008', 'B5.09.009', 'B5.10.001', 'B5.10.002', 'B5.10.003', 'B5.10.004', 'B5.10.005', 'B5.10.006', 'B5.10.007', 'B5.10.008', 'B5.10.009', 'B5.11.001', 'B5.11.002', 'B5.11.003', 'B5.11.004', 'B5.11.005', 'B5.11.006', 'B5.11.007', 'B5.11.008', 'B5.11.009', 'B5.12.001', 'B5.12.002', 'B5.12.003', 'B5.12.004', 'B5.12.005', 'B5.12.006', 'B5.13.001', 'B5.13.002', 'B5.13.003', 'B5.13.004', 'B5.13.005', 'B5.13.006'],
                    'floors': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                },
                'B7': {
                    'apartment_count': 40,
                    'apartments': ['B7. 1.001', 'B7. 1.002', 'B7.00.001', 'B7.00.T01', 'B7.00.T02', 'B7.00.T03', 'B7.00.T04', 'B7.01.001', 'B7.01.003', 'B7.02.001', 'B7.02.002', 'B7.02.003', 'B7.02.004', 'B7.02.005', 'B7.03.001', 'B7.03.002', 'B7.03.003', 'B7.03.004', 'B7.04.001', 'B7.04.002', 'B7.04.003', 'B7.04.004', 'B7.05.001', 'B7.05.002', 'B7.05.003', 'B7.06.001', 'B7.06.002', 'B7.06.003', 'B7.07.001', 'B7.07.002', 'B7.07.003', 'B7.08.001', 'B7.08.002', 'B7.09.001', 'B7.09.002', 'B7.10.001', 'B7.10.002', 'B7.12.001', 'B7.12.002', 'B7.13.001'],
                    'floors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                },
            }
        },
    },
    
    'apartment_types': {
        'B1-2A': {
            'count': 8,
            'bedrooms': 2,
            'apartments': ['B1.03.001', 'B1.04.001', 'B1.05.001', 'B1.06.001', 'B1.07.001', 'B1.08.001', 'B1.09.001', 'B1.10.001']
        },
        'B1-1A': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B1.03.002', 'B1.04.002', 'B1.05.002', 'B1.06.002', 'B1.07.002', 'B1.08.002']
        },
        'B1-2B.1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B1.03.003']
        },
        'B1-2C': {
            'count': 9,
            'bedrooms': 2,
            'apartments': ['B1.03.004', 'B1.04.004', 'B1.05.004', 'B1.06.004', 'B1.07.004', 'B1.08.004', 'B1.09.002', 'B1.10.002', 'B1.11.002']
        },
        'B1-2B': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B1.04.003', 'B1.05.003', 'B1.06.003', 'B1.07.003', 'B1.08.003']
        },
        'B1-2A.1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B1.11.001']
        },
        'B1-3A': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B1.12.001']
        },
        'B2-2B': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B2.02.001']
        },
        'B2-2A': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B2.02.002']
        },
        'B2-2D': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B2.03.001']
        },
        'B2-1A': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B2.03.002']
        },
        'B2-2C': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B2.03.003']
        },
        'B2-3A': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B2.03.004']
        },
        'B2-2H': {
            'count': 17,
            'bedrooms': 2,
            'apartments': ['B2.04.001', 'B2.05.001', 'B2.06.001', 'B2.07.001', 'B2.08.001', 'B2.09.001', 'B2.10.001', 'B2.11.001', 'B2.12.001', 'B2.13.001', 'B2.14.001', 'B2.15.001', 'B2.16.001', 'B2.17.001', 'B2.18.001', 'B2.19.001', 'B2.20.001']
        },
        'B2-2E': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B2.04.002', 'B2.05.002', 'B2.06.002', 'B2.07.002', 'B2.08.002', 'B2.09.002']
        },
        'B2-1B': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B2.04.003', 'B2.05.003', 'B2.06.003', 'B2.07.003', 'B2.08.003', 'B2.09.003']
        },
        'B2-2F': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B2.04.004', 'B2.05.004', 'B2.06.004', 'B2.07.004', 'B2.08.004', 'B2.09.004']
        },
        'B2-2G': {
            'count': 17,
            'bedrooms': 2,
            'apartments': ['B2.04.005', 'B2.05.005', 'B2.06.005', 'B2.07.005', 'B2.08.005', 'B2.09.005', 'B2.10.004', 'B2.11.004', 'B2.12.004', 'B2.13.004', 'B2.14.004', 'B2.15.004', 'B2.16.004', 'B2.17.004', 'B2.18.004', 'B2.19.004', 'B2.20.004']
        },
        'B2-1C': {
            'count': 17,
            'bedrooms': 1,
            'apartments': ['B2.04.006', 'B2.05.006', 'B2.06.006', 'B2.07.006', 'B2.08.006', 'B2.09.006', 'B2.10.005', 'B2.11.005', 'B2.12.005', 'B2.13.005', 'B2.14.005', 'B2.15.005', 'B2.16.005', 'B2.17.005', 'B2.18.005', 'B2.19.005', 'B2.20.005']
        },
        'B2-2J': {
            'count': 11,
            'bedrooms': 2,
            'apartments': ['B2.10.002', 'B2.11.002', 'B2.12.002', 'B2.13.002', 'B2.14.002', 'B2.15.002', 'B2.16.002', 'B2.17.002', 'B2.18.002', 'B2.19.002', 'B2.20.002']
        },
        'B2-2K': {
            'count': 11,
            'bedrooms': 2,
            'apartments': ['B2.10.003', 'B2.11.003', 'B2.12.003', 'B2.13.003', 'B2.14.003', 'B2.15.003', 'B2.16.003', 'B2.17.003', 'B2.18.003', 'B2.19.003', 'B2.20.003']
        },
        'B2-3E': {
            'count': 6,
            'bedrooms': 3,
            'apartments': ['B2.21.001', 'B2.22.001', 'B2.23.001', 'B2.24.001', 'B2.25.001', 'B2.26.001']
        },
        'B2-3B': {
            'count': 6,
            'bedrooms': 3,
            'apartments': ['B2.21.002', 'B2.22.002', 'B2.23.002', 'B2.24.002', 'B2.25.002', 'B2.26.002']
        },
        'B2-3C': {
            'count': 6,
            'bedrooms': 3,
            'apartments': ['B2.21.003', 'B2.22.003', 'B2.23.003', 'B2.24.003', 'B2.25.003', 'B2.26.003']
        },
        'B2-3D': {
            'count': 8,
            'bedrooms': 3,
            'apartments': ['B2.21.004', 'B2.22.004', 'B2.23.004', 'B2.24.004', 'B2.25.004', 'B2.26.004', 'B2.27.002', 'B2.28.002']
        },
        'B2-3G': {
            'count': 2,
            'bedrooms': 3,
            'apartments': ['B2.27.001', 'B2.28.001']
        },
        'B2-3K DUP': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B2.27.002']
        },
        'B2-3M DUP': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B2.27.004']
        },
        'B2-3J DUP': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B2.29.001']
        },
        'B2-3H DUP': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B2.29.002']
        },
        'B3-1A': {
            'count': 10,
            'bedrooms': 1,
            'apartments': ['B3.02.001', 'B3.03.001', 'B3.04.001', 'B3.05.001', 'B3.06.001', 'B3.07.001', 'B3.08.001', 'B3.09.001', 'B3.10.001', 'B3.11.001']
        },
        'B3-1B': {
            'count': 8,
            'bedrooms': 1,
            'apartments': ['B3.02.002', 'B3.03.002', 'B3.04.002', 'B3.05.002', 'B3.06.002', 'B3.07.002', 'B3.08.002', 'B3.09.002']
        },
        'B3-1C.1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B3.02.003']
        },
        'B3-1D': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B3.02.004', 'B3.03.004', 'B3.04.004', 'B3.05.004']
        },
        'B3-1E': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B3.02.005']
        },
        'B3-2A': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B3.02.006']
        },
        'B3-2B': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B3.02.007']
        },
        'B3-1C': {
            'count': 9,
            'bedrooms': 1,
            'apartments': ['B3.03.003', 'B3.04.003', 'B3.05.003', 'B3.06.003', 'B3.07.003', 'B3.08.003', 'B3.09.003', 'B3.10.003', 'B3.11.003']
        },
        'B3-1E.1': {
            'count': 3,
            'bedrooms': 1,
            'apartments': ['B3.03.005', 'B3.04.005', 'B3.05.005']
        },
        'B3-2A.1': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B3.03.006', 'B3.04.006', 'B3.05.006']
        },
        'B3-2C': {
            'count': 9,
            'bedrooms': 2,
            'apartments': ['B3.03.007', 'B3.04.007', 'B3.05.007', 'B3.06.006', 'B3.07.006', 'B3.08.006', 'B3.09.006', 'B3.10.006', 'B3.11.006']
        },
        'B3-2B.1': {
            'count': 9,
            'bedrooms': 2,
            'apartments': ['B3.03.008', 'B3.04.008', 'B3.05.008', 'B3.06.007', 'B3.07.007', 'B3.08.007', 'B3.09.007', 'B3.10.007', 'B3.11.007']
        },
        'B3-1F': {
            'count': 3,
            'bedrooms': 1,
            'apartments': ['B3.06.004', 'B3.07.004', 'B3.08.004']
        },
        'B3-2D': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B3.06.005', 'B3.07.005', 'B3.08.005']
        },
        'B3-1G': {
            'count': 3,
            'bedrooms': 1,
            'apartments': ['B3.09.004', 'B3.10.004', 'B3.11.004']
        },
        'B3-3A': {
            'count': 3,
            'bedrooms': 3,
            'apartments': ['B3.09.005', 'B3.10.005', 'B3.11.005']
        },
        'B3-1B.1': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B3.10.002', 'B3.11.002']
        },
        'B3-3B': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B3.12.001']
        },
        'B3-3C': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B3.12.002']
        },
        'B4-1A': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B4.02.001', 'B4.03.001', 'B4.04.001', 'B4.05.001']
        },
        'B4-1B.2': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B4.02.002', 'B4.03.002', 'B4.04.002', 'B4.05.002', 'B4.06.002', 'B4.07.002']
        },
        'B4-1C.1': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B4.02.003', 'B4.03.003', 'B4.04.003', 'B4.05.003', 'B4.06.003', 'B4.07.003']
        },
        'B4-1D': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B4.02.004', 'B4.03.004', 'B4.04.004', 'B4.05.004', 'B4.06.004']
        },
        'B4-2A': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B4.02.005']
        },
        'B4-1E': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B4.02.006']
        },
        'B4-1F': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B4.02.007']
        },
        'B4-2A.2': {
            'count': 4,
            'bedrooms': 2,
            'apartments': ['B4.03.005', 'B4.04.005', 'B4.05.005', 'B4.06.005']
        },
        'B4-2B.1': {
            'count': 4,
            'bedrooms': 2,
            'apartments': ['B4.03.006', 'B4.04.006', 'B4.05.006', 'B4.06.006']
        },
        'B4-2C': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B4.03.007', 'B4.04.007', 'B4.05.007']
        },
        'B4-1F.1': {
            'count': 3,
            'bedrooms': 1,
            'apartments': ['B4.03.008', 'B4.04.008', 'B4.05.008']
        },
        'B4-1G.1': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B4.06.001', 'B4.07.001']
        },
        'B4-2D.1': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B4.06.007', 'B4.07.007']
        },
        'B4-1D.2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B4.07.004']
        },
        'B4-2A.1': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B4.07.005', 'B4.08.005', 'B4.09.005', 'B4.10.005', 'B4.11.005', 'B4.12.005']
        },
        'B4-2B': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B4.07.006', 'B4.08.006', 'B4.09.006', 'B4.10.006', 'B4.11.006', 'B4.12.006']
        },
        'B4-1G': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B4.08.001', 'B4.09.001', 'B4.10.001', 'B4.11.001', 'B4.12.001']
        },
        'B4-1B': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B4.08.002', 'B4.09.002', 'B4.10.002', 'B4.11.002']
        },
        'B4-1C': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B4.08.003', 'B4.09.003', 'B4.10.003', 'B4.11.003', 'B4.12.003']
        },
        'B4-1D.1': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B4.08.004', 'B4.09.004', 'B4.10.004', 'B4.11.004', 'B4.12.004']
        },
        'B4-2D': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B4.08.007', 'B4.09.007', 'B4.10.007', 'B4.11.007', 'B4.12.007']
        },
        'B4-1B.1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B4.12.002']
        },
        'B4-3A': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B4.13.001']
        },
        'B4-3B': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B4.13.002']
        },
        'B4-3A.1': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B4.14.001']
        },
        'B4-3B.1': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B4.14.002']
        },
        'B5-1A.1': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B5.02.001', 'B5.03.001', 'B5.04.001', 'B5.05.001']
        },
        'B5-1B.1': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B5.02.002', 'B5.03.002', 'B5.04.002', 'B5.05.002']
        },
        'B5-2A': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B5.02.003']
        },
        'B5-3A': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B5.02.004']
        },
        'B5-3B': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B5.02.005']
        },
        'B5-1C': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B5.02.006']
        },
        'B5-1D.1': {
            'count': 3,
            'bedrooms': 1,
            'apartments': ['B5.03.003', 'B5.04.003', 'B5.05.003']
        },
        'B5-2B.1': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B5.03.004', 'B5.04.004', 'B5.05.004']
        },
        'B5-2C.1': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B5.03.005', 'B5.04.005', 'B5.05.005']
        },
        'B5-2D.1': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B5.03.006', 'B5.04.006', 'B5.05.006']
        },
        'B5-2E.1': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B5.03.007', 'B5.04.007', 'B5.05.007']
        },
        'B5-2F.1': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B5.03.008', 'B5.04.008', 'B5.05.008']
        },
        'B5-1C.2': {
            'count': 3,
            'bedrooms': 1,
            'apartments': ['B5.03.009', 'B5.04.009', 'B5.05.009']
        },
        'B5-1A': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B5.06.001', 'B5.07.001', 'B5.08.001', 'B5.09.001', 'B5.10.001', 'B5.11.001']
        },
        'B5-1B': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B5.06.002', 'B5.07.002', 'B5.08.002', 'B5.09.002', 'B5.10.002', 'B5.11.002']
        },
        'B5-1D': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B5.06.003', 'B5.07.003', 'B5.08.003', 'B5.09.003', 'B5.10.003', 'B5.11.003']
        },
        'B5-2B': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B5.06.004', 'B5.07.004', 'B5.08.004', 'B5.09.004', 'B5.10.004', 'B5.11.004']
        },
        'B5-2C': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B5.06.005', 'B5.07.005', 'B5.08.005', 'B5.09.005', 'B5.10.005', 'B5.11.005']
        },
        'B5-2D': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B5.06.006', 'B5.07.006', 'B5.08.006', 'B5.09.006', 'B5.10.006', 'B5.11.006']
        },
        'B5-2E': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B5.06.007', 'B5.07.007', 'B5.08.007', 'B5.09.007', 'B5.10.007', 'B5.11.007']
        },
        'B5-2F': {
            'count': 6,
            'bedrooms': 2,
            'apartments': ['B5.06.008', 'B5.07.008', 'B5.08.008', 'B5.09.008', 'B5.10.008', 'B5.11.008']
        },
        'B5-1C.1': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B5.06.009', 'B5.07.009', 'B5.08.009', 'B5.09.009', 'B5.10.009', 'B5.11.009']
        },
        'B5-1E': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B5.12.001', 'B5.13.001']
        },
        'B5-1F': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B5.12.002', 'B5.13.002']
        },
        'B5-2G': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B5.12.003', 'B5.13.003']
        },
        'B5-1G': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B5.12.004', 'B5.13.004']
        },
        'B5-1H': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B5.12.005', 'B5.13.005']
        },
        'B5-2H': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B5.12.006', 'B5.13.006']
        },
        'B5-4D TH': {
            'count': 1,
            'bedrooms': 4,
            'apartments': ['B5.02.007']
        },
        'B5-4C TH': {
            'count': 1,
            'bedrooms': 4,
            'apartments': ['B5.02.008']
        },
        'B5-4A TH': {
            'count': 1,
            'bedrooms': 4,
            'apartments': ['B5.02.009']
        },
        'B5-4B TH': {
            'count': 1,
            'bedrooms': 4,
            'apartments': ['B5.02.010']
        },
        'B7-2A': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B7.00.001', 'B7.01.003']
        },
        'B7-2B': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B7.01.001']
        },
        'B7-3A': {
            'count': 11,
            'bedrooms': 3,
            'apartments': ['B7. 1.001', 'B7.02.001', 'B7.03.001', 'B7.05.001', 'B7.06.001', 'B7.07.001', 'B7.08.001', 'B7.09.001', 'B7.10.001', 'B7.12.001', 'B7.13.001']
        },
        'B7-2D': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B7.02.003']
        },
        'B7-1A': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B7.02.004']
        },
        'B7-1B': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B7.03.002', 'B7.04.002', 'B7.05.002', 'B7.06.002', 'B7.07.002']
        },
        'B7-2E': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B7.03.003', 'B7.04.003']
        },
        'B7-3C': {
            'count': 2,
            'bedrooms': 3,
            'apartments': ['B7.03.004', 'B7.04.004']
        },
        'B7-2F': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B7.04.001']
        },
        'B7-2D.1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B7.05.003']
        },
        'B7-2G': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B7.06.003', 'B7.07.003']
        },
        'B7-2H': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B7. 1.002', 'B7.08.002', 'B7.09.002', 'B7.10.002', 'B7.12.002']
        },
        'B7-2C Dup': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B7.02.002']
        },
        'B7-3B Dup': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B7.02.005']
        },
        'B7-3D TH': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B7.00.T01']
        },
        'B7-3ETH': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B7.00.T02']
        },
        'B7-3F TH': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B7.00.T03']
        },
        'B7-4A TH': {
            'count': 1,
            'bedrooms': 4,
            'apartments': ['B7.00.T04']
        },
    },
    
    'tenures': {
        'Private': {
            'count': 276,
            'apartments': ['B1.03.001', 'B1.03.002', 'B1.03.003', 'B1.03.004', 'B1.04.001', 'B1.04.002', 'B1.04.003', 'B1.04.004', 'B1.05.001', 'B1.05.002', 'B1.05.003', 'B1.05.004', 'B1.06.001', 'B1.06.002', 'B1.06.003', 'B1.06.004', 'B1.07.001', 'B1.07.002', 'B1.07.003', 'B1.07.004', 'B1.08.001', 'B1.08.002', 'B1.08.003', 'B1.08.004', 'B1.09.001', 'B1.09.002', 'B1.10.001', 'B1.10.002', 'B1.11.001', 'B1.11.002', 'B1.12.001', 'B2.02.001', 'B2.02.002', 'B2.03.001', 'B2.03.002', 'B2.03.003', 'B2.03.004', 'B2.04.001', 'B2.04.002', 'B2.04.003', 'B2.04.004', 'B2.04.005', 'B2.04.006', 'B2.05.001', 'B2.05.002', 'B2.05.003', 'B2.05.004', 'B2.05.005', 'B2.05.006', 'B2.06.001', 'B2.06.002', 'B2.06.003', 'B2.06.004', 'B2.06.005', 'B2.06.006', 'B2.07.001', 'B2.07.002', 'B2.07.003', 'B2.07.004', 'B2.07.005', 'B2.07.006', 'B2.08.001', 'B2.08.002', 'B2.08.003', 'B2.08.004', 'B2.08.005', 'B2.08.006', 'B2.09.001', 'B2.09.002', 'B2.09.003', 'B2.09.004', 'B2.09.005', 'B2.09.006', 'B2.10.001', 'B2.10.002', 'B2.10.003', 'B2.10.004', 'B2.10.005', 'B2.11.001', 'B2.11.002', 'B2.11.003', 'B2.11.004', 'B2.11.005', 'B2.12.001', 'B2.12.002', 'B2.12.003', 'B2.12.004', 'B2.12.005', 'B2.13.001', 'B2.13.002', 'B2.13.003', 'B2.13.004', 'B2.13.005', 'B2.14.001', 'B2.14.002', 'B2.14.003', 'B2.14.004', 'B2.14.005', 'B2.15.001', 'B2.15.002', 'B2.15.003', 'B2.15.004', 'B2.15.005', 'B2.16.001', 'B2.16.002', 'B2.16.003', 'B2.16.004', 'B2.16.005', 'B2.17.001', 'B2.17.002', 'B2.17.003', 'B2.17.004', 'B2.17.005', 'B2.18.001', 'B2.18.002', 'B2.18.003', 'B2.18.004', 'B2.18.005', 'B2.19.001', 'B2.19.002', 'B2.19.003', 'B2.19.004', 'B2.19.005', 'B2.20.001', 'B2.20.002', 'B2.20.003', 'B2.20.004', 'B2.20.005', 'B2.21.001', 'B2.21.002', 'B2.21.003', 'B2.21.004', 'B2.22.001', 'B2.22.002', 'B2.22.003', 'B2.22.004', 'B2.23.001', 'B2.23.002', 'B2.23.003', 'B2.23.004', 'B2.24.001', 'B2.24.002', 'B2.24.003', 'B2.24.004', 'B2.25.001', 'B2.25.002', 'B2.25.003', 'B2.25.004', 'B2.26.001', 'B2.26.002', 'B2.26.003', 'B2.26.004', 'B2.27.001', 'B2.27.002', 'B2.27.002', 'B2.27.004', 'B2.28.001', 'B2.28.002', 'B2.29.001', 'B2.29.002', 'B3.02.001', 'B3.02.002', 'B3.02.003', 'B3.02.004', 'B3.02.005', 'B3.02.006', 'B3.02.007', 'B3.03.001', 'B3.03.002', 'B3.03.003', 'B3.03.004', 'B3.03.005', 'B3.03.006', 'B3.03.007', 'B3.03.008', 'B3.04.001', 'B3.04.002', 'B3.04.003', 'B3.04.004', 'B3.04.005', 'B3.04.006', 'B3.04.007', 'B3.04.008', 'B3.05.001', 'B3.05.002', 'B3.05.003', 'B3.05.004', 'B3.05.005', 'B3.05.006', 'B3.05.007', 'B3.05.008', 'B3.06.001', 'B3.06.002', 'B3.06.003', 'B3.06.004', 'B3.06.005', 'B3.06.006', 'B3.06.007', 'B3.07.001', 'B3.07.002', 'B3.07.003', 'B3.07.004', 'B3.07.005', 'B3.07.006', 'B3.07.007', 'B3.08.001', 'B3.08.002', 'B3.08.003', 'B3.08.004', 'B3.08.005', 'B3.08.006', 'B3.08.007', 'B3.09.001', 'B3.09.002', 'B3.09.003', 'B3.09.004', 'B3.09.005', 'B3.09.006', 'B3.09.007', 'B3.10.001', 'B3.10.002', 'B3.10.003', 'B3.10.004', 'B3.10.005', 'B3.10.006', 'B3.10.007', 'B3.11.001', 'B3.11.002', 'B3.11.003', 'B3.11.004', 'B3.11.005', 'B3.11.006', 'B3.11.007', 'B3.12.001', 'B3.12.002', 'B4.07.005', 'B4.07.006', 'B4.08.001', 'B4.08.002', 'B4.08.003', 'B4.08.004', 'B4.08.005', 'B4.08.006', 'B4.08.007', 'B4.09.001', 'B4.09.002', 'B4.09.003', 'B4.09.004', 'B4.09.005', 'B4.09.006', 'B4.09.007', 'B4.10.001', 'B4.10.002', 'B4.10.003', 'B4.10.004', 'B4.10.005', 'B4.10.006', 'B4.10.007', 'B4.11.001', 'B4.11.002', 'B4.11.003', 'B4.11.004', 'B4.11.005', 'B4.11.006', 'B4.11.007', 'B4.12.001', 'B4.12.002', 'B4.12.003', 'B4.12.004', 'B4.12.005', 'B4.12.006', 'B4.12.007', 'B4.13.001', 'B4.13.002', 'B4.14.001', 'B4.14.002']
        },
        'Discount London Living Rent': {
            'count': 113,
            'apartments': ['B4.02.001', 'B4.02.002', 'B4.02.003', 'B4.02.004', 'B4.02.005', 'B4.02.006', 'B4.02.007', 'B4.03.001', 'B4.03.002', 'B4.03.003', 'B4.03.004', 'B4.03.005', 'B4.03.006', 'B4.03.007', 'B4.03.008', 'B4.04.001', 'B4.04.002', 'B4.04.003', 'B4.04.004', 'B4.04.005', 'B4.04.006', 'B4.04.007', 'B4.04.008', 'B4.05.001', 'B4.05.002', 'B4.05.003', 'B4.05.004', 'B4.05.005', 'B4.05.006', 'B4.05.007', 'B4.05.008', 'B4.06.001', 'B4.06.002', 'B4.06.003', 'B4.06.004', 'B4.06.005', 'B4.06.006', 'B4.06.007', 'B4.07.001', 'B4.07.002', 'B4.07.003', 'B4.07.004', 'B4.07.007', 'B5.02.007', 'B5.02.008', 'B5.02.009', 'B5.02.010', 'B5.06.001', 'B5.06.002', 'B5.06.003', 'B5.06.004', 'B5.06.005', 'B5.06.006', 'B5.06.007', 'B5.06.008', 'B5.06.009', 'B5.07.001', 'B5.07.002', 'B5.07.003', 'B5.07.004', 'B5.07.005', 'B5.07.006', 'B5.07.007', 'B5.07.008', 'B5.07.009', 'B5.08.001', 'B5.08.002', 'B5.08.003', 'B5.08.004', 'B5.08.005', 'B5.08.006', 'B5.08.007', 'B5.08.008', 'B5.08.009', 'B5.09.001', 'B5.09.002', 'B5.09.003', 'B5.09.004', 'B5.09.005', 'B5.09.006', 'B5.09.007', 'B5.09.008', 'B5.09.009', 'B5.10.001', 'B5.10.002', 'B5.10.003', 'B5.10.004', 'B5.10.005', 'B5.10.006', 'B5.10.007', 'B5.10.008', 'B5.10.009', 'B5.11.001', 'B5.11.002', 'B5.11.003', 'B5.11.004', 'B5.11.005', 'B5.11.006', 'B5.11.007', 'B5.11.008', 'B5.11.009', 'B5.12.001', 'B5.12.002', 'B5.12.003', 'B5.12.004', 'B5.12.005', 'B5.12.006', 'B5.13.001', 'B5.13.002', 'B5.13.003', 'B5.13.004', 'B5.13.005', 'B5.13.006']
        },
        'London Affordable Rent': {
            'count': 73,
            'apartments': ['B5.02.001', 'B5.02.002', 'B5.02.003', 'B5.02.004', 'B5.02.005', 'B5.02.006', 'B5.03.001', 'B5.03.002', 'B5.03.003', 'B5.03.004', 'B5.03.005', 'B5.03.006', 'B5.03.007', 'B5.03.008', 'B5.03.009', 'B5.04.001', 'B5.04.002', 'B5.04.003', 'B5.04.004', 'B5.04.005', 'B5.04.006', 'B5.04.007', 'B5.04.008', 'B5.04.009', 'B5.05.001', 'B5.05.002', 'B5.05.003', 'B5.05.004', 'B5.05.005', 'B5.05.006', 'B5.05.007', 'B5.05.008', 'B5.05.009', 'B7. 1.001', 'B7. 1.002', 'B7.00.001', 'B7.00.T01', 'B7.00.T02', 'B7.00.T03', 'B7.00.T04', 'B7.01.001', 'B7.01.003', 'B7.02.001', 'B7.02.002', 'B7.02.003', 'B7.02.004', 'B7.02.005', 'B7.03.001', 'B7.03.002', 'B7.03.003', 'B7.03.004', 'B7.04.001', 'B7.04.002', 'B7.04.003', 'B7.04.004', 'B7.05.001', 'B7.05.002', 'B7.05.003', 'B7.06.001', 'B7.06.002', 'B7.06.003', 'B7.07.001', 'B7.07.002', 'B7.07.003', 'B7.08.001', 'B7.08.002', 'B7.09.001', 'B7.09.002', 'B7.10.001', 'B7.10.002', 'B7.12.001', 'B7.12.002', 'B7.13.001']
        },
    },
    
    'apartment_lookup': {
        # Full apartment lookup dictionary with 461 apartments
        'B1.03.001': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.03.002': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'B1-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B1.03.003': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'B1-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.03.004': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.04.001': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.04.002': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'B1-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B1.04.003': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'B1-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.04.004': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.05.001': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.05.002': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'B1-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B1.05.003': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'B1-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.05.004': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.06.001': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.06.002': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'B1-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B1.06.003': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'B1-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.06.004': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.07.001': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.07.002': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'B1-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B1.07.003': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'B1-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.07.004': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.08.001': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.08.002': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'B1-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B1.08.003': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'B1-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.08.004': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.09.001': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.09.002': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.10.001': {'phase': None, 'block': 'B1', 'floor': 10, 'type': 'B1-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.10.002': {'phase': None, 'block': 'B1', 'floor': 10, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.11.001': {'phase': None, 'block': 'B1', 'floor': 11, 'type': 'B1-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.11.002': {'phase': None, 'block': 'B1', 'floor': 11, 'type': 'B1-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B1.12.001': {'phase': None, 'block': 'B1', 'floor': 12, 'type': 'B1-3A', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.02.001': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'B2-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.02.002': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'B2-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.03.001': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'B2-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.03.002': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'B2-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.03.003': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'B2-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.03.004': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'B2-3A', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.04.001': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.04.002': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'B2-2E', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.04.003': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'B2-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.04.004': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'B2-2F', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.04.005': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.04.006': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.05.001': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.05.002': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'B2-2E', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.05.003': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'B2-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.05.004': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'B2-2F', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.05.005': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.05.006': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.06.001': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.06.002': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'B2-2E', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.06.003': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'B2-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.06.004': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'B2-2F', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.06.005': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.06.006': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.07.001': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.07.002': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'B2-2E', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.07.003': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'B2-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.07.004': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'B2-2F', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.07.005': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.07.006': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.08.001': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.08.002': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'B2-2E', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.08.003': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'B2-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.08.004': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'B2-2F', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.08.005': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.08.006': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.09.001': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.09.002': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'B2-2E', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.09.003': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'B2-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.09.004': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'B2-2F', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.09.005': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.09.006': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.10.001': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.10.002': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.10.003': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.10.004': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.10.005': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.11.001': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.11.002': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.11.003': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.11.004': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.11.005': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.12.001': {'phase': None, 'block': 'B2', 'floor': 12, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.12.002': {'phase': None, 'block': 'B2', 'floor': 12, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.12.003': {'phase': None, 'block': 'B2', 'floor': 12, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.12.004': {'phase': None, 'block': 'B2', 'floor': 12, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.12.005': {'phase': None, 'block': 'B2', 'floor': 12, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.13.001': {'phase': None, 'block': 'B2', 'floor': 13, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.13.002': {'phase': None, 'block': 'B2', 'floor': 13, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.13.003': {'phase': None, 'block': 'B2', 'floor': 13, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.13.004': {'phase': None, 'block': 'B2', 'floor': 13, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.13.005': {'phase': None, 'block': 'B2', 'floor': 13, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.14.001': {'phase': None, 'block': 'B2', 'floor': 14, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.14.002': {'phase': None, 'block': 'B2', 'floor': 14, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.14.003': {'phase': None, 'block': 'B2', 'floor': 14, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.14.004': {'phase': None, 'block': 'B2', 'floor': 14, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.14.005': {'phase': None, 'block': 'B2', 'floor': 14, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.15.001': {'phase': None, 'block': 'B2', 'floor': 15, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.15.002': {'phase': None, 'block': 'B2', 'floor': 15, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.15.003': {'phase': None, 'block': 'B2', 'floor': 15, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.15.004': {'phase': None, 'block': 'B2', 'floor': 15, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.15.005': {'phase': None, 'block': 'B2', 'floor': 15, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.16.001': {'phase': None, 'block': 'B2', 'floor': 16, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.16.002': {'phase': None, 'block': 'B2', 'floor': 16, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.16.003': {'phase': None, 'block': 'B2', 'floor': 16, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.16.004': {'phase': None, 'block': 'B2', 'floor': 16, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.16.005': {'phase': None, 'block': 'B2', 'floor': 16, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.17.001': {'phase': None, 'block': 'B2', 'floor': 17, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.17.002': {'phase': None, 'block': 'B2', 'floor': 17, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.17.003': {'phase': None, 'block': 'B2', 'floor': 17, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.17.004': {'phase': None, 'block': 'B2', 'floor': 17, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.17.005': {'phase': None, 'block': 'B2', 'floor': 17, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.18.001': {'phase': None, 'block': 'B2', 'floor': 18, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.18.002': {'phase': None, 'block': 'B2', 'floor': 18, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.18.003': {'phase': None, 'block': 'B2', 'floor': 18, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.18.004': {'phase': None, 'block': 'B2', 'floor': 18, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.18.005': {'phase': None, 'block': 'B2', 'floor': 18, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.19.001': {'phase': None, 'block': 'B2', 'floor': 19, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.19.002': {'phase': None, 'block': 'B2', 'floor': 19, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.19.003': {'phase': None, 'block': 'B2', 'floor': 19, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.19.004': {'phase': None, 'block': 'B2', 'floor': 19, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.19.005': {'phase': None, 'block': 'B2', 'floor': 19, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.20.001': {'phase': None, 'block': 'B2', 'floor': 20, 'type': 'B2-2H', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.20.002': {'phase': None, 'block': 'B2', 'floor': 20, 'type': 'B2-2J', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.20.003': {'phase': None, 'block': 'B2', 'floor': 20, 'type': 'B2-2K', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.20.004': {'phase': None, 'block': 'B2', 'floor': 20, 'type': 'B2-2G', 'bedrooms': 2, 'tenure': 'Private'},
        'B2.20.005': {'phase': None, 'block': 'B2', 'floor': 20, 'type': 'B2-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B2.21.001': {'phase': None, 'block': 'B2', 'floor': 21, 'type': 'B2-3E', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.21.002': {'phase': None, 'block': 'B2', 'floor': 21, 'type': 'B2-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.21.003': {'phase': None, 'block': 'B2', 'floor': 21, 'type': 'B2-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.21.004': {'phase': None, 'block': 'B2', 'floor': 21, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.22.001': {'phase': None, 'block': 'B2', 'floor': 22, 'type': 'B2-3E', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.22.002': {'phase': None, 'block': 'B2', 'floor': 22, 'type': 'B2-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.22.003': {'phase': None, 'block': 'B2', 'floor': 22, 'type': 'B2-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.22.004': {'phase': None, 'block': 'B2', 'floor': 22, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.23.001': {'phase': None, 'block': 'B2', 'floor': 23, 'type': 'B2-3E', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.23.002': {'phase': None, 'block': 'B2', 'floor': 23, 'type': 'B2-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.23.003': {'phase': None, 'block': 'B2', 'floor': 23, 'type': 'B2-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.23.004': {'phase': None, 'block': 'B2', 'floor': 23, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.24.001': {'phase': None, 'block': 'B2', 'floor': 24, 'type': 'B2-3E', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.24.002': {'phase': None, 'block': 'B2', 'floor': 24, 'type': 'B2-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.24.003': {'phase': None, 'block': 'B2', 'floor': 24, 'type': 'B2-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.24.004': {'phase': None, 'block': 'B2', 'floor': 24, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.25.001': {'phase': None, 'block': 'B2', 'floor': 25, 'type': 'B2-3E', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.25.002': {'phase': None, 'block': 'B2', 'floor': 25, 'type': 'B2-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.25.003': {'phase': None, 'block': 'B2', 'floor': 25, 'type': 'B2-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.25.004': {'phase': None, 'block': 'B2', 'floor': 25, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.26.001': {'phase': None, 'block': 'B2', 'floor': 26, 'type': 'B2-3E', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.26.002': {'phase': None, 'block': 'B2', 'floor': 26, 'type': 'B2-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.26.003': {'phase': None, 'block': 'B2', 'floor': 26, 'type': 'B2-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.26.004': {'phase': None, 'block': 'B2', 'floor': 26, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.27.001': {'phase': None, 'block': 'B2', 'floor': 27, 'type': 'B2-3G', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.27.002': {'phase': None, 'block': 'B2', 'floor': 27, 'type': 'B2-3K DUP', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.28.001': {'phase': None, 'block': 'B2', 'floor': 28, 'type': 'B2-3G', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.28.002': {'phase': None, 'block': 'B2', 'floor': 28, 'type': 'B2-3D', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.27.004': {'phase': None, 'block': 'B2', 'floor': 27, 'type': 'B2-3M DUP', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.29.001': {'phase': None, 'block': 'B2', 'floor': 29, 'type': 'B2-3J DUP', 'bedrooms': 3, 'tenure': 'Private'},
        'B2.29.002': {'phase': None, 'block': 'B2', 'floor': 29, 'type': 'B2-3H DUP', 'bedrooms': 3, 'tenure': 'Private'},
        'B3.02.001': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.02.002': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.02.003': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-1C.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.02.004': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-1D', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.02.005': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-1E', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.02.006': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-2A', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.02.007': {'phase': None, 'block': 'B3', 'floor': 2, 'type': 'B3-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.03.001': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.03.002': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.03.003': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.03.004': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-1D', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.03.005': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-1E.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.03.006': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.03.007': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.03.008': {'phase': None, 'block': 'B3', 'floor': 3, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.04.001': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.04.002': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.04.003': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.04.004': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-1D', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.04.005': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-1E.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.04.006': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.04.007': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.04.008': {'phase': None, 'block': 'B3', 'floor': 4, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.05.001': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.05.002': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.05.003': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.05.004': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-1D', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.05.005': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-1E.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.05.006': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.05.007': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.05.008': {'phase': None, 'block': 'B3', 'floor': 5, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.06.001': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.06.002': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.06.003': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.06.004': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-1F', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.06.005': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.06.006': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.06.007': {'phase': None, 'block': 'B3', 'floor': 6, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.07.001': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.07.002': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.07.003': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.07.004': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-1F', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.07.005': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.07.006': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.07.007': {'phase': None, 'block': 'B3', 'floor': 7, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.08.001': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.08.002': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.08.003': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.08.004': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-1F', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.08.005': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.08.006': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.08.007': {'phase': None, 'block': 'B3', 'floor': 8, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.09.001': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.09.002': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.09.003': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.09.004': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.09.005': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-3A', 'bedrooms': 3, 'tenure': 'Private'},
        'B3.09.006': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.09.007': {'phase': None, 'block': 'B3', 'floor': 9, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.10.001': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.10.002': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-1B.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.10.003': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.10.004': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.10.005': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-3A', 'bedrooms': 3, 'tenure': 'Private'},
        'B3.10.006': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.10.007': {'phase': None, 'block': 'B3', 'floor': 10, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.11.001': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-1A', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.11.002': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-1B.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.11.003': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.11.004': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B3.11.005': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-3A', 'bedrooms': 3, 'tenure': 'Private'},
        'B3.11.006': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-2C', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.11.007': {'phase': None, 'block': 'B3', 'floor': 11, 'type': 'B3-2B.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B3.12.001': {'phase': None, 'block': 'B3', 'floor': 12, 'type': 'B3-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B3.12.002': {'phase': None, 'block': 'B3', 'floor': 12, 'type': 'B3-3C', 'bedrooms': 3, 'tenure': 'Private'},
        'B4.02.001': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.02.002': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-1B.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.02.003': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.02.004': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.02.005': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-2A', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.02.006': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-1E', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.02.007': {'phase': None, 'block': 'B4', 'floor': 2, 'type': 'B4-1F', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.03.001': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.03.002': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-1B.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.03.003': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.03.004': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.03.005': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-2A.2', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.03.006': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-2B.1', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.03.007': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.03.008': {'phase': None, 'block': 'B4', 'floor': 3, 'type': 'B4-1F.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.04.001': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.04.002': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-1B.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.04.003': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.04.004': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.04.005': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-2A.2', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.04.006': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-2B.1', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.04.007': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.04.008': {'phase': None, 'block': 'B4', 'floor': 4, 'type': 'B4-1F.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.05.001': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.05.002': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-1B.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.05.003': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.05.004': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.05.005': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-2A.2', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.05.006': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-2B.1', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.05.007': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.05.008': {'phase': None, 'block': 'B4', 'floor': 5, 'type': 'B4-1F.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.06.001': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-1G.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.06.002': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-1B.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.06.003': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.06.004': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.06.005': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-2A.2', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.06.006': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-2B.1', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.06.007': {'phase': None, 'block': 'B4', 'floor': 6, 'type': 'B4-2D.1', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.07.001': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-1G.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.07.002': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-1B.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.07.003': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.07.004': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-1D.2', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B4.07.005': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.07.006': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.07.007': {'phase': None, 'block': 'B4', 'floor': 7, 'type': 'B4-2D.1', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B4.08.001': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.08.002': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.08.003': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.08.004': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-1D.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.08.005': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.08.006': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.08.007': {'phase': None, 'block': 'B4', 'floor': 8, 'type': 'B4-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.09.001': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.09.002': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.09.003': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.09.004': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-1D.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.09.005': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.09.006': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.09.007': {'phase': None, 'block': 'B4', 'floor': 9, 'type': 'B4-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.10.001': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.10.002': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.10.003': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.10.004': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-1D.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.10.005': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.10.006': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.10.007': {'phase': None, 'block': 'B4', 'floor': 10, 'type': 'B4-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.11.001': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.11.002': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-1B', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.11.003': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.11.004': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-1D.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.11.005': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.11.006': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.11.007': {'phase': None, 'block': 'B4', 'floor': 11, 'type': 'B4-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.12.001': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-1G', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.12.002': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-1B.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.12.003': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-1C', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.12.004': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-1D.1', 'bedrooms': 1, 'tenure': 'Private'},
        'B4.12.005': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-2A.1', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.12.006': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-2B', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.12.007': {'phase': None, 'block': 'B4', 'floor': 12, 'type': 'B4-2D', 'bedrooms': 2, 'tenure': 'Private'},
        'B4.13.001': {'phase': None, 'block': 'B4', 'floor': 13, 'type': 'B4-3A', 'bedrooms': 3, 'tenure': 'Private'},
        'B4.13.002': {'phase': None, 'block': 'B4', 'floor': 13, 'type': 'B4-3B', 'bedrooms': 3, 'tenure': 'Private'},
        'B4.14.001': {'phase': None, 'block': 'B4', 'floor': 14, 'type': 'B4-3A.1', 'bedrooms': 3, 'tenure': 'Private'},
        'B4.14.002': {'phase': None, 'block': 'B4', 'floor': 14, 'type': 'B4-3B.1', 'bedrooms': 3, 'tenure': 'Private'},
        'B5.02.001': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-1A.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.02.002': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-1B.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.02.003': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-2A', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.02.004': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B5.02.005': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-3B', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B5.02.006': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-1C', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.03.001': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-1A.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.03.002': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-1B.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.03.003': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-1D.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.03.004': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-2B.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.03.005': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-2C.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.03.006': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-2D.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.03.007': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-2E.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.03.008': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-2F.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.03.009': {'phase': None, 'block': 'B5', 'floor': 3, 'type': 'B5-1C.2', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.04.001': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-1A.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.04.002': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-1B.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.04.003': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-1D.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.04.004': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-2B.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.04.005': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-2C.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.04.006': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-2D.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.04.007': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-2E.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.04.008': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-2F.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.04.009': {'phase': None, 'block': 'B5', 'floor': 4, 'type': 'B5-1C.2', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.05.001': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-1A.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.05.002': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-1B.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.05.003': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-1D.1', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.05.004': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-2B.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.05.005': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-2C.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.05.006': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-2D.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.05.007': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-2E.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.05.008': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-2F.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B5.05.009': {'phase': None, 'block': 'B5', 'floor': 5, 'type': 'B5-1C.2', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B5.06.001': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.06.002': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-1B', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.06.003': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.06.004': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-2B', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.06.005': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.06.006': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-2D', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.06.007': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-2E', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.06.008': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-2F', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.06.009': {'phase': None, 'block': 'B5', 'floor': 6, 'type': 'B5-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.07.001': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.07.002': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-1B', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.07.003': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.07.004': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-2B', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.07.005': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.07.006': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-2D', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.07.007': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-2E', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.07.008': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-2F', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.07.009': {'phase': None, 'block': 'B5', 'floor': 7, 'type': 'B5-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.08.001': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.08.002': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-1B', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.08.003': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.08.004': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-2B', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.08.005': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.08.006': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-2D', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.08.007': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-2E', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.08.008': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-2F', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.08.009': {'phase': None, 'block': 'B5', 'floor': 8, 'type': 'B5-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.09.001': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.09.002': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-1B', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.09.003': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.09.004': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-2B', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.09.005': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.09.006': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-2D', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.09.007': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-2E', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.09.008': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-2F', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.09.009': {'phase': None, 'block': 'B5', 'floor': 9, 'type': 'B5-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.10.001': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.10.002': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-1B', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.10.003': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.10.004': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-2B', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.10.005': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.10.006': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-2D', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.10.007': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-2E', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.10.008': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-2F', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.10.009': {'phase': None, 'block': 'B5', 'floor': 10, 'type': 'B5-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.11.001': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-1A', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.11.002': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-1B', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.11.003': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-1D', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.11.004': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-2B', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.11.005': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-2C', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.11.006': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-2D', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.11.007': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-2E', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.11.008': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-2F', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.11.009': {'phase': None, 'block': 'B5', 'floor': 11, 'type': 'B5-1C.1', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.12.001': {'phase': None, 'block': 'B5', 'floor': 12, 'type': 'B5-1E', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.12.002': {'phase': None, 'block': 'B5', 'floor': 12, 'type': 'B5-1F', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.12.003': {'phase': None, 'block': 'B5', 'floor': 12, 'type': 'B5-2G', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.12.004': {'phase': None, 'block': 'B5', 'floor': 12, 'type': 'B5-1G', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.12.005': {'phase': None, 'block': 'B5', 'floor': 12, 'type': 'B5-1H', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.12.006': {'phase': None, 'block': 'B5', 'floor': 12, 'type': 'B5-2H', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.13.001': {'phase': None, 'block': 'B5', 'floor': 13, 'type': 'B5-1E', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.13.002': {'phase': None, 'block': 'B5', 'floor': 13, 'type': 'B5-1F', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.13.003': {'phase': None, 'block': 'B5', 'floor': 13, 'type': 'B5-2G', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.13.004': {'phase': None, 'block': 'B5', 'floor': 13, 'type': 'B5-1G', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.13.005': {'phase': None, 'block': 'B5', 'floor': 13, 'type': 'B5-1H', 'bedrooms': 1, 'tenure': 'Discount London Living Rent'},
        'B5.13.006': {'phase': None, 'block': 'B5', 'floor': 13, 'type': 'B5-2H', 'bedrooms': 2, 'tenure': 'Discount London Living Rent'},
        'B5.02.007': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-4D TH', 'bedrooms': 4, 'tenure': 'Discount London Living Rent'},
        'B5.02.008': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-4C TH', 'bedrooms': 4, 'tenure': 'Discount London Living Rent'},
        'B5.02.009': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-4A TH', 'bedrooms': 4, 'tenure': 'Discount London Living Rent'},
        'B5.02.010': {'phase': None, 'block': 'B5', 'floor': 2, 'type': 'B5-4B TH', 'bedrooms': 4, 'tenure': 'Discount London Living Rent'},
        'B7.00.001': {'phase': None, 'block': 'B7', 'floor': 0, 'type': 'B7-2A', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.01.001': {'phase': None, 'block': 'B7', 'floor': 1, 'type': 'B7-2B', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.01.003': {'phase': None, 'block': 'B7', 'floor': 1, 'type': 'B7-2A', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.02.001': {'phase': None, 'block': 'B7', 'floor': 2, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.02.003': {'phase': None, 'block': 'B7', 'floor': 2, 'type': 'B7-2D', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.02.004': {'phase': None, 'block': 'B7', 'floor': 2, 'type': 'B7-1A', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B7.03.001': {'phase': None, 'block': 'B7', 'floor': 3, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.03.002': {'phase': None, 'block': 'B7', 'floor': 3, 'type': 'B7-1B', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B7.03.003': {'phase': None, 'block': 'B7', 'floor': 3, 'type': 'B7-2E', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.03.004': {'phase': None, 'block': 'B7', 'floor': 3, 'type': 'B7-3C', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.04.001': {'phase': None, 'block': 'B7', 'floor': 4, 'type': 'B7-2F', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.04.002': {'phase': None, 'block': 'B7', 'floor': 4, 'type': 'B7-1B', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B7.04.003': {'phase': None, 'block': 'B7', 'floor': 4, 'type': 'B7-2E', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.04.004': {'phase': None, 'block': 'B7', 'floor': 4, 'type': 'B7-3C', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.05.001': {'phase': None, 'block': 'B7', 'floor': 5, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.05.002': {'phase': None, 'block': 'B7', 'floor': 5, 'type': 'B7-1B', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B7.05.003': {'phase': None, 'block': 'B7', 'floor': 5, 'type': 'B7-2D.1', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.06.001': {'phase': None, 'block': 'B7', 'floor': 6, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.06.002': {'phase': None, 'block': 'B7', 'floor': 6, 'type': 'B7-1B', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B7.06.003': {'phase': None, 'block': 'B7', 'floor': 6, 'type': 'B7-2G', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.07.001': {'phase': None, 'block': 'B7', 'floor': 7, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.07.002': {'phase': None, 'block': 'B7', 'floor': 7, 'type': 'B7-1B', 'bedrooms': 1, 'tenure': 'London Affordable Rent'},
        'B7.07.003': {'phase': None, 'block': 'B7', 'floor': 7, 'type': 'B7-2G', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.08.001': {'phase': None, 'block': 'B7', 'floor': 8, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.08.002': {'phase': None, 'block': 'B7', 'floor': 8, 'type': 'B7-2H', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.09.001': {'phase': None, 'block': 'B7', 'floor': 9, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.09.002': {'phase': None, 'block': 'B7', 'floor': 9, 'type': 'B7-2H', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.10.001': {'phase': None, 'block': 'B7', 'floor': 10, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.10.002': {'phase': None, 'block': 'B7', 'floor': 10, 'type': 'B7-2H', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7. 1.001': {'phase': None, 'block': 'B7', 'floor': 11, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7. 1.002': {'phase': None, 'block': 'B7', 'floor': 11, 'type': 'B7-2H', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.12.001': {'phase': None, 'block': 'B7', 'floor': 12, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.12.002': {'phase': None, 'block': 'B7', 'floor': 12, 'type': 'B7-2H', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.13.001': {'phase': None, 'block': 'B7', 'floor': 13, 'type': 'B7-3A', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.02.002': {'phase': None, 'block': 'B7', 'floor': 2, 'type': 'B7-2C Dup', 'bedrooms': 2, 'tenure': 'London Affordable Rent'},
        'B7.02.005': {'phase': None, 'block': 'B7', 'floor': 2, 'type': 'B7-3B Dup', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.00.T01': {'phase': None, 'block': 'B7', 'floor': 0, 'type': 'B7-3D TH', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.00.T02': {'phase': None, 'block': 'B7', 'floor': 0, 'type': 'B7-3ETH', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.00.T03': {'phase': None, 'block': 'B7', 'floor': 0, 'type': 'B7-3F TH', 'bedrooms': 3, 'tenure': 'London Affordable Rent'},
        'B7.00.T04': {'phase': None, 'block': 'B7', 'floor': 0, 'type': 'B7-4A TH', 'bedrooms': 4, 'tenure': 'London Affordable Rent'},
    }
}

