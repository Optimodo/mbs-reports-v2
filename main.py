import os
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
from config import *
import re
import time
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import openpyxl.styles
import argparse
from openpyxl.worksheet.page import PageMargins

# Overall Summary Sheet Style Configuration
OVERALL_SUMMARY_STYLES = {
    'title': {
        'font': Font(name='Calibri', size=14, bold=True, color='000000'),
        'alignment': Alignment(horizontal='left', vertical='center'),
        'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    },
    'timestamp': {
        'font': Font(name='Calibri', size=11, italic=True, color='000000'),
        'alignment': Alignment(horizontal='left', vertical='center'),
        'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    },
    'section_header': {
        'font': Font(name='Calibri', size=12, bold=True, color='000000'),
        'alignment': Alignment(horizontal='left', vertical='center'),
        'fill': PatternFill(start_color='F0F0F0', end_color='F0F0F0', fill_type='solid')
    },
    'column_header': {
        'font': Font(name='Calibri', size=11, bold=True, color='000000'),
        'alignment': Alignment(horizontal='left', vertical='center'),
        'fill': PatternFill(start_color='E6E6E6', end_color='E6E6E6', fill_type='solid')
    },
    'data_cell': {
        'font': Font(name='Calibri', size=11, color='000000'),
        'alignment': Alignment(horizontal='left', vertical='center'),
        'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    },
    'total_cell': {
        'font': Font(name='Calibri', size=11, bold=True, color='000000'),
        'alignment': Alignment(horizontal='left', vertical='center'),
        'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    },
    'border': Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
}

# Status-based conditional formatting
STATUS_STYLES = {
    'STATUS A': {
        'search_terms': ['A - Authorized and Accepted', 'Accepted', 'A', 'A - Proceed', 'A - Proceed (Lead Reviewer)'],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='25E82C', end_color='25E82C', fill_type='solid')
        }
    },
    'STATUS B': {
        'search_terms': ['B - Partial Sign Off (with comment)', 'Accepted with Comments', 'B', 'B - Proceed with Comments', 'B - Proceed with Comments (Lead Reviewer)'],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='EDDDA1', end_color='EDDDA1', fill_type='solid')
        }
    },
    'STATUS C': {
        'search_terms': ['Rejected', 'QA - Rejected', 'C - Rejected', 'QA Rejected', 'C', 'C - Rejected (Lead Reviewer)', 'C-Rejected',],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='ED1111', end_color='ED1111', fill_type='solid')
        }
    },
    'INFORMATION': {
        'search_terms': ['Information', 'Withdrawn-Obsolete', 'QA Passed', 'QA - Passed', 'For Status Change', 'For Commenting', 'Awaiting QC Check', 'QC Accepted', 'QC Checked', 'Under Review'],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        }
    },
    'REVIEWED': {
        'search_terms': ['Reviewed'],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        }
    },
    'PUBLISHED': {
        'search_terms': ['Published'],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='67DBB5', end_color='67DBB5', fill_type='solid')
        }
    },
    'SHARED': {
        'search_terms': ['Shared'],
        'style': {
            'font': Font(name='Calibri', size=11, bold=True, color='000000'),
            'fill': PatternFill(start_color='E0F090', end_color='E0F090', fill_type='solid')
        }
    },
    # 'SUBMITTED': {
    #     'search_terms': ['H - Submitted', 'H - For Review'],
    #     'style': {
    #         'font': Font(name='Calibri', size=11, bold=True, color='000000'),
    #         'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    #     }
    # },
    # 'COMPLETED': {
    #     'search_terms': ['I - Completed', 'I - Final'],
    #     'style': {
    #         'font': Font(name='Calibri', size=11, bold=True, color='000000'),
    #         'fill': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    #     }
    # }
}

def apply_status_style(cell, status_name):
    """Apply conditional formatting based on status name"""
    for style_config in STATUS_STYLES.values():
        if any(term == status_name for term in style_config['search_terms']):
            cell.font = style_config['style']['font']
            cell.fill = style_config['style']['fill']
            return style_config['style']  # Return the style config for reuse
    # If no matching style found, use default data cell style
    cell.font = OVERALL_SUMMARY_STYLES['data_cell']['font']
    cell.fill = OVERALL_SUMMARY_STYLES['data_cell']['fill']
    return OVERALL_SUMMARY_STYLES['data_cell']  # Return default style

# Example of how to use these styles in the code:
# cell = overall_summary['A1']
# cell.font = OVERALL_SUMMARY_STYLES['title']['font']
# cell.alignment = OVERALL_SUMMARY_STYLES['title']['alignment']
# cell.fill = OVERALL_SUMMARY_STYLES['title']['fill']
# cell.border = OVERALL_SUMMARY_STYLES['border']

