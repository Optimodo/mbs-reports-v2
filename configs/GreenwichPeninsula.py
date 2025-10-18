"""Configuration for Greenwich Peninsula project."""

PROJECT_TITLE = "Greenwich Peninsula"

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
        "File Type",
        "File Number",
        "Last Updated (WET)",
        "Doc Path"
    ]
}

# Column mappings - Map raw Excel columns to standardized names
COLUMN_MAPPINGS = {
    'File Type': 'File Type',  # Already standardized
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
    "column_name": "File Type",  # Column name for file type
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "File Type Summary"  # Title for the summary section
} 

# Drawing Settings (for main summary report focus)
DRAWING_SETTINGS = {
    'enabled': True,
    # File type filtering (Method 1) - EXACT matches only
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',
        'drawing_types': ['DR - Drawing (DR)', 'SC - Schematic Drawings (SC)']
    },
    # Doc Ref pattern filtering (Method 2) - 2-letter codes
    'doc_ref_filter': {
        'enabled': False,  # Enable if you want to filter by Doc Ref patterns
        'column_name': 'Doc Ref',
        'drawing_patterns': ['DR', 'SC']  # 2-letter codes to match in Doc Ref
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
        'column_name': 'File Type',
        'certificate_types': ['CE - Certificate (CE)']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': True,
        'column_name': 'Doc Ref',
        'certificate_patterns': ['CE']  # 2-letter codes to match in Doc Ref
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
        'technical_submittal_types': ['TS - Technical submission (TS)']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': False,
        'column_name': 'Doc Ref',
        'technical_submittal_patterns': ['TS', 'TX']
    }
}

# Status Mappings - Maps actual status values to standardized categories
# This allows project-specific status terminology to be properly categorized
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A',
        'color': '25E82C',  # Green
        'statuses': [
            'A - Authorized and Accepted'
        ],
        'description': 'Approved/Accepted documents'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'B - Partial Sign Off (with comment)'
        ],
        'description': 'Approved with comments'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'C-Rejected'
        ],
        'description': 'Rejected documents'
    },
    'Information': {
        'display_name': 'For Information',
        'color': 'FFFFFF',  # White
        'statuses': [
            'For Information'
        ],
        'description': 'Informational or under review'
    },
    'Review': {
        'display_name': 'Under Review/For Commenting',
        'color': 'FFFFFF',  # White
        'statuses': [
            'For Status Change',
            'For Commenting',
            'Reviewed'
        ],
        'description': 'For commenting or under review'
    }

}

# Display order for progression reports (order matters for chart generation)
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'Information',
    'Review'
] 