"""Configuration for Greenwich Peninsula project."""

PROJECT_TITLE = "Greenwich Peninsula"

# Accommodation Schedule Configuration
# Used by scripts/update_accommodation_data.py to parse the accommodation schedule
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,  # Set to False to disable accommodation schedule parsing
    'file_path': 'GP Accommodation Schedule 201025.xlsx',  # Standard format: <ProjectCode> Accommodation Schedule <DDMMYY>.xlsx
    
    # Excel/CSV reading configuration
    'read_config': {
        'sheet_name': 0,  # First sheet
        'skiprows': 3,    # Skip first 3 rows (headers are on row 4, data starts row 5)
        'nrows': 476,     # Read 476 rows (data ends at row 480, which is 476 rows after row 4)
        'usecols': 'B:M'  # Only read columns A through N (O onwards can be ignored)
    },
    
    # Column mapping - maps standard names to actual column names in the schedule
    'column_mapping': {
        'apartment': 'Unit Ref',         # REQUIRED - Column containing apartment/unit numbers
        'phase': 'Phase',                # OPTIONAL - Column containing phase information
        'block': 'Building',             # OPTIONAL - Column containing block information  
        'floor': 'Floor',                # OPTIONAL - Column containing floor information
        'apartment_type': 'FRA Unit Type Ref',  # OPTIONAL - Column containing apartment type
        'bedrooms': 'Beds',              # OPTIONAL - Column containing number of bedrooms
        'tenure': 'Tenure'               # OPTIONAL - Column containing tenure type (e.g., Private, Rented, Shared Ownership)
    },
    
    # Apartment number cleaning configuration
    'apartment_cleaning': {
        'remove_prefix': '',  # Remove prefix like "Apt " or "Flat " (if any)
        'extract_pattern': r'\d+'  # Extract just the number part (optional regex)
    },
    
    # Floor cleaning configuration
    'floor_cleaning': {
        'remove_prefix': 'L',  # Remove "L" from "L01" -> "01"
        'remove_suffix': '',   # Remove suffix if needed
        'convert_to_int': True  # Convert "01" -> 1 (set False to keep as string)
    }
}

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
        "Doc Path",
        "Publisher"
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
    'Doc Path': 'Doc Path',
    'Publisher': 'Publisher'
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

