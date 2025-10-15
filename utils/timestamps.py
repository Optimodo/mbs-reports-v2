"""Timestamp extraction utilities."""

import pandas as pd
import re
from datetime import datetime
from pathlib import Path


def get_file_timestamp(file_path):
    """Get the timestamp from cell B4 of the Excel file or from CSV file.
    
    Args:
        file_path: Path to Excel or CSV file
        
    Returns:
        tuple: (date_str, time_str) or (None, None) if parsing fails
    """
    try:
        file_path_str = str(file_path).lower()
        
        if file_path_str.endswith('.csv'):
            # For CSV files, try to get timestamp from 'Report Created' column first
            df = pd.read_csv(file_path, nrows=1)
            if 'Report Created' in df.columns and not df['Report Created'].isna().all():
                timestamp_str = df['Report Created'].iloc[0]
                if pd.notna(timestamp_str):
                    # Parse the timestamp (format: "08-07-2025 07:03")
                    try:
                        # Split by space to separate date and time
                        date_part, time_part = timestamp_str.split(' ')
                        # Parse date (DD-MM-YYYY format)
                        date_obj = datetime.strptime(date_part, '%d-%m-%Y')
                        time_obj = datetime.strptime(time_part, '%H:%M').time()
                        return date_obj.strftime('%d-%b-%Y'), time_obj.strftime('%H:%M')
                    except Exception as e:
                        print(f"Warning: Could not parse CSV timestamp '{timestamp_str}': {str(e)}")
                        return None, None
            
            # If no 'Report Created' column, try to extract date from filename
            # Format: "XX Document Listing DDMMYY.csv"
            filename = Path(file_path).name
            # Look for 6-digit date pattern (DDMMYY)
            date_match = re.search(r'(\d{6})(?:\.csv)?$', filename)
            if date_match:
                date_str = date_match.group(1)
                try:
                    # Parse DDMMYY format
                    date_obj = datetime.strptime(date_str, '%d%m%y')
                    # Default time to 12:00 for filename-based timestamps
                    return date_obj.strftime('%d-%b-%Y'), '12:00'
                except ValueError as e:
                    print(f"Warning: Could not parse date from filename '{filename}': {str(e)}")
                    return None, None
            
            print(f"Warning: Could not extract timestamp from CSV file or filename: {filename}")
            return None, None
        else:
            # Excel file - Read just cell B4 (which is merged from B to I)
            timestamp_df = pd.read_excel(file_path, usecols="B", nrows=4, header=None)
            timestamp_str = timestamp_df.iloc[3, 0]
            
            # Split by commas and get the third part (date and time)
            parts = timestamp_str.split(',')
            if len(parts) >= 3:
                date_time_part = parts[2].strip()
                # Split by space to separate date and time
                date_time = date_time_part.split()
                if len(date_time) >= 2:
                    date_str = date_time[0]  # Keep as text
                    time_str = date_time[1]  # Keep as text
                    return date_str, time_str
            
            print(f"Warning: Could not parse timestamp from {file_path.name}")
            return None, None
    except Exception as e:
        print(f"Error reading timestamp from {file_path.name}: {str(e)}")
        return None, None

