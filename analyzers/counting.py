"""Document counting and aggregation logic."""

import pandas as pd
from utils.data_cleaning import clean_revision


def get_counts(df, config=None):
    """Get counts of revisions and statuses from the dataframe.
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        
    Returns:
        dict: Dictionary of counts by revision, status, and file type
    """
    counts = {}
    
    try:
        # Clean the Rev column
        if 'Rev' in df.columns:
            df['Rev'] = df['Rev'].apply(clean_revision)
        
        # Check if certificate separation is enabled
        cert_config = config.get('CERTIFICATE_SETTINGS', {}) if config else {}
        cert_enabled = cert_config.get('enabled', False)
        file_type_col = None
        cert_types = []
        
        if cert_enabled and config:
            file_type_settings = config.get('FILE_TYPE_SETTINGS', {})
            file_type_col = file_type_settings.get('column_name')
            cert_types = cert_config.get('certificate_types', [])
        
        # Separate certificate and non-certificate data if enabled
        if cert_enabled and file_type_col and file_type_col in df.columns:
            cert_data = df[df[file_type_col].isin(cert_types)]
            non_cert_data = df[~df[file_type_col].isin(cert_types)]
        else:
            cert_data = pd.DataFrame()
            non_cert_data = df
        
        # Count revisions
        if cert_enabled and not cert_data.empty:
            # Count all revisions first
            all_rev_counts = df['Rev'].value_counts()
            cert_rev_counts = cert_data['Rev'].value_counts()
            
            # For each revision, separate certificates from non-certificates
            for rev, total_count in all_rev_counts.items():
                cert_count = cert_rev_counts.get(rev, 0)
                non_cert_count = total_count - cert_count
                
                # Add non-certificate count (this will be the regular P01, P02, etc.)
                if non_cert_count > 0:
                    counts[f'Rev_{rev}'] = non_cert_count
            
            # Add total certificate count for P revisions only
            p_cert_total = 0
            for rev, cert_count in cert_rev_counts.items():
                if rev.startswith('P') and cert_count > 0:
                    p_cert_total += cert_count
            
            if p_cert_total > 0:
                counts['Rev_P_Certificates'] = p_cert_total
        else:
            # Regular revision counting
            rev_counts = df['Rev'].value_counts()
            for rev, count in rev_counts.items():
                counts[f'Rev_{rev}'] = count
        
        # Count statuses
        if cert_enabled and not cert_data.empty:
            # Count non-certificate statuses only
            non_cert_status_counts = non_cert_data['Status'].value_counts()
            for status, count in non_cert_status_counts.items():
                counts[f'Status_{status}'] = count
            
            # Count certificate statuses with suffix (separate from regular statuses)
            cert_status_counts = cert_data['Status'].value_counts()
            cert_suffix = cert_config.get('status_suffix', ' (Certificates)')
            for status, count in cert_status_counts.items():
                counts[f'Status_{status}{cert_suffix}'] = count
        else:
            # Regular status counting
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

