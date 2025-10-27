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

# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,
    'file_path': 'OVB Accommodation Schedule 201025.xlsx',
    'read_config': {
        'sheet_name': 0,
        'skiprows': [0, 1, 3],  # Skip rows 1-2 and row 4 ("Technical"), use row 3 as header
        'nrows': 226,        # Rows 5-230 (226 apartments)
        'usecols': 'A:E'     # Columns A through E
    },
    'column_mapping': {
        'apartment': 'Plot No.',         # Column A (e.g., B.1-1-4)
        'tenure': 'Tenure',              # Column B
        'apartment_type': 'Type',        # Column C (remove "Type " prefix)
        'bedrooms': 'No of Bed & Persons',  # Column D (extract first number from e.g., "2B3P")
        # Block and Floor will be extracted from Plot No. using custom logic
    },
    'apartment_cleaning': {
        'remove_prefix': '',             # Keep plot numbers as-is (B.1-1-4)
        'extract_pattern': None          # Don't extract, keep full string
    },
    'apartment_type_cleaning': {
        'remove_prefix': 'Type '         # Remove "Type " prefix from apartment types
    },
    'bedrooms_cleaning': {
        'extract_pattern': r'^(\d+)'     # Extract first digit from codes like '2B3P'
    },
    # Custom extraction from plot number (e.g., "B.1-1-4")
    'custom_extractors': {
        'block': {
            'source_column': 'Plot No.',
            'pattern': r'^([A-Z])\.(\d+)',  # Extract "B" and "1" from "B.1-1-4"
            'format': '{0}{1}'               # Combine as "B1"
        },
        'floor': {
            'source_column': 'Plot No.',
            'pattern': r'^[A-Z]\.\d+-(\d+)',  # Extract floor number after first dash
            'convert_to_int': True
        }
    }
}

# Accommodation Data - Imported from separate file
# Run scripts/update_accommodation_data.py to regenerate
from configs.accommodation_data.OvalBlockB import ACCOMMODATION_DATA

