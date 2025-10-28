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
    },
    # Tenure bundling configuration (for projects with multiple tenures per type)
    'tenure_config': {
        'enabled': True,  # Enable tenure bundling for OvalBlockB
        'format': '({tenure})',  # Format: "Type A-1 (PD)", "Type A-1 (Int)", etc.
        'strip_patterns': [' (WC)']  # Remove "(WC)" from type names - drawings don't include this marker
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
        'file_type_patterns': ['DR - Drawings (DR)'],  # Detect drawing files
        'doc_ref_patterns': [],
        'exclude_patterns': ['Schedule', 'Detail', 'Section', 'Elevation'],
    },
    
    # Block detection for layout drawings - handles B1, B2, and Block B patterns
    'block_detection': {
        'patterns': [
            r'\bBlock\s+(B[12])\b',       # Match "Block B1" or "Block B2" - captures "B1" or "B2"
            r'\bBlock\s+(B)\b',           # Match "Block B" (without number) - captures "B"
            r'\b(B[12])\b',               # Match "B1" or "B2" standalone - captures "B1" or "B2"
            r'\\Block\s*(B[12])\\',       # Match in paths: "\Block B1\" or "\Block B2\" - captures "B1" or "B2"
            r'\\Block\s*(B)\\',           # Match in paths: "\Block B\" - captures "B"
        ],
        'doc_title_patterns': []
    },
    
    'categories': {
        'apartment_layouts': {
            'enabled': True,  # Enabled for tracking apartment layouts
            
            'layout_types': {
                'ventilation': {
                    'display_name': 'Ventilation Apartment Layout',
                    'patterns': ['VENTILATION LAYOUT', 'VENTILATION APARTMENT LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': True,
                    'description': 'Ventilation apartment layout',
                    'greylisted_apartment_types': []
                },
                'mechanical_pipework': {
                    'display_name': 'Mechanical Pipework Apartment Layout',
                    'patterns': ['MECHANICAL PIPEWORK LAYOUT', 'MECHANICAL PIPEWORK APARTMENT LAYOUT', 'MECHANICAL LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': True,
                    'description': 'Mechanical pipework apartment layout',
                    'greylisted_apartment_types': []
                },
                'electrical_services': {
                    'display_name': 'Electrical Services Apartment Layout',
                    'patterns': ['ELECTRICAL SERVICES LAYOUT', 'ELECTRICAL SERVICES APARTMENT LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': True,
                    'description': 'Electrical services apartment layout',
                    'greylisted_apartment_types': []
                },
                'utility_cupboard': {
                    'display_name': 'Utility Cupboard Apartment Layout',
                    'patterns': ['UTILITY CUPBOARD LAYOUT', 'UTILITY CUPBOARD APARTMENT LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': True,
                    'description': 'Utility cupboard apartment layout',
                    'greylisted_apartment_types': []
                },
                'rcp': {
                    'display_name': 'RCP (Reflected Ceiling Plan) Apartment Layout',
                    'patterns': ['RCP'],
                    'doc_ref_patterns': [],
                    'required': True,
                    'description': 'RCP apartment layout (reflected ceiling plan)',
                    'greylisted_apartment_types': []
                }
            },
            
            'apartment_type_detection': {
                # Pattern to extract apartment type with tenure: "TYPE AA (PD)" or "- TYPE B-1 (INT)"
                'title_patterns': [
                    r'(?:APARTMENT\s+)?-?\s*TYPE\s+([A-Z0-9-]+\s*\([A-Za-z]+\))',  # Matches "TYPE AA (PD)", "- TYPE B-1 (INT)", etc.
                ],
                'doc_ref_patterns': [],
                'path_patterns': []
            }
            
            # Note: Block detection not needed - OvalBlockB doesn't separate B1/B2 for apartment layouts
        },
        
        'communal_layouts': {
            'enabled': True,
            # NOTE: Expected floors per block are now defined in PROJECT_STRUCTURE['blocks']
            'layout_types': {
                'communal_lighting_power': {
                    'display_name': 'Communal Lighting & Small Power Layout',
                    'patterns': ['Communal Lighting & Small Power Layout', 'COMMUNAL LIGHTING & SMALL POWER LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Communal lighting and small power layout',
                    'greylisted_blocks': []  # Required for both B1 and B2
                },
                'sprinkler': {
                    'display_name': 'Sprinkler Layout',
                    'patterns': [
                        'Sprinkler Layout',
                        'Sprinkler pipe work Layout',
                        'Sprinkler pipework Layout',
                        'SPRINKLER LAYOUT'
                    ],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Sprinkler layout for corridors and communal areas',
                    'greylisted_blocks': []  # Required for both B1 and B2
                },
                'rwp_svp_services': {
                    'display_name': 'RWP & SVP Services Layout',
                    'patterns': ['RWP & SVP Services Layout', 'RWP & SVP', 'RWP AND SVP'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Rainwater pipe (RWP) and soil vent pipe (SVP) services layout',
                    'greylisted_blocks': []  # Required for Block B (both sub-blocks)
                },
                'mechanical_combined_services': {
                    'display_name': 'Mechanical Combined Services Layout',
                    'patterns': ['Mechanical Combined Services Layout', 'MECHANICAL COMBINED SERVICES'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Mechanical combined services layout for communal corridors (multi-sheet documents)',
                    'greylisted_blocks': [],  # Required for Block B (both sub-blocks)
                    'track_sheets': True  # Enable sheet tracking for this layout type
                },
                'electrical_primary_distribution': {
                    'display_name': 'Electrical Services Primary Distribution Layout',
                    'patterns': ['Electrical Services Primary Distribution Layout', 'ELECTRICAL SERVICES PRIMARY DISTRIBUTION'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Electrical services primary distribution layout for residential levels',
                    'greylisted_blocks': []  # Required for Block B (both sub-blocks)
                }
            },
            'coverage_detection': {
                'floor_patterns': [
                    # Standard numeric patterns
                    r'Level\s+(\d+)',  # "Level 08"
                    r'Level\s+(\d+)-(\d+)',  # "Level 02-05"
                    r'Level\s+(\d+)\s+to\s+Level\s+(\d+)',  # "Level 02 to Level 05"
                    r'Level\s+(\d+)\s+to\s+(\d+)',  # "Level 02 to 05"
                    r'Floor\s+(\d+)',  # "Floor 07"
                    r'Floor\s+(\d+)-(\d+)',  # "Floor 02-05"
                    # Word-based floor numbers (for sprinkler layouts)
                    r'First\s+floor',  # Floor 1
                    r'Second\s+floor',  # Floor 2
                    r'Third\s+floor',  # Floor 3
                    r'Fourth\s+floor',  # Floor 4
                    r'Fifth\s+floor',  # Floor 5
                    r'Sixth\s+floor',  # Floor 6
                    r'Seventh\s+floor',  # Floor 7
                    r'Eighth\s+floor',  # Floor 8
                    r'Ninth\s+floor',  # Floor 9
                    r'Tenth\s+floor',  # Floor 10
                    r'Eleventh\s+floor',  # Floor 11
                    r'Twelfth\s+floor',  # Floor 12
                    # Special cases
                    r'Ground Floor',  # Floor 0
                    r'Roof Level',  # Roof
                ]
            }
        }
    }
}

