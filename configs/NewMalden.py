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

# Column mappings - Map raw Excel columns to standardized names
COLUMN_MAPPINGS = {
    'File Type': 'Form',  # New Malden uses 'Form' column for file types
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
    "column_name": "File Type",  # Standardized column name in database
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "Form Type Summary"  # Title for the summary section
} 

# Drawing Settings (for main summary report focus)
DRAWING_SETTINGS = {
    'enabled': True,
    # File type filtering (Method 1) - EXACT matches only
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Standardized column name in database
        'drawing_types': ['Drawing (DR)', 'Schematic (SM)']
    },
    # Doc Ref pattern filtering (Method 2) - 2-letter codes
    'doc_ref_filter': {
        'enabled': False,  # Enable if you want to filter by Doc Ref patterns
        'column_name': 'Doc Ref',
        'drawing_patterns': ['DR', 'SM']  # 2-letter codes to match in Doc Ref
    }
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': False,  # No technical submittals for this project yet
    'generate_report': False
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

# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,
    'file_path': 'NM Accommodation Schedule 201025.xlsx',
    'read_config': {
        'sheet_name': 0,
        'skiprows': 16,      # Skip rows 1-16, use row 17 as header
        'nrows': 456,        # Rows 18-473 (456 apartments)
        'usecols': 'A:M'     # Columns A through M
    },
    'column_mapping': {
        'apartment': 'Apt No.',          # Column B
        'floor': 'Level',                # Column C
        'block': 'Block',                # Column D
        'apartment_type': 'Apartment Type',  # Column F
        'bedrooms': 'Beds',              # Column I
        'tenure': 'Tenure'               # Column M
        # Note: No 'phase' column - will default to None
    },
    'apartment_cleaning': {
        'remove_prefix': '',             # Adjust if apartment numbers have prefixes
        'extract_pattern': r'\d+'        # Extract numeric portion
    },
    'floor_cleaning': {
        'remove_prefix': 'Level ',       # Remove "Level " prefix from floor numbers
        'remove_suffix': '',
        'convert_to_int': True
    },
    # Postal address extraction (optional) - DISABLED for this project
    # Enable this when postal addresses become available in the accommodation schedule
    'postal_address_extraction': {
        'enabled': False,  # Set to True when addresses are available
        'flat_no': {
            'source_column': None,  # Specify column name when enabling
            'extract_pattern': None
        },
        'address_line1': {
            'source_column': None,
            'extract_pattern': None,
            'strip': True
        },
        'address_line2': {
            'enabled': False
        },
        'city': {
            'enabled': False
        },
        'postcode': {
            'source_column': None,
            'extract_pattern': None,
            'strip': True
        }
    }
}

# ============================================================================
# PROJECT STRUCTURE - Centralized metadata for phases, blocks, floors
# ============================================================================
# This section contains structural information about the project that reports
# and analyzers reference. Makes it easy to maintain across all reports.
PROJECT_STRUCTURE = {
    # Phase metadata
    'phases': {
        'Default': {
            'display_name': 'Default',
            'description': 'NewMalden development',
            'blocks': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        }
    },
    
    # Block metadata - expected floors per block (for layout tracking)
    # These are the floors we expect to see in communal layouts
    # Ground (0) and roof floors are NOT included - only added if detected
    'blocks': {
        'A': {
            'expected_floors': list(range(1, 13)),  # Floors 1-12
            'phase': 'Default'
        },
        'B': {
            'expected_floors': list(range(1, 11)),  # Floors 1-10
            'phase': 'Default'
        },
        'C': {
            'expected_floors': list(range(1, 9)),   # Floors 1-8
            'phase': 'Default'
        },
        'D': {
            'expected_floors': list(range(1, 8)),   # Floors 1-7
            'phase': 'Default'
        },
        'E': {
            'expected_floors': list(range(1, 15)),  # Floors 1-14
            'phase': 'Default'
        },
        'F': {
            'expected_floors': list(range(1, 9)),   # Floors 1-8
            'phase': 'Default'
        },
        'G': {
            'expected_floors': list(range(1, 9)),   # Floors 1-8
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
        # File type filtering - match by Form column
        'file_type_filter': {
            'enabled': True,  # Already configured with Form column
            'column_name': 'Form',
            'certificate_types': ['Certificate', 'CERT']
        },
        # Doc Ref filtering - match by patterns in Doc Ref
        'doc_ref_filter': {
            'enabled': True,
            'column_name': 'Doc Ref',
            'patterns': ['CE', 'CT']  # Common certificate codes
        },
        # Path filtering - distinguish apartment vs communal certificates
        'path_filter': {
            'enabled': False,
            # Include only certificates in block-specific folders (apartment certificates)
            'include_patterns': [
            ],
            # Exclude certificates in landlord/communal folders
            'exclude_patterns': [
            ]
        }
    },
    
    # Metadata extraction - extract phase/block from document metadata
    'phase_detection': {
        'patterns': [r'Phase\s*(\d+)', r'Block\s*(\d+)'],  # NewMalden uses numbered blocks
        'doc_title_patterns': [r'Plot\s+(\d+)', r'Apt\s+(\d+)', r'Unit\s+(\d+)'],
        'doc_ref_patterns': []
    },
    
    'block_detection': {
        'patterns': [
            r'\bBlock\s*(\d+)\b',      # Match "Block 1", "Block 2", etc.
            r'\bBlk\s*(\d+)\b',        # Match "Blk 1", "Blk 2", etc.
            r'\\Block\s*(\d+)\\',      # Match in paths: "\Block 1\"
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
from configs.accommodation_data.NewMalden import ACCOMMODATION_DATA

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

