"""Configuration for West Cromwell Road project."""

import pandas as pd

PROJECT_TITLE = "West Cromwell Road"

# CSV Settings for West Cromwell Road
CSV_SETTINGS = {
    'encoding': 'utf-8',
    'sep': ',',
    'quotechar': '"',
    'escapechar': '\\',
    'na_values': ['', 'nan', 'NaN', 'NULL'],
    'keep_default_na': True
}

# Column mappings - Now using Excel source (previously CSV)
# Excel has both 'Status' and 'Revision Workflow' columns
# We'll use both: Status for superseded detection, Revision Workflow for main status
COLUMN_MAPPINGS = {
    'Doc Ref': 'Name',                        # Document reference is in Name column
    'Doc Title': 'Description',               # Document title is in Description column  
    'Rev': 'Revision',                        # Revision is in Revision column
    'Status': 'Revision Workflow',            # Primary status from Revision Workflow column
    'Date (WET)': 'Revision Date Modified',   # Date is in Revision Date Modified column
    'Doc Path': 'Full Path'                   # Full folder path for filtering
}

# Excel processing settings
# Using new Excel source with Full Path column
EXCEL_SETTINGS = {
    "sheet_name": 0
    # No skiprows or usecols - load all columns from the Excel file
    # Column mapping will handle transforming to standard format
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
    "output_format": "excel",
    "include_charts": True
} 

# File type settings
FILE_TYPE_SETTINGS = {
    "enabled": False
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': False,
    'generate_report': False
}

# Drawing Settings (for main summary report - all documents in this case)
DRAWING_SETTINGS = {
    'enabled': False  # No file type column, so include all documents
}

# Status Mappings - Maps actual Revision Workflow values to standardized categories
# Note: Now using 'Revision Workflow' column instead of 'Status' column
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A (Approved)',
        'color': '25E82C',  # Green
        'statuses': [
            'EA+DM - Status A'
        ],
        'description': 'Approved documents - ready to proceed'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'Status B',
        ],
        'description': 'Approved documents - ready to proceed'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'QA Rejected',
            'Not Approved',
            'DM - Status C'
        ],
        'description': 'Rejected documents requiring revision'
    },
    'Under Review': {
        'display_name': 'Under Review',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Under DC Review',
            'Yes - Proceed to EA Review',
            'Yes - Proceed to Consultant Review',
            'Under ACL DM Review',
            'Yes - Proceed to DM Review',
            'QA Approved'
        ],
        'description': 'Documents currently under review'
    },
    'Other': {
        'display_name': 'Other',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Superseeded',
            'Withdrawn',
            'Ardmore Package Manager'
        ],
        'description': 'Superseeded or Withdrawn documents'
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

def map_wcr_status(row):
    """
    Custom status mapping for West Cromwell Road.
    
    Special logic:
    - Documents in '/SS/' folder (superseded) → map to 'Superseeded' status
    - This ensures superseded documents are categorized as 'Other' status
    
    The Excel file has both 'Status' and 'Revision Workflow' columns:
    - 'Status' column shows document state (Superseded, ACTIVE, REVISED, etc.)
    - 'Revision Workflow' column shows workflow status (QA Approved, Not Approved, etc.)
    - 'Full Path' column shows folder location
    
    We use:
    1. Full Path to detect /SS/ folder → set to 'Superseeded'
    2. Otherwise, use Revision Workflow for normal status mapping
    """
    # Get the full path (after column mapping, this will be in 'Doc Path')
    doc_path = row.get('Full Path', '') if pd.notna(row.get('Full Path', '')) else ''
    doc_path = str(doc_path).strip()
    
    # Check if document is in SS (superseded) folder
    # Path format is "/ SS /" with spaces around SS
    if '/ SS /' in doc_path or '/ ss /' in doc_path or '/SS/' in doc_path or '/ss/' in doc_path:
        return 'Superseeded'
    
    # Get the status column value (this will be raw 'Status' from Excel)
    status_raw = row.get('Status', '') if pd.notna(row.get('Status', '')) else ''
    status_raw = str(status_raw).strip()
    
    # If Status column explicitly says Superseded (regardless of folder)
    if status_raw.lower() == 'superseded':
        return 'Superseeded'
    
    # Otherwise, use Revision Workflow column for normal status mapping
    revision_workflow = row.get('Revision Workflow', '') if pd.notna(row.get('Revision Workflow', '')) else ''
    revision_workflow = str(revision_workflow).strip()
    
    # Handle string 'nan' from pandas string conversion
    if revision_workflow.lower() == 'nan':
        revision_workflow = ''
    
    # Return the Revision Workflow value (will be mapped by STATUS_MAPPINGS)
    if revision_workflow:
        return revision_workflow
    
    return 'Other'

# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,
    'file_path': 'WCR Accommodation Schedule 201025.xlsx',
    'read_config': {
        'sheet_name': 0,
        'skiprows': 1,       # Skip row 1, use row 2 as header
        'nrows': 462,        # Rows 3-464 (462 apartments)
        'usecols': 'A:G'     # Columns A through G
    },
    'column_mapping': {
        'apartment': 'Name',             # Column C (e.g., B1.03.001)
        'block': 'Building',             # Column A (e.g., B1)
        'floor': 'Level',                # Column B (already numeric)
        'apartment_type': 'Apt Type',    # Column D
        'bedrooms': 'Beds',              # Column E (already numeric)
        'tenure': 'Tenure'               # Column G
    },
    'apartment_cleaning': {
        'remove_prefix': '',             # Keep apartment numbers as-is (B1.03.001)
        'extract_pattern': None          # Don't extract, keep full string
    },
    'floor_cleaning': {
        'remove_prefix': '',             # Floor is already numeric
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
            'description': 'West Cromwell Road development',
            'blocks': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']  # Note: No B6 in this project
        }
    },
    
    # Block metadata - expected floors per block (for layout tracking)
    # These are the floors we expect to see in communal layouts
    # Ground (0) and roof floors are NOT included - only added if detected
    'blocks': {
        'B1': {
            'expected_floors': list(range(3, 13)),   # Floors 3-12
            'phase': 'Default'
        },
        'B2': {
            'expected_floors': list(range(2, 30)),   # Floors 2-29
            'phase': 'Default'
        },
        'B3': {
            'expected_floors': list(range(2, 13)),   # Floors 2-12
            'phase': 'Default'
        },
        'B4': {
            'expected_floors': list(range(2, 15)),   # Floors 2-14
            'phase': 'Default'
        },
        'B5': {
            'expected_floors': list(range(2, 14)),   # Floors 2-13
            'phase': 'Default'
        },
        'B7': {
            'expected_floors': list(range(1, 14)),   # Floors 1-13 (ground floor 0 excluded)
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
            'enabled': True,
            'column_name': 'File Type',
            'certificate_types': ['CE - Certificate (CE)', 'CT - Certificate (CT)']
        },
        # Doc Ref filtering - match by patterns in Doc Ref
        'doc_ref_filter': {
            'enabled': True,
            'column_name': 'Doc Ref',
            'patterns': ['CE', 'CT']  # 2-letter codes to match in Doc Ref
        },
        # Path filtering - distinguish apartment vs communal certificates
        'path_filter': {
            'enabled': True,
            # Include only certificates in block-specific folders (apartment certificates)
            'include_patterns': [
                r'\\Apartments\\',         # Apartment-specific folders
                r'\\Units\\',              # Unit-specific folders
                r'\\Flats\\',              # Flat-specific folders
            ],
            # Exclude certificates in landlord/communal folders
            'exclude_patterns': [
                r'\\Landlords\\',
                r'\\Communal\\',
                r'\\Common\s*Areas\\',
            ]
        }
    },
    
    # Metadata extraction - extract phase/block from document metadata
    'phase_detection': {
        'patterns': [r'WCR', r'West\s*Cromwell'],  # WestCromwellRoad single building
        'doc_title_patterns': [r'Plot\s+(\d+)', r'Apt\s+(\d+)', r'Unit\s+(\d+)', r'Flat\s+(\d+)'],
        'doc_ref_patterns': []
    },
    
    'block_detection': {
        'patterns': [
            r'\bWCR\b',                # Match "WCR"
            r'West\s*Cromwell',        # Match "West Cromwell" or "WestCromwell"
            r'\\WCR\\',                # Match in paths: "\WCR\"
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
from configs.accommodation_data.WestCromwellRoad import ACCOMMODATION_DATA

# ============================================================================
# APARTMENT LAYOUT TRACKING - Configuration for layout reports
# ============================================================================
# Set enabled=True and configure patterns when ready to track layouts
APARTMENT_LAYOUT_TRACKING = {
    'enabled': True,  # Enabled - will generate empty report until patterns are configured
    
    'detection': {
        'file_type_patterns': [],
        'doc_ref_patterns': ['DR', 'SM'], # Detect drawing and schematic files
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


