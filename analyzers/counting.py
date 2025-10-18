"""Document counting and aggregation logic."""

import warnings
import pandas as pd
from utils.data_cleaning import clean_revision
from utils.document_filters import (
    filter_certificates,
    filter_technical_submittals,
    get_main_report_data
)

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)


def get_counts(df, config=None, report_type='main'):
    """Get counts of revisions and statuses from the dataframe.
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        report_type: Type of report to generate counts for ('main', 'certificate', 'technical_submittal', 'all')
        
    Returns:
        dict: Dictionary of counts by revision, status, and file type
    """
    counts = {}
    
    try:
        # Clean the Rev column
        if 'Rev' in df.columns:
            df['Rev'] = df['Rev'].apply(clean_revision)
        
        # Filter data based on report type
        if report_type == 'main':
            # Main report: exclude certificates and technical submittals
            filtered_df = get_main_report_data(df, config) if config else df
        elif report_type == 'certificate':
            # Certificate report: only certificates
            filtered_df = filter_certificates(df, config) if config else pd.DataFrame()
        elif report_type == 'technical_submittal':
            # Technical submittal report: only technical submittals
            filtered_df = filter_technical_submittals(df, config) if config else pd.DataFrame()
        else:  # 'all'
            # All documents (used for backwards compatibility)
            filtered_df = df
        
        # If filtered_df is empty, return empty counts
        if filtered_df.empty:
            return counts
        
        # Use filtered_df for all subsequent counting
        df = filtered_df
        
        # Count revisions (simple counting - filtering already done)
        rev_counts = df['Rev'].value_counts()
        for rev, count in rev_counts.items():
            counts[f'Rev_{rev}'] = count
        
        # Count statuses - use STATUS_MAPPINGS if available to group statuses
        if config and 'STATUS_MAPPINGS' in config:
            # Use project-specific status mappings
            status_mappings = config['STATUS_MAPPINGS']
            
            # Initialize category counts
            grouped_status_counts = {}
            for category in status_mappings.keys():
                grouped_status_counts[category] = 0
            
            # Count all statuses with grouping (filtering already done upstream)
            for status_value in df['Status']:
                # Find which category this status belongs to
                categorized = False
                for category, mapping in status_mappings.items():
                    if status_value in mapping.get('statuses', []):
                        grouped_status_counts[category] += 1
                        categorized = True
                        break
                
                # If not categorized and 'Other' exists, add to Other
                if not categorized and 'Other' in grouped_status_counts:
                    grouped_status_counts['Other'] += 1
            
            # Add grouped counts to main counts dictionary
            for category, count in grouped_status_counts.items():
                if count > 0:  # Only add non-zero counts
                    counts[f'Status_{category}'] = count
        else:
            # Fallback: Regular status counting without grouping (legacy behavior)
            status_counts = df['Status'].value_counts()
            for status, count in status_counts.items():
                counts[f'Status_{status}'] = count
        
        # Count file types if the column exists
        if 'OVL - File Type' in df.columns:
            file_type_counts = df['OVL - File Type'].value_counts()
            for file_type, count in file_type_counts.items():
                counts[f'FileType_{file_type}'] = count
        elif 'Form' in df.columns:
            file_type_counts = df['Form'].value_counts()
            for file_type, count in file_type_counts.items():
                counts[f'FileType_{file_type}'] = count
        elif 'File Type' in df.columns:
            file_type_counts = df['File Type'].value_counts()
            for file_type, count in file_type_counts.items():
                counts[f'FileType_{file_type}'] = count
        
        return counts
    except Exception as e:
        print(f"Error in get_counts: {str(e)}")
        print("DataFrame columns:", df.columns.tolist())
        print("DataFrame head:")
        print(df.head())
        raise