class DocumentRegisterProcessor:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.reports_dir = REPORTS_DIR
        self.history_file = self.data_dir / "file_history.json"
        self.load_history()
        self.latest_changes = {}  # Store the latest changes

    def load_history(self):
        """Load the file processing history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {}

    def save_history(self):
        """Save the file processing history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def process_excel_file(self, file_path):
        """Process a single Excel file and track changes"""
        # Skip temporary Excel files
        if file_path.name.startswith('~$'):
            print(f"Skipping temporary file: {file_path.name}")
            return None

        file_name = file_path.name
        current_hash = self._get_file_hash(file_path)
        
        try:
            # Read the Excel file
            df = pd.read_excel(file_path, **EXCEL_SETTINGS)
            
            # Get the timestamp from cell B4
            timestamp_df = pd.read_excel(file_path, usecols="B", nrows=4, header=None)
            timestamp_str = timestamp_df.iloc[3, 0]  # Get value from B4
            
            # Extract the date and time from the timestamp string
            try:
                # Split by commas and get the third part (date and time)
                parts = timestamp_str.split(',')
                if len(parts) >= 3:
                    date_time_part = parts[2].strip()
                    # Split by space to separate date and time
                    date_time = date_time_part.split()
                    if len(date_time) >= 2:
                        file_date = datetime.strptime(date_time[0], '%d-%b-%Y')
                        file_time = datetime.strptime(date_time[1], '%H:%M').time()
                    else:
                        print(f"Warning: Could not parse date/time from {file_name}")
                        file_date = datetime.min
                else:
                    print(f"Warning: Could not parse timestamp in {file_name}")
                    file_date = datetime.min
            except Exception as e:
                print(f"Warning: Error parsing date from {file_name}: {str(e)}")
                file_date = datetime.min
            
            # Save the processed data with timestamp
            self._save_processed_data(file_name, df, file_date)
            
            # Check if we have previous version
            if file_name in self.history:
                old_hash = self.history[file_name]['hash']
                if old_hash != current_hash:
                    changes = self._detect_changes(df, file_name)
                    self._update_history(file_name, current_hash, changes)
                    self.latest_changes[file_name] = changes  # Store the changes
                    return changes
            else:
                # First time processing this file
                self._update_history(file_name, current_hash, {'new_file': True})
                self.latest_changes[file_name] = {'new_file': True}
                return {'new_file': True}
                
        except Exception as e:
            print(f"Error processing file {file_name}: {str(e)}")
            return None

    def _save_processed_data(self, file_name, df, file_date):
        """Save the processed data for later use"""
        data_file = self.data_dir / f"{file_name}.parquet"
        # Save the dataframe with the file date as metadata
        df.to_parquet(data_file, engine='pyarrow')
        # Save the date separately
        date_file = self.data_dir / f"{file_name}.date"
        with open(date_file, 'w') as f:
            f.write(file_date.isoformat())

    def _get_file_hash(self, file_path):
        """Get a simple hash of the file for change detection"""
        return str(os.path.getmtime(file_path))

    def _detect_changes(self, current_df, file_name):
        """Detect changes between current and previous version"""
        try:
            # Load previous version
            prev_data_file = self.data_dir / f"{file_name}.parquet"
            if not prev_data_file.exists():
                return {'new_file': True}
            
            prev_df = pd.read_parquet(prev_data_file)
            
            # Find documents that exist in both versions
            common_docs = set(current_df['Doc Ref']).intersection(set(prev_df['Doc Ref']))
            
            changes = {
                'status_changes': [],
                'revision_changes': [],
                'date_changes': [],
                'new_documents': [],
                'removed_documents': []
            }
            
            # Check for new and removed documents
            current_docs = set(current_df['Doc Ref'])
            prev_docs = set(prev_df['Doc Ref'])
            
            changes['new_documents'] = list(current_docs - prev_docs)
            changes['removed_documents'] = list(prev_docs - current_docs)
            
            # Check for changes in existing documents
            for doc_ref in common_docs:
                current_doc = current_df[current_df['Doc Ref'] == doc_ref].iloc[0]
                prev_doc = prev_df[prev_df['Doc Ref'] == doc_ref].iloc[0]
                
                # Check status changes
                if current_doc['Status'] != prev_doc['Status']:
                    changes['status_changes'].append({
                        'doc_ref': doc_ref,
                        'doc_title': current_doc['Doc Title'],
                        'old_status': prev_doc['Status'],
                        'new_status': current_doc['Status']
                    })
                
                # Check revision changes
                if current_doc['Rev'] != prev_doc['Rev']:
                    changes['revision_changes'].append({
                        'doc_ref': doc_ref,
                        'doc_title': current_doc['Doc Title'],
                        'old_rev': prev_doc['Rev'],
                        'new_rev': current_doc['Rev']
                    })
                
                # Check date changes
                if current_doc['Date (WET)'] != prev_doc['Date (WET)']:
                    changes['date_changes'].append({
                        'doc_ref': doc_ref,
                        'doc_title': current_doc['Doc Title'],
                        'old_date': prev_doc['Date (WET)'],
                        'new_date': current_doc['Date (WET)']
                    })
            
            return changes
            
        except Exception as e:
            print(f"Error detecting changes: {str(e)}")
            return {'error': str(e)}

    def _update_history(self, file_name, file_hash, changes):
        """Update the processing history"""
        self.history[file_name] = {
            'last_processed': datetime.now().isoformat(),
            'hash': file_hash,
            'changes': changes
        }
        self.save_history()