# ============================================================================
# PROJECT STRUCTURE - Centralized metadata for phases, blocks, floors
# ============================================================================
# This section contains structural information about the project that reports
# and analyzers reference. Makes it easy to maintain across all reports.
PROJECT_STRUCTURE = {
    # Phase metadata
    'phases': {
        '18.02': {
            'display_name': 'Phase 18.02',
            'description': 'Phase 18.02 development',
            'blocks': ['A', 'B', 'C']
        },
        '18.03': {
            'display_name': 'Phase 18.03',
            'description': 'Phase 18.03 development',
            'blocks': ['D', 'E', 'F', 'G']
        }
    },
    
    # Block metadata - expected floors per block (for layout tracking)
    # These are the floors we expect to see in communal layouts
    # Ground (0) and roof floors are NOT included - only added if detected
    'blocks': {
        'A': {
            'expected_floors': list(range(1, 30)),  # Floors 1-29
            'phase': '18.02'
        },
        'B': {
            'expected_floors': list(range(1, 10)),  # Floors 1-9
            'phase': '18.02'
        },
        'C': {
            'expected_floors': list(range(1, 4)),   # Floors 1-3
            'phase': '18.02'
        },
        'D': {
            'expected_floors': list(range(1, 4)),   # Floors 1-3
            'phase': '18.03'
        },
        'E': {
            'expected_floors': list(range(1, 22)),  # Floors 1-21
            'phase': '18.03'
        },
        'F': {
            'expected_floors': list(range(1, 10)),  # Floors 1-9
            'phase': '18.03'
        },
        'G': {
            'expected_floors': list(range(1, 7)),   # Floors 1-6
            'phase': '18.03'
        }
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

# Certificate Tracking Configuration
CERTIFICATE_TRACKING = {
    # Phase/Block detection patterns (how to identify them in document metadata)
    'phase_detection': {
        'patterns': [r'18\.02', r'18\.03'],  # Regex patterns to find phase in title/ref/path
        'doc_title_patterns': [r'Plot\s+(\d{2}\.\d{2})'],  # Extract phase from doc title
        'doc_ref_patterns': []  # Could extract from doc ref if needed
    },
    
    'block_detection': {
        'patterns': [
            r'\bBlock\s*-\s*([A-G])\b',  # Match "Block - A" or "Block -A" or "Block- A"
            r'\bBlock\s+([A-G])\b',      # Match "Block A"
            r'\b([A-G])\s+Block\b'       # Match "A Block"
        ],
        'doc_title_patterns': []  # Could extract from doc title if needed
    },
    
    # Certificate categories to track
    # NOTE: max_count is now automatically derived from ACCOMMODATION_DATA['total_apartments']
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
from configs.accommodation_data.GreenwichPeninsula import ACCOMMODATION_DATA


# Apartment Layout Tracking Configuration
APARTMENT_LAYOUT_TRACKING = {
    'enabled': True,
    
    'detection': {
        'file_type_patterns': ['DR'],  # Drawing file type
        'doc_ref_patterns': [],  # Add doc ref patterns if needed
        'exclude_patterns': ['Schedule', 'Detail', 'Section', 'Elevation'],
    },
    
    'categories': {
        'apartment_layouts': {
            'enabled': True,
            
            'layout_types': {
                'ventilation': {
                    'display_name': 'Ventilation Apartment Layout',
                    'patterns': ['Ventilation Apartment Layout'],
                    'doc_ref_patterns': [],  # Add specific doc ref patterns if needed
                    'required': True,
                    'description': 'Ventilation apartment layout'
                },
                'drainage': {
                    'display_name': 'Drainage & Domestic Services Apartment Layout',
                    'patterns': ['Drainage and Domestic Services Layout Apartment'],
                    'doc_ref_patterns': [],  # Add specific doc ref patterns if needed
                    'required': True,
                    'description': 'Drainage and domestic services apartment layout'
                },
                'kitchen_electrical': {
                    'display_name': 'Kitchen Electrical Setting Out',
                    'patterns': ['Kitchen Electrical Setting Out - Type'],
                    'doc_ref_patterns': [],  # Add specific doc ref patterns if needed
                    'required': True,
                    'description': 'Kitchen electrical setting out layout'
                },
            },
            
            'apartment_type_detection': {
                'title_patterns': [
                    # First extract the "TYPE XX ..." section, then find all type codes in it
                    # This handles: "TYPE 5", "TYPE 5 & 5A", "TYPE 30A Plot 123", etc.
                    # Pattern captures everything after TYPE until PLOT, Block (not followed by &), or end
                    r'TYPE\s+([0-9]+[A-Za-z]?(?:\s*[&,]\s*[0-9]+[A-Za-z]?)*)',
                ],
                'doc_ref_patterns': [
                    r'-TYPE-([A-Z0-9]+[a-z]?)-',
                    r'-T([A-Z0-9]+[a-z]?)-'
                ],
                'path_patterns': [
                    r'\\Type\s+([A-Z0-9]+[a-z]?)\\',
                    r'\\([A-Z0-9]+[a-z]?)\s+Type\\'
                ]
            }
        },
        
        'communal_layouts': {
            'enabled': True,
            # NOTE: Expected floors per block are now defined in PROJECT_STRUCTURE['blocks']
            'layout_types': {
                'mechanical_services': {
                    'display_name': 'Mechanical Services Layout',
                    'patterns': ['Mechanical services layout'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Mechanical services communal layout'
                },
                'communal_lighting_power': {
                    'display_name': 'Communal Lighting & Small Power Layout',
                    'patterns': ['COMMUNAL LIGHTING & SMALL POWER LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Communal lighting and small power layout'
                },
                'above_ground_foul_rainwater': {
                    'display_name': 'Above Ground Foul & Rainwater Drainage Layout',
                    'patterns': ['ABOVE GROUND FOUL & RAINWATER DRAINAGE LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Above ground foul and rainwater drainage layout'
                },
                'electrical_services': {
                    'display_name': 'Electrical Services Layout',
                    'patterns': [
                        'Electrical services layout',
                        'APARTMENT ELECTRICAL SERVICES RCP AND SMALL POWER',
                        'APARTMENT ELECTRICAL SERVICES RCP'
                    ],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Electrical services communal layout'
                },
                'underfloor_heating': {
                    'display_name': 'Underfloor Heating Layout',
                    'patterns': ['UNDERFLOOR HEATING LAYOUT'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'Underfloor heating communal layout'
                },
                'mep_combined_services': {
                    'display_name': 'MEP Combined Services Layout',
                    'patterns': ['MEP Combined Services'],
                    'doc_ref_patterns': [],
                    'required': False,
                    'description': 'MEP (Mechanical, Electrical, Plumbing) combined services layout'
                }
            },
            'coverage_detection': {
                'floor_patterns': [
                    r'Level\s+(\d+)',  # Single level: "Level 01", "Level 15"
                    r'Level\s+(\d+)-(\d+)',  # Range: "Level 20-29"
                    r'Level\s+(\d+)\s+to\s+(\d+)',  # Range: "Level 02 to 06"
                    r'Level\s+(\d+)\s*&\s*(\d+)',  # Multiple single levels: "Level 15 & 16"
                    r'Level\s+(\d+)-(\d+)\s*&\s*(\d+)',  # Range & single: "Level 03-13 & 14"
                    r'Level\s+(\d+)\s*&\s*Roof',  # Single level & roof: "Level 06 & ROOF"
                    r'Levels\s+(\d+),\s*(\d+)\s*&\s*Roof',  # Multiple levels & roof: "LEVELS 08, 09 & ROOF"
                    r'Ground Floor',  # Ground floor
                    r'Roof Level',  # Roof level
                    r'Level\s+00',  # Ground floor as level 00
                    # Underfloor heating specific patterns
                    r'TO\s+FLOOR\s+(\d+)',  # "TO FLOOR 09"
                    r'TO\s+FLOOR\s+(\d+)-(\d+)',  # "TO FLOOR 02-14"
                    r'TO\s+FLOOR\s+(\d+)\s*-\s*(\d+)',  # "TO FLOOR 02 - 08" (with spaces)
                    r'TO\s+FIRST\s+FLOOR',  # "TO FIRST FLOOR" (maps to floor 1)
                    r'TO\s+GROUND\s+FLOOR',  # "TO GROUND FLOOR" (maps to floor 0)
                ]
            }
        }
    }
}
