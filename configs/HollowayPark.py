import pandas as pd
# Holloway Park Project Configuration
# This project uses CSV files instead of Excel files

PROJECT_TITLE = "Holloway Park"

# CSV Settings for Holloway Park
CSV_SETTINGS = {
    'encoding': 'utf-8',
    'sep': ',',
    'quotechar': '"',
    'escapechar': '\\',
    'na_values': ['', 'nan', 'NaN', 'NULL'],
    'keep_default_na': True
}

# Column mappings for CSV to standard format
COLUMN_MAPPINGS = {
    'Doc Ref': 'Title',           # Document reference is in Title column
    'Doc Title': 'Subject',       # Document title is in Subject column  
    'Doc Path': 'Project Folder', # Document path is in Project Folder column
    'Status': 'Status',           # Status is in Status column (column F)
    'Design Status': 'Design Status',  # Design Status is in Design Status column (column I)
    'Rev': 'Rev',                 # Revision is in Rev column
    'Date (WET)': 'Date',         # Date is in Date column
    'Description': 'Description'   # Description is in Description column
}

# MBS Filtering - only include documents with MBS in the title
MBS_FILTER = {
    'enabled': True,
    'search_columns': ['Title'],  # Only search in Title column for MBS
    'case_sensitive': False       # Case insensitive search
}

# File type settings (not applicable for this project)
FILE_TYPE_SETTINGS = {
    'enabled': False
}

# Drawing Settings (for main summary report - all documents in this case)
DRAWING_SETTINGS = {
    'enabled': False  # No file type column, so include all documents
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': False,
    'generate_report': False
}

# Status Mappings - Maps actual status values to standardized categories
# Note: The custom map_holloway_park_status() function transforms dual-column
# statuses into these standardized values, which are then mapped here
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A (Construction)',
        'color': '25E82C',  # Green
        'statuses': [
            'Status A'  # From map_holloway_park_status when Status='Construction'
        ],
        'description': 'Construction status documents'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'Status B'  # From map_holloway_park_status when Design Status='B'
        ],
        'description': 'Design Status B'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'Status C'  # From map_holloway_park_status when Design Status='C'
        ],
        'description': 'Design Status C'
    },
    'IFC-pending': {
        'display_name': 'IFC-pending',
        'color': 'FFFFFF',  # White
        'statuses': [
            'IFC-pending'  # From map_holloway_park_status when Status='IFC-pending'
        ],
        'description': 'IFC-pending documents awaiting approval'
    },
    'Other': {
        'display_name': 'Other',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Other'  # Information, Tender, Contract, As-Built, Record, Planning, Preliminary, Withdrawn, etc.
        ],
        'description': 'Information, Tender, Contract, As-Built, Record, Planning, Preliminary, Withdrawn etc.'
    }
}

# Display order for progression reports
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'IFC-pending',
    'Other'
]

# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,
    'file_path': 'HP Accommodation Schedule 201025.xlsx',
    'read_config': {
        'sheet_name': 0,
        'skiprows': 2,       # Skip rows 1-2, use row 3 as header
        'nrows': None,       # Read all remaining rows (we'll determine actual count)
        'usecols': 'A:J'     # Columns A through J
    },
    'column_mapping': {
        'apartment': 'Plot',             # Column A (e.g., C1-01-01)
        'phase': 'Building',             # Column B
        'block': 'Core',                 # Column C
        'floor': 'Level.1',              # Column E (numeric floor: 1, 2, 3)
        'apartment_type': 'Flat Type Ref.',  # Column I
        'bedrooms': 'Beds',              # Column J (needs extraction: '3B4P' -> 3)
        'tenure': 'Tenure'               # Column H
    },
    'apartment_cleaning': {
        'remove_prefix': '',             # Keep apartment numbers as-is (C1-01-01)
        'extract_pattern': None          # Don't extract, keep full string
    },
    'floor_cleaning': {
        'remove_prefix': '',             # Floor is already numeric in column E
        'remove_suffix': '',
        'convert_to_int': True
    },
    'bedrooms_cleaning': {
        'extract_pattern': r'^(\d+)'     # Extract first digit from codes like '3B4P'
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
        'C': {
            'display_name': 'Phase C',
            'description': 'Phase C development',
            'blocks': ['C1', 'C2']
        },
        'D': {
            'display_name': 'Phase D',
            'description': 'Phase D development',
            'blocks': ['D1', 'D2', 'D3']
        },
        'E': {
            'display_name': 'Phase E',
            'description': 'Phase E development',
            'blocks': ['E1', 'E2']
        }
    },
    
    # Block metadata - expected floors per block (for layout tracking)
    # These are the floors we expect to see in communal layouts
    # Ground (0) and roof floors are NOT included - only added if detected
    'blocks': {
        'C1': {
            'expected_floors': list(range(1, 13)),  # Floors 1-12
            'phase': 'C'
        },
        'C2': {
            'expected_floors': list(range(1, 10)),  # Floors 1-9
            'phase': 'C'
        },
        'D1': {
            'expected_floors': list(range(1, 9)),   # Floors 1-8 (ground excluded)
            'phase': 'D'
        },
        'D2': {
            'expected_floors': list(range(1, 8)),   # Floors 1-7 (ground excluded)
            'phase': 'D'
        },
        'D3': {
            'expected_floors': list(range(1, 7)),   # Floors 1-6 (ground excluded)
            'phase': 'D'
        },
        'E1': {
            'expected_floors': list(range(1, 7)),   # Floors 1-6 (ground excluded)
            'phase': 'E'
        },
        'E2': {
            'expected_floors': list(range(1, 7)),   # Floors 1-6 (ground excluded)
            'phase': 'E'
        }
    }
}

