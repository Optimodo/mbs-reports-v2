import os
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import plotly.express as px
import plotly.graph_objects as go
from config import *
import re
import time
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

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
            
            # Extract the date from the timestamp string
            try:
                # Look for date pattern like "20-May-2025"
                import re
                date_match = re.search(r'\d{1,2}-[A-Za-z]{3}-\d{4}', timestamp_str)
                if date_match:
                    file_date = datetime.strptime(date_match.group(), '%d-%b-%Y')
                else:
                    print(f"Warning: Could not parse date from timestamp in {file_name}")
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

    def generate_weekly_summary(self):
        """Generate a weekly summary report"""
        # Get all processed data files
        data_files = list(self.data_dir.glob("*.parquet"))
        
        if not data_files:
            print("No processed data files found.")
            return

        # Find the most recent version of each file
        latest_files = {}
        for data_file in data_files:
            file_name = data_file.stem
            date_file = self.data_dir / f"{file_name}.date"
            
            if date_file.exists():
                with open(date_file, 'r') as f:
                    file_date = datetime.fromisoformat(f.read().strip())
                
                if file_name not in latest_files or file_date > latest_files[file_name][1]:
                    latest_files[file_name] = (data_file, file_date)

        # Use only the most recent version of each file
        latest_data_files = [f[0] for f in latest_files.values()]
        
        # Combine all data from the most recent files
        all_data = pd.concat([pd.read_parquet(f) for f in latest_data_files])
        
        # Create summary statistics
        summary = {
            'total_documents': len(all_data),
            'revision_counts': all_data['Rev'].value_counts().to_dict(),
            'status_counts': all_data['Status'].value_counts().to_dict(),
            'type_counts': all_data['Type'].value_counts().to_dict(),
            'publisher_counts': all_data['Publisher'].value_counts().to_dict(),
            'documents_by_date': all_data['Date (WET)'].value_counts().sort_index().to_dict()
        }

        # Generate visualizations
        self._generate_visualizations(all_data)

        # Save summary to Excel
        self._save_summary_to_excel(summary, all_data)

        # Generate changes report
        self._generate_changes_report()

        return summary

    def _generate_changes_report(self):
        """Generate a detailed changes report"""
        if not self.latest_changes:
            return

        # Create HTML report
        html_content = """
        <html>
        <head>
            <title>Document Register Changes Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2 {{ color: #333; }}
                .change-section {{ margin: 20px 0; }}
                .change-item {{ margin: 10px 0; padding: 10px; background-color: #f5f5f5; }}
                .change-details {{ margin-left: 20px; }}
            </style>
        </head>
        <body>
            <h1>Document Register Changes Report</h1>
            <p>Generated on: {}</p>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        for file_name, changes in self.latest_changes.items():
            html_content += f"<h2>Changes in {file_name}</h2>"
            
            if 'status_changes' in changes and changes['status_changes']:
                html_content += "<div class='change-section'>"
                html_content += "<h3>Status Changes</h3>"
                for change in changes['status_changes']:
                    html_content += f"""
                    <div class='change-item'>
                        <strong>{change['doc_ref']} - {change['doc_title']}</strong>
                        <div class='change-details'>
                            Status: {change['old_status']} → {change['new_status']}
                        </div>
                    </div>
                    """
                html_content += "</div>"

            if 'revision_changes' in changes and changes['revision_changes']:
                html_content += "<div class='change-section'>"
                html_content += "<h3>Revision Changes</h3>"
                for change in changes['revision_changes']:
                    html_content += f"""
                    <div class='change-item'>
                        <strong>{change['doc_ref']} - {change['doc_title']}</strong>
                        <div class='change-details'>
                            Revision: {change['old_rev']} → {change['new_rev']}
                        </div>
                    </div>
                    """
                html_content += "</div>"

            if 'date_changes' in changes and changes['date_changes']:
                html_content += "<div class='change-section'>"
                html_content += "<h3>Date Changes</h3>"
                for change in changes['date_changes']:
                    html_content += f"""
                    <div class='change-item'>
                        <strong>{change['doc_ref']} - {change['doc_title']}</strong>
                        <div class='change-details'>
                            Date: {change['old_date']} → {change['new_date']}
                        </div>
                    </div>
                    """
                html_content += "</div>"

            if 'new_documents' in changes and changes['new_documents']:
                html_content += "<div class='change-section'>"
                html_content += "<h3>New Documents</h3>"
                for doc_ref in changes['new_documents']:
                    html_content += f"<div class='change-item'>{doc_ref}</div>"
                html_content += "</div>"

            if 'removed_documents' in changes and changes['removed_documents']:
                html_content += "<div class='change-section'>"
                html_content += "<h3>Removed Documents</h3>"
                for doc_ref in changes['removed_documents']:
                    html_content += f"<div class='change-item'>{doc_ref}</div>"
                html_content += "</div>"

        html_content += """
        </body>
        </html>
        """

        # Save HTML report
        with open(self.reports_dir / 'changes_report.html', 'w') as f:
            f.write(html_content)

    def _generate_visualizations(self, df):
        """Generate and save visualizations"""
        # Revision distribution
        rev_counts = df['Rev'].value_counts().reset_index()
        rev_counts.columns = ['Revision', 'Count']
        fig_rev = px.bar(
            rev_counts,
            x='Revision',
            y='Count',
            title='Document Distribution by Revision'
        )
        fig_rev.write_html(self.reports_dir / 'revision_distribution.html')

        # Status distribution
        fig_status = px.pie(
            df,
            names='Status',
            title='Document Distribution by Status'
        )
        fig_status.write_html(self.reports_dir / 'status_distribution.html')

        # Type distribution
        type_counts = df['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig_type = px.bar(
            type_counts,
            x='Type',
            y='Count',
            title='Document Distribution by Type'
        )
        fig_type.write_html(self.reports_dir / 'type_distribution.html')

        # Publisher distribution
        publisher_counts = df['Publisher'].value_counts().reset_index()
        publisher_counts.columns = ['Publisher', 'Count']
        fig_publisher = px.bar(
            publisher_counts,
            x='Publisher',
            y='Count',
            title='Document Distribution by Publisher'
        )
        fig_publisher.write_html(self.reports_dir / 'publisher_distribution.html')

    def _save_summary_to_excel(self, summary, df):
        """Save summary statistics to Excel"""
        with pd.ExcelWriter(self.reports_dir / 'weekly_summary.xlsx') as writer:
            # Summary sheet
            summary_df = pd.DataFrame([
                {'Metric': 'Total Documents', 'Value': summary['total_documents']},
                {'Metric': 'Unique Revisions', 'Value': len(summary['revision_counts'])},
                {'Metric': 'Unique Statuses', 'Value': len(summary['status_counts'])},
                {'Metric': 'Unique Types', 'Value': len(summary['type_counts'])},
                {'Metric': 'Unique Publishers', 'Value': len(summary['publisher_counts'])}
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Revision counts
            pd.DataFrame.from_dict(summary['revision_counts'], orient='index', columns=['Count']).to_excel(
                writer, sheet_name='Revision Counts'
            )

            # Status counts
            pd.DataFrame.from_dict(summary['status_counts'], orient='index', columns=['Count']).to_excel(
                writer, sheet_name='Status Counts'
            )

            # Type counts
            pd.DataFrame.from_dict(summary['type_counts'], orient='index', columns=['Count']).to_excel(
                writer, sheet_name='Type Counts'
            )

            # Publisher counts
            pd.DataFrame.from_dict(summary['publisher_counts'], orient='index', columns=['Count']).to_excel(
                writer, sheet_name='Publisher Counts'
            )

            # Documents by date
            pd.DataFrame.from_dict(summary['documents_by_date'], orient='index', columns=['Count']).to_excel(
                writer, sheet_name='Documents by Date'
            )

            # Changes sheet
            if self.latest_changes:
                changes_data = []
                for file_name, changes in self.latest_changes.items():
                    if 'status_changes' in changes:
                        for change in changes['status_changes']:
                            changes_data.append({
                                'File': file_name,
                                'Document': change['doc_ref'],
                                'Title': change['doc_title'],
                                'Change Type': 'Status',
                                'Old Value': change['old_status'],
                                'New Value': change['new_status']
                            })
                    if 'revision_changes' in changes:
                        for change in changes['revision_changes']:
                            changes_data.append({
                                'File': file_name,
                                'Document': change['doc_ref'],
                                'Title': change['doc_title'],
                                'Change Type': 'Revision',
                                'Old Value': change['old_rev'],
                                'New Value': change['new_rev']
                            })
                    if 'date_changes' in changes:
                        for change in changes['date_changes']:
                            changes_data.append({
                                'File': file_name,
                                'Document': change['doc_ref'],
                                'Title': change['doc_title'],
                                'Change Type': 'Date',
                                'Old Value': change['old_date'],
                                'New Value': change['new_date']
                            })
                    if 'new_documents' in changes:
                        for doc_ref in changes['new_documents']:
                            changes_data.append({
                                'File': file_name,
                                'Document': doc_ref,
                                'Title': '',
                                'Change Type': 'New Document',
                                'Old Value': '',
                                'New Value': ''
                            })
                    if 'removed_documents' in changes:
                        for doc_ref in changes['removed_documents']:
                            changes_data.append({
                                'File': file_name,
                                'Document': doc_ref,
                                'Title': '',
                                'Change Type': 'Removed Document',
                                'Old Value': '',
                                'New Value': ''
                            })
                
                if changes_data:
                    pd.DataFrame(changes_data).to_excel(writer, sheet_name='Changes', index=False)

            # Raw data
            df.to_excel(writer, sheet_name='Raw Data', index=False)

def get_file_timestamp(file_path):
    """Get the timestamp from cell B4 of the Excel file"""
    try:
        # Read just cell B4 (which is merged from B to I)
        timestamp_df = pd.read_excel(file_path, usecols="B", nrows=4, header=None)
        timestamp_str = timestamp_df.iloc[3, 0]
        
        # Extract date and time using regex
        # Looking for pattern like "20-May-2025 13:39"
        match = re.search(r'(\d{1,2}-[A-Za-z]{3}-\d{4})\s+(\d{1,2}:\d{2})', timestamp_str)
        if match:
            date_str = match.group(1)
            time_str = match.group(2)
            date = datetime.strptime(date_str, '%d-%b-%Y')
            time = datetime.strptime(time_str, '%H:%M').time()
            return date, time
        return None, None
    except Exception as e:
        print(f"Error reading timestamp from {file_path.name}: {str(e)}")
        return None, None

def get_counts(df):
    """Get counts of revisions and statuses from the dataframe"""
    counts = {}
    
    # Count revisions
    rev_counts = df['Rev'].value_counts()
    for rev, count in rev_counts.items():
        counts[f'Rev_{rev}'] = count
    
    # Count statuses
    status_counts = df['Status'].value_counts()
    for status, count in status_counts.items():
        counts[f'Status_{status}'] = count
    
    return counts

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

def save_excel_with_retry(summary_df, changes_df, latest_data_df, output_file, max_retries=3):
    """Try to save the Excel file with retries"""
    for attempt in range(max_retries):
        try:
            # Try to load existing file
            try:
                book = load_workbook(output_file)
                
                # Remove existing Changes sheet if it exists
                if 'Changes' in book.sheetnames:
                    book.remove(book['Changes'])
                
                with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    # Save changes sheet (it's new since we removed the old one)
                    changes_df.to_excel(writer, sheet_name='Changes', index=False)
                    
                    # Save latest data sheet
                    latest_data_df.to_excel(writer, sheet_name='Latest Data', index=False)
                    
                    # Get existing summary sheet
                    if 'Summary' in book.sheetnames:
                        # Read existing summary
                        existing_summary = pd.read_excel(output_file, sheet_name='Summary')
                        # Combine with new data
                        combined_summary = pd.concat([existing_summary, summary_df]).drop_duplicates(subset=['Date', 'Time'], keep='last')
                        
                        # Get the existing sheet
                        summary_sheet = book['Summary']
                        
                        # Store existing column widths
                        column_widths = {}
                        for col in summary_sheet.column_dimensions:
                            column_widths[col] = summary_sheet.column_dimensions[col].width
                        
                        # Store existing row heights
                        row_heights = {}
                        for row in summary_sheet.row_dimensions:
                            row_heights[row] = summary_sheet.row_dimensions[row].height
                        
                        # Store existing cell formats
                        cell_formats = {}
                        for row in summary_sheet.iter_rows():
                            for cell in row:
                                if cell.has_style:
                                    cell_formats[cell.coordinate] = {
                                        'font': cell.font,
                                        'fill': cell.fill,
                                        'border': cell.border,
                                        'alignment': cell.alignment,
                                        'number_format': cell.number_format
                                    }
                        
                        # Save combined summary
                        combined_summary.to_excel(writer, sheet_name='Summary', index=False)
                        
                        # Get the new sheet
                        new_summary_sheet = book['Summary']
                        
                        # Restore column widths
                        for col, width in column_widths.items():
                            if width is not None:
                                new_summary_sheet.column_dimensions[col].width = width
                        
                        # Restore row heights
                        for row, height in row_heights.items():
                            if height is not None:
                                new_summary_sheet.row_dimensions[row].height = height
                        
                        # Restore cell formats
                        for coord, formats in cell_formats.items():
                            if coord in new_summary_sheet:
                                cell = new_summary_sheet[coord]
                                cell.font = formats['font']
                                cell.fill = formats['fill']
                                cell.border = formats['border']
                                cell.alignment = formats['alignment']
                                cell.number_format = formats['number_format']
                    else:
                        # If no existing summary, save new one
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)
            except FileNotFoundError:
                # If file doesn't exist, create new one
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                    changes_df.to_excel(writer, sheet_name='Changes', index=False)
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
            for sheet_name in ['Summary', 'Changes', 'Latest Data']:
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

def main():
    # Setup directories
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
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
        date, time = get_file_timestamp(file_path)
        if not date or not time:
            print(f"Skipping {file_path.name} - could not read timestamp")
            continue
            
        if latest_timestamp is None or (date, time) > latest_timestamp:
            latest_timestamp = (date, time)
            latest_file = file_path
    
    if latest_file is None:
        print("No valid files found to process")
        return
    
    print(f"\nProcessing latest file: {latest_file.name}")
    
    # Read the latest file
    try:
        current_df = pd.read_excel(latest_file, skiprows=6)
        # Convert all columns to string
        for col in current_df.columns:
            current_df[col] = current_df[col].astype(str)
        
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
                doc_ref = current_row['Doc Ref']
                doc_path = current_row['Doc Path']
                doc_title = current_row['Doc Title']
                key = (doc_ref, doc_path)
                
                if key in prev_data_dict:
                    # Document exists in both - check for changes
                    prev_row = prev_data_dict[key]
                    changes = []
                    
                    # Compare each column
                    for col in current_df.columns:
                        if col not in ['Doc Ref', 'Doc Path']:
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
            
            # Check for removed documents
            current_keys = set((ref, path) for ref, path in zip(current_df['Doc Ref'], current_df['Doc Path']))
            for (doc_ref, doc_path), prev_row in prev_data_dict.items():
                if (doc_ref, doc_path) not in current_keys:
                    # Check if this Doc Ref exists in a different path
                    matching_docs = [(ref, path, row) for (ref, path), row in zip(current_df['Doc Ref'], current_df['Doc Path'], current_df.itertuples(index=False))
                                   if ref == doc_ref]
                    
                    if matching_docs:
                        # Found a document with the same Doc Ref in a different path
                        # Check if it's the same document by comparing titles
                        prev_title = prev_row['Doc Title']
                        for curr_ref, curr_path, curr_row in matching_docs:
                            curr_title = curr_row.Doc_Title
                            
                            if curr_title == prev_title:
                                # Same document, just moved
                                change_row = prev_row.copy()
                                change_row['Change Type'] = 'Document Moved'
                                change_row['Change Details'] = f'Document moved from: {doc_path} to: {curr_path}'
                                all_changes.append(change_row)
                                break
                        else:
                            # No matching title found - this is a removed document
                            change_row = prev_row.copy()
                            change_row['Change Type'] = 'Removed Document'
                            change_row['Change Details'] = f'Document removed. Other documents with this Doc Ref exist in: {", ".join(path for _, path, _ in matching_docs)}'
                            all_changes.append(change_row)
                    else:
                        # Removed document
                        change_row = prev_row.copy()
                        change_row['Change Type'] = 'Removed Document'
                        change_row['Change Details'] = 'Document removed'
                        all_changes.append(change_row)
        
        # Get counts for summary
        counts = get_counts(current_df)
        all_counts[latest_timestamp] = counts
        
        # Update processed files record
        file_key = f"{latest_timestamp[0].strftime('%Y-%m-%d')}_{latest_timestamp[1].strftime('%H:%M')}"
        processed_files[latest_file.name] = file_key
        
    except Exception as e:
        print(f"Error processing {latest_file.name}: {str(e)}")
        return
    
    # Create summary DataFrame
    summary_data = []
    for (date, time) in sorted(all_counts.keys()):
        row = {
            'Date': date,
            'Time': time
        }
        counts = all_counts[(date, time)]
        for key in sorted(counts.keys()):
            row[key] = counts.get(key, 0)
        summary_data.append(row)
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create changes DataFrame
    changes_df = pd.DataFrame(all_changes) if all_changes else pd.DataFrame(columns=list(current_df.columns) + ['Change Type', 'Change Details'])
    
    # Save to Excel
    if save_excel_with_retry(summary_df, changes_df, current_df, output_file):
        # Save processed files record
        save_processed_files(processed_files)
        print(f"\nSummary updated in {output_file}")
    else:
        print("\nPlease close any open Excel files and try again.")

if __name__ == "__main__":
    main() 