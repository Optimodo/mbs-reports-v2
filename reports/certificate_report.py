"""Certificate report generation module."""

import warnings
import pandas as pd
from datetime import datetime
from pathlib import Path
import time
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.worksheet.page import PageMargins
from openpyxl.chart import PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.drawing.fill import ColorChoice, PatternFillProperties

from styles.formatting import (
    OVERALL_SUMMARY_STYLES,
    apply_status_style
)
from utils.status_mapping import (
    get_status_category,
    get_status_color,
    get_grouped_status_counts,
    get_status_display_order
)

# Suppress openpyxl warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def get_chart_safe_color(config_color, category):
    """Convert config colors to chart-safe colors.
    
    Ensures that white/very light colors are converted to visible colors for charts.
    
    Args:
        config_color: Color from config (hex string)
        category: Status category name for fallback mapping
        
    Returns:
        str: Chart-safe hex color
    """
    # Define chart-safe colors for common white/light statuses
    chart_safe_mapping = {
        'Other': 'C0C0C0',        # Light gray
        'Information': 'D3D3D3',   # Light gray
        'Review': 'E6E6FA',       # Lavender
        'IFC-pending': 'F0E68C',  # Khaki
        'Under Review': 'DDA0DD', # Plum
        'Shared': 'E0F090',       # Light yellow-green
        'Published': '90EE90'     # Light green
    }
    
    # If config color is white or very light, use chart-safe color
    if config_color and config_color.upper() in ['FFFFFF', 'FFF', 'FFFFFFFF']:
        return chart_safe_mapping.get(category, 'C0C0C0')
    
    # Check if color is very light (all RGB components > 240)
    if config_color and len(config_color) >= 6:
        try:
            r = int(config_color[0:2], 16)
            g = int(config_color[2:4], 16)
            b = int(config_color[4:6], 16)
            if r > 240 and g > 240 and b > 240:
                return chart_safe_mapping.get(category, 'C0C0C0')
        except ValueError:
            pass
    
    return config_color


