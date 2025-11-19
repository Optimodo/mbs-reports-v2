"""
Print Settings Utility

Provides functions to apply print settings to Excel worksheets.
Makes print settings easily configurable and editable.
"""

from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.page import PrintPageSetup


# Default print settings - easily editable
DEFAULT_PRINT_SETTINGS = {
    'orientation': 'portrait',  # 'portrait' or 'landscape'
    'paper_size': 9,  # 9 = A4
    'fit_to_width': 1,  # Fit all columns to one page width
    'fit_to_height': 1,  # Fit all rows to one page height
    'margins': {
        'left': 0.5,
        'right': 0.5,
        'top': 0.75,
        'bottom': 0.75,
        'header': 0.3,
        'footer': 0.3
    },
    'horizontal_centered': True,
    'vertical_centered': False
}


def apply_print_settings(worksheet, settings=None):
    """
    Apply print settings to an Excel worksheet.
    
    Args:
        worksheet: openpyxl worksheet object
        settings: Optional dict with print settings. If None, uses DEFAULT_PRINT_SETTINGS.
        
    Settings keys:
        orientation: 'portrait' or 'landscape'
        paper_size: Paper size code (9 = A4)
        fit_to_width: Number of pages wide (1 = fit to one page)
        fit_to_height: Number of pages tall (1 = fit to one page)
        margins: Dict with left, right, top, bottom, header, footer values
        horizontal_centered: Boolean to center horizontally
        vertical_centered: Boolean to center vertically
    """
    if settings is None:
        settings = DEFAULT_PRINT_SETTINGS.copy()
    
    # Set orientation
    if 'orientation' in settings:
        worksheet.page_setup.orientation = settings['orientation']
    
    # Set paper size
    if 'paper_size' in settings:
        worksheet.page_setup.paperSize = settings['paper_size']
    
    # Set fit to page
    if 'fit_to_width' in settings:
        worksheet.page_setup.fitToWidth = settings['fit_to_width']
    if 'fit_to_height' in settings:
        worksheet.page_setup.fitToHeight = settings['fit_to_height']
    
    # Set margins
    if 'margins' in settings:
        margins = settings['margins']
        worksheet.page_margins = PageMargins(
            left=margins.get('left', 0.5),
            right=margins.get('right', 0.5),
            top=margins.get('top', 0.75),
            bottom=margins.get('bottom', 0.75),
            header=margins.get('header', 0.3),
            footer=margins.get('footer', 0.3)
        )
    
    # Set centering
    if 'horizontal_centered' in settings:
        worksheet.print_options.horizontalCentered = settings['horizontal_centered']
    if 'vertical_centered' in settings:
        worksheet.print_options.verticalCentered = settings['vertical_centered']


def apply_to_all_sheets(workbook, settings=None):
    """
    Apply print settings to all sheets in a workbook.
    
    Args:
        workbook: openpyxl workbook object
        settings: Optional dict with print settings. If None, uses DEFAULT_PRINT_SETTINGS.
    """
    for sheet in workbook.worksheets:
        apply_print_settings(sheet, settings)

