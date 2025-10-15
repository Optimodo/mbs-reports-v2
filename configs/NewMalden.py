"""Configuration for New Malden project."""

PROJECT_TITLE = "New Malden"

# Excel processing settings
EXCEL_SETTINGS = {
    "sheet_name": 0,  # First sheet by default
    "skiprows": 6,    # Skip the first 6 rows
    "usecols": [
        "Doc Title",
        "Doc Ref",
        "Rev",
        "Status",
        "Purpose of Issue",
        "Date (WET)",
        "Last Status Change (WET)",
        "Form",
        "Number (5 digits)",
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
    "output_format": "excel",  # Options: excel, pdf, html
    "include_charts": True
} 

# File type settings
FILE_TYPE_SETTINGS = {
    "column_name": "Form",  # Column name for file type
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "Form Type Summary"  # Title for the summary section
} 

# Certificate Settings
CERTIFICATE_SETTINGS = {
    'enabled': True,
    'certificate_types': ['Certificate'],
    'summary_label': 'P01-PXX (Certificates)',
    'status_suffix': ' (Certificates)'
}

# Status Mappings - Maps actual status values to standardized categories
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A',
        'color': '25E82C',  # Green
        'statuses': [
            'A - Proceed',
            'A - Proceed (Lead Reviewer)'
        ],
        'description': 'Approved to proceed'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'B - Proceed with Comments',
            'B - Proceed with Comments (Lead Reviewer)'
        ],
        'description': 'Proceed with comments'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'C - Rejected',
            'C - Rejected (Lead Reviewer)',
            'QC Rejected'
        ],
        'description': 'Rejected documents'
    },
    'Under Review': {
        'display_name': 'Under Review',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Under Review',
            'QC Checked'
        ],
        'description': 'Under review or QC check'
    },
    'Other': {
        'display_name': 'Other',
        'color': 'D3D3D3',  # Light gray
        'statuses': [
            '---'
        ],
        'description': 'Other or unspecified status'
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