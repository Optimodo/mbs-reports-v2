"""Data comparison and change detection logic."""

import pandas as pd


def compare_values(current_val, prev_val, col_name):
    """Compare values and return True if they are actually different.
    
    Args:
        current_val: Current value
        prev_val: Previous value
        col_name: Column name (used for special handling of date fields)
        
    Returns:
        bool: True if values are different, False otherwise
    """
    # Convert both values to strings, handling NaN/None
    current_str = str(current_val).strip() if pd.notna(current_val) else ''
    prev_str = str(prev_val).strip() if pd.notna(prev_val) else ''
    
    # If both are empty, no change
    if not current_str and not prev_str:
        return False
    
    # If one is empty and the other isn't, that's a change
    if not current_str or not prev_str:
        return True
    
    # For date fields, normalize the format
    if 'Date' in col_name or 'WET' in col_name:
        try:
            # Try to parse and normalize the dates
            current_date = pd.to_datetime(current_str)
            prev_date = pd.to_datetime(prev_str)
            # Compare the normalized date strings
            current_str = current_date.strftime('%d-%b-%Y')
            prev_str = prev_date.strftime('%d-%b-%Y')
        except:
            # If date parsing fails, use the original strings
            pass
    
    # Compare the normalized strings
    return current_str != prev_str