def save_certificate_report(summary_df, latest_data, output_file, config):
    """
    Save a comprehensive certificate report to Excel.
    
    Args:
        summary_df: DataFrame with summary data (revision/status counts over time)
        latest_data: DataFrame with the latest certificate data
        output_file: Path to the output Excel file
        config: Project configuration dictionary
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create Excel writer
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Write Summary Data sheet
            summary_df.to_excel(writer, sheet_name='Summary Data', index=False)
            
            # Write Latest Certificate Data sheet
            latest_data.to_excel(writer, sheet_name='Latest Certificate Data', index=False)
        
        # Load the workbook to add the Overall Summary sheet
        wb = load_workbook(output_file)
        
        # Create Overall Summary sheet at the beginning
        if 'Overall Summary' in wb.sheetnames:
            del wb['Overall Summary']
        overall_summary = wb.create_sheet('Overall Summary', 0)
        
        # Set up page layout
        overall_summary.page_setup.fitToWidth = 1
        overall_summary.page_setup.fitToHeight = 0
        overall_summary.page_margins = PageMargins(left=0.5, right=0.5, top=0.75, bottom=0.75)
        
        # Add title and project info
        project_title = config.get('PROJECT_TITLE', 'Project')
        cert_settings = config.get('CERTIFICATE_SETTINGS', {})
        
        overall_summary['A1'] = f"{project_title} - Certificate Report"
        overall_summary['A1'].font = Font(name='Calibri', size=16, bold=True)
        overall_summary['A1'].alignment = Alignment(horizontal='left', vertical='center')
        
        # Get latest row from summary
        latest_row = summary_df.iloc[-1] if not summary_df.empty else {}
        latest_date = latest_row.get('Date', 'N/A')
        latest_time = latest_row.get('Time', 'N/A')
        
        overall_summary['A2'] = f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        overall_summary['A2'].font = Font(name='Calibri', size=10, italic=True)
        
        overall_summary['A3'] = f"Latest Data: {latest_date} {latest_time}"
        overall_summary['A3'].font = Font(name='Calibri', size=10, italic=True)
        
        # Add total certificate count
        total_certs = len(latest_data)
        overall_summary['A5'] = 'Total Certificates:'
        overall_summary['B5'] = total_certs
        overall_summary['A5'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
        overall_summary['A5'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
        overall_summary['A5'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
        overall_summary['B5'].font = OVERALL_SUMMARY_STYLES['total_cell']['font']
        overall_summary['B5'].alignment = OVERALL_SUMMARY_STYLES['total_cell']['alignment']
        overall_summary['B5'].fill = OVERALL_SUMMARY_STYLES['total_cell']['fill']
        
        # Get revision columns from summary data
        all_columns = summary_df.columns.tolist()
        rev_columns = [col for col in all_columns if col.startswith('Rev_')]
        
        # Sort revision columns
        p_revs = sorted([col for col in rev_columns if col.startswith('Rev_P')], 
                      key=lambda x: int(x.split('_')[1][1:]) if x.split('_')[1][1:].isdigit() else float('inf'))
        c_revs = sorted([col for col in rev_columns if col.startswith('Rev_C')],
                      key=lambda x: int(x.split('_')[1][1:]) if x.split('_')[1][1:].isdigit() else float('inf'))
        other_revs = sorted([col for col in rev_columns if not (
            col.startswith('Rev_P') or col.startswith('Rev_C')
        )])
        
        # Function to add revision and status summary
        def add_certificate_revision_summary(start_row, rev_columns, title):
            """Add a certificate revision summary section with status breakdown"""
            if not rev_columns:
                return start_row
            
            # Add section header
            overall_summary[f'A{start_row}'] = title
            overall_summary[f'A{start_row}'].font = OVERALL_SUMMARY_STYLES['section_header']['font']
            overall_summary[f'A{start_row}'].alignment = OVERALL_SUMMARY_STYLES['section_header']['alignment']
            overall_summary[f'A{start_row}'].fill = OVERALL_SUMMARY_STYLES['section_header']['fill']
            
            # Add headers
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
                
                # Get count from summary data
                count = latest_row.get(rev_col, 0)
                # Handle NaN values from pandas
                total_count += 0 if pd.isna(count) else count
                
                # Count statuses for this revision
                rev_data = latest_data[latest_data['Rev'] == rev_name]
                
                # Use get_grouped_status_counts to properly group raw status values
                if not rev_data.empty:
                    grouped_counts = get_grouped_status_counts(rev_data['Status'], config)
                    for status, status_count in grouped_counts.items():
                        status_counts[status] = status_counts.get(status, 0) + status_count
            
            # Add revision data
            row = start_row + 2
            for rev_col in rev_columns:
                rev_name = rev_col.replace('Rev_', '')
                
                # Get the count from the summary data
                count = latest_row.get(rev_col, 0)
                # Handle NaN values from pandas
                count = 0 if pd.isna(count) else count
                
                # Only add revision row if there are actually documents with this revision
                if count > 0:
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
            row += 1
            
            # Add status summary
            status_row = start_row + 2
            total_status_count = 0
            
            # Create ordered list using project-specific categories
            ordered_statuses = []
            
            # Build ordered list using project-specific display order
            if config and 'STATUS_DISPLAY_ORDER' in config:
                display_order = config['STATUS_DISPLAY_ORDER']
                
                # Add statuses in the order defined by STATUS_DISPLAY_ORDER
                for category in display_order:
                    if category in status_counts:
                        ordered_statuses.append((category, status_counts[category]))
                
                # Add any remaining statuses that weren't in display order
                for status, count in status_counts.items():
                    if status not in display_order:
                        ordered_statuses.append((status, count))
            else:
                # Fallback to alphabetical order if no display order defined
                ordered_statuses = sorted(status_counts.items())
            
            for status, count in ordered_statuses:
                total_status_count += count
                
                # Add status name with conditional formatting
                status_cell = overall_summary[f'C{status_row}']
                status_cell.value = status
                style = apply_status_style(status_cell, status, config)
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
            
            return max(row, status_row) + 2
        
        # Add revision summaries
        current_row = 7
        if p_revs:
            current_row = add_certificate_revision_summary(current_row, p_revs, 'P Revision Certificates')
        if c_revs:
            current_row = add_certificate_revision_summary(current_row, c_revs, 'C Revision Certificates')
        if other_revs:
            current_row = add_certificate_revision_summary(current_row, other_revs, 'Other Revision Certificates')
        
        # Add overall status pie chart
        if not latest_data.empty and 'Status' in latest_data.columns:
            # Use get_grouped_status_counts to properly group raw status values
            chart_grouped_counts = get_grouped_status_counts(latest_data['Status'], config)
            
            if len(chart_grouped_counts) > 0:
                # Create temporary worksheet for chart data
                chart_data_sheet = wb.create_sheet('ChartData_Temp')
                chart_data_sheet['A1'] = 'Status'
                chart_data_sheet['B1'] = 'Count'
                
                row_idx = 2
                for status, count in chart_grouped_counts.items():
                    chart_data_sheet[f'A{row_idx}'] = status
                    chart_data_sheet[f'B{row_idx}'] = count
                    row_idx += 1
                
                # Create pie chart
                chart = PieChart()
                chart.title = "Certificate Status Distribution"
                chart.style = 10
                chart.height = 10
                chart.width = 15
                
                # Add data to chart
                data = Reference(chart_data_sheet, min_col=2, min_row=1, max_row=row_idx-1)
                cats = Reference(chart_data_sheet, min_col=1, min_row=2, max_row=row_idx-1)
                chart.add_data(data, titles_from_data=True)
                chart.set_categories(cats)
                
                # Add data labels
                chart.dataLabels = DataLabelList()
                chart.dataLabels.showCatName = True
                chart.dataLabels.showVal = True
                chart.dataLabels.showPercent = True
                
                # Apply colors from config
                # Note: Chart coloring is complex with openpyxl and can cause compatibility issues
                # Leaving charts with default Excel colors for better compatibility
                # Colors are still applied to the table cells for visual differentiation
                
                # Position chart
                overall_summary.add_chart(chart, 'G2')
                
                # Hide the temporary chart data sheet
                chart_data_sheet.sheet_state = 'hidden'
        
        # Adjust column widths
        overall_summary.column_dimensions['A'].width = 25
        overall_summary.column_dimensions['B'].width = 12
        overall_summary.column_dimensions['C'].width = 25
        overall_summary.column_dimensions['D'].width = 12
        
        # Save the workbook
        wb.save(output_file)
        return True
        
    except Exception as e:
        print(f"Error generating certificate report: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def save_certificate_report_with_retry(summary_df, latest_data, output_file, config, max_retries=3, retry_delay=1):
    """
    Save certificate report with retry logic for file access issues.
    
    Args:
        summary_df: DataFrame with summary data
        latest_data: DataFrame with the latest certificate data
        output_file: Path to the output Excel file
        config: Project configuration dictionary
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    for attempt in range(max_retries):
        if save_certificate_report(summary_df, latest_data, output_file, config):
            return True
        
        if attempt < max_retries - 1:
            print(f"Retry {attempt + 1}/{max_retries - 1} in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    return False

