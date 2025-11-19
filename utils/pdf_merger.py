"""
PDF Merger Utility

Combines multiple PDF reports into a single document with styled title pages.
Includes Table of Contents and page numbers.
Matches the styling used in certificate and layout reports.
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from datetime import datetime

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

# Project order for merging
PROJECT_ORDER = ['GreenwichPeninsula', 'OvalBlockB', 'NewMalden', 'HollowayPark', 'WestCromwellRoad']

# Report type order for merging
REPORT_TYPE_ORDER = ['summary', 'progression_condensed', 'layouts', 'certificates']

# Project display names
PROJECT_DISPLAY_NAMES = {
    'GreenwichPeninsula': 'Greenwich Peninsula',
    'OvalBlockB': 'Oval Block B',
    'NewMalden': 'New Malden',
    'HollowayPark': 'Holloway Park',
    'WestCromwellRoad': 'West Cromwell Road'
}

# Report type display names
REPORT_TYPE_DISPLAY_NAMES = {
    'summary': 'Summary Report',
    'progression_condensed': 'Progression Report',
    'layouts': 'Layout Tracking Report',
    'certificates': 'Certificate Report'
}


def create_toc_page(toc: List[Tuple], page_size: tuple = (595, 842)) -> fitz.Document:
    """
    Create a Table of Contents page.
    
    Args:
        toc: List of (entry_text, page_number, is_project) tuples for Table of Contents
             or (entry_text, page_number) tuples (for backwards compatibility)
        page_size: Page size in points (default A4 portrait: 595x842)
        
    Returns:
        fitz.Document: PDF document with TOC page
    """
    if not HAS_PYMUPDF:
        raise ImportError("PyMuPDF (fitz) is required for creating TOC pages")
    
    doc = fitz.open()
    page = doc.new_page(width=page_size[0], height=page_size[1])
    
    # Colors matching report styling
    dark_blue = (0.125, 0.220, 0.392)  # #203864
    white = (1.0, 1.0, 1.0)
    black = (0.0, 0.0, 0.0)
    gray = (0.4, 0.4, 0.4)
    light_gray = (0.85, 0.85, 0.85)
    
    # Draw header background
    header_rect = fitz.Rect(0, 0, page_size[0], 100)
    page.draw_rect(header_rect, color=dark_blue, fill=dark_blue)
    
    # TOC Title in header
    toc_title_font_size = 20
    toc_title_rect = fitz.Rect(50, 30, page_size[0] - 50, 90)
    page.insert_textbox(
        toc_title_rect,
        "Table of Contents",
        fontsize=toc_title_font_size,
        color=white,
        fontname="hebo",  # Helvetica-Bold
        align=1  # Center alignment
    )
    
    # TOC Items
    toc_start_y = 120
    toc_item_font_size = 11
    toc_project_font_size = 12  # Slightly larger for project names
    line_height = 20
    project_line_height = 24  # More space for project entries
    
    y_pos = toc_start_y
    
    for entry in toc:
        # Handle both old format (text, page) and new format (text, page, is_project)
        if len(entry) == 2:
            entry_text, page_num = entry
            is_project = False
        else:
            entry_text, page_num, is_project = entry
        
        if y_pos + (project_line_height if is_project else line_height) > page_size[1] - 100:
            # Create new page if needed
            page = doc.new_page(width=page_size[0], height=page_size[1])
            y_pos = 50
        
        # Determine indentation and font based on whether it's a project or report
        if is_project:
            # Project name: bold, no indentation, slightly larger font
            entry_x = 80
            font_size = toc_project_font_size
            font_name = "hebo"  # Bold
            current_line_height = project_line_height
        else:
            # Report name: normal, indented
            entry_x = 100  # Indented 20 points from projects
            font_size = toc_item_font_size
            font_name = "helv"  # Regular
            current_line_height = line_height
        
        # Entry text (left aligned)
        entry_rect = fitz.Rect(entry_x, y_pos, page_size[0] - 120, y_pos + current_line_height)
        page.insert_textbox(
            entry_rect,
            entry_text,
            fontsize=font_size,
            color=black,
            fontname=font_name,
            align=0  # Left alignment
        )
        
        # Page number (right aligned)
        page_num_rect = fitz.Rect(page_size[0] - 120, y_pos, page_size[0] - 50, y_pos + current_line_height)
        page.insert_textbox(
            page_num_rect,
            str(page_num),
            fontsize=font_size,
            color=black,
            fontname=font_name,
            align=2  # Right alignment
        )
        
        # Dotted line between text and page number
        dot_y = y_pos + (current_line_height / 2)  # Middle of line
        # Estimate positions based on text lengths (approximately 6 points per character)
        estimated_text_width = len(entry_text) * 6
        estimated_num_width = len(str(page_num)) * 6
        text_x_end = entry_x + estimated_text_width + 10
        num_x_start = page_size[0] - 120 - estimated_num_width - 5
        
        if num_x_start > text_x_end + 10:
            # Draw dotted line
            current_x = text_x_end
            dot_spacing = 4
            while current_x < num_x_start - 5:
                page.draw_circle(fitz.Point(current_x, dot_y), 0.8, color=gray, fill=gray)
                current_x += dot_spacing
        
        y_pos += current_line_height
    
    return doc


def create_title_page(title: str, subtitle: Optional[str] = None, toc: Optional[List[Tuple[str, int]]] = None, 
                      logo_path: Optional[Path] = None, description: Optional[str] = None, 
                      author: Optional[str] = None, page_size: tuple = (595, 842)) -> fitz.Document:
    """
    Create a styled title page PDF matching the report styling.
    
    Args:
        title: Main title text
        subtitle: Optional subtitle text
        toc: Optional list of (entry_text, page_number) tuples for brief TOC (e.g., on divider pages)
        logo_path: Optional path to logo image file
        description: Optional brief description of report contents
        author: Optional author information
        page_size: Page size in points (default A4 portrait: 595x842)
        
    Returns:
        fitz.Document: PDF document with title page
    """
    if not HAS_PYMUPDF:
        raise ImportError("PyMuPDF (fitz) is required for creating title pages")
    
    # Create new PDF document
    doc = fitz.open()
    page = doc.new_page(width=page_size[0], height=page_size[1])
    
    # Colors matching report styling
    # Main header: #203864 (dark blue)
    # Section header: #4472C4 (blue)
    # Text: #FFFFFF (white) for headers, #000000 (black) for body
    
    dark_blue = (0.125, 0.220, 0.392)  # #203864
    blue = (0.267, 0.447, 0.769)  # #4472C4
    white = (1.0, 1.0, 1.0)
    black = (0.0, 0.0, 0.0)
    gray = (0.4, 0.4, 0.4)
    light_gray = (0.85, 0.85, 0.85)
    
    # Draw header background (matching report style) - for both main cover and divider pages
    header_height = 100
    header_rect = fitz.Rect(0, 0, page_size[0], header_height)
    page.draw_rect(header_rect, color=dark_blue, fill=dark_blue)
    
    # For main cover page: Add date in top bar
    if not toc:
        now = datetime.now()
        day = now.day
        suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        date_str = f"Report Date: {day}{suffix} {now.strftime('%B %Y')}"
        
        date_font_size = 12
        date_rect = fitz.Rect(50, 30, page_size[0] - 50, 90)
        page.insert_textbox(
            date_rect,
            date_str,
            fontsize=date_font_size,
            color=white,
            fontname="helv",
            align=1  # Center alignment
        )
    # For divider pages: Add project title in header
    else:
        project_title_font_size = 20
        project_title_rect = fitz.Rect(50, 30, page_size[0] - 50, 90)
        page.insert_textbox(
            project_title_rect,
            title,
            fontsize=project_title_font_size,
            color=white,
            fontname="hebo",  # Bold Helvetica
            align=1  # Center alignment
        )
    
    # Add logo if provided (only for main cover page, not divider pages)
    logo_y_start = 150  # Below top bar
    if logo_path and logo_path.exists() and not toc:
        try:
            # Open image and get its dimensions
            img = fitz.open(logo_path)
            img_rect = img[0].rect
            
            # Calculate logo size (max width 400 points, maintain aspect ratio)
            max_logo_width = 400
            logo_scale = min(max_logo_width / img_rect.width, 1.0)
            logo_width = img_rect.width * logo_scale
            logo_height = img_rect.height * logo_scale
            
            # Center logo horizontally
            logo_x = (page_size[0] - logo_width) / 2
            logo_y = logo_y_start
            
            # Insert logo image
            logo_rect = fitz.Rect(logo_x, logo_y, logo_x + logo_width, logo_y + logo_height)
            page.insert_image(logo_rect, filename=str(logo_path))
            
            img.close()
            
            # Adjust starting position for title (below logo)
            logo_y_start = logo_y + logo_height + 40
        except Exception:
            # If logo fails to load, continue without it
            pass
    
    # Add document title in the middle of white area (only for main cover page)
    if not toc:
        document_title = "MBS Weekly Project Reports"
        # Position title in the vertical center of the white area
        # White area: from header (100) to footer (842-60=782)
        # Center: (100 + 782) / 2 = 441
        title_font_size = 28  # Large but not overwhelming
        title_center_y = 441  # Vertical center of white area
        title_rect = fitz.Rect(50, title_center_y - 30, page_size[0] - 50, title_center_y + 30)
        page.insert_textbox(
            title_rect,
            document_title,
            fontsize=title_font_size,
            color=black,  # Black text as requested
            fontname="hebo",  # Bold Helvetica
            align=1  # Center alignment
        )
    
    # Add brief TOC if provided (for divider pages)
    if toc:
        toc_start_y = 140
        toc_title_font_size = 14
        toc_item_font_size = 10
        
        # Brief TOC title
        toc_title_rect = fitz.Rect(50, toc_start_y, page_size[0] - 50, toc_start_y + 20)
        page.insert_textbox(
            toc_title_rect,
            "Reports in this section:",
            fontsize=toc_title_font_size,
            color=dark_blue,
            fontname="hebo",  # Helvetica-Bold
            align=0  # Left alignment
        )
        
        # Brief TOC items
        y_pos = toc_start_y + 30
        line_height = 18
        
        for entry_text, page_num in toc[:6]:  # Limit to 6 items max for brief TOC
            if y_pos + line_height > page_size[1] - 80:  # Don't go too close to bottom
                break
            
            # Entry text with page number (left aligned, simple format)
            toc_entry = f"- {entry_text} ................... {page_num}"
            entry_rect = fitz.Rect(70, y_pos, page_size[0] - 50, y_pos + line_height)
            page.insert_textbox(
                entry_rect,
                toc_entry,
                fontsize=toc_item_font_size,
                color=black,
                fontname="helv",
                align=0  # Left alignment
            )
            
            y_pos += line_height
    
    # Add footer bar with author (only for main cover page, not divider pages)
    if not toc:
        # Draw footer background (matching header style)
        footer_height = 60
        footer_rect = fitz.Rect(0, page_size[1] - footer_height, page_size[0], page_size[1])
        page.draw_rect(footer_rect, color=dark_blue, fill=dark_blue)
        
        # Add author in footer (white text on blue background)
        if author:
            # Format author text: "Author: Mike McLean, mike.mclean@malcolmbuildingservices.co.uk"
            author_text = f"Author: {author.replace(chr(10), ', ')}"  # Replace newline with comma-space
            author_font_size = 12
            author_footer_rect = fitz.Rect(50, page_size[1] - footer_height + 20, page_size[0] - 50, page_size[1] - 10)
            page.insert_textbox(
                author_footer_rect,
                author_text,
                fontsize=author_font_size,
                color=white,
                fontname="helv",
                align=1  # Center alignment
            )
    
    return doc


def add_page_numbers(pdf_doc: fitz.Document, start_page: int = 1) -> int:
    """
    Add page number watermarks to all pages in a PDF document.
    
    Args:
        pdf_doc: PyMuPDF document
        start_page: Starting page number (default 1)
        
    Returns:
        int: Total number of pages (for calculating next start page)
    """
    if not HAS_PYMUPDF:
        return len(pdf_doc)
    
    gray = (0.5, 0.5, 0.5)
    
    for page_num in range(len(pdf_doc)):
        page = pdf_doc[page_num]
        page_size = page.rect
        
        # Calculate page number position (bottom center, outside margin)
        actual_page_num = start_page + page_num
        page_num_text = f"Page {actual_page_num}"
        
        # Position at bottom center (about 15 points from bottom, centered)
        page_num_font_size = 9
        
        # Estimate text width (approximately 6 points per character)
        text_width = len(page_num_text) * 6
        
        x_pos = (page_size.width - text_width) / 2
        y_pos = page_size.height - 15
        
        # Insert page number
        page.insert_text(
            fitz.Point(x_pos, y_pos),
            page_num_text,
            fontsize=page_num_font_size,
            color=gray,
            fontname="helv"
        )
    
    return len(pdf_doc)


def get_project_order_key(filename: str) -> tuple:
    """
    Get sort key for ordering files by project and report type.
    
    Returns:
        tuple: (project_index, report_type_index) for sorting
    """
    filename_lower = filename.lower()
    
    # Find project index
    project_index = len(PROJECT_ORDER)
    for i, project in enumerate(PROJECT_ORDER):
        project_slug = project.lower().replace(' ', '')
        if project_slug in filename_lower or project.lower() in filename_lower:
            project_index = i
            break
    
    # Find report type index
    report_type_index = len(REPORT_TYPE_ORDER)
    for i, report_type in enumerate(REPORT_TYPE_ORDER):
        if report_type in filename_lower:
            report_type_index = i
            break
    
    return (project_index, report_type_index)


def merge_reports_to_pdf(output_dir: Path, project_name: Optional[str] = None, verbose: bool = True) -> Optional[Path]:
    """
    Merge all PDF reports into a single document with styled title pages.
    Includes Table of Contents and page numbers.
    
    Args:
        output_dir: Directory containing PDF report files
        project_name: Optional project name to filter by. If None, merges all projects
        verbose: If True, prints progress messages
        
    Returns:
        Path to merged PDF file, or None if failed
    """
    if not HAS_PYMUPDF:
        if verbose:
            print("  ✗ PyMuPDF not available - cannot merge PDFs")
        return None
    
    if verbose:
        print("\n" + "="*60)
        print("Merging PDF Reports")
        print("="*60)
    
    # Find all PDF files
    pdf_files = list(output_dir.glob("*.pdf"))
    
    # Filter out merged PDFs and intermediate files
    pdf_files = [f for f in pdf_files if not f.name.startswith('complete_report') and '_sheet' not in f.name]
    
    if not pdf_files:
        if verbose:
            print("  ℹ No PDF files found to merge")
        return None
    
    # Filter by project if specified
    if project_name:
        from utils import slugify
        project_slug = slugify(project_name)
        filtered_files = []
        for pdf_file in pdf_files:
            if project_slug.lower() in pdf_file.stem.lower():
                filtered_files.append(pdf_file)
        pdf_files = filtered_files
    
    if not pdf_files:
        if verbose:
            print(f"  ℹ No PDF files found for project: {project_name}")
        return None
    
    # Sort files by project and report type order
    pdf_files.sort(key=lambda f: get_project_order_key(f.name))
    
    # Group files by project and collect metadata for TOC
    projects_files: Dict[str, List[Tuple[Path, str]]] = {}
    for pdf_file in pdf_files:
        # Detect project from filename
        project = None
        filename_lower = pdf_file.stem.lower()
        
        for proj in PROJECT_ORDER:
            proj_variations = [
                proj.lower().replace(' ', ''),
                proj.lower().replace(' ', '_'),
                proj.lower(),
            ]
            
            abbrev_map = {
                'greenwichpeninsula': 'gp',
                'ovalblockb': 'ovb',
                'newmalden': 'nm',
                'hollowaypark': 'hp',
                'westcromwellroad': 'wcr'
            }
            
            proj_key = proj.lower().replace(' ', '')
            if proj_key in abbrev_map:
                proj_variations.append(abbrev_map[proj_key])
            
            for variation in proj_variations:
                if variation in filename_lower:
                    project = proj
                    break
            
            if project:
                break
        
        if project is None:
            project = 'Unknown'
        
        # Detect report type
        report_type = None
        for rt in REPORT_TYPE_ORDER:
            if rt in filename_lower:
                report_type = rt
                break
        
        if project not in projects_files:
            projects_files[project] = []
        projects_files[project].append((pdf_file, report_type))
    
    # Sort files within each project by report type order
    for project in projects_files:
        projects_files[project].sort(key=lambda x: (
            REPORT_TYPE_ORDER.index(x[1]) if x[1] in REPORT_TYPE_ORDER else len(REPORT_TYPE_ORDER)
        ))
    
    # First pass: Calculate page numbers for TOC
    toc_entries: List[Tuple] = []
    current_page = 1  # Cover page (no page number shown)
    
    # Cover page (page 1, but no number displayed)
    toc_entries.append(("Cover Page", current_page, False))
    current_page += 1
    
    # TOC page (page 2, first numbered page)
    toc_entries.append(("Table of Contents", current_page, False))
    current_page += 1
    
    # Calculate page numbers for all reports
    for project in PROJECT_ORDER:
        if project not in projects_files:
            continue
        
        project_files = projects_files[project]
        if not project_files:
            continue
        
        project_display = PROJECT_DISPLAY_NAMES.get(project, project)
        toc_entries.append((project_display, current_page, True))  # True = is_project (bold)
        current_page += 1
        
        # Add report entries for this project
        for pdf_file, report_type in project_files:
            if pdf_file.exists():
                try:
                    doc = fitz.open(str(pdf_file))
                    report_display = REPORT_TYPE_DISPLAY_NAMES.get(report_type, report_type or 'Report')
                    toc_entries.append((report_display, current_page, False))  # False = is_report (normal)
                    current_page += len(doc)
                    doc.close()
                except Exception:
                    pass
    
    # Second pass: Actually merge PDFs with page numbers
    merged_doc = fitz.open()
    current_page = 1  # Track actual page number (starts at 1)
    page_number_display = 2  # Page numbers displayed start at 2 (cover page has no number)
    
    # Create and add main title page
    # Always use the same main title regardless of single or all projects
    main_title = "MBS Weekly Projects Reports"
    if project_name:
        main_subtitle = PROJECT_DISPLAY_NAMES.get(project_name, project_name)
    else:
        main_subtitle = "All Projects"
    
    # Look for logo in the main project directory (parent of output_dir)
    logo_path = output_dir.parent / "mbs-new-logo.png"
    if not logo_path.exists():
        logo_path = None
    
    # Author information
    author = "Mike McLean\nmike.mclean@malcolmbuildingservices.co.uk"
    
    main_title_page = create_title_page(
        main_title, 
        main_subtitle,
        logo_path=logo_path,
        author=author
    )
    # Don't add page numbers to the cover page (page 1 has no number displayed)
    merged_doc.insert_pdf(main_title_page)
    main_title_page.close()
    current_page += 1
    
    if verbose:
        print(f"  ✓ Added main title page")
    
    # Create and add TOC page (starts at page 2)
    toc_page = create_toc_page(toc_entries)
    add_page_numbers(toc_page, start_page=page_number_display)
    merged_doc.insert_pdf(toc_page)
    toc_page.close()
    current_page += 1
    page_number_display += 1  # TOC page is page 2
    
    if verbose:
        print(f"  ✓ Added Table of Contents")
    
    # Add project sections
    for project in PROJECT_ORDER:
        if project not in projects_files:
            continue
        
        project_files = projects_files[project]
        if not project_files:
            continue
        
        project_display = PROJECT_DISPLAY_NAMES.get(project, project)
        
        # Build project-specific TOC
        project_toc: List[Tuple[str, int]] = []
        project_start_page = page_number_display + 1  # +1 for divider page
        
        # Calculate page counts for TOC without keeping documents open
        pdf_page_counts = {}
        for pdf_file, report_type in project_files:
            if pdf_file.exists():
                try:
                    doc = fitz.open(str(pdf_file))
                    page_count = len(doc)
                    doc.close()
                    pdf_page_counts[pdf_file] = (report_type, page_count)
                    report_display = REPORT_TYPE_DISPLAY_NAMES.get(report_type, report_type or 'Report')
                    project_toc.append((report_display, project_start_page))
                    project_start_page += page_count
                except Exception:
                    pass
        
        # Create and add project divider page with TOC
        project_title = create_title_page(project_display, "Project Reports", toc=project_toc)
        add_page_numbers(project_title, start_page=page_number_display)
        merged_doc.insert_pdf(project_title)
        project_title.close()
        current_page += 1
        page_number_display += 1  # Divider page
        
        if verbose:
            print(f"  ✓ Added divider: {project_display}")
        
        # Add reports for this project in order
        for pdf_file, report_type in project_files:
            if pdf_file.exists():
                doc = None
                try:
                    doc = fitz.open(str(pdf_file))
                    if doc.is_closed:
                        if verbose:
                            print(f"    ✗ Failed to add {pdf_file.name}: document is closed")
                        continue
                    
                    report_display = REPORT_TYPE_DISPLAY_NAMES.get(report_type, report_type or 'Report')
                    page_count = len(doc)
                    
                    # Add page numbers to this document before merging
                    add_page_numbers(doc, start_page=page_number_display)
                    
                    # Ensure document is still open before merging
                    if not doc.is_closed:
                        merged_doc.insert_pdf(doc)
                        current_page += page_count
                        page_number_display += page_count  # Update displayed page number
                        
                        if verbose:
                            print(f"    ✓ Added: {report_display} ({page_count} pages)")
                    else:
                        if verbose:
                            print(f"    ✗ Failed to add {pdf_file.name}: document closed before merge")
                except Exception as e:
                    if verbose:
                        print(f"    ✗ Failed to add {pdf_file.name}: {str(e)}")
                finally:
                    if doc is not None and not doc.is_closed:
                        doc.close()
    
    # Save merged PDF
    if project_name:
        merged_filename = f"{project_name}_complete_report.pdf"
    else:
        merged_filename = "complete_report_all_projects.pdf"
    
    merged_path = output_dir / merged_filename
    page_count = len(merged_doc)
    merged_doc.save(str(merged_path))
    merged_doc.close()
    
    if verbose:
        print(f"\n✓ Merged PDF created: {merged_path.name}")
        print(f"  Total pages: {page_count}")
    
    return merged_path


if __name__ == "__main__":
    # Command-line usage
    if len(sys.argv) < 2:
        print("Usage: python -m utils.pdf_merger <output_dir> [project_name]")
        print("Example: python -m utils.pdf_merger output GreenwichPeninsula")
        sys.exit(1)
    
    output_dir = Path(sys.argv[1])
    project_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not output_dir.exists():
        print(f"Error: Directory not found: {output_dir}")
        sys.exit(1)
    
    result = merge_reports_to_pdf(output_dir, project_name)
    sys.exit(0 if result else 1)
