"""Dynamic counting for report generation - calculates counts on-the-fly from filtered data."""

import pandas as pd
from utils.data_cleaning import clean_revision
from utils.status_mapping import get_grouped_status_counts


def get_dynamic_counts(df, config):
    """
    Calculate counts dynamically from a filtered dataset.
    
    This function replaces the need to query summary tables from the database.
    Instead, it takes filtered data (e.g., only drawings) and calculates counts fresh.
    
    Args:
        df: Filtered DataFrame (e.g., only drawings, or only certificates)
        config: Project configuration
        
    Returns:
        dict: Three datasets in the format that reports expect:
            - 'revision_counts': {Rev_P01: 50, Rev_P02: 30, ...}
            - 'status_counts': {Status_A: 100, Status_B: 20, ...}
            - 'file_type_counts': {FileType_DR: 80, FileType_SH: 20, ...}
    """
    if df.empty:
        return {
            'revision_counts': {},
            'status_counts': {},
            'file_type_counts': {}
        }
    
    # Clean revisions
    if 'Rev' in df.columns:
        df = df.copy()  # Don't modify original
        df['Rev'] = df['Rev'].apply(clean_revision)
    
    # 1. Count revisions
    revision_counts = {}
    if 'Rev' in df.columns:
        rev_value_counts = df['Rev'].value_counts()
        for rev, count in rev_value_counts.items():
            revision_counts[f'Rev_{rev}'] = int(count)
    
    # 2. Count statuses (with grouping from STATUS_MAPPINGS)
    status_counts = {}
    if 'Status' in df.columns:
        if config and 'STATUS_MAPPINGS' in config:
            # Use project-specific status mappings to group statuses
            grouped_counts = get_grouped_status_counts(df['Status'], config)
            for category, count in grouped_counts.items():
                if count > 0:
                    status_counts[f'Status_{category}'] = int(count)
        else:
            # Fallback: count raw status values
            status_value_counts = df['Status'].value_counts()
            for status, count in status_value_counts.items():
                status_counts[f'Status_{status}'] = int(count)
    
    # 3. Count file types
    file_type_counts = {}
    
    # Try different file type column names
    file_type_col = None
    if 'File Type' in df.columns:
        file_type_col = 'File Type'
    elif 'OVL - File Type' in df.columns:
        file_type_col = 'OVL - File Type'
    elif 'Form' in df.columns:
        file_type_col = 'Form'
    
    if file_type_col:
        ft_value_counts = df[file_type_col].value_counts()
        for file_type, count in ft_value_counts.items():
            if pd.notna(file_type):
                file_type_counts[f'FileType_{file_type}'] = int(count)
    
    return {
        'revision_counts': revision_counts,
        'status_counts': status_counts,
        'file_type_counts': file_type_counts
    }


def create_summary_row(date, time, df, config):
    """
    Create a single summary row for a snapshot (mimics database summary table row).
    
    This is what reports expect - a row with Date, Time, and all the counts.
    
    Args:
        date: Date string (DD-MMM-YYYY format)
        time: Time string (HH:MM format)
        df: Filtered DataFrame for this snapshot
        config: Project configuration
        
    Returns:
        dict: Summary row with all counts (ready to add to DataFrame)
    """
    counts_dict = get_dynamic_counts(df, config)
    
    # Combine all counts into a single row
    row = {
        'Date': date,
        'Time': time
    }
    
    # Add all revision counts
    row.update(counts_dict['revision_counts'])
    
    # Add all status counts
    row.update(counts_dict['status_counts'])
    
    # Add all file type counts
    row.update(counts_dict['file_type_counts'])
    
    return row


def create_summary_dataframe(snapshots_data, config):
    """
    Create a summary DataFrame from multiple snapshots (mimics database summary query).
    
    This replaces db.get_summary_dataframe() with dynamic calculation.
    
    Args:
        snapshots_data: List of tuples: [(date, time, df), (date, time, df), ...]
        config: Project configuration
        
    Returns:
        pd.DataFrame: Summary data with Date, Time, and all counts per snapshot
    """
    summary_rows = []
    
    for date, time, df in snapshots_data:
        row = create_summary_row(date, time, df, config)
        summary_rows.append(row)
    
    if not summary_rows:
        return pd.DataFrame()
    
    summary_df = pd.DataFrame(summary_rows)
    
    # Ensure Date and Time are first columns
    cols = ['Date', 'Time'] + [c for c in summary_df.columns if c not in ['Date', 'Time']]
    summary_df = summary_df[cols]
    
    # Fill NaN with 0 (for revisions/statuses that don't exist in some snapshots)
    summary_df = summary_df.fillna(0)
    
    return summary_df


