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

# Accommodation Data (Auto-generated - DO NOT EDIT MANUALLY)
# Run scripts/update_accommodation_data.py to regenerate this section


# Accommodation Data - Auto-generated by update_accommodation_data.py
# Last updated: 2025-10-21
# Source: OVB Accommodation Schedule 201025.xlsx
ACCOMMODATION_DATA = {
    'total_apartments': 226,
    'last_updated': '2025-10-21',
    'source_file': 'OVB Accommodation Schedule 201025.xlsx',
    
    'phases': {
        'Default': {
            'apartment_count': 226,
            'apartments': ['B.1-0-1', 'B.1-0-2', 'B.1-0-3', 'B.1-0-4', 'B.1-0-5', 'B.1-0-6', 'B.1-1-1', 'B.1-1-10', 'B.1-1-11', 'B.1-1-2', 'B.1-1-3', 'B.1-1-4', 'B.1-1-5', 'B.1-1-6', 'B.1-1-7', 'B.1-1-8', 'B.1-1-9', 'B.1-10-1', 'B.1-10-2', 'B.1-10-3', 'B.1-10-4', 'B.1-11-1', 'B.1-11-2', 'B.1-11-3', 'B.1-11-4', 'B.1-12-1', 'B.1-12-2', 'B.1-12-3', 'B.1-12-4', 'B.1-13-1', 'B.1-13-2', 'B.1-13-3', 'B.1-13-4', 'B.1-14-1', 'B.1-14-2', 'B.1-14-3', 'B.1-14-4', 'B.1-15-1', 'B.1-15-2', 'B.1-15-3', 'B.1-16-1', 'B.1-16-2', 'B.1-16-3', 'B.1-17-1', 'B.1-17-2', 'B.1-17-3', 'B.1-18-1', 'B.1-18-2', 'B.1-18-3', 'B.1-2-1', 'B.1-2-10', 'B.1-2-11', 'B.1-2-2', 'B.1-2-3', 'B.1-2-4', 'B.1-2-5', 'B.1-2-6', 'B.1-2-7', 'B.1-2-8', 'B.1-2-9', 'B.1-3-1', 'B.1-3-10', 'B.1-3-11', 'B.1-3-2', 'B.1-3-3', 'B.1-3-4', 'B.1-3-5', 'B.1-3-6', 'B.1-3-7', 'B.1-3-8', 'B.1-3-9', 'B.1-4-1', 'B.1-4-10', 'B.1-4-11', 'B.1-4-2', 'B.1-4-3', 'B.1-4-4', 'B.1-4-5', 'B.1-4-6', 'B.1-4-7', 'B.1-4-8', 'B.1-4-9', 'B.1-5-1', 'B.1-5-10', 'B.1-5-11', 'B.1-5-2', 'B.1-5-3', 'B.1-5-4', 'B.1-5-5', 'B.1-5-6', 'B.1-5-7', 'B.1-5-8', 'B.1-5-9', 'B.1-6-1', 'B.1-6-10', 'B.1-6-11', 'B.1-6-2', 'B.1-6-3', 'B.1-6-4', 'B.1-6-5', 'B.1-6-6', 'B.1-6-7', 'B.1-6-8', 'B.1-6-9', 'B.1-7-1', 'B.1-7-10', 'B.1-7-2', 'B.1-7-3', 'B.1-7-4', 'B.1-7-5', 'B.1-7-6', 'B.1-7-7', 'B.1-7-8', 'B.1-7-9', 'B.1-8-1', 'B.1-8-10', 'B.1-8-2', 'B.1-8-3', 'B.1-8-4', 'B.1-8-5', 'B.1-8-6', 'B.1-8-7', 'B.1-8-8', 'B.1-8-9', 'B.1-9-1', 'B.1-9-10', 'B.1-9-2', 'B.1-9-3', 'B.1-9-4', 'B.1-9-5', 'B.1-9-6', 'B.1-9-7', 'B.1-9-8', 'B.1-9-9', 'B.2-0-1', 'B.2-0-2', 'B.2-0-3', 'B.2-0-4', 'B.2-0-5', 'B.2-1-1', 'B.2-1-10', 'B.2-1-11', 'B.2-1-2', 'B.2-1-3', 'B.2-1-4', 'B.2-1-5', 'B.2-1-6', 'B.2-1-7', 'B.2-1-8', 'B.2-1-9', 'B.2-10-1', 'B.2-10-2', 'B.2-10-4', 'B.2-10-5', 'B.2-11-1', 'B.2-11-2', 'B.2-2-1', 'B.2-2-10', 'B.2-2-11', 'B.2-2-2', 'B.2-2-3', 'B.2-2-4', 'B.2-2-5', 'B.2-2-6', 'B.2-2-7', 'B.2-2-8', 'B.2-2-9', 'B.2-3-1', 'B.2-3-10', 'B.2-3-11', 'B.2-3-2', 'B.2-3-3', 'B.2-3-4', 'B.2-3-5', 'B.2-3-6', 'B.2-3-8', 'B.2-3-9', 'B.2-4-1', 'B.2-4-10', 'B.2-4-11', 'B.2-4-2', 'B.2-4-3', 'B.2-4-4', 'B.2-4-5', 'B.2-4-6', 'B.2-4-8', 'B.2-4-9', 'B.2-5-1', 'B.2-5-10', 'B.2-5-11', 'B.2-5-2', 'B.2-5-3', 'B.2-5-4', 'B.2-5-5', 'B.2-5-6', 'B.2-5-8', 'B.2-5-9', 'B.2-6-1', 'B.2-6-10', 'B.2-6-11', 'B.2-6-2', 'B.2-6-3', 'B.2-6-4', 'B.2-6-5', 'B.2-6-6', 'B.2-6-8', 'B.2-6-9', 'B.2-7-1', 'B.2-7-10', 'B.2-7-2', 'B.2-7-3', 'B.2-7-4', 'B.2-7-5', 'B.2-7-6', 'B.2-7-8', 'B.2-7-9', 'B.2-8-1', 'B.2-8-2', 'B.2-8-4', 'B.2-8-5', 'B.2-8-6', 'B.2-9-1', 'B.2-9-2', 'B.2-9-4', 'B.2-9-5', 'B.2-9-6'],
            'blocks': {
                'B1': {
                    'apartment_count': 134,
                    'apartments': ['B.1-0-1', 'B.1-0-2', 'B.1-0-3', 'B.1-0-4', 'B.1-0-5', 'B.1-0-6', 'B.1-1-1', 'B.1-1-10', 'B.1-1-11', 'B.1-1-2', 'B.1-1-3', 'B.1-1-4', 'B.1-1-5', 'B.1-1-6', 'B.1-1-7', 'B.1-1-8', 'B.1-1-9', 'B.1-10-1', 'B.1-10-2', 'B.1-10-3', 'B.1-10-4', 'B.1-11-1', 'B.1-11-2', 'B.1-11-3', 'B.1-11-4', 'B.1-12-1', 'B.1-12-2', 'B.1-12-3', 'B.1-12-4', 'B.1-13-1', 'B.1-13-2', 'B.1-13-3', 'B.1-13-4', 'B.1-14-1', 'B.1-14-2', 'B.1-14-3', 'B.1-14-4', 'B.1-15-1', 'B.1-15-2', 'B.1-15-3', 'B.1-16-1', 'B.1-16-2', 'B.1-16-3', 'B.1-17-1', 'B.1-17-2', 'B.1-17-3', 'B.1-18-1', 'B.1-18-2', 'B.1-18-3', 'B.1-2-1', 'B.1-2-10', 'B.1-2-11', 'B.1-2-2', 'B.1-2-3', 'B.1-2-4', 'B.1-2-5', 'B.1-2-6', 'B.1-2-7', 'B.1-2-8', 'B.1-2-9', 'B.1-3-1', 'B.1-3-10', 'B.1-3-11', 'B.1-3-2', 'B.1-3-3', 'B.1-3-4', 'B.1-3-5', 'B.1-3-6', 'B.1-3-7', 'B.1-3-8', 'B.1-3-9', 'B.1-4-1', 'B.1-4-10', 'B.1-4-11', 'B.1-4-2', 'B.1-4-3', 'B.1-4-4', 'B.1-4-5', 'B.1-4-6', 'B.1-4-7', 'B.1-4-8', 'B.1-4-9', 'B.1-5-1', 'B.1-5-10', 'B.1-5-11', 'B.1-5-2', 'B.1-5-3', 'B.1-5-4', 'B.1-5-5', 'B.1-5-6', 'B.1-5-7', 'B.1-5-8', 'B.1-5-9', 'B.1-6-1', 'B.1-6-10', 'B.1-6-11', 'B.1-6-2', 'B.1-6-3', 'B.1-6-4', 'B.1-6-5', 'B.1-6-6', 'B.1-6-7', 'B.1-6-8', 'B.1-6-9', 'B.1-7-1', 'B.1-7-10', 'B.1-7-2', 'B.1-7-3', 'B.1-7-4', 'B.1-7-5', 'B.1-7-6', 'B.1-7-7', 'B.1-7-8', 'B.1-7-9', 'B.1-8-1', 'B.1-8-10', 'B.1-8-2', 'B.1-8-3', 'B.1-8-4', 'B.1-8-5', 'B.1-8-6', 'B.1-8-7', 'B.1-8-8', 'B.1-8-9', 'B.1-9-1', 'B.1-9-10', 'B.1-9-2', 'B.1-9-3', 'B.1-9-4', 'B.1-9-5', 'B.1-9-6', 'B.1-9-7', 'B.1-9-8', 'B.1-9-9'],
                    'floors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
                },
                'B2': {
                    'apartment_count': 92,
                    'apartments': ['B.2-0-1', 'B.2-0-2', 'B.2-0-3', 'B.2-0-4', 'B.2-0-5', 'B.2-1-1', 'B.2-1-10', 'B.2-1-11', 'B.2-1-2', 'B.2-1-3', 'B.2-1-4', 'B.2-1-5', 'B.2-1-6', 'B.2-1-7', 'B.2-1-8', 'B.2-1-9', 'B.2-10-1', 'B.2-10-2', 'B.2-10-4', 'B.2-10-5', 'B.2-11-1', 'B.2-11-2', 'B.2-2-1', 'B.2-2-10', 'B.2-2-11', 'B.2-2-2', 'B.2-2-3', 'B.2-2-4', 'B.2-2-5', 'B.2-2-6', 'B.2-2-7', 'B.2-2-8', 'B.2-2-9', 'B.2-3-1', 'B.2-3-10', 'B.2-3-11', 'B.2-3-2', 'B.2-3-3', 'B.2-3-4', 'B.2-3-5', 'B.2-3-6', 'B.2-3-8', 'B.2-3-9', 'B.2-4-1', 'B.2-4-10', 'B.2-4-11', 'B.2-4-2', 'B.2-4-3', 'B.2-4-4', 'B.2-4-5', 'B.2-4-6', 'B.2-4-8', 'B.2-4-9', 'B.2-5-1', 'B.2-5-10', 'B.2-5-11', 'B.2-5-2', 'B.2-5-3', 'B.2-5-4', 'B.2-5-5', 'B.2-5-6', 'B.2-5-8', 'B.2-5-9', 'B.2-6-1', 'B.2-6-10', 'B.2-6-11', 'B.2-6-2', 'B.2-6-3', 'B.2-6-4', 'B.2-6-5', 'B.2-6-6', 'B.2-6-8', 'B.2-6-9', 'B.2-7-1', 'B.2-7-10', 'B.2-7-2', 'B.2-7-3', 'B.2-7-4', 'B.2-7-5', 'B.2-7-6', 'B.2-7-8', 'B.2-7-9', 'B.2-8-1', 'B.2-8-2', 'B.2-8-4', 'B.2-8-5', 'B.2-8-6', 'B.2-9-1', 'B.2-9-2', 'B.2-9-4', 'B.2-9-5', 'B.2-9-6'],
                    'floors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                },
            }
        },
    },
    
    'apartment_types': {
        'BB': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-0-1']
        },
        'E': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-0-2']
        },
        'F': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-0-3']
        },
        'CC': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-0-4']
        },
        'A-1': {
            'count': 3,
            'bedrooms': None,
            'apartments': ['B.1-0-5', 'B.1-5-10', 'B.1-6-10']
        },
        'B-1': {
            'count': 1,
            'bedrooms': None,
            'apartments': ['B.1-0-6']
        },
        'NN-2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-1-1']
        },
        'I-2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-1-2']
        },
        'FF-1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-1-3']
        },
        'J-1 (WC)': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-1-4']
        },
        'K-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-1-5']
        },
        'L-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-1-6']
        },
        'OO-2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-1-7']
        },
        'M-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-1-8']
        },
        'N-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-1-9']
        },
        'AB-1': {
            'count': 1,
            'bedrooms': None,
            'apartments': ['B.1-1-10']
        },
        'B-2': {
            'count': 1,
            'bedrooms': None,
            'apartments': ['B.1-1-11']
        },
        'NN-3': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-2-1']
        },
        'I-3': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-2-2']
        },
        'FF': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B.1-2-3', 'B.1-3-3', 'B.1-4-3', 'B.1-5-3', 'B.1-6-3']
        },
        'J (WC)': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B.1-2-4', 'B.1-3-4', 'B.1-4-4', 'B.1-5-4', 'B.1-6-4']
        },
        'K': {
            'count': 8,
            'bedrooms': 1,
            'apartments': ['B.1-2-5', 'B.1-3-5', 'B.1-4-5', 'B.1-5-5', 'B.1-6-5', 'B.1-7-4', 'B.1-8-4', 'B.1-9-4']
        },
        'L': {
            'count': 8,
            'bedrooms': 1,
            'apartments': ['B.1-2-6', 'B.1-3-6', 'B.1-4-6', 'B.1-5-6', 'B.1-6-6', 'B.1-7-5', 'B.1-8-5', 'B.1-9-5']
        },
        'OO': {
            'count': 8,
            'bedrooms': 2,
            'apartments': ['B.1-2-7', 'B.1-3-7', 'B.1-4-7', 'B.1-5-7', 'B.1-6-7', 'B.1-7-6', 'B.1-8-6', 'B.1-9-6']
        },
        'M': {
            'count': 8,
            'bedrooms': 1,
            'apartments': ['B.1-2-8', 'B.1-3-8', 'B.1-4-8', 'B.1-5-8', 'B.1-6-8', 'B.1-7-7', 'B.1-8-7', 'B.1-9-7']
        },
        'N': {
            'count': 8,
            'bedrooms': 1,
            'apartments': ['B.1-2-9', 'B.1-3-9', 'B.1-4-9', 'B.1-5-9', 'B.1-6-9', 'B.1-7-8', 'B.1-8-8', 'B.1-9-8']
        },
        'AB': {
            'count': 3,
            'bedrooms': None,
            'apartments': ['B.1-2-10', 'B.1-3-10', 'B.1-4-10']
        },
        'B': {
            'count': 8,
            'bedrooms': None,
            'apartments': ['B.1-2-11', 'B.1-3-11', 'B.1-4-11', 'B.1-5-11', 'B.1-6-11', 'B.1-7-10', 'B.1-8-10', 'B.1-9-10']
        },
        'NN': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B.1-3-1', 'B.1-4-1', 'B.1-5-1']
        },
        'I': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B.1-3-2', 'B.1-4-2', 'B.1-8-2', 'B.1-9-2']
        },
        'I-1': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B.1-5-2', 'B.1-6-2']
        },
        'NN-1': {
            'count': 4,
            'bedrooms': 2,
            'apartments': ['B.1-6-1', 'B.1-7-1', 'B.1-8-1', 'B.1-9-1']
        },
        'V': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.1-7-2']
        },
        'HH': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-7-3']
        },
        'A': {
            'count': 3,
            'bedrooms': None,
            'apartments': ['B.1-7-9', 'B.1-8-9', 'B.1-9-9']
        },
        'HH-1': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B.1-8-3', 'B.1-9-3']
        },
        'QQ': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B.1-10-1', 'B.1-11-1', 'B.1-12-1', 'B.1-13-1', 'B.1-14-1']
        },
        'OO-1': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B.1-10-2', 'B.1-11-2', 'B.1-12-2', 'B.1-13-2', 'B.1-14-2']
        },
        'RR': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B.1-10-3']
        },
        'JJ': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-10-4']
        },
        'RR-1': {
            'count': 4,
            'bedrooms': 3,
            'apartments': ['B.1-11-3', 'B.1-12-3', 'B.1-13-3', 'B.1-14-3']
        },
        'LL': {
            'count': 3,
            'bedrooms': 2,
            'apartments': ['B.1-11-4', 'B.1-12-4', 'B.1-13-4']
        },
        'LL-1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.1-14-4']
        },
        'WW': {
            'count': 2,
            'bedrooms': 3,
            'apartments': ['B.1-15-1', 'B.1-16-1']
        },
        'SS': {
            'count': 2,
            'bedrooms': 3,
            'apartments': ['B.1-15-2', 'B.1-16-2']
        },
        'XX': {
            'count': 4,
            'bedrooms': 3,
            'apartments': ['B.1-15-3', 'B.1-16-3', 'B.1-17-3', 'B.1-18-3']
        },
        'YY': {
            'count': 2,
            'bedrooms': 3,
            'apartments': ['B.1-17-1', 'B.1-18-1']
        },
        'TT': {
            'count': 2,
            'bedrooms': 3,
            'apartments': ['B.1-17-2', 'B.1-18-2']
        },
        'DD': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-0-1']
        },
        'EE': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-0-2']
        },
        'G': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-0-3']
        },
        'MM': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-0-4']
        },
        'H': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-0-5']
        },
        'C-1': {
            'count': 1,
            'bedrooms': None,
            'apartments': ['B.2-1-1']
        },
        'AC-1': {
            'count': 1,
            'bedrooms': None,
            'apartments': ['B.2-1-2']
        },
        'O-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-1-3']
        },
        'P-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-1-4']
        },
        'PP': {
            'count': 9,
            'bedrooms': 2,
            'apartments': ['B.2-1-5', 'B.2-2-5', 'B.2-3-5', 'B.2-4-5', 'B.2-5-5', 'B.2-6-5', 'B.2-7-5', 'B.2-8-5', 'B.2-9-5']
        },
        'Q-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-1-6']
        },
        'R': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B.2-1-7', 'B.2-2-7']
        },
        'S-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-1-8']
        },
        'GG-1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-1-9']
        },
        'T-1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-1-10']
        },
        'U-1': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B.2-1-11', 'B.2-2-11']
        },
        'C': {
            'count': 8,
            'bedrooms': None,
            'apartments': ['B.2-2-1', 'B.2-3-1', 'B.2-4-1', 'B.2-5-1', 'B.2-6-1', 'B.2-7-1', 'B.2-8-1', 'B.2-9-1']
        },
        'AC': {
            'count': 3,
            'bedrooms': None,
            'apartments': ['B.2-2-2', 'B.2-3-2', 'B.2-4-2']
        },
        'O': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B.2-2-3', 'B.2-3-3', 'B.2-4-3', 'B.2-5-3', 'B.2-6-3', 'B.2-7-3']
        },
        'P': {
            'count': 6,
            'bedrooms': 1,
            'apartments': ['B.2-2-4', 'B.2-3-4', 'B.2-4-4', 'B.2-5-4', 'B.2-6-4', 'B.2-7-4']
        },
        'Q': {
            'count': 2,
            'bedrooms': 1,
            'apartments': ['B.2-2-6', 'B.2-8-6']
        },
        'S': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-2-8']
        },
        'GG': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B.2-2-9', 'B.2-3-9', 'B.2-4-9', 'B.2-5-9', 'B.2-6-9']
        },
        'T-2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-2-10']
        },
        'AD': {
            'count': 5,
            'bedrooms': 2,
            'apartments': ['B.2-3-6', 'B.2-4-6', 'B.2-5-6', 'B.2-6-6', 'B.2-7-6']
        },
        'AE': {
            'count': 4,
            'bedrooms': 2,
            'apartments': ['B.2-3-8', 'B.2-4-8', 'B.2-5-8', 'B.2-6-8']
        },
        'T': {
            'count': 4,
            'bedrooms': 1,
            'apartments': ['B.2-3-10', 'B.2-4-10', 'B.2-5-10', 'B.2-6-10']
        },
        'U': {
            'count': 5,
            'bedrooms': 1,
            'apartments': ['B.2-3-11', 'B.2-4-11', 'B.2-5-11', 'B.2-6-11', 'B.2-7-10']
        },
        'D-1': {
            'count': 1,
            'bedrooms': None,
            'apartments': ['B.2-5-2']
        },
        'D': {
            'count': 2,
            'bedrooms': None,
            'apartments': ['B.2-6-2', 'B.2-7-2']
        },
        'W': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-7-8']
        },
        'X': {
            'count': 1,
            'bedrooms': 1,
            'apartments': ['B.2-7-9']
        },
        'AG': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B.2-8-2', 'B.2-9-2']
        },
        'AH': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B.2-8-4', 'B.2-9-4']
        },
        'II': {
            'count': 2,
            'bedrooms': 2,
            'apartments': ['B.2-10-5', 'B.2-9-6']
        },
        'KK': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-10-1']
        },
        'Y': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-10-2']
        },
        'AA': {
            'count': 1,
            'bedrooms': 2,
            'apartments': ['B.2-10-4']
        },
        'UU': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B.2-11-1']
        },
        'VV': {
            'count': 1,
            'bedrooms': 3,
            'apartments': ['B.2-11-2']
        },
    },
    
    'tenures': {
        'Soc': {
            'count': 4,
            'apartments': ['B.1-0-1', 'B.1-0-2', 'B.1-0-3', 'B.1-0-4']
        },
        'Int': {
            'count': 46,
            'apartments': ['B.1-0-5', 'B.1-0-6', 'B.1-1-1', 'B.1-1-10', 'B.1-1-11', 'B.1-1-2', 'B.1-1-3', 'B.1-1-4', 'B.1-1-5', 'B.1-1-6', 'B.1-1-7', 'B.1-1-8', 'B.1-1-9', 'B.1-2-1', 'B.1-2-10', 'B.1-2-11', 'B.1-2-2', 'B.1-2-3', 'B.1-2-4', 'B.1-2-5', 'B.1-2-6', 'B.1-2-7', 'B.1-2-8', 'B.1-2-9', 'B.1-3-1', 'B.1-3-10', 'B.1-3-11', 'B.1-3-2', 'B.1-3-3', 'B.1-3-4', 'B.1-3-5', 'B.1-3-6', 'B.1-3-7', 'B.1-3-8', 'B.1-3-9', 'B.1-4-1', 'B.1-4-10', 'B.1-4-11', 'B.1-4-2', 'B.1-4-3', 'B.1-4-4', 'B.1-4-5', 'B.1-4-6', 'B.1-4-7', 'B.1-4-8', 'B.1-4-9']
        },
        'PD': {
            'count': 176,
            'apartments': ['B.1-10-1', 'B.1-10-2', 'B.1-10-3', 'B.1-10-4', 'B.1-11-1', 'B.1-11-2', 'B.1-11-3', 'B.1-11-4', 'B.1-12-1', 'B.1-12-2', 'B.1-12-3', 'B.1-12-4', 'B.1-13-1', 'B.1-13-2', 'B.1-13-3', 'B.1-13-4', 'B.1-14-1', 'B.1-14-2', 'B.1-14-3', 'B.1-14-4', 'B.1-15-1', 'B.1-15-2', 'B.1-15-3', 'B.1-16-1', 'B.1-16-2', 'B.1-16-3', 'B.1-17-1', 'B.1-17-2', 'B.1-17-3', 'B.1-18-1', 'B.1-18-2', 'B.1-18-3', 'B.1-5-1', 'B.1-5-10', 'B.1-5-11', 'B.1-5-2', 'B.1-5-3', 'B.1-5-4', 'B.1-5-5', 'B.1-5-6', 'B.1-5-7', 'B.1-5-8', 'B.1-5-9', 'B.1-6-1', 'B.1-6-10', 'B.1-6-11', 'B.1-6-2', 'B.1-6-3', 'B.1-6-4', 'B.1-6-5', 'B.1-6-6', 'B.1-6-7', 'B.1-6-8', 'B.1-6-9', 'B.1-7-1', 'B.1-7-10', 'B.1-7-2', 'B.1-7-3', 'B.1-7-4', 'B.1-7-5', 'B.1-7-6', 'B.1-7-7', 'B.1-7-8', 'B.1-7-9', 'B.1-8-1', 'B.1-8-10', 'B.1-8-2', 'B.1-8-3', 'B.1-8-4', 'B.1-8-5', 'B.1-8-6', 'B.1-8-7', 'B.1-8-8', 'B.1-8-9', 'B.1-9-1', 'B.1-9-10', 'B.1-9-2', 'B.1-9-3', 'B.1-9-4', 'B.1-9-5', 'B.1-9-6', 'B.1-9-7', 'B.1-9-8', 'B.1-9-9', 'B.2-0-1', 'B.2-0-2', 'B.2-0-3', 'B.2-0-4', 'B.2-0-5', 'B.2-1-1', 'B.2-1-10', 'B.2-1-11', 'B.2-1-2', 'B.2-1-3', 'B.2-1-4', 'B.2-1-5', 'B.2-1-6', 'B.2-1-7', 'B.2-1-8', 'B.2-1-9', 'B.2-10-1', 'B.2-10-2', 'B.2-10-4', 'B.2-10-5', 'B.2-11-1', 'B.2-11-2', 'B.2-2-1', 'B.2-2-10', 'B.2-2-11', 'B.2-2-2', 'B.2-2-3', 'B.2-2-4', 'B.2-2-5', 'B.2-2-6', 'B.2-2-7', 'B.2-2-8', 'B.2-2-9', 'B.2-3-1', 'B.2-3-10', 'B.2-3-11', 'B.2-3-2', 'B.2-3-3', 'B.2-3-4', 'B.2-3-5', 'B.2-3-6', 'B.2-3-8', 'B.2-3-9', 'B.2-4-1', 'B.2-4-10', 'B.2-4-11', 'B.2-4-2', 'B.2-4-3', 'B.2-4-4', 'B.2-4-5', 'B.2-4-6', 'B.2-4-8', 'B.2-4-9', 'B.2-5-1', 'B.2-5-10', 'B.2-5-11', 'B.2-5-2', 'B.2-5-3', 'B.2-5-4', 'B.2-5-5', 'B.2-5-6', 'B.2-5-8', 'B.2-5-9', 'B.2-6-1', 'B.2-6-10', 'B.2-6-11', 'B.2-6-2', 'B.2-6-3', 'B.2-6-4', 'B.2-6-5', 'B.2-6-6', 'B.2-6-8', 'B.2-6-9', 'B.2-7-1', 'B.2-7-10', 'B.2-7-2', 'B.2-7-3', 'B.2-7-4', 'B.2-7-5', 'B.2-7-6', 'B.2-7-8', 'B.2-7-9', 'B.2-8-1', 'B.2-8-2', 'B.2-8-4', 'B.2-8-5', 'B.2-8-6', 'B.2-9-1', 'B.2-9-2', 'B.2-9-4', 'B.2-9-5', 'B.2-9-6']
        },
    },
    
    'apartment_lookup': {
        # Full apartment lookup dictionary with 226 apartments
        'B.1-0-1': {'phase': None, 'block': 'B1', 'floor': 0, 'type': 'BB', 'bedrooms': 2, 'tenure': 'Soc'},
        'B.1-0-2': {'phase': None, 'block': 'B1', 'floor': 0, 'type': 'E', 'bedrooms': 1, 'tenure': 'Soc'},
        'B.1-0-3': {'phase': None, 'block': 'B1', 'floor': 0, 'type': 'F', 'bedrooms': 1, 'tenure': 'Soc'},
        'B.1-0-4': {'phase': None, 'block': 'B1', 'floor': 0, 'type': 'CC', 'bedrooms': 2, 'tenure': 'Soc'},
        'B.1-0-5': {'phase': None, 'block': 'B1', 'floor': 0, 'type': 'A-1', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-0-6': {'phase': None, 'block': 'B1', 'floor': 0, 'type': 'B-1', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-1-1': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'NN-2', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-1-2': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'I-2', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-1-3': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'FF-1', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-1-4': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'J-1 (WC)', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-1-5': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'K-1', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-1-6': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'L-1', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-1-7': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'OO-2', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-1-8': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'M-1', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-1-9': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'N-1', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-1-10': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'AB-1', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-1-11': {'phase': None, 'block': 'B1', 'floor': 1, 'type': 'B-2', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-2-1': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'NN-3', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-2-2': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'I-3', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-2-3': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'FF', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-2-4': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'J (WC)', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-2-5': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'K', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-2-6': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'L', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-2-7': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'OO', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-2-8': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'M', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-2-9': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'N', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-2-10': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'AB', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-2-11': {'phase': None, 'block': 'B1', 'floor': 2, 'type': 'B', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-3-1': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'NN', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-3-2': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'I', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-3-3': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'FF', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-3-4': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'J (WC)', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-3-5': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'K', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-3-6': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'L', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-3-7': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'OO', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-3-8': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'M', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-3-9': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'N', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-3-10': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'AB', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-3-11': {'phase': None, 'block': 'B1', 'floor': 3, 'type': 'B', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-4-1': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'NN', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-4-2': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'I', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-4-3': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'FF', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-4-4': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'J (WC)', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-4-5': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'K', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-4-6': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'L', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-4-7': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'OO', 'bedrooms': 2, 'tenure': 'Int'},
        'B.1-4-8': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'M', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-4-9': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'N', 'bedrooms': 1, 'tenure': 'Int'},
        'B.1-4-10': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'AB', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-4-11': {'phase': None, 'block': 'B1', 'floor': 4, 'type': 'B', 'bedrooms': None, 'tenure': 'Int'},
        'B.1-5-1': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'NN', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-5-2': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'I-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-5-3': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'FF', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-5-4': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'J (WC)', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-5-5': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'K', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-5-6': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'L', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-5-7': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'OO', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-5-8': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'M', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-5-9': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'N', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-5-10': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'A-1', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-5-11': {'phase': None, 'block': 'B1', 'floor': 5, 'type': 'B', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-6-1': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'NN-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-6-2': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'I-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-6-3': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'FF', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-6-4': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'J (WC)', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-6-5': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'K', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-6-6': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'L', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-6-7': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'OO', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-6-8': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'M', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-6-9': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'N', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-6-10': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'A-1', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-6-11': {'phase': None, 'block': 'B1', 'floor': 6, 'type': 'B', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-7-1': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'NN-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-7-2': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'V', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-7-3': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'HH', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-7-4': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'K', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-7-5': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'L', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-7-6': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'OO', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-7-7': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'M', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-7-8': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'N', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-7-9': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'A', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-7-10': {'phase': None, 'block': 'B1', 'floor': 7, 'type': 'B', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-8-1': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'NN-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-8-2': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'I', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-8-3': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'HH-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-8-4': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'K', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-8-5': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'L', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-8-6': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'OO', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-8-7': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'M', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-8-8': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'N', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-8-9': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'A', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-8-10': {'phase': None, 'block': 'B1', 'floor': 8, 'type': 'B', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-9-1': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'NN-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-9-2': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'I', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-9-3': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'HH-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-9-4': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'K', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-9-5': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'L', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-9-6': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'OO', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-9-7': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'M', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-9-8': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'N', 'bedrooms': 1, 'tenure': 'PD'},
        'B.1-9-9': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'A', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-9-10': {'phase': None, 'block': 'B1', 'floor': 9, 'type': 'B', 'bedrooms': None, 'tenure': 'PD'},
        'B.1-10-1': {'phase': None, 'block': 'B1', 'floor': 10, 'type': 'QQ', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-10-2': {'phase': None, 'block': 'B1', 'floor': 10, 'type': 'OO-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-10-3': {'phase': None, 'block': 'B1', 'floor': 10, 'type': 'RR', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-10-4': {'phase': None, 'block': 'B1', 'floor': 10, 'type': 'JJ', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-11-1': {'phase': None, 'block': 'B1', 'floor': 11, 'type': 'QQ', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-11-2': {'phase': None, 'block': 'B1', 'floor': 11, 'type': 'OO-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-11-3': {'phase': None, 'block': 'B1', 'floor': 11, 'type': 'RR-1', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-11-4': {'phase': None, 'block': 'B1', 'floor': 11, 'type': 'LL', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-12-1': {'phase': None, 'block': 'B1', 'floor': 12, 'type': 'QQ', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-12-2': {'phase': None, 'block': 'B1', 'floor': 12, 'type': 'OO-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-12-3': {'phase': None, 'block': 'B1', 'floor': 12, 'type': 'RR-1', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-12-4': {'phase': None, 'block': 'B1', 'floor': 12, 'type': 'LL', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-13-1': {'phase': None, 'block': 'B1', 'floor': 13, 'type': 'QQ', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-13-2': {'phase': None, 'block': 'B1', 'floor': 13, 'type': 'OO-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-13-3': {'phase': None, 'block': 'B1', 'floor': 13, 'type': 'RR-1', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-13-4': {'phase': None, 'block': 'B1', 'floor': 13, 'type': 'LL', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-14-1': {'phase': None, 'block': 'B1', 'floor': 14, 'type': 'QQ', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-14-2': {'phase': None, 'block': 'B1', 'floor': 14, 'type': 'OO-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-14-3': {'phase': None, 'block': 'B1', 'floor': 14, 'type': 'RR-1', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-14-4': {'phase': None, 'block': 'B1', 'floor': 14, 'type': 'LL-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.1-15-1': {'phase': None, 'block': 'B1', 'floor': 15, 'type': 'WW', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-15-2': {'phase': None, 'block': 'B1', 'floor': 15, 'type': 'SS', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-15-3': {'phase': None, 'block': 'B1', 'floor': 15, 'type': 'XX', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-16-1': {'phase': None, 'block': 'B1', 'floor': 16, 'type': 'WW', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-16-2': {'phase': None, 'block': 'B1', 'floor': 16, 'type': 'SS', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-16-3': {'phase': None, 'block': 'B1', 'floor': 16, 'type': 'XX', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-17-1': {'phase': None, 'block': 'B1', 'floor': 17, 'type': 'YY', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-17-2': {'phase': None, 'block': 'B1', 'floor': 17, 'type': 'TT', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-17-3': {'phase': None, 'block': 'B1', 'floor': 17, 'type': 'XX', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-18-1': {'phase': None, 'block': 'B1', 'floor': 18, 'type': 'YY', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-18-2': {'phase': None, 'block': 'B1', 'floor': 18, 'type': 'TT', 'bedrooms': 3, 'tenure': 'PD'},
        'B.1-18-3': {'phase': None, 'block': 'B1', 'floor': 18, 'type': 'XX', 'bedrooms': 3, 'tenure': 'PD'},
        'B.2-0-1': {'phase': None, 'block': 'B2', 'floor': 0, 'type': 'DD', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-0-2': {'phase': None, 'block': 'B2', 'floor': 0, 'type': 'EE', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-0-3': {'phase': None, 'block': 'B2', 'floor': 0, 'type': 'G', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-0-4': {'phase': None, 'block': 'B2', 'floor': 0, 'type': 'MM', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-0-5': {'phase': None, 'block': 'B2', 'floor': 0, 'type': 'H', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-1': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'C-1', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-1-2': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'AC-1', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-1-3': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'O-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-4': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'P-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-5': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-1-6': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'Q-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-7': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'R', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-8': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'S-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-9': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'GG-1', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-1-10': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'T-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-1-11': {'phase': None, 'block': 'B2', 'floor': 1, 'type': 'U-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-1': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-2-2': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'AC', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-2-3': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'O', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-4': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'P', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-5': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-2-6': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'Q', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-7': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'R', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-8': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'S', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-9': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'GG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-2-10': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'T-2', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-2-11': {'phase': None, 'block': 'B2', 'floor': 2, 'type': 'U-1', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-3-1': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-3-2': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'AC', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-3-3': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'O', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-3-4': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'P', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-3-5': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-3-6': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'AD', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-3-8': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'AE', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-3-9': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'GG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-3-10': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'T', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-3-11': {'phase': None, 'block': 'B2', 'floor': 3, 'type': 'U', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-4-1': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-4-2': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'AC', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-4-3': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'O', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-4-4': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'P', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-4-5': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-4-6': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'AD', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-4-8': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'AE', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-4-9': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'GG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-4-10': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'T', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-4-11': {'phase': None, 'block': 'B2', 'floor': 4, 'type': 'U', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-5-1': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-5-2': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'D-1', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-5-3': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'O', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-5-4': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'P', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-5-5': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-5-6': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'AD', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-5-8': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'AE', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-5-9': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'GG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-5-10': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'T', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-5-11': {'phase': None, 'block': 'B2', 'floor': 5, 'type': 'U', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-6-1': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-6-2': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'D', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-6-3': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'O', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-6-4': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'P', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-6-5': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-6-6': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'AD', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-6-8': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'AE', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-6-9': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'GG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-6-10': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'T', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-6-11': {'phase': None, 'block': 'B2', 'floor': 6, 'type': 'U', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-7-1': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-7-2': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'D', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-7-3': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'O', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-7-4': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'P', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-7-5': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-7-6': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'AD', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-7-8': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'W', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-7-9': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'X', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-7-10': {'phase': None, 'block': 'B2', 'floor': 7, 'type': 'U', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-8-1': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-8-2': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'AG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-8-4': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'AH', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-8-5': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-8-6': {'phase': None, 'block': 'B2', 'floor': 8, 'type': 'Q', 'bedrooms': 1, 'tenure': 'PD'},
        'B.2-9-1': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'C', 'bedrooms': None, 'tenure': 'PD'},
        'B.2-9-2': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'AG', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-9-4': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'AH', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-9-5': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'PP', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-9-6': {'phase': None, 'block': 'B2', 'floor': 9, 'type': 'II', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-10-1': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'KK', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-10-2': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'Y', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-10-4': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'AA', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-10-5': {'phase': None, 'block': 'B2', 'floor': 10, 'type': 'II', 'bedrooms': 2, 'tenure': 'PD'},
        'B.2-11-1': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'UU', 'bedrooms': 3, 'tenure': 'PD'},
        'B.2-11-2': {'phase': None, 'block': 'B2', 'floor': 11, 'type': 'VV', 'bedrooms': 3, 'tenure': 'PD'},
    }
}