# ============================================================================
# CERTIFICATE TRACKING - Consolidated certificate configuration
# ============================================================================
# Set enabled=True and configure patterns when ready to track certificates
CERTIFICATE_TRACKING = {
    # Enable/disable certificate tracking and report generation
    'enabled': True,  # TODO: Enable when ready to track certificates
    'generate_report': True,
    
    # Document detection - which documents ARE certificates?
    'document_detection': {
        # File type filtering - match by File Type column
        'file_type_filter': {
            'enabled': True,
            'column_name': 'File Type',
            'certificate_types': ['CE - Certificate (CE)']
        },
        # Doc Ref filtering - match by patterns in Doc Ref
        'doc_ref_filter': {
            'enabled': True,
            'column_name': 'Doc Ref',
            'patterns': ['CE']  # 2-letter codes to match in Doc Ref
        },
        # Path filtering - distinguish apartment vs communal certificates
        'path_filter': {
            'enabled': True,
            # Include only certificates in block-specific folders (apartment certificates)
            'include_patterns': [
                r'\\Block\s*-\s*[CDE]\d\\',  # Match "\Block - C1\", "\Block-D2\", etc.
                r'\\Block\s*[CDE]\d\\',      # Alternative: "\BlockC1\", "\BlockD2\", etc.
            ],
            # Exclude certificates in landlord/communal folders
            'exclude_patterns': [
                r'\\Landlords\\',  # Landlord/communal certificates
                r'\\Communal\\',   # Communal areas
            ]
        }
    },
    
    # Metadata extraction - extract phase/block from document metadata
    'phase_detection': {
        'patterns': [r'Phase\s*([CDE])', r'\b([CDE])\d\b'],  # Match Phase C, D, E or C1, D2, E1, etc.
        'doc_title_patterns': [r'Plot\s+(\d+)'],  # Extract plot number from doc title
        'doc_ref_patterns': []
    },
    
    'block_detection': {
        'patterns': [
            r'\bBlock\s*-?\s*([CDE]\d)\b',  # Match "Block C1", "Block-C1", "Block C2", etc.
            r'\b([CDE]\d)\s+Block\b',       # Match "C1 Block", "D2 Block", etc.
            r'\\Block\s*-?\s*([CDE]\d)\\',  # Match in paths: "\Block-C1\", "\BlockC1\"
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
from configs.accommodation_data.HollowayPark import ACCOMMODATION_DATA

# ============================================================================
# APARTMENT LAYOUT TRACKING - Configuration for layout reports
# ============================================================================
# Set enabled=True and configure patterns when ready to track layouts
APARTMENT_LAYOUT_TRACKING = {
    'enabled': True,  # Enabled - will generate empty report until patterns are configured
    
    'detection': {
        'file_type_patterns': [],
        'doc_ref_patterns': ['DR', 'SM'], # Detect drawing and schematic files
        'path_patterns': [r'Trade_Contractor[/\\]Mechanical_\(Malcolm\)'],  # Filter by Mechanical folder path
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


# Custom status mapping for Holloway Park
# This project uses a dual-column status system:
# - Column F: 'Status' (can be 'Construction', 'IFC-pending', etc.)
# - Column I: 'Design Status' (can be 'B', 'C', or empty)
# Design Status takes precedence over Status when present

def map_holloway_park_status(row):
    """
    Custom status mapping for Holloway Park project.
    Checks both 'Status' (column F) and 'Design Status' (column I) columns.
    
    Priority Logic:
    1. Design Status takes precedence if present (B or C)
    2. If no Design Status, check Status column:
       - 'Construction' → 'Status A'
       - 'IFC-pending' → 'IFC-pending' (its own category)
       - 'Preliminary' → 'Other' (bundled with other statuses)
       - Everything else → 'Other'
    
    Returns:
        - 'Status B' if Design Status is 'B' (regardless of Status column)
        - 'Status C' if Design Status is 'C' (regardless of Status column)
        - 'Status A' if Status is 'Construction' and no Design Status
        - 'IFC-pending' if Status is 'IFC-pending' and no Design Status
        - 'Other' for all other combinations (Information, Tender, Preliminary, etc.)
    """
    # Get values from both status columns
    status_col_f = row.get('Status', '') if pd.notna(row.get('Status', '')) else ''
    design_status_col_i = row.get('Design Status', '') if pd.notna(row.get('Design Status', '')) else ''
    
    # Clean the values
    status_col_f = str(status_col_f).strip()
    design_status_col_i = str(design_status_col_i).strip()
    
    # Design Status takes precedence when present
    if design_status_col_i:
        if design_status_col_i.upper() == 'B':
            return 'Status B'
        elif design_status_col_i.upper() == 'C':
            return 'Status C'
        else:
            # Any other design status value
            return 'Other'
    
    # If no Design Status, check the Status column
    if status_col_f:
        if status_col_f.lower() == 'construction':
            return 'Status A'
        elif status_col_f.lower() == 'ifc-pending':
            return 'IFC-pending'  # Now its own category
        elif status_col_f.lower() == 'preliminary':
            return 'Other'  # Moved to Other category
        else:
            # Any other status value (Information, Tender, Contract, etc.)
            return 'Other'
    
    # If both columns are empty
    return 'Other'

# Legacy status mappings (kept for compatibility - not used by new system)
# Note: The new system uses the STATUS_MAPPINGS dictionary above with the custom mapping function
LEGACY_STATUS_MAPPINGS = {
    'Construction': 'Status A',
    'Preliminary': 'Other',  # Now bundled with Other
    'IFC-pending': 'IFC-pending',  # Now its own category
    'Information': 'Other', 
    'Tender': 'Other',
    'Contract': 'Other',
    'For-approval': 'Other'
}

# Revision cleaning function for Holloway Park
def clean_revision_hp(val):
    """Clean revision values for Holloway Park project"""
    if pd.isna(val):
        return ''
    s = str(val).replace('\u00A0', ' ').strip().upper()
    # Replace Cyrillic 'С' (U+0421) with Latin 'C'
    s = s.replace('\u0421', 'C')
    # Handle special cases like '-' or empty revisions
    if s == '-' or s == '':
        return '0'  # Convert to '0' for consistency
    return s

# Date format for Holloway Park (DD-MMM-YY format)
DATE_FORMAT = '%d-%b-%y'

# Timestamp extraction function for CSV files
def get_csv_timestamp(csv_file_path):
    """Extract timestamp from CSV file (first row, first column)"""
    try:
        # Read just the first few rows to get the timestamp
        df = pd.read_csv(csv_file_path, nrows=1)
        if 'Report Created' in df.columns and not df['Report Created'].isna().all():
            timestamp_str = df['Report Created'].iloc[0]
            if pd.notna(timestamp_str):
                # Parse the timestamp (format: "08-07-2025 07:03")
                from datetime import datetime
                try:
                    # Split by space to separate date and time
                    date_part, time_part = timestamp_str.split(' ')
                    # Parse date (DD-MM-YYYY format)
                    date_obj = datetime.strptime(date_part, '%d-%m-%Y')
                    # Parse time (HH:MM format)
                    time_obj = datetime.strptime(time_part, '%H:%M').time()
                    return date_obj, time_obj
                except Exception as e:
                    print(f"Warning: Could not parse timestamp '{timestamp_str}': {str(e)}")
                    return None, None
        return None, None
    except Exception as e:
        print(f"Error reading CSV timestamp: {str(e)}")
        return None, None

# Data filtering function for Holloway Park
def filter_holloway_park_data(df):
    """Filter data to only include MBS-related documents"""
    if not MBS_FILTER['enabled']:
        return df
    
    # Create filter mask for MBS entries
    filter_mask = pd.Series([False] * len(df), index=df.index)
    
    for column in MBS_FILTER['search_columns']:
        if column in df.columns:
            if MBS_FILTER['case_sensitive']:
                mask = df[column].str.contains('MBS', na=False)
            else:
                mask = df[column].str.contains('MBS', case=False, na=False)
            filter_mask = filter_mask | mask
    
    filtered_df = df[filter_mask].copy()
    print(f"Filtered {len(df)} total records to {len(filtered_df)} MBS records")
    
    return filtered_df

# Data transformation function for Holloway Park
def transform_holloway_park_data(df):
    """Transform CSV data to match expected format"""
    # Create a copy to avoid modifying original
    transformed_df = df.copy()
    
    # Apply column mappings
    for target_col, source_col in COLUMN_MAPPINGS.items():
        if source_col in transformed_df.columns:
            transformed_df[target_col] = transformed_df[source_col]
    
    # Clean revision column
    if 'Rev' in transformed_df.columns:
        transformed_df['Rev'] = transformed_df['Rev'].apply(clean_revision_hp)
    
    # Apply custom status mapping
    if 'Status' in transformed_df.columns or 'Design Status' in transformed_df.columns:
        # Apply the custom status mapping function to each row
        transformed_df['Status'] = transformed_df.apply(map_holloway_park_status, axis=1)
    
    # Convert date format if needed
    if 'Date' in transformed_df.columns:
        # The dates are already in a good format, just ensure consistency
        pass
    
    return transformed_df 