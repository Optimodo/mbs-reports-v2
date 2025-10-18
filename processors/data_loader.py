"""Data loading and processing for Excel and CSV files."""

import warnings
import pandas as pd
from pathlib import Path
from utils.data_cleaning import clean_revision

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)


def process_csv_file(file_path, config):
    """Process a CSV file and transform it to match expected format.
    
    Args:
        file_path: Path to CSV file
        config: Project configuration dictionary
        
    Returns:
        DataFrame: Processed dataframe
    """
    try:
        # Read the CSV file
        csv_settings = config.get('CSV_SETTINGS', {})
        df = pd.read_csv(file_path, **csv_settings)
        
        # Apply MBS filtering if enabled
        mbs_filter = config.get('MBS_FILTER')
        if mbs_filter and mbs_filter.get('enabled', False):
            filter_mask = pd.Series([False] * len(df), index=df.index)
            
            for column in mbs_filter.get('search_columns', []):
                if column in df.columns:
                    case_sensitive = mbs_filter.get('case_sensitive', False)
                    mask = df[column].str.contains('MBS', case=not case_sensitive, na=False)
                    filter_mask = filter_mask | mask
            
            df = df[filter_mask].copy()
            print(f"Filtered to {len(df)} MBS records")
        
        # Apply column mappings if provided
        column_mappings = config.get('COLUMN_MAPPINGS')
        if column_mappings:
            for target_col, source_col in column_mappings.items():
                if source_col in df.columns:
                    df[target_col] = df[source_col]
        
        # Apply custom status mapping for Holloway Park
        if config.get('PROJECT_TITLE') == 'Holloway Park':
            # Import the custom status mapping function
            try:
                from configs.HollowayPark import map_holloway_park_status
                if 'Status' in df.columns or 'Design Status' in df.columns:
                    # Apply the custom status mapping function to each row
                    df['Status'] = df.apply(map_holloway_park_status, axis=1)
                    print("Applied custom Holloway Park status mapping")
            except ImportError:
                print("Warning: Could not import Holloway Park status mapping function")
        
        # Clean revision column
        if 'Rev' in df.columns:
            df['Rev'] = df['Rev'].apply(clean_revision)
        
        return df
        
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
        raise


def load_document_listing(file_path, config):
    """Load a document listing file (Excel or CSV) based on file type.
    
    Args:
        file_path: Path to document listing file
        config: Project configuration dictionary
        
    Returns:
        DataFrame: Loaded and processed dataframe
    """
    file_path = Path(file_path)
    file_path_str = str(file_path).lower()
    
    # Skip temporary Excel files
    if file_path.name.startswith('~$'):
        print(f"Skipping temporary file: {file_path.name}")
        return None
    
    try:
        if file_path_str.endswith('.csv'):
            # Process CSV file (clean_revision already called in process_csv_file)
            df = process_csv_file(file_path, config)
        else:
            # Process Excel file
            excel_settings = config.get('EXCEL_SETTINGS', {})
            df = pd.read_excel(file_path, **excel_settings)
            
            # Apply column mappings if provided (same as CSV processing)
            column_mappings = config.get('COLUMN_MAPPINGS')
            if column_mappings:
                for target_col, source_col in column_mappings.items():
                    if source_col in df.columns:
                        df[target_col] = df[source_col]
            
            # Clean revision column for Excel files (CSV already cleaned in process_csv_file)
            if 'Rev' in df.columns:
                df['Rev'] = df['Rev'].apply(clean_revision)
        
        # Convert all columns to string for consistency
        # IMPORTANT: This must happen AFTER clean_revision to avoid converting 'nan' to string 'nan'
        for col in df.columns:
            try:
                df[col] = df[col].astype(str)
            except Exception as e:
                print(f"Warning: Error converting column '{col}' to string: {str(e)}")
        
        return df
        
    except Exception as e:
        print(f"Error loading document listing from {file_path.name}: {str(e)}")
        raise

