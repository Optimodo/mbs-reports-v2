"""
PDF Generation Utility

Converts Excel report files to PDF using win32com (Windows COM automation).
Respects all print settings set in openpyxl.

Requires:
- Microsoft Excel installed
- Microsoft Print to PDF printer available
- pywin32 package installed
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict

try:
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False


# Print settings per report type
PRINT_SETTINGS_BY_TYPE: Dict[str, Dict] = {
    'summary': {
        'orientation': 2,  # xlLandscape = 2
        'fit_to_width': 1,
        'fit_to_height': 1,
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.75, 'bottom': 0.75},
        'center_horizontally': True,  # Default: not aligned
        'center_vertically': True,  # Default: not aligned
        'print_area': 'A1:P52'  # None = print all, or specify range like 'A1:Z100'
    },
    'certificates': {
        'orientation': 1,  # xlPortrait = 1
        'fit_to_width': 1,
        'fit_to_height': 1,
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.75, 'bottom': 0.75},
        'center_horizontally': True,  # Default: not aligned
        'center_vertically': False,  # Default: not aligned
        'print_area': None
    },
    'layouts': {
        'orientation': 1,  # xlPortrait = 1
        'fit_to_width': 1,
        'fit_to_height': 1,
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.75, 'bottom': 0.75},
        'center_horizontally': True,  # Default: not aligned
        'center_vertically': False,  # Default: not aligned
        'print_area': None
    },
    'progression_condensed': {
        'orientation': 2,  # xlLandscape = 2
        'fit_to_width': 1,
        'fit_to_height': 1,
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.75, 'bottom': 0.75},
        'center_horizontally': True,  # Default: not aligned
        'center_vertically': False,  # Default: not aligned
        'print_area': None
    },
    # Default settings (fallback)
    'default': {
        'orientation': 1,  # xlPortrait = 1
        'fit_to_width': 1,
        'fit_to_height': 1,
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.75, 'bottom': 0.75},
        'center_horizontally': False,  # Default: not aligned
        'center_vertically': False,  # Default: not aligned
        'print_area': None
    }
}


def detect_report_type(filename: str) -> str:
    """
    Detect report type from filename.
    
    Args:
        filename: Excel filename (e.g., 'GreenwichPeninsula_certificates.xlsx')
        
    Returns:
        str: Report type ('summary', 'certificates', 'layouts', 'progression_condensed', or 'default')
    """
    filename_lower = filename.lower()
    
    if 'summary' in filename_lower:
        return 'summary'
    elif 'certificate' in filename_lower:
        return 'certificates'
    elif 'layout' in filename_lower:
        return 'layouts'
    elif 'progression_condensed' in filename_lower or 'progression' in filename_lower:
        return 'progression_condensed'
    else:
        return 'default'


def apply_print_settings_via_com(sheet, excel_app, settings: Dict):
    """
    Apply print settings via Excel COM to a worksheet.
    
    Args:
        sheet: Excel worksheet object (from COM)
        excel_app: Excel application object
        settings: Dictionary with print settings
        
    Settings keys:
        orientation: 1 for Portrait, 2 for Landscape
        fit_to_width: Number of pages wide (1 = fit to one page)
        fit_to_height: Number of pages tall (1 = fit to one page)
        margins: Dict with left, right, top, bottom values in inches
        center_horizontally: Boolean to center horizontally (default: False)
        center_vertically: Boolean to center vertically (default: False)
        print_area: Range string (e.g., 'A1:Z100'), 'auto' for used range, or None for all
    """
    # Set orientation
    if 'orientation' in settings:
        sheet.PageSetup.Orientation = settings['orientation']  # 1=Portrait, 2=Landscape
    
    # Set fit to page
    if settings.get('fit_to_width') or settings.get('fit_to_height'):
        sheet.PageSetup.Zoom = False  # Disable zoom to use FitToPages
        if 'fit_to_width' in settings:
            sheet.PageSetup.FitToPagesWide = settings['fit_to_width']
        if 'fit_to_height' in settings:
            sheet.PageSetup.FitToPagesTall = settings['fit_to_height']
    else:
        sheet.PageSetup.Zoom = True
    
    # Set margins
    if 'margins' in settings:
        margins = settings['margins']
        if 'left' in margins:
            sheet.PageSetup.LeftMargin = excel_app.InchesToPoints(margins['left'])
        if 'right' in margins:
            sheet.PageSetup.RightMargin = excel_app.InchesToPoints(margins['right'])
        if 'top' in margins:
            sheet.PageSetup.TopMargin = excel_app.InchesToPoints(margins['top'])
        if 'bottom' in margins:
            sheet.PageSetup.BottomMargin = excel_app.InchesToPoints(margins['bottom'])
    
    # Set centering (default to False if not specified)
    center_horizontally = settings.get('center_horizontally', False)
    center_vertically = settings.get('center_vertically', False)
    sheet.PageSetup.CenterHorizontally = center_horizontally
    sheet.PageSetup.CenterVertically = center_vertically
    
    # Set print area if specified
    if 'print_area' in settings and settings['print_area']:
        if settings['print_area'] == 'auto':
            # Auto-detect print area from used range
            used_range = sheet.UsedRange
            if used_range:
                sheet.PageSetup.PrintArea = used_range.Address
        else:
            # Use specified range (e.g., 'A1:Z100' or 'A1:Z100,A105:Z200' for multiple ranges)
            sheet.PageSetup.PrintArea = settings['print_area']
    else:
        # Clear print area (print all)
        sheet.PageSetup.PrintArea = ""


def excel_to_pdf(excel_path: Path, pdf_path: Optional[Path] = None, report_type: Optional[str] = None, verbose: bool = True) -> tuple[bool, str]:
    """
    Convert an Excel file to PDF using Windows COM automation.
    
    Args:
        excel_path: Path to the Excel file (.xlsx)
        pdf_path: Optional output PDF path. If None, uses same name as Excel file with .pdf extension
        report_type: Optional report type to use specific print settings. If None, auto-detects from filename
        verbose: If True, prints progress messages
        
    Returns:
        tuple: (success: bool, message: str)
    """
    if not HAS_WIN32COM:
        return False, "win32com not available (requires pywin32 package)"
    
    if not excel_path.exists():
        return False, f"Excel file not found: {excel_path}"
    
    # Determine output PDF path
    if pdf_path is None:
        pdf_path = excel_path.parent / f"{excel_path.stem}.pdf"
    
    # Delete existing PDF if it exists
    if pdf_path.exists():
        try:
            pdf_path.unlink()
        except Exception:
            pass  # Ignore deletion errors
    
    # Detect report type if not provided
    if report_type is None:
        report_type = detect_report_type(excel_path.name)
    
    # Get print settings for this report type
    settings = PRINT_SETTINGS_BY_TYPE.get(report_type, PRINT_SETTINGS_BY_TYPE['default']).copy()
    
    excel = None
    workbook = None
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        try:
            excel.Visible = False
        except Exception:
            # Some Excel configurations don't allow setting Visible property
            pass
        try:
            excel.DisplayAlerts = False
        except Exception:
            # Some Excel configurations don't allow setting DisplayAlerts
            pass
        try:
            excel.ScreenUpdating = False
        except Exception:
            pass
        
        # Open workbook (with error handling)
        try:
            workbook = excel.Workbooks.Open(str(excel_path.absolute()), ReadOnly=True)
        except Exception as e:
            # If opening fails, try to quit Excel and return error
            try:
                if excel:
                    excel.Quit()
            except:
                pass
            return False, f"Error opening Excel file: {str(e)}"
        
        # Get first sheet
        first_sheet = workbook.Worksheets(1)  # Index 1 is first sheet
        
        # Apply print settings via COM (Excel doesn't respect openpyxl settings)
        try:
            apply_print_settings_via_com(first_sheet, excel, settings)
        except Exception as e:
            # Continue even if print settings fail
            pass
        
        # Export ONLY the first sheet to PDF
        first_sheet.ExportAsFixedFormat(
            Type=0,  # xlTypePDF
            Filename=str(pdf_path.absolute()),
            Quality=0,  # xlQualityStandard
            IncludeDocProperties=True,
            IgnorePrintAreas=False,  # Respect print areas!
            OpenAfterPublish=False
        )
        
        if verbose:
            orientation_str = "landscape" if settings.get('orientation') == 2 else "portrait"
            print(f"  ✓ Converted to PDF ({orientation_str}): {pdf_path.name}")
        return True, f"Converted to {pdf_path}"
            
    except Exception as e:
        error_msg = str(e)
        if "No printers are installed" in error_msg or "printer" in error_msg.lower():
            return False, "No PDF printer available. Install 'Microsoft Print to PDF' printer (Windows Settings > Printers & scanners)"
        return False, f"Error converting to PDF: {error_msg}"
    finally:
        # Always try to clean up, even if there was an error
        try:
            if workbook:
                workbook.Close(SaveChanges=False)
        except Exception:
            pass
        try:
            if excel:
                excel.Quit()
        except Exception:
            pass
        # Small delay to allow Excel to fully close
        time.sleep(0.1)


def convert_reports_to_pdf(output_dir: Path, report_types: Optional[List[str]] = None, project_name: Optional[str] = None, verbose: bool = True) -> dict:
    """
    Convert all Excel report files in output directory to PDF.
    
    Args:
        output_dir: Directory containing Excel report files
        report_types: Optional list of report type suffixes to convert (e.g., ['summary', 'certificates'])
                     If None, converts all .xlsx files
        project_name: Optional project name to filter by (e.g., 'GreenwichPeninsula', 'OvalBlockB')
                     If None, converts all projects
        verbose: If True, prints progress messages
        
    Returns:
        dict: Statistics {'total': int, 'successful': int, 'failed': int, 'files': list}
    """
    if verbose:
        print("\n" + "="*60)
        print("Converting Excel Reports to PDF")
        if project_name:
            print(f"For project: {project_name}")
        print("="*60)
    
    # Find Excel files
    excel_files = list(output_dir.glob("*.xlsx"))
    
    if not excel_files:
        if verbose:
            print("  ℹ No Excel files found in output directory")
        return {'total': 0, 'successful': 0, 'failed': 0, 'files': []}
    
    # Filter by project name if specified
    if project_name:
        from utils import slugify
        project_slug = slugify(project_name)
        filtered_files = []
        for excel_file in excel_files:
            if project_slug.lower() in excel_file.stem.lower():
                filtered_files.append(excel_file)
        excel_files = filtered_files
    
    # Filter by report types if specified
    if report_types:
        filtered_files = []
        for excel_file in excel_files:
            for report_type in report_types:
                if report_type.lower() in excel_file.stem.lower():
                    filtered_files.append(excel_file)
                    break
        excel_files = filtered_files
    
    # Clean up any existing intermediate PDF files (e.g., _sheet1.pdf)
    for pdf_file in output_dir.glob("*_sheet*.pdf"):
        try:
            pdf_file.unlink()
        except Exception:
            pass  # Ignore deletion errors
    
    # Convert each file
    stats = {
        'total': len(excel_files),
        'successful': 0,
        'failed': 0,
        'files': []
    }
    
    for excel_file in excel_files:
        pdf_file = excel_file.parent / f"{excel_file.stem}.pdf"
        # Auto-detect report type from filename
        report_type = detect_report_type(excel_file.name)
        success, message = excel_to_pdf(excel_file, pdf_file, report_type=report_type, verbose=verbose)
        
        file_stat = {
            'excel_file': excel_file.name,
            'pdf_file': pdf_file.name if success else None,
            'report_type': report_type,
            'success': success,
            'message': message
        }
        stats['files'].append(file_stat)
        
        if success:
            stats['successful'] += 1
        else:
            stats['failed'] += 1
            if verbose:
                print(f"  ✗ {excel_file.name}: {message}")
    
    if verbose:
        print(f"\n✓ PDF Conversion Complete: {stats['successful']}/{stats['total']} successful")
    
    # Merge PDFs into single document if any were successfully converted
    if stats['successful'] > 0:
        try:
            from utils.pdf_merger import merge_reports_to_pdf
            merged_path = merge_reports_to_pdf(output_dir, project_name=project_name, verbose=verbose)
            if merged_path:
                stats['merged_file'] = str(merged_path)
        except Exception as e:
            if verbose:
                print(f"  ⚠ PDF merging failed: {str(e)}")
    
    return stats


if __name__ == "__main__":
    # Command-line usage
    if len(sys.argv) < 2:
        print("Usage: python -m utils.pdf_generator <output_dir> [report_types...]")
        print("Example: python -m utils.pdf_generator output summary certificates layouts")
        sys.exit(1)
    
    output_dir = Path(sys.argv[1])
    report_types = sys.argv[2:] if len(sys.argv) > 2 else None
    
    if not output_dir.exists():
        print(f"Error: Directory not found: {output_dir}")
        sys.exit(1)
    
    stats = convert_reports_to_pdf(output_dir, report_types)
    sys.exit(0 if stats['failed'] == 0 else 1)
