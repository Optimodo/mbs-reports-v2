"""Configuration for Oval Block B project."""

PROJECT_TITLE = "Oval Village Block B"

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
        "OVL - File Type",
        "OVL - Number",
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
        "Last Status Change (WET)",
        "Last Updated (WET)",
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
    "column_name": "OVL - File Type",  # Column name for file type
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "File Type Summary"  # Title for the summary section
}

# Certificate Settings
CERTIFICATE_SETTINGS = {
    'enabled': True,
    'certificate_types': ['CT - Certificate (CT)'],
    'summary_label': 'P01-PXX (Certificates)',
    'status_suffix': ' (Certificates)'
}

# Status Mappings - Maps actual status values to standardized categories
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A',
        'color': '25E82C',  # Green
        'statuses': [
            'Accepted',
            'Published'
        ],
        'description': 'Approved/Accepted documents'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'Accepted with Comments'
        ],
        'description': 'Approved with comments'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'Rejected',
            'QA - Rejected'
        ],
        'description': 'Rejected documents'
    },
    'Shared': {
        'display_name': 'Shared',
        'color': 'E0F090',  # Light yellow-green
        'statuses': [
            'Shared',
            'For Sharing'
        ],
        'description': 'Shared for review'
    },
    'Withdrawn': {
        'display_name': 'Withdrawn/Obsolete',
        'color': 'D3D3D3',  # Light gray
        'statuses': [
            'Withdrawn-Obsolete'
        ],
        'description': 'Withdrawn or obsolete documents'
    }
}

# Display order for progression reports
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'Shared',
    'Withdrawn'
]