def get_file_timestamp(file_path):
    """Get the timestamp from cell B4 of the Excel file"""
    try:
        # Read just cell B4 (which is merged from B to I)
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

def clean_revision(val):
    if pd.isna(val):
        return ''
    s = str(val).replace('\u00A0', ' ').strip().upper()
    # Replace Cyrillic 'С' (U+0421) with Latin 'C'
    s = s.replace('\u0421', 'C')
    return s

def get_counts(df):
    """Get counts of revisions and statuses from the dataframe"""
    counts = {}
    
    try:
        # Clean the Rev column
        if 'Rev' in df.columns:
            df['Rev'] = df['Rev'].apply(clean_revision)
        # Count revisions
        rev_counts = df['Rev'].value_counts()
        for rev, count in rev_counts.items():
            counts[f'Rev_{rev}'] = count
        
        # Count statuses
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

def load_processed_files():
    """Load the record of processed files"""
    try:
        with open('processed_files.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_processed_files(processed_files):
    """Save the record of processed files"""
    with open('processed_files.json', 'w') as f:
        json.dump(processed_files, f, indent=2, default=str)

def compare_values(current_val, prev_val, col_name):
    """Compare values and return True if they are actually different"""
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

def save_excel_with_retry(summary_df, changes_df, latest_data_df, output_file, config, max_retries=3):
    """Try to save the Excel file with retries"""
    for attempt in range(max_retries):
        try:
            # Try to load existing file
            try:
                book = load_workbook(output_file)
                
                # Remove existing Changes sheet if it exists
                if 'Changes' in book.sheetnames:
                    book.remove(book['Changes'])
                
                # Read existing summary data if it exists
                existing_summary = None
                if 'Summary Data' in book.sheetnames:
                    existing_summary = pd.read_excel(output_file, sheet_name='Summary Data')
                    # Remove the sheet as we'll recreate it with appended data
                    book.remove(book['Summary Data'])
                
                with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    # Append new changes to changes sheet
                    changes_df.to_excel(writer, sheet_name='Changes', index=False)
                    
                    # If we have existing summary data, append new data to it
                    if existing_summary is not None:
                        combined_summary = pd.concat([existing_summary, summary_df], ignore_index=True)
                        combined_summary.to_excel(writer, sheet_name='Summary Data', index=False)
                    else:
                        summary_df.to_excel(writer, sheet_name='Summary Data', index=False)
                    
                    # Update latest data sheet
                    latest_data_df.to_excel(writer, sheet_name='Latest Data', index=False)
            except FileNotFoundError:
                # If file doesn't exist, create new one
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    changes_df.to_excel(writer, sheet_name='Changes', index=False)
                    summary_df.to_excel(writer, sheet_name='Summary Data', index=False)
                    latest_data_df.to_excel(writer, sheet_name='Latest Data', index=False)
            
            # Add highlighting to changes
            book = load_workbook(output_file)
            changes_sheet = book['Changes']
            yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
            
            # Highlight cells where data has changed
            for row in changes_sheet.iter_rows(min_row=2):  # Skip header
                change_details = row[-1].value  # Last column is Change Details
                if change_details and '→' in str(change_details):
                    # Split the change details to get the column names that changed
                    changes = str(change_details).split('; ')
                    for change in changes:
                        if '→' in change:
                            col_name = change.split(':')[0].strip()
                            # Find the column index for this column name
                            for idx, cell in enumerate(changes_sheet[1]):  # Header row
                                if cell.value == col_name:
                                    # Highlight the changed cell
                                    row[idx].fill = yellow_fill
            
            # Auto-adjust column widths for all sheets
            for sheet_name in ['Summary Data', 'Changes', 'Latest Data']:
                sheet = book[sheet_name]
                for column in sheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    sheet.column_dimensions[column_letter].width = adjusted_width
            
            # Create or update Overall Summary sheet first
            if 'Overall Summary' in book.sheetnames:
                book.remove(book['Overall Summary'])
            overall_summary = book.create_sheet('Overall Summary', 0)  # Create at index 0 (first position)

            # Set print layout: fit to 1 page, center, narrow margins
            overall_summary.page_setup.fitToWidth = 1
            overall_summary.page_setup.fitToHeight = 0
            overall_summary.page_setup.horizontalCentered = True
            overall_summary.page_setup.verticalCentered = True
            overall_summary.page_margins = PageMargins(left=0.25, right=0.25, top=0.75, bottom=0.75, header=0.3, footer=0.3)
            # Extra reliability for centering
            overall_summary.sheet_properties.pageSetUpPr.horizontalCentered = True
            overall_summary.sheet_properties.pageSetUpPr.verticalCentered = True
            
            # Add title
            overall_summary['A1'] = 'Document Register Overall Summary'
            overall_summary['A1'].font = OVERALL_SUMMARY_STYLES['title']['font']
            overall_summary['A1'].alignment = OVERALL_SUMMARY_STYLES['title']['alignment']
            overall_summary['A1'].fill = OVERALL_SUMMARY_STYLES['title']['fill']
            overall_summary['A1'].border = OVERALL_SUMMARY_STYLES['border']
            
            # Get the latest data from Summary Data
            summary_data = pd.read_excel(output_file, sheet_name='Summary Data')
            latest_row = summary_data.iloc[-1]  # Get the last row
            
            # Add data export timestamp from Summary Data (now in row 2)
            export_date = latest_row['Date'].strftime("%d-%m-%Y") if isinstance(latest_row['Date'], datetime) else latest_row['Date']
            export_time = latest_row['Time'].strftime("%H-%M-%S") if isinstance(latest_row['Time'], datetime) else latest_row['Time']
            overall_summary['A2'] = f'Data Export: {export_date} {export_time}'
            overall_summary['A2'].font = OVERALL_SUMMARY_STYLES['timestamp']['font']
            overall_summary['A2'].alignment = OVERALL_SUMMARY_STYLES['timestamp']['alignment']
            overall_summary['A2'].fill = OVERALL_SUMMARY_STYLES['timestamp']['fill']
            
            # Get all column names from Summary Data
            all_columns = summary_data.columns.tolist()
            
            # Add total documents
            overall_summary['A5'] = 'Total Documents:'
            # Get total from Latest Data sheet
            latest_data = pd.read_excel(output_file, sheet_name='Latest Data')
            total_docs = len(latest_data)  # len() already gives us the correct count
            overall_summary['B5'] = total_docs
            overall_summary['B5'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
            overall_summary['B5'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
            overall_summary['B5'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
            
            # Filter and sort revision columns
            rev_columns = [col for col in all_columns if col.startswith('Rev_')]
            
            # Group revisions by type
            p_revs = sorted([col for col in rev_columns if col.startswith('Rev_P')], 
                          key=lambda x: int(x.split('_')[1][1:]) if x.split('_')[1][1:].isdigit() else float('inf'))
            c_revs = sorted([col for col in rev_columns if col.startswith('Rev_C')],
                          key=lambda x: int(x.split('_')[1][1:]) if x.split('_')[1][1:].isdigit() else float('inf'))
            other_revs = sorted([col for col in rev_columns if not (col.startswith('Rev_P') or col.startswith('Rev_C'))])
            
            # Function to add revision and status summary
            def add_revision_summary(start_row, rev_columns, title):
                """Add a revision summary section with a combined status summary"""
                # Add section header
                overall_summary[f'A{start_row}'] = title
                overall_summary[f'A{start_row}'].font = OVERALL_SUMMARY_STYLES['section_header']['font']
                overall_summary[f'A{start_row}'].alignment = OVERALL_SUMMARY_STYLES['section_header']['alignment']
                overall_summary[f'A{start_row}'].fill = OVERALL_SUMMARY_STYLES['section_header']['fill']
                
                # Add revision headers
                overall_summary[f'A{start_row + 1}'] = 'Revision'
                overall_summary[f'B{start_row + 1}'] = 'Count'
                overall_summary[f'C{start_row + 1}'] = 'Status'
                overall_summary[f'D{start_row + 1}'] = 'Count'
                
                # Style headers
                for col in ['A', 'B', 'C', 'D']:
                    overall_summary[f'{col}{start_row + 1}'].font = OVERALL_SUMMARY_STYLES['column_header']['font']
                    overall_summary[f'{col}{start_row + 1}'].alignment = OVERALL_SUMMARY_STYLES['column_header']['alignment']
                    overall_summary[f'{col}{start_row + 1}'].fill = OVERALL_SUMMARY_STYLES['column_header']['fill']
                    overall_summary[f'{col}{start_row + 1}'].border = OVERALL_SUMMARY_STYLES['border']
                
                # Get status counts for all revisions in this group
                status_counts = {}
                total_count = 0
                
                for rev_col in rev_columns:
                    rev_name = rev_col.replace('Rev_', '')
                    count = latest_row.get(rev_col, 0)
                    total_count += count
                    
                    # Filter latest data for this revision
                    rev_data = latest_data[latest_data['Rev'] == rev_name]
                    # Count statuses
                    for status, count in rev_data['Status'].value_counts().items():
                        status_counts[status] = status_counts.get(status, 0) + count
                
                # Add revision data
                row = start_row + 2
                for rev_col in rev_columns:
                    rev_name = rev_col.replace('Rev_', '')
                    count = latest_row.get(rev_col, 0)
                    
                    # Add revision name and count
                    overall_summary[f'A{row}'] = rev_name
                    overall_summary[f'B{row}'] = count
                    overall_summary[f'A{row}'].font = OVERALL_SUMMARY_STYLES['data_cell']['font']
                    overall_summary[f'A{row}'].alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
                    overall_summary[f'A{row}'].fill = OVERALL_SUMMARY_STYLES['data_cell']['fill']
                    overall_summary[f'A{row}'].border = OVERALL_SUMMARY_STYLES['border']
                    overall_summary[f'B{row}'].font = OVERALL_SUMMARY_STYLES['data_cell']['font']
                    overall_summary[f'B{row}'].alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
                    overall_summary[f'B{row}'].fill = OVERALL_SUMMARY_STYLES['data_cell']['fill']
                    overall_summary[f'B{row}'].border = OVERALL_SUMMARY_STYLES['border']
                    row += 1
                
                # Add total row for revisions
                overall_summary[f'A{row}'] = 'Total'
                overall_summary[f'B{row}'] = total_count
                overall_summary[f'A{row}'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
                overall_summary[f'A{row}'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
                overall_summary[f'A{row}'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
                overall_summary[f'A{row}'].border = OVERALL_SUMMARY_STYLES['border']
                overall_summary[f'B{row}'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
                overall_summary[f'B{row}'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
                overall_summary[f'B{row}'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
                overall_summary[f'B{row}'].border = OVERALL_SUMMARY_STYLES['border']
                
                # Add status summary
                status_row = start_row + 2
                total_status_count = 0
                for status, count in sorted(status_counts.items()):
                    total_status_count += count
                    
                    # Add status name with conditional formatting
                    status_cell = overall_summary[f'C{status_row}']
                    status_cell.value = status
                    style = apply_status_style(status_cell, status)
                    status_cell.alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
                    status_cell.border = OVERALL_SUMMARY_STYLES['border']
                    
                    # Add count with matching style
                    count_cell = overall_summary[f'D{status_row}']
                    count_cell.value = count
                    count_cell.font = Font(
                        name=style['font'].name,
                        size=style['font'].size,
                        bold=style['font'].bold,
                        italic=style['font'].italic,
                        color=style['font'].color
                    )
                    count_cell.fill = style['fill']
                    count_cell.alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
                    count_cell.border = OVERALL_SUMMARY_STYLES['border']
                    
                    status_row += 1
                
                # Add total row for status counts
                overall_summary[f'C{status_row}'] = 'Total'
                overall_summary[f'D{status_row}'] = total_status_count
                overall_summary[f'C{status_row}'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
                overall_summary[f'C{status_row}'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
                overall_summary[f'C{status_row}'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
                overall_summary[f'C{status_row}'].border = OVERALL_SUMMARY_STYLES['border']
                overall_summary[f'D{status_row}'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
                overall_summary[f'D{status_row}'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
                overall_summary[f'D{status_row}'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
                overall_summary[f'D{status_row}'].border = OVERALL_SUMMARY_STYLES['border']
                
                return max(row, status_row) + 2  # Return the next row to start from
            
            # Add P revision summary
            current_row = 7
            current_row = add_revision_summary(current_row, p_revs, 'P Revision Summary')
            
            # Add C revision summary
            current_row = add_revision_summary(current_row, c_revs, 'C Revision Summary')
            
            # Add other revision summary
            current_row = add_revision_summary(current_row, other_revs, 'Other Revision Summary')
            
            # Add file type summary section if enabled in config
            if config.get('FILE_TYPE_SETTINGS', {}).get('include_in_summary', False):
                file_type_col = config['FILE_TYPE_SETTINGS']['column_name']
                if file_type_col in latest_data.columns:
                    # Add file type summary section
                    file_type_start_row = current_row + 2
                    overall_summary[f'A{file_type_start_row}'] = config['FILE_TYPE_SETTINGS']['summary_title']
                    overall_summary[f'A{file_type_start_row}'].font = OVERALL_SUMMARY_STYLES['section_header']['font']
                    overall_summary[f'A{file_type_start_row}'].alignment = OVERALL_SUMMARY_STYLES['section_header']['alignment']
                    overall_summary[f'A{file_type_start_row}'].fill = OVERALL_SUMMARY_STYLES['section_header']['fill']
                    
                    # Add file type headers
                    overall_summary[f'A{file_type_start_row + 1}'] = 'File Type'
                    overall_summary[f'B{file_type_start_row + 1}'] = 'Count'
                    overall_summary[f'A{file_type_start_row + 1}'].font = OVERALL_SUMMARY_STYLES['column_header']['font']
                    overall_summary[f'A{file_type_start_row + 1}'].alignment = OVERALL_SUMMARY_STYLES['column_header']['alignment']
                    overall_summary[f'A{file_type_start_row + 1}'].fill = OVERALL_SUMMARY_STYLES['column_header']['fill']
                    overall_summary[f'B{file_type_start_row + 1}'].font = OVERALL_SUMMARY_STYLES['column_header']['font']
                    overall_summary[f'B{file_type_start_row + 1}'].alignment = OVERALL_SUMMARY_STYLES['column_header']['alignment']
                    overall_summary[f'B{file_type_start_row + 1}'].fill = OVERALL_SUMMARY_STYLES['column_header']['fill']
                    
                    # Add file type data
                    row = file_type_start_row + 2
                    file_type_counts = latest_data[file_type_col].value_counts()
                    total_file_types = 0
                    for file_type, count in file_type_counts.items():
                        total_file_types += count
                        overall_summary[f'A{row}'] = file_type
                        overall_summary[f'B{row}'] = count
                        overall_summary[f'A{row}'].font = OVERALL_SUMMARY_STYLES['data_cell']['font']
                        overall_summary[f'A{row}'].alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
                        overall_summary[f'A{row}'].fill = OVERALL_SUMMARY_STYLES['data_cell']['fill']
                        overall_summary[f'A{row}'].border = OVERALL_SUMMARY_STYLES['border']
                        overall_summary[f'B{row}'].font = OVERALL_SUMMARY_STYLES['data_cell']['font']
                        overall_summary[f'B{row}'].alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
                        overall_summary[f'B{row}'].fill = OVERALL_SUMMARY_STYLES['data_cell']['fill']
                        overall_summary[f'B{row}'].border = OVERALL_SUMMARY_STYLES['border']
                        row += 1
                    
                    # Add total row for file types
                    overall_summary[f'A{row}'] = 'Total'
                    overall_summary[f'B{row}'] = total_file_types
                    overall_summary[f'A{row}'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
                    overall_summary[f'A{row}'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
                    overall_summary[f'A{row}'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
                    overall_summary[f'A{row}'].border = OVERALL_SUMMARY_STYLES['border']
                    overall_summary[f'B{row}'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
                    overall_summary[f'B{row}'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
                    overall_summary[f'B{row}'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
                    overall_summary[f'B{row}'].border = OVERALL_SUMMARY_STYLES['border']
            
            # Add borders and formatting
            for row in range(1, row + 1):
                for col in ['A', 'B', 'C', 'D']:
                    cell = overall_summary[f'{col}{row}']
                    cell.border = OVERALL_SUMMARY_STYLES['border']
                    cell.alignment = OVERALL_SUMMARY_STYLES['data_cell']['alignment']
            
            # Auto-adjust column widths for Overall Summary
            for column in overall_summary.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                overall_summary.column_dimensions[column_letter].width = adjusted_width
            
            book.save(output_file)
            return True
            
        except PermissionError:
            if attempt < max_retries - 1:
                print(f"File {output_file} is in use. Waiting before retry...")
                time.sleep(2)
            else:
                print(f"Could not save to {output_file} - file is in use.")
                return False
    return False

def generate_standalone_report(input_file, output_file, config):
    """Generate a standalone report from a single input file"""
    try:
        # Read the input file
        current_df = pd.read_excel(input_file, **config['EXCEL_SETTINGS'])
        # Convert all columns to string
        for col in current_df.columns:
            current_df[col] = current_df[col].astype(str)
        
        # Get counts for summary
        counts = get_counts(current_df)
        
        # Create summary DataFrame with single row
        summary_data = [{
            'Date': datetime.now().strftime('%d-%b-%Y'),
            'Time': datetime.now().strftime('%H:%M')
        }]
        for key in sorted(counts.keys()):
            summary_data[0][key] = counts.get(key, 0)
        
        summary_df = pd.DataFrame(summary_data)
        
        # Create empty changes DataFrame since this is a standalone report
        changes_df = pd.DataFrame(columns=list(current_df.columns) + ['Change Type', 'Change Details'])
        
        # Save to Excel
        if save_excel_with_retry(summary_df, changes_df, current_df, output_file, config):
            print(f"\nStandalone report generated in {output_file}")
            return True
        else:
            print("\nPlease close any open Excel files and try again.")
            return False
            
    except Exception as e:
        print(f"Error generating standalone report: {str(e)}")
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Document Register Report Generator')
    parser.add_argument('--standalone', action='store_true', help='Generate a standalone report')
    parser.add_argument('--input', type=str, help='Input file for standalone report')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--project', type=str, help='Project name (e.g., GreenwichPeninsula, NewMalden, OvalBlockB)')
    args = parser.parse_args()
    
    # Setup directories
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    if args.standalone:
        if not args.input:
            print("Error: --input argument is required for standalone reports")
            return
            
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"Error: Input file {input_file} does not exist")
            return
            
        # Load project configuration based on input file
        config = load_project_config(args.project, input_file)
        
        output_file = Path(args.output) if args.output else output_dir / f"standalone_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        generate_standalone_report(input_file, output_file, config)
        return
    
    # Regular weekly report mode
    # Load processed files record
    processed_files = load_processed_files()
    
    # Dictionary to store all counts
    all_counts = {}
    all_changes = []
    
    # Get the previous latest data
    previous_latest_data = None
    output_file = output_dir / 'summary.xlsx'
    if output_file.exists():
        try:
            previous_latest_data = pd.read_excel(output_file, sheet_name='Latest Data')
            # Convert all columns to string
            for col in previous_latest_data.columns:
                previous_latest_data[col] = previous_latest_data[col].astype(str)
        except Exception as e:
            print(f"Warning: Could not load previous latest data: {str(e)}")
    
    # Find the most recent file based on timestamps
    latest_file = None
    latest_timestamp = None
    
    for file_path in input_dir.glob("*.xlsx"):
        if file_path.name.startswith('~$'):  # Skip temporary files
            continue
            
        # Get timestamp from B4
        date_str, time_str = get_file_timestamp(file_path)
        if not date_str or not time_str:
            print(f"Skipping {file_path.name} - could not read timestamp")
            continue
            
        # Convert to datetime for comparison
        try:
            date = datetime.strptime(date_str, '%d-%b-%Y')
            time = datetime.strptime(time_str, '%H:%M').time()
            if latest_timestamp is None or (date, time) > latest_timestamp:
                latest_timestamp = (date, time)
                latest_file = file_path
        except ValueError as e:
            print(f"Warning: Could not parse date/time from {file_path.name}: {str(e)}")
            continue
    
    if latest_file is None:
        print("No valid files found to process")
        return
    
    print(f"\nProcessing latest file: {latest_file.name}")
    
    # Load project configuration based on the latest file
    config = load_project_config(args.project, latest_file)
    
    # Read the latest file
    try:
        if args.debug:
            print(f"Reading Excel file: {latest_file}")
            print("Excel settings:", config['EXCEL_SETTINGS'])
        
        current_df = pd.read_excel(latest_file, **config['EXCEL_SETTINGS'])
        
        if args.debug:
            print("\nDataFrame info:")
            print(current_df.info())
            print("\nDataFrame columns:", current_df.columns.tolist())
            print("\nFirst few rows:")
            print(current_df.head())
        
        # Convert all columns to string
        for col in current_df.columns:
            try:
                current_df[col] = current_df[col].astype(str)
            except Exception as e:
                print(f"Warning: Error converting column '{col}' to string: {str(e)}")
                if args.debug:
                    print(f"Column '{col}' unique values:", current_df[col].unique())
        
        # Compare with previous latest data if it exists
        if previous_latest_data is not None:
            # Create a dictionary of previous data using composite key (Doc Ref + Doc Path)
            prev_data_dict = {}
            for _, row in previous_latest_data.iterrows():
                key = (row['Doc Ref'], row['Doc Path'])
                prev_data_dict[key] = row
            
            # Check for duplicate Doc Refs in current data
            doc_ref_counts = current_df['Doc Ref'].value_counts()
            duplicate_doc_refs = doc_ref_counts[doc_ref_counts > 1].index.tolist()
            
            if duplicate_doc_refs:
                print("\nWarning: Found duplicate Doc Refs in current data:")
                for doc_ref in duplicate_doc_refs:
                    print(f"Doc Ref: {doc_ref}")
                    print("Locations:")
                    for _, row in current_df[current_df['Doc Ref'] == doc_ref].iterrows():
                        print(f"  - {row['Doc Path']} (Title: {row['Doc Title']})")
            
            # Compare each row in current data
            for _, current_row in current_df.iterrows():
                try:
                    doc_ref = current_row['Doc Ref']
                    doc_path = current_row['Doc Path']
                    doc_title = current_row['Doc Title']
                    key = (doc_ref, doc_path)
                    
                    if key in prev_data_dict:
                        # Document exists in both - check for changes
                        prev_row = prev_data_dict[key]
                        changes = []
                        
                        # Compare each column
                        for col in config['CHANGE_DETECTION']['track_columns']:
                            if col not in config['CHANGE_DETECTION']['ignore_columns']:
                                current_val = current_row[col]
                                prev_val = prev_row[col]
                                
                                if compare_values(current_val, prev_val, col):
                                    changes.append(f"{col}: {prev_val} → {current_val}")
                        
                        if changes:
                            # Add to changes with all current data and change details
                            change_row = current_row.copy()
                            change_row['Change Type'] = 'Data Change'
                            change_row['Change Details'] = '; '.join(changes)
                            all_changes.append(change_row)
                    else:
                        # Check if this Doc Ref exists in a different path
                        matching_docs = [(ref, path, row) for (ref, path), row in prev_data_dict.items() 
                                       if ref == doc_ref]
                        
                        if matching_docs:
                            # Found a document with the same Doc Ref in a different path
                            # Check if it's the same document by comparing titles
                            for prev_ref, prev_path, prev_row in matching_docs:
                                prev_title = prev_row['Doc Title']
                                
                                if prev_title == doc_title:
                                    # Same document, just moved
                                    change_row = current_row.copy()
                                    change_row['Change Type'] = 'Document Moved'
                                    change_row['Change Details'] = f'Document moved from: {prev_path} to: {doc_path}'
                                    all_changes.append(change_row)
                                    break
                            else:
                                # No matching title found - this is a new document with duplicate Doc Ref
                                change_row = current_row.copy()
                                change_row['Change Type'] = 'New Document'
                                change_row['Change Details'] = f'New document with duplicate Doc Ref. Existing documents with this Doc Ref: {", ".join(path for _, path, _ in matching_docs)}'
                                all_changes.append(change_row)
                        else:
                            # New document
                            change_row = current_row.copy()
                            change_row['Change Type'] = 'New Document'
                            change_row['Change Details'] = 'New document added'
                            all_changes.append(change_row)
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    if args.debug:
                        print("Row data:", current_row.to_dict())
                    continue
        
        # Get counts for summary
        try:
            counts = get_counts(current_df)
            all_counts[latest_timestamp] = counts
        except Exception as e:
            print(f"Error getting counts: {str(e)}")
            if args.debug:
                print("Current DataFrame state:")
                print(current_df.info())
            raise
        
        # Update processed files record
        file_key = f"{date_str}_{time_str}"  # Use the string versions
        processed_files[latest_file.name] = file_key
        
    except Exception as e:
        print(f"Error processing {latest_file.name}: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return
    
    # Create summary DataFrame
    summary_data = []
    for (date, time) in sorted(all_counts.keys()):
        row = {
            'Date': date.strftime('%d-%b-%Y'),  # Convert to string
            'Time': time.strftime('%H:%M')      # Convert to string
        }
        counts = all_counts[(date, time)]
        for key in sorted(counts.keys()):
            row[key] = counts.get(key, 0)
        summary_data.append(row)
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create changes DataFrame
    changes_df = pd.DataFrame(all_changes) if all_changes else pd.DataFrame(columns=list(current_df.columns) + ['Change Type', 'Change Details'])
    
    # Save to Excel
    if save_excel_with_retry(summary_df, changes_df, current_df, output_file, config):
        # Save processed files record
        save_processed_files(processed_files)
        print(f"\nSummary updated in {output_file}")
    else:
        print("\nPlease close any open Excel files and try again.")

if __name__ == "__main__":
    main() 