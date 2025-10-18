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

# Column mappings - Map raw Excel columns to standardized names
COLUMN_MAPPINGS = {
    'File Type': 'OVL - File Type',  # Standard name: Raw column name
    'Doc Ref': 'Doc Ref',
    'Doc Title': 'Doc Title',
    'Rev': 'Rev',
    'Status': 'Status',
    'Date (WET)': 'Date (WET)',
    'Doc Path': 'Doc Path'
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
    "column_name": "File Type",  # Standardized column name in database
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "File Type Summary"  # Title for the summary section
}

# Drawing Settings (for main summary report focus)
DRAWING_SETTINGS = {
    'enabled': True,
    # File type filtering (Method 1) - EXACT matches only
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Standardized column name in database
        'drawing_types': ['DR - Drawings (DR)']
    },
    # Doc Ref pattern filtering (Method 2) - 2-letter codes
    'doc_ref_filter': {
        'enabled': False,  # Enable if you want to filter by Doc Ref patterns
        'column_name': 'Doc Ref',
        'drawing_patterns': ['DR']  # 2-letter codes to match in Doc Ref
    }
}

# Certificate Settings
CERTIFICATE_SETTINGS = {
    'enabled': True,
    # Report generation settings
    'generate_report': True,  # Set to False to disable certificate report generation
    'summary_label': 'P01-PXX (Certificates)',
    'status_suffix': ' (Certificates)',
    # File type filtering (Method 1)
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Standardized column name in database
        'certificate_types': ['CT - Certificate (CT)']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': True,
        'column_name': 'Doc Ref',
        'certificate_patterns': ['CT']  # 2-letter codes to match in Doc Ref
    }
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': True,
    # Report generation settings
    'generate_report': False,  # Set to True when ready to create technical submittal reports
    # File type filtering (Method 1)
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Standardized column name in database
        'technical_submittal_types': ['TX - Technical Submittals (TX)', 'Technical Submittal']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': True,
        'column_name': 'Doc Ref',
        'technical_submittal_patterns': ['TX', 'TS']  # 2-letter codes to match in Doc Ref
    }
}

# Status Mappings - Maps actual status values to standardized categories
STATUS_MAPPINGS = {
    'Published': {
        'display_name': 'Published',
        'color': '18BABE',  # Teal
        'statuses': [
            'Published'
        ],
        'description': 'Published documents'
    },
    'Status A': {
        'display_name': 'Status A',
        'color': '25E82C',  # Green
        'statuses': [
            'Accepted'
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
    'Other': {
        'display_name': 'Other',
        'color': 'D3D3D3',  # Light gray
        'statuses': [
            'Withdrawn-Obsolete'
        ],
        'description': 'Other or Withdrawn or obsolete documents'
    }
}

# Display order for progression reports
STATUS_DISPLAY_ORDER = [
    'Published',
    'Status A',
    'Status B',
    'Status C',
    'Shared',
    'Other'
]