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

# Column mappings for CSV to standard format
COLUMN_MAPPINGS = {
    'Doc Ref': 'Name',                        # Document reference is in Name column
    'Doc Title': 'Description',               # Document title is in Description column  
    'Rev': 'Revision',                        # Revision is in Revision column
    'Status': 'Status',                       # Status is in Status column
    'Date (WET)': 'Revision Date Modified',   # Date is in Revision Date Modified column
    'Doc Path': 'Name'                        # Use Name as Doc Path (same as Doc Ref)
}

# Excel processing settings (for backward compatibility)
EXCEL_SETTINGS = {
    "sheet_name": 0,
    "skiprows": 6,
    "usecols": [
        "Doc Title",
        "Doc Ref",
        "Rev",
        "Status",
        "Purpose of Issue",
        "Date (WET)",
        "Last Status Change (WET)",
        "File Type",
        "File Number",
        "Last Updated (WET)",
        "Doc Path"
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
    'certificate_types': [],
    'summary_label': 'P01-PXX (Certificates)',
    'status_suffix': ' (Certificates)'
}

