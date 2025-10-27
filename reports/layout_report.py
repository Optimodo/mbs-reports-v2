"""Layout tracking report generation module.

This module generates reports for tracking apartment layout drawings,
showing coverage by apartment type with detailed progress tracking.
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from pathlib import Path

from analyzers.document_tracker import get_layout_tracking_summary


# Styling constants
HEADER_FONT = Font(name='Calibri', size=14, bold=True, color='FFFFFF')
HEADER_FILL = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')

SECTION_FONT = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
SECTION_FILL = PatternFill(start_color='5B9BD5', end_color='5B9BD5', fill_type='solid')

SUBHEADER_FONT = Font(name='Calibri', size=10, bold=True)
SUBHEADER_FILL = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')

BORDER_THIN = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)


def create_progress_bar(percentage, length=50):
    """Create a text-based progress bar using block characters."""
    filled = int(percentage / 100 * length)
    empty = length - filled
    return f"{'█' * filled}{'░' * empty} {percentage}%"


def add_overview_section(ws, layout_summary, accommodation_data):
    """Add overview statistics section."""
    row = 5
    
    # Section header
    ws[f'A{row}'] = 'LAYOUT TRACKING OVERVIEW'
    ws[f'A{row}'].font = SECTION_FONT
    ws[f'A{row}'].fill = SECTION_FILL
    ws[f'A{row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{row}:G{row}')
    row += 2
    
    # Statistics
    total_types = len(accommodation_data.get('apartment_types', {})) if accommodation_data else 0
    total_layouts = layout_summary.get('total_layouts', 0)
    withdrawn = layout_summary.get('withdrawn_count', 0)
    categorized = layout_summary.get('categorized', 0)
    uncategorized = layout_summary.get('uncategorized', 0)
    
    stats = [
        ('Total Apartment Types in Project:', total_types),
        ('', ''),
        ('Total Layout Drawings Found:', total_layouts),
        ('Withdrawn (Excluded):', withdrawn),
        ('Categorized Layouts:', categorized),
        ('Uncategorized Layouts:', uncategorized),
    ]
    
    for label, value in stats:
        if label:
            ws[f'A{row}'] = label
            ws[f'B{row}'] = value
            ws[f'A{row}'].font = Font(name='Calibri', size=10, bold=True)
            ws[f'B{row}'].font = Font(name='Calibri', size=10)
            ws[f'B{row}'].alignment = Alignment(horizontal='left')
        row += 1
    
    return row + 2


def add_apartment_layouts_section(ws, apartment_progress, start_row):
    """Add detailed apartment layout tracking table."""
    
    # Section header
    ws[f'A{start_row}'] = 'APARTMENT LAYOUT CATEGORIES'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = SECTION_FILL
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:G{start_row}')
    start_row += 2
    
    # Column headers
    headers = ['Layout Category', 'Types Found', 'Coverage %', 'Unique Layouts', 
               'Alternative Layouts', 'Total Documents', 'Progress Bar']
    
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_idx, value=header)
        cell.font = SUBHEADER_FONT
        cell.fill = SUBHEADER_FILL
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = BORDER_THIN
    start_row += 1
    
    # Add data for each layout category
    for layout_key, progress in apartment_progress.items():
        display_name = progress['display_name']
        types_found = f"{progress['types_with_layout']} / {progress['total_expected_types']}"
        coverage_pct = progress['coverage_percentage']
        unique_count = progress['unique_document_count']
        duplicate_count = progress['duplicate_count']
        total_docs = progress['document_count']
        
        # Layout category name
        ws.cell(row=start_row, column=1, value=display_name).font = Font(name='Calibri', size=10, bold=True)
        
        # Types found (fraction)
        ws.cell(row=start_row, column=2, value=types_found)
        ws.cell(row=start_row, column=2).alignment = Alignment(horizontal='center')
        
        # Coverage percentage
        cell = ws.cell(row=start_row, column=3, value=f"{coverage_pct}%")
        cell.alignment = Alignment(horizontal='center')
        
        # Color code based on coverage
        if coverage_pct >= 90:
            cell.font = Font(name='Calibri', size=10, bold=True, color='00B050')
        elif coverage_pct >= 75:
            cell.font = Font(name='Calibri', size=10, bold=True, color='FFC000')
        else:
            cell.font = Font(name='Calibri', size=10, bold=True, color='C00000')
        
        # Unique layouts count
        ws.cell(row=start_row, column=4, value=unique_count)
        ws.cell(row=start_row, column=4).alignment = Alignment(horizontal='center')
        
        # Alternative/duplicate layouts
        cell = ws.cell(row=start_row, column=5, value=duplicate_count)
        cell.alignment = Alignment(horizontal='center')
        if duplicate_count > 0:
            cell.font = Font(name='Calibri', size=10, color='FF6600')  # Orange for info
        
        # Total documents
        ws.cell(row=start_row, column=6, value=total_docs)
        ws.cell(row=start_row, column=6).alignment = Alignment(horizontal='center')
        
        # Progress bar
        progress_bar = create_progress_bar(coverage_pct, length=50)
        ws.cell(row=start_row, column=7, value=progress_bar)
        ws.cell(row=start_row, column=7).font = Font(name='Consolas', size=9)
        
        start_row += 1
    
    start_row += 2
    
    return start_row + 2


def add_duplicates_section(ws, apartment_progress, start_row):
    """Add section showing types with alternative/duplicate layouts."""
    
    # Check if there are any duplicates
    has_duplicates = any(progress['duplicate_count'] > 0 for progress in apartment_progress.values())
    
    if not has_duplicates:
        return start_row
    
    # Section header
    ws[f'A{start_row}'] = 'APARTMENT TYPES WITH ALTERNATIVE LAYOUTS'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = PatternFill(start_color='FF6600', end_color='FF6600', fill_type='solid')
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:H{start_row}')
    start_row += 2
    
    ws[f'A{start_row}'] = 'Some apartment types have multiple layout variations (e.g., for different plot numbers or design alternatives).'
    ws[f'A{start_row}'].font = Font(name='Calibri', size=9, italic=True, color='666666')
    ws.merge_cells(f'A{start_row}:H{start_row}')
    start_row += 2
    
    for layout_key, progress in apartment_progress.items():
        duplicate_types = progress.get('duplicate_types', [])
        duplicate_count = progress['duplicate_count']
        
        if duplicate_types:
            display_name = progress['display_name']
            ws[f'A{start_row}'] = f'{display_name}:'
            ws[f'A{start_row}'].font = Font(name='Calibri', size=10, bold=True, color='FF6600')
            ws[f'B{start_row}'] = f"{duplicate_count} alternative layout(s) for {len(duplicate_types)} type(s)"
            ws[f'B{start_row}'].font = Font(name='Calibri', size=10)
            start_row += 1
            
            # List types with alternatives
            types_str = ', '.join(duplicate_types[:15])
            if len(duplicate_types) > 15:
                types_str += f' ... and {len(duplicate_types) - 15} more'
            ws[f'B{start_row}'] = types_str
            ws[f'B{start_row}'].font = Font(name='Calibri', size=9, color='666666')
            ws.merge_cells(f'B{start_row}:H{start_row}')
            start_row += 2
    
    return start_row + 2


def add_communal_layouts_section(ws, communal_progress, start_row):
    """Add detailed communal layout tracking table."""
    
    # Section header
    ws[f'A{start_row}'] = 'COMMUNAL LAYOUT CATEGORIES'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = SECTION_FILL
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:G{start_row}')
    start_row += 1
    
    # Column headers for summary (swapped Coverage % and Floors Covered, progress bar in column G)
    headers = ['Layout Category', 'Floors Covered', 'Coverage %', 'Documents', '', '', 'Progress Bar']
    
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_idx, value=header)
        cell.font = SUBHEADER_FONT
        cell.fill = SUBHEADER_FILL
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = BORDER_THIN
    start_row += 1
    
    # Add summary data for each layout category
    for layout_key, progress in communal_progress.items():
        display_name = progress['display_name']
        coverage_pct = progress['coverage_percentage']
        total_floors = progress['total_expected_floors']
        doc_count = progress['document_count']
        
        # Layout category name
        ws.cell(row=start_row, column=1, value=display_name).font = Font(name='Calibri', size=10, bold=True)
        
        # Total floors (covered / expected) - centered
        floors_covered = progress['floors_covered']
        floors_cell = ws.cell(row=start_row, column=2, value=f"{floors_covered} / {total_floors}")
        floors_cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Coverage percentage - centered
        cell = ws.cell(row=start_row, column=3, value=f"{coverage_pct}%")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        if coverage_pct >= 90:
            cell.font = Font(name='Calibri', size=10, bold=True, color='00B050')
        elif coverage_pct >= 75:
            cell.font = Font(name='Calibri', size=10, bold=True, color='FFC000')
        else:
            cell.font = Font(name='Calibri', size=10, bold=True, color='C00000')
        
        # Documents count - centered
        docs_cell = ws.cell(row=start_row, column=4, value=doc_count)
        docs_cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Progress bar - moved to column G
        progress_bar = create_progress_bar(coverage_pct, length=50)
        ws.cell(row=start_row, column=7, value=progress_bar)
        ws.cell(row=start_row, column=7).font = Font(name='Consolas', size=9)
        
        start_row += 1
    
    start_row += 2
    
    # Add detailed block coverage section
    ws[f'A{start_row}'] = 'BLOCK COVERAGE BREAKDOWN'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = SECTION_FILL
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:G{start_row}')
    start_row += 1
    
    # Block coverage headers (simplified layout)
    block_headers = ['Layout Category', 'Block', 'Covered Floors', 'Missing Floors', 'Status']
    
    for col_idx, header in enumerate(block_headers, 1):
        cell = ws.cell(row=start_row, column=col_idx, value=header)
        cell.font = SUBHEADER_FONT
        cell.fill = SUBHEADER_FILL
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = BORDER_THIN
    start_row += 1
    
    # Add block-by-block data
    for layout_key, progress in communal_progress.items():
        display_name = progress['display_name']
        expected_by_block = progress.get('expected_floors_by_block', {})
        coverage_by_block = progress.get('coverage_by_block', {})
        
        # Get all blocks for this layout type
        all_blocks = set(expected_by_block.keys()) | set(coverage_by_block.keys())
        
        # Blacklist of blocks to exclude from the details page
        blacklisted_blocks = {'18.02', '18.03'}
        
        # Filter out blacklisted blocks but keep track for section header
        filtered_blocks = [block for block in sorted(all_blocks) if block not in blacklisted_blocks]
        
        # Always show section header even if all blocks are filtered out
        if filtered_blocks:
            # Layout category name (only show once per category, vertically centered)
            category_cell = ws.cell(row=start_row, column=1, value=display_name)
            category_cell.font = Font(name='Calibri', size=10, bold=True)
            category_cell.alignment = Alignment(horizontal='center', vertical='center')
            # Merge cells vertically for this category
            if len(filtered_blocks) > 1:
                ws.merge_cells(f'A{start_row}:A{start_row + len(filtered_blocks) - 1}')
        
        for block in filtered_blocks:
            expected_floors = expected_by_block.get(block, [])
            covered_floors = coverage_by_block.get(block, [])
            
            # Only count floors that are both expected AND covered (intersection)
            covered_expected_floors = set(expected_floors) & set(covered_floors)
            missing_floors = set(expected_floors) - set(covered_floors)
            
            expected_count = len(expected_floors)
            covered_count = len(covered_expected_floors)  # Use intersection, not all covered floors
            missing_count = len(missing_floors)
            
            # Block name (centered)
            block_cell = ws.cell(row=start_row, column=2, value=f"Block {block}")
            block_cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Covered floors (centered)
            covered_cell = ws.cell(row=start_row, column=3, value=covered_count)
            covered_cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Missing floors - show actual floor numbers instead of count (centered)
            if missing_count == 0:
                missing_text = "None"
                missing_cell = ws.cell(row=start_row, column=4, value=missing_text)
            else:
                missing_list = sorted(list(missing_floors))
                missing_text = ', '.join(map(str, missing_list[:10]))  # Limit to 10 floors for readability
                if len(missing_list) > 10:
                    missing_text += f' ... and {len(missing_list) - 10} more'
                missing_cell = ws.cell(row=start_row, column=4, value=missing_text)
                missing_cell.font = Font(name='Calibri', size=10, color='C00000')
            missing_cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Status - improved text
            if missing_count == 0 and expected_count > 0:
                status = "✓ Complete"
                status_cell = ws.cell(row=start_row, column=5, value=status)
                status_cell.font = Font(name='Calibri', size=10, bold=True, color='00B050')
            elif expected_count == 0:
                status = "N/A"
                status_cell = ws.cell(row=start_row, column=5, value=status)
                status_cell.font = Font(name='Calibri', size=10, color='666666')
            else:
                status = f"Missing {missing_count} floors"
                status_cell = ws.cell(row=start_row, column=5, value=status)
                status_cell.font = Font(name='Calibri', size=10, color='C00000')
            
            start_row += 1
        
        # Add spacing between layout categories
        start_row += 1
    
    return start_row


def add_missing_types_section(ws, apartment_progress, start_row):
    """Add section showing missing apartment types by category."""
    
    # Section header
    ws[f'A{start_row}'] = 'MISSING APARTMENT TYPES BY CATEGORY'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = SECTION_FILL
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:H{start_row}')
    start_row += 2
    
    for layout_key, progress in apartment_progress.items():
        missing_types = progress.get('missing_types', [])
        display_name = progress['display_name']
        
        if missing_types:
            ws[f'A{start_row}'] = f'{display_name}:'
            ws[f'A{start_row}'].font = Font(name='Calibri', size=10, bold=True, color='4472C4')
            ws[f'B{start_row}'] = f"{len(missing_types)} type(s) missing"
            ws[f'B{start_row}'].font = Font(name='Calibri', size=10)
            start_row += 1
            
            # List missing types
            types_str = ', '.join(missing_types[:20])
            if len(missing_types) > 20:
                types_str += f' ... and {len(missing_types) - 20} more'
            ws[f'B{start_row}'] = types_str
            ws[f'B{start_row}'].font = Font(name='Calibri', size=9, color='666666')
            ws.merge_cells(f'B{start_row}:H{start_row}')
            start_row += 2
        else:
            ws[f'A{start_row}'] = f'{display_name}: All types covered ✓'
            ws[f'A{start_row}'].font = Font(name='Calibri', size=10, bold=True, color='70AD47')
            start_row += 2
    
    return start_row


def add_alternatives_section(ws, apartment_progress, start_row):
    """Add section showing types with alternative/duplicate layouts."""
    
    # Check if there are any duplicates
    has_duplicates = any(progress['duplicate_count'] > 0 for progress in apartment_progress.values())
    
    if not has_duplicates:
        return start_row
    
    # Section header
    ws[f'A{start_row}'] = 'APARTMENT TYPES WITH ALTERNATIVE LAYOUTS'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = PatternFill(start_color='FF6600', end_color='FF6600', fill_type='solid')
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:H{start_row}')
    start_row += 2
    
    ws[f'A{start_row}'] = 'Some apartment types have multiple layout variations (e.g., for different plot numbers or design alternatives).'
    ws[f'A{start_row}'].font = Font(name='Calibri', size=9, italic=True, color='666666')
    ws.merge_cells(f'A{start_row}:H{start_row}')
    start_row += 2
    
    for layout_key, progress in apartment_progress.items():
        duplicate_types = progress.get('duplicate_types', [])
        duplicate_count = progress['duplicate_count']
        
        if duplicate_types:
            display_name = progress['display_name']
            ws[f'A{start_row}'] = f'{display_name}:'
            ws[f'A{start_row}'].font = Font(name='Calibri', size=10, bold=True, color='FF6600')
            ws[f'B{start_row}'] = f"{duplicate_count} alternative layout(s) for {len(duplicate_types)} type(s)"
            ws[f'B{start_row}'].font = Font(name='Calibri', size=10)
            start_row += 1
            
            # List types with alternatives
            types_str = ', '.join(duplicate_types[:15])
            if len(duplicate_types) > 15:
                types_str += f' ... and {len(duplicate_types) - 15} more'
            ws[f'B{start_row}'] = types_str
            ws[f'B{start_row}'].font = Font(name='Calibri', size=9, color='666666')
            ws.merge_cells(f'B{start_row}:H{start_row}')
            start_row += 2
    
    return start_row


def add_block_coverage_details_section(ws, communal_progress, start_row):
    """Add block coverage details without example documents."""
    
    # Section header
    ws[f'A{start_row}'] = 'BLOCK COVERAGE DETAILS'
    ws[f'A{start_row}'].font = SECTION_FONT
    ws[f'A{start_row}'].fill = SECTION_FILL
    ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
    ws.merge_cells(f'A{start_row}:H{start_row}')
    start_row += 2
    
    for layout_key, progress in communal_progress.items():
        display_name = progress['display_name']
        coverage_by_block = progress.get('coverage_by_block', {})
        expected_floors_by_block = progress.get('expected_floors_by_block', {})
        
        if coverage_by_block:
            # Layout category header
            ws[f'A{start_row}'] = f'{display_name} Block Coverage:'
            ws[f'A{start_row}'].font = Font(name='Calibri', size=11, bold=True, color='4472C4')
            start_row += 1
            
            # Block coverage details
            for block_name in sorted(coverage_by_block.keys()):
                covered_floors = set(coverage_by_block.get(block_name, []))
                expected_floors = set(expected_floors_by_block.get(block_name, []))
                missing_floors = expected_floors - covered_floors
                
                # Block row
                ws[f'A{start_row}'] = f'  Block {block_name}:'
                ws[f'A{start_row}'].font = Font(name='Calibri', size=10, bold=True)
                
                if missing_floors:
                    ws[f'B{start_row}'] = f'Covered: {len(covered_floors)} floors, Missing: {len(missing_floors)} floor(s)'
                    ws[f'B{start_row}'].font = Font(name='Calibri', size=10, color='D32F2F')
                    
                    # Show specific missing floors
                    missing_list = sorted(list(missing_floors))
                    missing_str = ', '.join(map(str, missing_list[:10]))  # Show first 10
                    if len(missing_list) > 10:
                        missing_str += f' ... and {len(missing_list) - 10} more'
                    
                    ws[f'C{start_row}'] = f'Missing floors: {missing_str}'
                    ws[f'C{start_row}'].font = Font(name='Calibri', size=9, color='D32F2F')
                    ws.merge_cells(f'C{start_row}:H{start_row}')
                else:
                    ws[f'B{start_row}'] = f'Covered: {len(covered_floors)} floors ✓'
                    ws[f'B{start_row}'].font = Font(name='Calibri', size=10, color='70AD47')
                
                start_row += 1
            
            start_row += 1
    
    return start_row


def add_details_tab(wb, layout_summary, apartment_progress, communal_progress):
    """Add detailed breakdown tab with missing types, alternatives, and block coverage."""
    
    ws = wb.create_sheet("Details")
    
    # Report header
    ws['A1'] = "Layout Tracking Details"
    ws['A1'].font = Font(name='Calibri', size=16, bold=True, color='FFFFFF')
    ws['A1'].fill = PatternFill(start_color='203864', end_color='203864', fill_type='solid')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws.merge_cells('A1:H1')
    ws.row_dimensions[1].height = 25
    
    current_row = 5
    
    # Missing apartment types section
    if apartment_progress:
        current_row = add_missing_types_section(ws, apartment_progress, current_row)
        current_row += 2
        
        # Alternative layouts section
        current_row = add_alternatives_section(ws, apartment_progress, current_row)
        current_row += 2
    
    # Block coverage details section (without example documents)
    if communal_progress:
        current_row = add_block_coverage_details_section(ws, communal_progress, current_row)
    
    # Set column widths
    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 18
    ws.column_dimensions['F'].width = 16
    ws.column_dimensions['G'].width = 60
    ws.column_dimensions['H'].width = 10
    
    # Page setup
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.paperSize = 9  # A4
    ws.print_options.horizontalCentered = True


def add_uncategorized_tab(wb, layout_summary):
    """Add detailed uncategorized layouts tab (like certificate report)."""
    
    uncategorized_count = layout_summary.get('uncategorized', 0)
    
    if uncategorized_count == 0:
        return
    
    # Create new sheet
    ws = wb.create_sheet("Uncategorized Layouts")
    
    # Title
    ws['A1'] = 'Uncategorized Layout Drawings'
    ws['A1'].font = Font(name='Calibri', size=14, bold=True, color='FFFFFF')
    ws['A1'].fill = PatternFill(start_color='C00000', end_color='C00000', fill_type='solid')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws.merge_cells('A1:F1')
    ws.row_dimensions[1].height = 25
    
    # Summary
    ws['A3'] = f'Total Uncategorized Layouts: {uncategorized_count}'
    ws['A3'].font = Font(name='Calibri', size=12, bold=True, color='C00000')
    ws['A3'].alignment = Alignment(horizontal='center', vertical='center')
    ws.merge_cells('A3:F3')
    
    ws['A4'] = 'These drawings were not matched to any configured layout category. Review titles to identify new patterns.'
    ws['A4'].font = Font(name='Calibri', size=9, italic=True, color='666666')
    ws['A4'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A4:F4')
    
    # Headers
    headers = ['Doc Title', 'Doc Ref', 'File Type', 'Status', 'Rev', 'Date']
    row = 6
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col_idx, value=header)
        cell.font = SUBHEADER_FONT
        cell.fill = SUBHEADER_FILL
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = BORDER_THIN
    row += 1
    
    # Get uncategorized data
    categorized_data = layout_summary.get('categorized_data')
    if categorized_data is not None and not categorized_data.empty:
        uncategorized = categorized_data[categorized_data['category'].isna()]
        
        for idx, layout in uncategorized.iterrows():
            ws.cell(row=row, column=1, value=layout.get('Doc Title', ''))
            ws.cell(row=row, column=2, value=layout.get('Doc Ref', ''))
            ws.cell(row=row, column=3, value=layout.get('File Type', ''))
            ws.cell(row=row, column=4, value=layout.get('Status', ''))
            ws.cell(row=row, column=5, value=layout.get('Rev', ''))
            ws.cell(row=row, column=6, value=layout.get('Date (WET)', ''))
            
            # Alternate row colors
            if row % 2 == 0:
                for col in range(1, 7):
                    ws.cell(row=row, column=col).fill = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')
            
            row += 1
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = None
        for cell in column:
            try:
                if hasattr(cell, 'column_letter'):
                    if column_letter is None:
                        column_letter = cell.column_letter
                    if cell.value and len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
            except:
                pass
        
        if column_letter is not None:
            adjusted_width = min(max_length + 2, 80)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    # Freeze panes
    ws.freeze_panes = 'A7'


def save_layout_report(latest_data, output_file, config):
    """
    Generate and save layout tracking report to Excel.
    
    Args:
        latest_data: DataFrame of latest documents
        output_file: Path to output Excel file
        config: Project configuration dictionary
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get layout tracking config
        layout_tracking = config.get('APARTMENT_LAYOUT_TRACKING', {})
        
        if not layout_tracking.get('enabled', False):
            print("⚠️  Layout tracking not enabled for this project")
            return False
        
        # Get accommodation data
        accommodation_data = config.get('ACCOMMODATION_DATA', {})
        
        # Get project structure
        project_structure = config.get('PROJECT_STRUCTURE', {})
        
        # Get layout tracking summary
        print("📊 Analyzing layout drawings...")
        layout_summary = get_layout_tracking_summary(latest_data, layout_tracking, accommodation_data, project_structure)
        
        if not layout_summary or layout_summary.get('total_layouts', 0) == 0:
            print("⚠️  No layout drawings found")
            return False
        
        print(f"✓ Found {layout_summary['total_layouts']} layout drawings")
        print(f"  - Withdrawn (excluded): {layout_summary.get('withdrawn_count', 0)}")
        print(f"  - Categorized: {layout_summary['categorized']}")
        print(f"  - Uncategorized: {layout_summary['uncategorized']}")
        
        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Layout Summary"
        
        # Report header
        project_name = config.get('PROJECT_TITLE', 'Unknown Project')
        ws['A1'] = f"{project_name} - Apartment/Communal Layouts Tracking Report"
        ws['A1'].font = Font(name='Calibri', size=16, bold=True, color='FFFFFF')
        ws['A1'].fill = PatternFill(start_color='203864', end_color='203864', fill_type='solid')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells('A1:G1')
        ws.row_dimensions[1].height = 25
        
        # Report date
        ws['A2'] = f"Report Date: {datetime.now().strftime('%d %B %Y')}"
        ws['A2'].font = Font(name='Calibri', size=10, italic=True)
        ws['A2'].alignment = Alignment(horizontal='center')
        ws.merge_cells('A2:G2')
        
        current_row = add_overview_section(ws, layout_summary, accommodation_data)
        
        # Add apartment layout section (summary only)
        apartment_progress = layout_summary.get('apartment_progress', {})
        if apartment_progress:
            current_row = add_apartment_layouts_section(ws, apartment_progress, current_row)
        
        # Add communal layout section (summary only)
        communal_progress = layout_summary.get('communal_progress', {})
        if communal_progress:
            current_row = add_communal_layouts_section(ws, communal_progress, current_row)
        
        # Set column widths
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 12
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 18
        ws.column_dimensions['F'].width = 16
        ws.column_dimensions['G'].width = 60
        ws.column_dimensions['H'].width = 10
        
        # Add details tab with missing types, alternatives, and block coverage
        add_details_tab(wb, layout_summary, apartment_progress, communal_progress)
        
        # Add uncategorized tab
        add_uncategorized_tab(wb, layout_summary)
        
        # Page setup for printing
        ws.page_setup.orientation = 'landscape'
        ws.page_setup.paperSize = 9  # A4
        ws.print_options.horizontalCentered = True
        
        # Save workbook
        wb.save(output_file)
        print(f"\n✅ Layout tracking report saved: {output_file}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error generating layout report: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
