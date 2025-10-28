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
        'usecols': 'A:F'     # Columns A through F (added F for Line 1/postal address)
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
    },
    # Postal address extraction (optional)
    'postal_address_extraction': {
        'enabled': True,  # Enable postal address extraction for this project
        'flat_no': {
            'source_column': 'Flat No.',  # Column E
            'extract_pattern': None        # Take value as-is (includes period, e.g., "Flat 4")
        },
        'address_line1': {
            'source_column': 'Line 1',     # Column F
            'extract_pattern': r'^([^,]+)',  # Extract everything before first comma
            'strip': True                   # Strip whitespace
        },
        'address_line2': {
            'enabled': False               # Not available for this project
        },
        'city': {
            'enabled': False               # Not available separately
        },
        'postcode': {
            'source_column': 'Line 1',     # Column F
            'extract_pattern': r',\s*([A-Z0-9\s]+)$',  # Extract after comma (postcode at end)
            'strip': True                   # Strip whitespace
        }
    }
}

# ============================================================================
# PROJECT STRUCTURE - Centralized metadata for phases, blocks, floors
# ============================================================================
# This section contains structural information about the project that reports
# and analyzers reference. Makes it easy to maintain across all reports.
# TODO: Fill in your project's phases and blocks
PROJECT_STRUCTURE = {
    # Phase metadata
    'phases': {
        'Default': {
            'display_name': 'Default',
            'description': 'Oval Block B development',
            'blocks': ['B1', 'B2']
        }
    },
    
    # Block metadata - expected floors per block (for layout tracking)
    # These are the floors we expect to see in communal layouts
    # Ground (0) and roof floors are NOT included - only added if detected
    'blocks': {
        'B1': {
            'expected_floors': list(range(1, 19)),  # Floors 1-18 (ground floor 0 excluded)
            'phase': 'Default'
        },
        'B2': {
            'expected_floors': list(range(1, 12)),  # Floors 1-11 (ground floor 0 excluded)
            'phase': 'Default'
        }
    }
}

# ============================================================================
# CERTIFICATE TRACKING - Consolidated certificate configuration
# ============================================================================
# Set enabled=True and configure patterns when ready to track certificates
CERTIFICATE_TRACKING = {
    # Enable/disable certificate tracking and report generation
    'enabled': True,
    'generate_report': True,
    
    # Document detection - which documents ARE certificates?
    'document_detection': {
        # File type filtering - match by File Type column
        'file_type_filter': {
            'enabled': True,  # Already configured
            'column_name': 'File Type',
            'certificate_types': ['CT - Certificate (CT)']
        },
        # Doc Ref filtering - match by patterns in Doc Ref
        'doc_ref_filter': {
            'enabled': True,  # Already configured
            'column_name': 'Doc Ref',
            'patterns': ['CT']  # 2-letter codes to match in Doc Ref
        },
        # Path filtering - distinguish apartment vs communal certificates
        # NOTE: OvalBlockB stores all certificates in one folder, so path filtering is disabled
        # Apartment certificates are identified by "B###" pattern in titles (e.g., "B112", "B151")
        'path_filter': {
            'enabled': False,
            'include_patterns': [],
            'exclude_patterns': []
        }
    },
    
    # Metadata extraction - extract phase/block from document metadata
    'phase_detection': {
        'patterns': [r'Block\s*B', r'\bB\b'],  # OvalBlockB is a single block
        'doc_title_patterns': [r'Plot\s+(\d+)', r'Apt\s+(\d+)', r'Unit\s+(\d+)'],
        'doc_ref_patterns': []
    },
    
    'block_detection': {
        'patterns': [
            r'\bBlock\s*B\b',          # Match "Block B"
            r'\bBlk\s*B\b',            # Match "Blk B"
            r'\\Block\s*B\\',          # Match in paths: "\Block B\"
        ],
        'doc_title_patterns': []
    },
    
    # Certificate categories to track (for apartment certificates)
    # NOTE: max_count is automatically derived from ACCOMMODATION_DATA['total_apartments']
    'apartment_certificates': {
        'part_p': {
            'patterns': ['Part P'],
            'display_name': 'Part P'
        },
        'electrical_cert': {
            'patterns': ['Electrical Cert'],
            'display_name': 'Electrical Cert'
        },
        'mvhr_ventilation': {
            'patterns': ['MVHR Cert', 'MVHR'],
            'display_name': 'MVHR / Ventilation'
        },
        'apartment_flushing': {
            'patterns': ['Apartment Flushing Certificate', 'Apartment Flushing'],
            'display_name': 'Apartment Flushing'
        },
        'fire_alarm': {
            'patterns': ['FA Cert', 'FA CERT', 'Fire'],
            'display_name': 'Fire Alarm'
        },
        'data_network': {
            'patterns': ['Data Network Cert', 'DATA NETWORK'],
            'display_name': 'Data Network'
        },
        'irs': {
            'patterns': ['IRS Cert', 'IRS'],
            'display_name': 'IRS'
        },
        'hiu_heating': {
            'patterns': ['HIU Cert', 'Heat'],
            'display_name': 'HIU / Heating'
        },
        'water_quality': {
            'patterns': ['Water Quality Cert', 'Water Quality'],
            'display_name': 'Water Quality'
        }
    }
}

# Accommodation Data - Imported from separate file
# Run scripts/update_accommodation_data.py to regenerate
from configs.accommodation_data.OvalBlockB import ACCOMMODATION_DATA

# ============================================================================
# APARTMENT LAYOUT TRACKING - Configuration for layout reports
# ============================================================================
# Set enabled=True and configure patterns when ready to track layouts
APARTMENT_LAYOUT_TRACKING = {
    'enabled': True,  # Enabled - will generate empty report until patterns are configured
    
    'detection': {
        'file_type_patterns': [],  # TODO: Add patterns like ['DR'] for drawings
        'doc_ref_patterns': [],
        'exclude_patterns': ['Schedule', 'Detail', 'Section', 'Elevation'],
    },
    
    'categories': {
        'apartment_layouts': {
            'enabled': False,  # TODO: Set to True when ready
            
            'layout_types': {
                # TODO: Add apartment layout types
                # Example:
                # 'ventilation': {
                #     'display_name': 'Ventilation Apartment Layout',
                #     'patterns': ['Ventilation Apartment Layout'],
                #     'doc_ref_patterns': [],
                #     'required': True,
                #     'description': 'Ventilation apartment layout'
                # }
            },
            
            'apartment_type_detection': {
                'title_patterns': [],  # TODO: Add patterns to extract apartment types
                'doc_ref_patterns': [],
                'path_patterns': []
            }
        },
        
        'communal_layouts': {
            'enabled': False,  # TODO: Set to True when ready
            # NOTE: Expected floors per block are now defined in PROJECT_STRUCTURE['blocks']
            'layout_types': {
                # TODO: Add communal layout types
                # Example:
                # 'mechanical_services': {
                #     'display_name': 'Mechanical Services Layout',
                #     'patterns': ['Mechanical services layout'],
                #     'doc_ref_patterns': [],
                #     'required': False,
                #     'description': 'Mechanical services communal layout'
                # }
            },
            'coverage_detection': {
                'floor_patterns': [
                    r'Level\s+(\d+)',
                    r'Level\s+(\d+)-(\d+)',
                    r'Level\s+(\d+)\s+to\s+(\d+)',
                    r'Ground Floor',
                    r'Roof Level',
                ]
            }
        }
    }
}

