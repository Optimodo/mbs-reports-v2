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

# Certificate settings (not applicable for this project)
CERTIFICATE_SETTINGS = {
    'enabled': False
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
    'Preliminary': {
        'display_name': 'Preliminary',
        'color': '87CEEB',  # Light blue
        'statuses': [
            'Preliminary'
        ],
        'description': 'Preliminary documents'
    },
    'Other': {
        'display_name': 'Other',
        'color': 'D3D3D3',  # Light gray
        'statuses': [
            'Other'  # All unmapped statuses (Information, Tender, IFC-pending, etc.)
        ],
        'description': 'Information, Tender, IFC-pending, Contract, As-Built, Record, Planning, etc.'
    }
}

# Display order for progression reports
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'Preliminary',
    'Other'
]

# Custom status mapping for Holloway Park
# This project uses a dual-column status system:
# - Column F: 'Status' (can be 'Construction', 'IFC-pending', etc.)
# - Column I: 'Design Status' (can be 'B', 'C', or empty)
# Design Status takes precedence over Status when present

def map_holloway_park_status(row):
    """
    Custom status mapping for Holloway Park project.
    Checks both 'Status' (column F) and 'Design Status' (column I) columns.
    
    Returns:
        - 'Status A' if Status is 'Construction' and Design Status is empty
        - 'Status B' if Design Status is 'B'
        - 'Status C' if Design Status is 'C'
        - 'Preliminary' if Status is 'Preliminary' and Design Status is empty
        - 'Other' if Status is 'IFC-pending' and Design Status is empty
        - 'Other' for any other combinations
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
        elif status_col_f.lower() == 'preliminary':
            return 'Preliminary'
        elif status_col_f.lower() == 'ifc-pending':
            return 'Other'
        else:
            # Any other status value
            return 'Other'
    
    # If both columns are empty
    return 'Other'

# Status mappings for Holloway Park (legacy, kept for compatibility)
STATUS_MAPPINGS = {
    'Construction': 'Status A',
    'Preliminary': 'Preliminary',
    'IFC-pending': 'Other',
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