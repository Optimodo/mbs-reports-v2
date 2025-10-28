"""Generic document tracking system for certificates and drawings.

This module provides flexible tracking for different document categories
(e.g., apartment certificates, communal certificates, apartment layouts)
with configurable detection patterns and progress visualization.

Supports optional phase and block tracking for projects completed in multiple phases.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Optional


def extract_apartment_number(doc_title: str, doc_ref: str = "", doc_path: str = "", category: str = None, path_filter_config: Dict = None) -> Optional[int]:
    """
    Extract apartment number from document metadata.
    
    Tries multiple patterns to find apartment numbers:
    - "Plot XXX" pattern (highest priority - matches Unit Ref in schedules)
    - "Unit XXX" pattern
    - "Apt XXX" pattern  
    - "Flat XXX" pattern (lower priority - often postal address, not unit ref)
    - 1-4 digit numbers in titles
    - Apartment numbers in doc refs or paths
    
    Args:
        doc_title: Document title
        doc_ref: Document reference (optional)
        doc_path: Document path (optional)
        category: Category name (for specialized extraction logic)
        path_filter_config: Optional path filter configuration for apartment vs communal detection
        
    Returns:
        Apartment number if found, None otherwise
    """
    if pd.isna(doc_title):
        doc_title = ""
    if pd.isna(doc_ref):
        doc_ref = ""
    if pd.isna(doc_path):
        doc_path = ""
    
    # Combine all text for searching
    search_text = f"{doc_title} {doc_ref} {doc_path}".upper()
    
    # Pattern 1 (HIGHEST PRIORITY): "Plot XXX" - matches Unit Ref in accommodation schedules
    # Handle variations: "Plot 123", "Plot No. 123", "Plot No: 123", "Plot Number 123", "Plot No 123"
    plot_match = re.search(r'PLOT\s+(?:NO[.:]?\s*|NUMBER\s+)?(\d{1,4})', search_text)
    if plot_match:
        return int(plot_match.group(1))
    
    # Pattern 2: "Unit XXX" or "UNIT XXX"
    unit_match = re.search(r'UNIT\s+(\d{1,4})', search_text)
    if unit_match:
        return int(unit_match.group(1))
    
    # Pattern 3: "B###" format (OvalBlockB specific - e.g., "B112", "B151")
    # This pattern matches "B" followed by 3 digits at word boundary
    b_code_match = re.search(r'\bB(\d{3})\b', search_text)
    if b_code_match:
        # Return the 3-digit code as the apartment identifier
        # B112 → 112, B151 → 151
        return int(b_code_match.group(1))
    
    # Pattern 4: "Apt XXX" or "APT XXX"
    apt_match = re.search(r'APT\s+(\d{1,4})', search_text)
    if apt_match:
        return int(apt_match.group(1))
    
    # Pattern 5: "Flat XXX" or "FLAT XXX" (lower priority - might be postal address)
    flat_match = re.search(r'FLAT\s+(\d{1,4})', search_text)
    if flat_match:
        return int(flat_match.group(1))
    
    # PRIMARY FILTER: Use document path to distinguish landlord/communal vs apartment certificates
    # If path_filter_config is provided, use it; otherwise use legacy hardcoded patterns
    if path_filter_config and path_filter_config.get('enabled', False):
        # Check exclude patterns (e.g., \Landlords\)
        exclude_patterns = path_filter_config.get('exclude_patterns', [])
        for pattern in exclude_patterns:
            if re.search(pattern, doc_path, re.IGNORECASE):
                return None
        
        # Check include patterns (e.g., \Block - X\)
        include_patterns = path_filter_config.get('include_patterns', [])
        if include_patterns:
            matches_include = False
            for pattern in include_patterns:
                if re.search(pattern, doc_path, re.IGNORECASE):
                    matches_include = True
                    break
            if not matches_include:
                return None
    else:
        # Legacy hardcoded patterns for backward compatibility
        # For Greenwich Peninsula: 
        # - Landlord/communal certs: \18.XX\Landlords\ (EXCLUDE these)
        # - Apartment certificates: \18.XX\Block - X\ (INCLUDE these - any cert type folder within blocks)
        if '\\Landlords\\' in doc_path or '/Landlords/' in doc_path:
            return None
        
        # Only process documents that are in block-specific folders (apartment certificates)
        # Must be in format: \18.XX\Block - X\ (where X is A, B, C, D, E, F, G)
        if not re.search(r'\\Block\s*-\s*[A-G]\\', doc_path):
            return None
    
    # GENERIC APPROACH: For all certificates in block folders, we're more lenient
    # Certificates might be misnamed but we still want to count them if they're in block folders
    # We'll try to extract apartment numbers but won't exclude them if we can't find one
    
    # SECONDARY FILTER: Exclusion patterns for title-based filtering
    # Since we're already filtering by path (block folders), we can be more lenient with title patterns
    # Only exclude very obvious communal patterns
    exclusion_patterns = [
        r'BLOCK\s+[A-G]\s*[-&]\s*[A-G]',  # Block A-B, Block F&G, etc. (multiple blocks)
        r'COMMUNAL',  # Communal areas
        r'CAR\s*PARK',  # Car park
        r'LIFT',  # Lift/elevator
        r'LEVEL\s+[0-9]+',  # Level 00, Level 9, etc.
        r'SCHEMATIC',  # Schematics
        r'TECHNICAL\s+SUBMITTAL',  # Technical submittals
        r'DESIGN\s+CERTIFICATE',  # Design certificates
        r'FIRE\s+CURTAIN',  # Fire curtains
        r'FIRE\s+DAMPER',  # Fire dampers
        r'CAR\s*PARK.*FIRE',  # Car park fire rated ductwork
        r'CAUSE\s+&\s+EFFECT',  # Cause & Effect Matrix
        r'CAR\s*PARK.*DUCTWORK',  # Car park fire rated ductwork
    ]
    
    # Check for exclusion patterns in title (secondary filter)
    # Since we're already filtering by path (block folders), we can be more lenient with title patterns
    # Only exclude very obvious communal patterns
    for pattern in exclusion_patterns:
        if re.search(pattern, search_text):
            return None
    
    # Pattern 5: FA Cert Plot XXX (specific pattern for Greenwich Peninsula)
    fa_cert_match = re.search(r'FA\s+CERT\s+PLOT\s+(\d{1,4})', search_text)
    if fa_cert_match:
        return int(fa_cert_match.group(1))
    
    # STRICT APPROACH: If we can't extract a valid apartment number, return None
    # We should not count certificates without plot numbers as this masks data quality issues
    # Only certificates with valid, extractable plot numbers should be counted
    return None


def extract_phase(doc_title: str, doc_ref: str, doc_path: str, phase_detection_config: Dict) -> Optional[str]:
    """
    Extract project phase from document metadata.
    
    Args:
        doc_title: Document title
        doc_ref: Document reference
        doc_path: Document path
        phase_detection_config: Configuration for phase detection patterns
        
    Returns:
        Phase identifier if found, None otherwise
    """
    if not phase_detection_config:
        return None
    
    if pd.isna(doc_title):
        doc_title = ""
    if pd.isna(doc_ref):
        doc_ref = ""
    if pd.isna(doc_path):
        doc_path = ""
    
    search_text = f"{doc_title} {doc_ref} {doc_path}"
    
    # Try doc title patterns first (most specific)
    doc_title_patterns = phase_detection_config.get('doc_title_patterns', [])
    for pattern in doc_title_patterns:
        match = re.search(pattern, doc_title, re.IGNORECASE)
        if match:
            return match.group(1) if match.groups() else match.group(0)
    
    # Try general patterns
    patterns = phase_detection_config.get('patterns', [])
    for pattern in patterns:
        match = re.search(pattern, search_text, re.IGNORECASE)
        if match:
            return match.group(1) if match.groups() else match.group(0)
    
    return None


def extract_block(doc_title: str, doc_ref: str, doc_path: str, block_detection_config: Dict) -> Optional[str]:
    """
    Extract building block from document metadata.
    
    Args:
        doc_title: Document title
        doc_ref: Document reference
        doc_path: Document path
        block_detection_config: Configuration for block detection patterns
        
    Returns:
        Block identifier if found, None otherwise
    """
    if not block_detection_config:
        return None
    
    if pd.isna(doc_title):
        doc_title = ""
    if pd.isna(doc_ref):
        doc_ref = ""
    if pd.isna(doc_path):
        doc_path = ""
    
    search_text = f"{doc_title} {doc_ref} {doc_path}"
    
    # Try doc title patterns first (most specific)
    doc_title_patterns = block_detection_config.get('doc_title_patterns', [])
    for pattern in doc_title_patterns:
        match = re.search(pattern, doc_title, re.IGNORECASE)
        if match:
            return match.group(1).upper() if match.groups() else match.group(0).upper()
    
    # Try general patterns
    patterns = block_detection_config.get('patterns', [])
    for pattern in patterns:
        match = re.search(pattern, search_text, re.IGNORECASE)
        if match:
            return match.group(1).upper() if match.groups() else match.group(0).upper()
    
    return None


def categorize_documents(df: pd.DataFrame, tracking_config: Dict, full_tracking_config: Dict = None) -> pd.DataFrame:
    """
    Categorize documents based on tracking configuration.
    
    Args:
        df: DataFrame containing document data
        tracking_config: Configuration dictionary with category definitions
        full_tracking_config: Full tracking configuration including phase/block detection (optional)
        
    Returns:
        DataFrame with added 'category', 'apartment_number', 'phase', and 'block' columns
    """
    result_df = df.copy()
    
    # Always add columns, even for empty DataFrame (needed for progress calculation)
    result_df['category'] = None  # Don't assign default category - only assign if valid match found
    result_df['apartment_number'] = None
    result_df['phase'] = None
    result_df['block'] = None
    
    if df.empty:
        return result_df
    
    # Extract phase and block information if configured
    if full_tracking_config:
        phase_detection = full_tracking_config.get('phase_detection', {})
        block_detection = full_tracking_config.get('block_detection', {})
        
        if phase_detection or block_detection:
            for idx in df.index:
                doc_title = df.loc[idx, 'Doc Title'] if 'Doc Title' in df.columns else ""
                doc_ref = df.loc[idx, 'Doc Ref'] if 'Doc Ref' in df.columns else ""
                doc_path = df.loc[idx, 'Doc Path'] if 'Doc Path' in df.columns else ""
                
                if phase_detection:
                    phase = extract_phase(doc_title, doc_ref, doc_path, phase_detection)
                    if phase:
                        result_df.loc[idx, 'phase'] = phase
                
                if block_detection:
                    block = extract_block(doc_title, doc_ref, doc_path, block_detection)
                    if block:
                        result_df.loc[idx, 'block'] = block
    
    # Process each category in the tracking config
    for category_name, category_config in tracking_config.items():
        if not isinstance(category_config, dict):
            continue
            
        # Get detection patterns for this category
        patterns = category_config.get('patterns', [])
        doc_ref_patterns = category_config.get('doc_ref_patterns', [])
        path_patterns = category_config.get('path_patterns', [])
        
        # Create mask for this category
        mask = pd.Series([False] * len(df), index=df.index)
        
        # Pattern matching on Doc Title
        if patterns:
            for pattern in patterns:
                pattern_mask = df['Doc Title'].fillna('').astype(str).str.contains(
                    re.escape(pattern), case=False, na=False
                )
                mask = mask | pattern_mask
        
        # Doc Ref pattern matching
        if doc_ref_patterns and 'Doc Ref' in df.columns:
            for pattern in doc_ref_patterns:
                ref_mask = df['Doc Ref'].fillna('').astype(str).str.contains(
                    rf'\b{re.escape(pattern)}\b', case=False, na=False, regex=True
                )
                mask = mask | ref_mask
        
        # Path pattern matching
        if path_patterns and 'Doc Path' in df.columns:
            for pattern in path_patterns:
                path_mask = df['Doc Path'].fillna('').astype(str).str.contains(
                    re.escape(pattern), case=False, na=False
                )
                mask = mask | path_mask
        
        # Get path filter config from full_tracking_config if available
        path_filter_config = None
        if full_tracking_config:
            document_detection = full_tracking_config.get('document_detection', {})
            path_filter_config = document_detection.get('path_filter', {})
        
        # Extract apartment numbers for matching documents and only categorize if apartment number exists
        for idx in df[mask].index:
            apartment_num = extract_apartment_number(
                df.loc[idx, 'Doc Title'],
                df.loc[idx, 'Doc Ref'] if 'Doc Ref' in df.columns else "",
                df.loc[idx, 'Doc Path'] if 'Doc Path' in df.columns else "",
                category_name,
                path_filter_config
            )
            # Only categorize if we successfully extracted a valid apartment number
            # This ensures data integrity and highlights missing/misnamed certificates
            if apartment_num is not None:
                result_df.loc[idx, 'category'] = category_name
                result_df.loc[idx, 'apartment_number'] = apartment_num
    
    return result_df


def get_uncategorized_certificates_in_blocks(all_certificates_df: pd.DataFrame, 
                                              categorized_df: pd.DataFrame) -> pd.DataFrame:
    """
    Find certificates that are in block folders but weren't categorized.
    These indicate potential naming issues or missing filters.
    
    Args:
        all_certificates_df: All certificate documents
        categorized_df: Categorized certificate documents
        
    Returns:
        DataFrame containing uncategorized certificates in block folders
    """
    # Find documents that are in block folders (apartment certificate locations)
    if 'Doc Path' not in all_certificates_df.columns:
        return pd.DataFrame()
    
    # Pattern to detect block folders: \18.XX\Block - X\
    in_block_folders = all_certificates_df[
        all_certificates_df['Doc Path'].fillna('').astype(str).str.contains(
            r'\\Block\s*-\s*[A-G]\\', 
            case=False, 
            na=False, 
            regex=True
        )
    ].copy()
    
    # Exclude documents that are in Landlords folders (communal certificates)
    in_block_folders = in_block_folders[
        ~in_block_folders['Doc Path'].fillna('').astype(str).str.contains(
            r'\\Landlords\\',
            case=False,
            na=False,
            regex=True
        )
    ]
    
    if in_block_folders.empty:
        return pd.DataFrame()
    
    # Find which ones were NOT categorized (no 'category' or category is NaN)
    categorized_indices = categorized_df[categorized_df['category'].notna()].index
    uncategorized = in_block_folders[~in_block_folders.index.isin(categorized_indices)].copy()
    
    # Extract block information for reporting
    def extract_block_from_path(path):
        match = re.search(r'\\Block\s*-\s*([A-G])\\', str(path), re.IGNORECASE)
        return match.group(1).upper() if match else 'Unknown'
    
    if not uncategorized.empty:
        uncategorized['extracted_block'] = uncategorized['Doc Path'].apply(extract_block_from_path)
    
    return uncategorized


def calculate_category_progress(categorized_df: pd.DataFrame, tracking_config: Dict, 
                                accommodation_data: Dict = None) -> Dict:
    """
    Calculate progress statistics for each category.
    
    Args:
        categorized_df: DataFrame with categorized documents
        tracking_config: Configuration dictionary with category definitions
        accommodation_data: Accommodation data from config (optional, provides accurate counts)
        
    Returns:
        Dictionary with progress statistics for each category
    """
    progress = {}
    
    # Get max count from accommodation data if available, otherwise from tracking config
    if accommodation_data and 'total_apartments' in accommodation_data:
        default_max_count = accommodation_data['total_apartments']
    else:
        default_max_count = 0
    
    for category_name, category_config in tracking_config.items():
        if not isinstance(category_config, dict):
            continue
        
        # Prefer accommodation data total, fallback to configured max_count
        max_count = category_config.get('max_count', default_max_count)
        if accommodation_data and 'total_apartments' in accommodation_data:
            max_count = accommodation_data['total_apartments']
        
        if max_count == 0:
            continue
        
        # Filter documents for this category
        category_docs = categorized_df[categorized_df['category'] == category_name]
        
        # Count unique apartments with documents
        # Only count apartments where we successfully extracted a valid plot number
        apartments_with_docs = category_docs['apartment_number'].dropna().nunique()
        
        # Calculate progress
        progress_pct = (apartments_with_docs / max_count * 100) if max_count > 0 else 0
        
        progress[category_name] = {
            'category_name': category_name,
            'documents_count': len(category_docs),
            'apartments_with_docs': apartments_with_docs,
            'max_apartments': max_count,
            'progress_percentage': round(progress_pct),
            'remaining_apartments': max_count - apartments_with_docs
        }
    
    return progress


def get_overall_progress(progress_stats: Dict) -> Dict:
    """
    Calculate overall progress across all categories.
    
    Args:
        progress_stats: Dictionary with progress statistics for each category
        
    Returns:
        Dictionary with overall progress statistics
    """
    if not progress_stats:
        return {
            'total_documents': 0,
            'total_apartments_with_docs': 0,
            'total_max_apartments': 0,
            'overall_progress_percentage': 0.0
        }
    
    total_documents = sum(stats['documents_count'] for stats in progress_stats.values())
    total_apartments_with_docs = sum(stats['apartments_with_docs'] for stats in progress_stats.values())
    total_max_apartments = sum(stats['max_apartments'] for stats in progress_stats.values())
    
    overall_progress = (total_apartments_with_docs / total_max_apartments * 100) if total_max_apartments > 0 else 0
    
    return {
        'total_documents': total_documents,
        'total_apartments_with_docs': total_apartments_with_docs,
        'total_max_apartments': total_max_apartments,
        'overall_progress_percentage': round(overall_progress)
    }


def calculate_progress_by_phase_block(categorized_df: pd.DataFrame, tracking_config: Dict, 
                                      full_tracking_config: Dict, accommodation_data: Dict = None,
                                      project_structure: Dict = None) -> Dict:
    """
    Calculate progress broken down by phase and block.
    
    Args:
        categorized_df: DataFrame with categorized documents (must include 'phase' and 'block' columns)
        tracking_config: Configuration dictionary with category definitions
        full_tracking_config: Full tracking configuration including phases definition
        accommodation_data: Accommodation data from config (provides accurate apartment counts)
        project_structure: Project structure from config (provides phase/block metadata)
        
    Returns:
        Dictionary with progress statistics by phase and block
    """
    phase_block_progress = {}
    
    # Use accommodation data for phase list and apartment counts
    if not accommodation_data or 'phases' not in accommodation_data:
        return phase_block_progress
    
    phases_source = accommodation_data['phases']
    
    # Calculate progress for each phase
    for phase_id, phase_config in phases_source.items():
        # Get apartment count from accommodation data
        phase_apartment_count = phase_config.get('apartment_count', 0)
        phase_blocks = phase_config.get('blocks', {})  # blocks is a dict in accommodation data
        
        # Get display name from PROJECT_STRUCTURE if available, otherwise use default
        if project_structure and 'phases' in project_structure and phase_id in project_structure['phases']:
            phase_display = project_structure['phases'][phase_id].get('display_name', f"Phase {phase_id}")
        else:
            phase_display = f"Phase {phase_id}"
        
        # Filter documents for this phase
        phase_docs = categorized_df[categorized_df['phase'] == phase_id]
        
        phase_stats = {}
        for category_name, category_config in tracking_config.items():
            if not isinstance(category_config, dict):
                continue
            
            category_docs = phase_docs[phase_docs['category'] == category_name]
            apartments_with_docs = category_docs['apartment_number'].dropna().nunique()
            
            phase_stats[category_name] = {
                'documents_count': len(category_docs),
                'apartments_with_docs': apartments_with_docs,
                'max_apartments': phase_apartment_count,
                'progress_percentage': round((apartments_with_docs / phase_apartment_count * 100)) if phase_apartment_count > 0 else 0
            }
        
        # Calculate progress for each block in this phase
        # phase_blocks is a dict where keys are block IDs
        block_stats = {}
        for block_id in phase_blocks.keys():
            block_docs = phase_docs[phase_docs['block'] == block_id]
            
            block_stats[block_id] = {}
            for category_name, category_config in tracking_config.items():
                if not isinstance(category_config, dict):
                    continue
                
                category_docs = block_docs[block_docs['category'] == category_name]
                apartments_with_docs = category_docs['apartment_number'].dropna().nunique()
                
                block_stats[block_id][category_name] = {
                    'documents_count': len(category_docs),
                    'apartments_with_docs': apartments_with_docs
                }
        
        phase_block_progress[phase_id] = {
            'display_name': phase_display,
            'phase_stats': phase_stats,
            'block_stats': block_stats
        }
    
    return phase_block_progress


def get_apartment_certificate_summary(categorized_df: pd.DataFrame, tracking_config: Dict, 
                                      full_tracking_config: Dict = None, accommodation_data: Dict = None,
                                      project_structure: Dict = None) -> Dict:
    """
    Get detailed summary of apartment certificate progress.
    
    Args:
        categorized_df: DataFrame with categorized documents
        tracking_config: Configuration dictionary
        full_tracking_config: Full tracking configuration including phase/block definitions (optional)
        accommodation_data: Accommodation data from config (provides apartment counts)
        project_structure: Project structure from config (provides phase/block metadata)
        
    Returns:
        Dictionary with detailed apartment certificate summary
    """
    # Calculate progress for each category
    progress_stats = calculate_category_progress(categorized_df, tracking_config, accommodation_data)
    
    # Get overall progress
    overall_progress = get_overall_progress(progress_stats)
    
    # Get apartment-level details
    apartment_details = {}
    for category_name in tracking_config.keys():
        if not isinstance(tracking_config[category_name], dict):
            continue
            
        category_docs = categorized_df[categorized_df['category'] == category_name]
        if category_docs.empty:
            continue
        
        # Group by apartment number
        apartment_groups = categorized_df[categorized_df['category'] == category_name].groupby('apartment_number').size()
        
        apartment_details[category_name] = {
            'apartments_with_docs': sorted(apartment_groups.index.tolist()),
            'apartments_missing': [],  # Could be calculated if we had the full apartment list
            'documents_per_apartment': apartment_groups.to_dict()
        }
    
    # Calculate phase/block progress if configured
    phase_block_progress = {}
    if full_tracking_config:
        phase_block_progress = calculate_progress_by_phase_block(
            categorized_df, tracking_config, full_tracking_config, accommodation_data, project_structure
        )
    
    return {
        'progress_stats': progress_stats,
        'overall_progress': overall_progress,
        'apartment_details': apartment_details,
        'phase_block_progress': phase_block_progress
    }


# =============================================================================
# LAYOUT TRACKING FUNCTIONS
# =============================================================================

def extract_apartment_types(doc_title: str, doc_ref: str = "", doc_path: str = "", 
                           type_patterns: Dict = None) -> List[str]:
    """
    Extract ALL apartment types from document metadata.
    
    Handles multiple types on single drawings (e.g., "TYPE 5 & 5A").
    
    Args:
        doc_title: Document title
        doc_ref: Document reference (optional)
        doc_path: Document path (optional)
        type_patterns: Dictionary of detection patterns from config
        
    Returns:
        List of apartment type codes found (may be empty)
    """
    if pd.isna(doc_title):
        doc_title = ""
    if pd.isna(doc_ref):
        doc_ref = ""
    if pd.isna(doc_path):
        doc_path = ""
    
    if not type_patterns:
        return []
    
    found_types = []
    
    # Try title patterns - find ALL matches, not just first
    for pattern in type_patterns.get('title_patterns', []):
        matches = re.findall(pattern, doc_title, re.IGNORECASE)
        for match in matches:
            # The match might be a string like "5 & 5A" or "30" or "1A"
            # Extract individual type codes from it
            type_codes = re.findall(r'\b([0-9]+[A-Za-z]?)\b', match)
            found_types.extend([code.upper() for code in type_codes])
    
    # Try doc ref patterns
    for pattern in type_patterns.get('doc_ref_patterns', []):
        matches = re.findall(pattern, doc_ref, re.IGNORECASE)
        for match in matches:
            type_codes = re.findall(r'\b([0-9]+[A-Za-z]?)\b', match)
            found_types.extend([code.upper() for code in type_codes])
    
    # Try path patterns
    for pattern in type_patterns.get('path_patterns', []):
        matches = re.findall(pattern, doc_path, re.IGNORECASE)
        for match in matches:
            type_codes = re.findall(r'\b([0-9]+[A-Za-z]?)\b', match)
            found_types.extend([code.upper() for code in type_codes])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_types = []
    for t in found_types:
        if t not in seen:
            seen.add(t)
            unique_types.append(t)
    
    return unique_types


def extract_floor_coverage(doc_title: str, doc_ref: str = "", doc_path: str = "",
                           floor_patterns: List[str] = None) -> List[int]:
    """
    Extract floor coverage from document (for communal layouts).
    
    Handles both single floors and multi-floor ranges (e.g., "Levels 04-08").
    
    Args:
        doc_title: Document title
        doc_ref: Document reference
        doc_path: Document path
        floor_patterns: List of regex patterns to detect floors
        
    Returns:
        List of floor numbers covered by this document
    """
    if pd.isna(doc_title):
        doc_title = ""
    if pd.isna(doc_ref):
        doc_ref = ""
    if pd.isna(doc_path):
        doc_path = ""
    
    if not floor_patterns:
        return []
    
    search_text = f"{doc_title} {doc_ref} {doc_path}"
    floors = set()
    
    # Handle special floor keywords first
    if re.search(r'Ground Floor', search_text, re.IGNORECASE):
        floors.add(0)
    if re.search(r'TO GROUND FLOOR', search_text, re.IGNORECASE):
        floors.add(0)
    if re.search(r'TO FIRST FLOOR', search_text, re.IGNORECASE):
        floors.add(1)
    # Note: Roof levels are not tracked numerically - they appear as "RF" in doc refs
    
    # Process complex patterns
    for pattern in floor_patterns:
        # Skip special floor patterns (already handled above)
        if 'Ground Floor' in pattern or 'Roof Level' in pattern:
            continue
            
        matches = list(re.finditer(pattern, search_text, re.IGNORECASE))
        
        for match in matches:
            groups = match.groups()
            
            # Handle different pattern types based on number of capture groups
            if len(groups) == 1:
                # Single floor: "Level 01"
                try:
                    floors.add(int(groups[0]))
                except (ValueError, IndexError):
                    pass
                    
            elif len(groups) == 2:
                # Range: "Level 20-29" or "Level 15 & 16"
                try:
                    first = int(groups[0])
                    second = int(groups[1])
                    
                    if '-' in match.group(0) or ' to ' in match.group(0).lower():
                        # Range pattern: 20-29 or "02 to 06"
                        floors.update(range(first, second + 1))
                    else:
                        # Multiple singles: 15 & 16
                        floors.update([first, second])
                except (ValueError, IndexError):
                    pass
                    
            elif len(groups) == 3:
                # Complex pattern: "Level 03-13 & 14" or "LEVELS 08, 09 & ROOF"
                try:
                    first = int(groups[0])
                    second = int(groups[1])
                    third = int(groups[2])
                    
                    if 'LEVELS' in match.group(0).upper():
                        # Multiple singles: "LEVELS 08, 09 & ROOF"
                        floors.update([first, second])
                        # Note: ROOF is not tracked numerically
                    else:
                        # Range + single: "Level 03-13 & 14"
                        floors.update(range(first, second + 1))
                        floors.add(third)
                except (ValueError, IndexError):
                    pass
    
    return sorted(list(floors))


def categorize_layouts(df: pd.DataFrame, layout_tracking_config: Dict,
                      accommodation_data: Dict = None) -> pd.DataFrame:
    """
    Categorize layout drawings based on tracking configuration.
    
    Similar to categorize_documents but specifically for layouts:
    - Apartment layouts: categorized by TYPE (not individual apartments)
    - Communal layouts: categorized by coverage (floor/multi-floor/building)
    - HANDLES MULTIPLE TYPES PER DOCUMENT by creating duplicate rows
    
    Args:
        df: DataFrame of filtered layout documents
        layout_tracking_config: Layout tracking configuration
        accommodation_data: Accommodation data for validation
        
    Returns:
        DataFrame with added columns: category, layout_type, apartment_type, 
        floor_coverage, block, phase
        Note: May have MORE rows than input if documents cover multiple types
    """
    if df.empty:
        return df.copy()
    
    # Track which documents have been categorized
    categorized_indices = set()
    expanded_rows = []
    
    # Process apartment layouts
    apartment_config = layout_tracking_config.get('categories', {}).get('apartment_layouts', {})
    if apartment_config.get('enabled', False):
        layout_types = apartment_config.get('layout_types', {})
        type_detection = apartment_config.get('apartment_type_detection', {})
        
        for layout_key, layout_config in layout_types.items():
            # Match documents for this layout type
            patterns = layout_config.get('patterns', [])
            doc_ref_patterns = layout_config.get('doc_ref_patterns', [])
            
            mask = pd.Series([False] * len(df), index=df.index)
            
            # Check title patterns
            for pattern in patterns:
                mask |= df['Doc Title'].fillna('').str.contains(pattern, case=False, na=False, regex=False)
            
            # Check doc ref patterns
            for pattern in doc_ref_patterns:
                mask |= df['Doc Ref'].fillna('').str.contains(pattern, case=False, na=False, regex=True)
            
            # For matching documents, extract ALL apartment types
            for idx in df[mask].index:
                apt_types = extract_apartment_types(
                    df.loc[idx, 'Doc Title'],
                    df.loc[idx, 'Doc Ref'] if 'Doc Ref' in df.columns else "",
                    df.loc[idx, 'Doc Path'] if 'Doc Path' in df.columns else "",
                    type_detection
                )
                
                # Create one row per apartment type found
                if apt_types:
                    categorized_indices.add(idx)  # Mark as categorized
                    for apt_type in apt_types:
                        row_dict = df.loc[idx].to_dict()
                        row_dict['category'] = 'apartment'
                        row_dict['layout_type'] = layout_key
                        row_dict['apartment_type'] = apt_type
                        row_dict['floor_coverage'] = None
                        row_dict['block'] = None
                        row_dict['phase'] = None
                        expanded_rows.append(row_dict)
    
    # Process communal layouts (not expanded for now)
    communal_config = layout_tracking_config.get('categories', {}).get('communal_layouts', {})
    if communal_config.get('enabled', False):
        layout_types = communal_config.get('layout_types', {})
        coverage_detection = communal_config.get('coverage_detection', {})
        
        for layout_key, layout_config in layout_types.items():
            patterns = layout_config.get('patterns', [])
            doc_ref_patterns = layout_config.get('doc_ref_patterns', [])
            
            mask = pd.Series([False] * len(df), index=df.index)
            
            # Check title patterns
            for pattern in patterns:
                mask |= df['Doc Title'].fillna('').str.contains(pattern, case=False, na=False, regex=False)
            
            # Check doc ref patterns
            for pattern in doc_ref_patterns:
                mask |= df['Doc Ref'].fillna('').str.contains(pattern, case=False, na=False, regex=True)
            
            # For matching documents, extract floor coverage
            for idx in df[mask].index:
                floors = extract_floor_coverage(
                    df.loc[idx, 'Doc Title'],
                    df.loc[idx, 'Doc Ref'] if 'Doc Ref' in df.columns else "",
                    df.loc[idx, 'Doc Path'] if 'Doc Path' in df.columns else "",
                    coverage_detection.get('floor_patterns', [])
                )
                
                # Categorize communal layout
                categorized_indices.add(idx)  # Mark as categorized
                row_dict = df.loc[idx].to_dict()
                row_dict['category'] = 'communal'
                row_dict['layout_type'] = layout_key
                row_dict['apartment_type'] = None
                row_dict['floor_coverage'] = str(floors) if floors else '[]'
                row_dict['block'] = None
                row_dict['phase'] = None
                expanded_rows.append(row_dict)
    
    # Add uncategorized documents (those NOT matched by any category)
    for idx in df.index:
        if idx not in categorized_indices:
            row_dict = df.loc[idx].to_dict()
            row_dict['category'] = None
            row_dict['layout_type'] = None
            row_dict['apartment_type'] = None
            row_dict['floor_coverage'] = None
            row_dict['block'] = None
            row_dict['phase'] = None
            expanded_rows.append(row_dict)
    
    # Create result DataFrame from expanded rows
    result_df = pd.DataFrame(expanded_rows)
    
    # Extract phase and block for categorized layouts
    block_detection_config = layout_tracking_config.get('block_detection', {})
    
    for idx in result_df[result_df['category'].notna()].index:
        doc_title = result_df.loc[idx, 'Doc Title']
        doc_ref = result_df.loc[idx, 'Doc Ref'] if 'Doc Ref' in result_df.columns else ""
        doc_path = result_df.loc[idx, 'Doc Path'] if 'Doc Path' in result_df.columns else ""
        
        # Extract phase (if available in config)
        phase = extract_phase(doc_title, doc_ref, doc_path, layout_tracking_config)
        if phase:
            result_df.loc[idx, 'phase'] = phase
        
        # Extract block using proper block_detection config
        block = extract_block(doc_title, doc_ref, doc_path, block_detection_config)
        if block:
            result_df.loc[idx, 'block'] = block
    
    return result_df


def normalize_type_code(type_code: str) -> str:
    """
    Normalize apartment type codes for comparison.
    
    Handles:
    - Case normalization (01a -> 01A)
    - Leading zero removal (01A -> 1A, but 01a -> 1a)
    - Returns normalized version for matching
    
    Args:
        type_code: Original type code (e.g., "01a", "1A", "13a")
        
    Returns:
        Normalized type code for comparison
    """
    if not type_code:
        return ""
    
    # Convert to uppercase
    normalized = type_code.upper()
    
    # Remove leading zeros from the numeric part
    # Pattern: optional leading zeros + digits + optional letter
    import re
    match = re.match(r'^0*(\d+)([A-Z]?)$', normalized)
    if match:
        digits = match.group(1)
        letter = match.group(2)
        normalized = digits + letter
    
    return normalized


def calculate_apartment_layout_progress(categorized_df: pd.DataFrame, 
                                        layout_tracking_config: Dict,
                                        accommodation_data: Dict = None) -> Dict:
    """
    Calculate progress for apartment layouts.
    
    For apartment layouts, we count:
    - How many apartment TYPES have each layout type
    - Which apartment types are missing layouts
    
    Args:
        categorized_df: DataFrame with categorized layouts
        layout_tracking_config: Layout tracking configuration
        accommodation_data: Accommodation schedule data
        
    Returns:
        Dictionary with progress statistics per layout type
    """
    apartment_layouts = categorized_df[categorized_df['category'] == 'apartment']
    
    if apartment_layouts.empty:
        return {}
    
    # Get expected apartment types from accommodation data
    expected_types = set()
    if accommodation_data and 'apartment_types' in accommodation_data:
        expected_types = set(accommodation_data['apartment_types'].keys())
    
    total_types = len(expected_types) if expected_types else 0
    
    # Calculate progress for each layout type
    apartment_config = layout_tracking_config.get('categories', {}).get('apartment_layouts', {})
    layout_types_config = apartment_config.get('layout_types', {})
    
    progress = {}
    for layout_key, layout_config in layout_types_config.items():
        layout_docs = apartment_layouts[apartment_layouts['layout_type'] == layout_key]
        
        # Get unique apartment types that have this layout
        types_with_layout = set(layout_docs['apartment_type'].dropna().unique())
        
        # Calculate duplicates: apartment types with more than one layout document
        type_counts = layout_docs['apartment_type'].dropna().value_counts()
        duplicate_types = type_counts[type_counts > 1]
        total_duplicates = (duplicate_types - 1).sum()  # Extra documents beyond the first
        
        # Get greylisted apartment types (optional types that don't count as missing)
        greylisted_types = set(layout_config.get('greylisted_apartment_types', []))
        
        # Calculate missing types with normalized matching (case + leading zeros)
        # Create a mapping of normalized -> original for found types
        found_types_map = {normalize_type_code(t): t for t in types_with_layout}
        
        # Check which expected types are missing (normalized matching)
        missing_types = set()
        greylisted_missing_types = set()
        types_matched = set()
        
        for expected_type in expected_types:
            normalized_expected = normalize_type_code(expected_type)
            if normalized_expected in found_types_map:
                # Found (normalized match)
                types_matched.add(expected_type)
            else:
                # Check if this type is greylisted
                if expected_type in greylisted_types or normalize_type_code(expected_type) in {normalize_type_code(t) for t in greylisted_types}:
                    greylisted_missing_types.add(expected_type)
                else:
                    # Missing (and required)
                    missing_types.add(expected_type)
        
        # Calculate percentage based on matched types + greylisted types (both count as "complete")
        required_types = total_types - len(greylisted_types)
        if required_types > 0:
            coverage_pct = (len(types_matched) / required_types) * 100
        else:
            coverage_pct = 100 if len(types_matched) > 0 else 0
        
        # Unique document count = total docs - duplicates
        unique_document_count = len(types_with_layout)
        
        progress[layout_key] = {
            'display_name': layout_config.get('display_name', layout_key),
            'types_with_layout': len(types_matched),  # Count of matched types (case-insensitive)
            'types_covered': sorted(list(types_matched)),  # Show expected types that were matched
            'missing_types': sorted(list(missing_types)),
            'greylisted_missing_types': sorted(list(greylisted_missing_types)),  # Missing but optional
            'total_expected_types': total_types,
            'total_required_types': required_types,  # Total minus greylisted
            'coverage_percentage': round(coverage_pct, 1),
            'document_count': len(layout_docs),  # Total documents including duplicates
            'unique_document_count': unique_document_count,  # Unique apartment types with layouts
            'duplicate_count': int(total_duplicates),  # Number of alternative/duplicate layouts
            'duplicate_types': sorted(duplicate_types.index.tolist()) if len(duplicate_types) > 0 else [],
            'required': layout_config.get('required', False)
        }
    
    return progress


def calculate_communal_layout_progress(categorized_df: pd.DataFrame,
                                       layout_tracking_config: Dict,
                                       accommodation_data: Dict = None) -> Dict:
    """
    Calculate progress for communal layouts.
    
    For communal layouts, we count:
    - Floor coverage for each layout type per block
    - Which floors/blocks are missing layouts
    - Handle multi-block layouts and special floors (roof, ground)
    
    Args:
        categorized_df: DataFrame with categorized layouts
        layout_tracking_config: Layout tracking configuration
        accommodation_data: Accommodation schedule data
        
    Returns:
        Dictionary with progress statistics per layout type
    """
    communal_layouts = categorized_df[categorized_df['category'] == 'communal']
    
    if communal_layouts.empty:
        return {}
    
    # Use floor counts from PROJECT_STRUCTURE if available, otherwise fall back to accommodation data
    expected_floors_by_block = {}
    all_expected_floors = set()
    
    # Check if PROJECT_STRUCTURE has block floor definitions
    project_structure = layout_tracking_config.get('project_structure', {})
    blocks_config = project_structure.get('blocks', {})
    
    if blocks_config:
        # Use PROJECT_STRUCTURE floor definitions
        for block_name, block_data in blocks_config.items():
            floors_list = block_data.get('expected_floors', [])
            if floors_list:
                expected_floors_by_block[block_name] = set(floors_list)
                all_expected_floors.update(floors_list)
        
        # Use defined floors as-is - ground (0) and roof floors only counted if detected, never expected
    else:
        # Fall back to accommodation data (old logic)
        if accommodation_data and 'phases' in accommodation_data:
            for phase_data in accommodation_data['phases'].values():
                for block_name, block_data in phase_data.get('blocks', {}).items():
                    floors = set(block_data.get('floors', []))
                    expected_floors_by_block[block_name] = floors
                    all_expected_floors.update(floors)
        
        # Convert to 1-based floors (exclude ground floor 0)
        for block_name, floors in expected_floors_by_block.items():
            if floors:
                max_floor = max(floors)
                expected_floors_by_block[block_name] = set(range(1, max_floor + 1))
        
        all_expected_floors = set()
        for floors in expected_floors_by_block.values():
            all_expected_floors.update(floors)
    
    # Add special floors that might not be in accommodation data
    # Ground floor (0) and roof (max floor + 1) are common for some layout types
    # But not all communal layouts need ground/roof coverage (e.g., mechanical services)
    # For now, we'll only add them if they're explicitly in accommodation data
    # This prevents false "missing" reports for floors that don't need layouts
    
    # Calculate progress for each layout type
    communal_config = layout_tracking_config.get('categories', {}).get('communal_layouts', {})
    layout_types_config = communal_config.get('layout_types', {})
    
    progress = {}
    for layout_key, layout_config in layout_types_config.items():
        layout_docs = communal_layouts[communal_layouts['layout_type'] == layout_key]
        
        # Track coverage by block
        coverage_by_block = {}
        total_missing_floors = set()
        document_details = []
        
        for _, doc in layout_docs.iterrows():
            # Parse floor coverage from the document
            floor_coverage_str = doc.get('floor_coverage', '')
            doc_title = doc.get('Doc Title', '')
            
            try:
                covered_floors = eval(floor_coverage_str) if floor_coverage_str else []
            except:
                covered_floors = []
            
            # Extract block information from title
            blocks_covered = extract_blocks_from_title(doc_title)
            
            # Store document details
            doc_info = {
                'title': doc_title,
                'blocks': blocks_covered,
                'floors': covered_floors,
                'coverage_type': 'multi-block' if len(blocks_covered) > 1 else 'single-block'
            }
            document_details.append(doc_info)
            
            # Update coverage by block
            for block in blocks_covered:
                if block not in coverage_by_block:
                    coverage_by_block[block] = set()
                coverage_by_block[block].update(covered_floors)
        
        # Get greylisted blocks (blocks that don't require this layout)
        greylisted_blocks = set(layout_config.get('greylisted_blocks', []))
        
        # Calculate missing floors per block and total covered floors
        total_missing_floors = set()
        greylisted_missing_blocks = {}  # {block: [missing floors]}
        total_covered_count = 0
        total_required_floors = 0
        
        for block_name, expected_floors in expected_floors_by_block.items():
            # Skip greylisted blocks in coverage calculations
            is_greylisted = block_name in greylisted_blocks
            
            covered_in_block = coverage_by_block.get(block_name, set())
            missing_in_block = expected_floors - covered_in_block
            
            if is_greylisted:
                # Track greylisted blocks separately
                if missing_in_block:
                    greylisted_missing_blocks[block_name] = sorted(list(missing_in_block))
            else:
                # Count towards required coverage
                total_missing_floors.update(missing_in_block)
                # Count how many expected floors are covered for this block
                covered_expected_floors = expected_floors & covered_in_block
                total_covered_count += len(covered_expected_floors)
                total_required_floors += len(expected_floors)
        
        # Calculate overall percentage using only required blocks (not greylisted)
        # Each floor in each block counts separately for communal layouts
        total_expected_floors = sum(len(expected_floors) for block_name, expected_floors in expected_floors_by_block.items() 
                                   if block_name not in greylisted_blocks)
        
        if total_required_floors > 0:
            coverage_pct = (total_covered_count / total_required_floors) * 100
        else:
            coverage_pct = 100 if total_covered_count > 0 else 0
        
        progress[layout_key] = {
            'display_name': layout_config.get('display_name', layout_key),
            'floors_covered': total_covered_count,
            'floors_missing': sorted(list(total_missing_floors)),
            'total_expected_floors': total_expected_floors,
            'total_required_floors': total_required_floors,  # Excludes greylisted blocks
            'coverage_percentage': round(coverage_pct, 1),
            'document_count': len(layout_docs),
            'coverage_by_block': {block: sorted(list(floors)) for block, floors in coverage_by_block.items()},
            'expected_floors_by_block': {block: sorted(list(floors)) for block, floors in expected_floors_by_block.items()},
            'greylisted_blocks': sorted(list(greylisted_blocks)),
            'greylisted_missing_blocks': greylisted_missing_blocks,  # {block: [missing floors]}
            'document_details': document_details,
            'coverage_type': 'block-based'
        }
    
    return progress


def extract_blocks_from_title(doc_title: str) -> List[str]:
    """
    Extract block names from document title.
    
    Handles:
    - Single blocks: "Block B" -> ["B"]
    - Multi blocks: "Block G&F" -> ["G", "F"] 
    - Multi blocks: "Block F&G" -> ["F", "G"]
    - Plot identifiers: "Plot 18.03" -> ["18.03"]
    
    Args:
        doc_title: Document title
        
    Returns:
        List of block names
    """
    import re
    
    blocks = []
    
    # Pattern to match "Block X" or "Block X&Y" or "Block Y&X"
    block_pattern = r'Block\s+([A-Z](?:&[A-Z])*)'
    match = re.search(block_pattern, doc_title, re.IGNORECASE)
    
    if match:
        blocks_str = match.group(1).upper()
        # Split by & to get individual blocks
        blocks.extend([block.strip() for block in blocks_str.split('&')])
    
    # Pattern to match "Plot X.Y" 
    plot_pattern = r'Plot\s+([0-9]+\.[0-9]+)'
    plot_match = re.search(plot_pattern, doc_title, re.IGNORECASE)
    
    if plot_match:
        plot_id = plot_match.group(1)
        blocks.append(plot_id)
    
    return blocks


def get_layout_tracking_summary(latest_data: pd.DataFrame, layout_tracking_config: Dict,
                                accommodation_data: Dict = None, project_structure: Dict = None) -> Dict:
    """
    Main entry point for layout tracking analysis.
    
    Args:
        latest_data: DataFrame of latest documents
        layout_tracking_config: Layout tracking configuration
        accommodation_data: Accommodation schedule data
        project_structure: Project structure (phases, blocks, expected floors)
        
    Returns:
        Dictionary with complete layout tracking summary
    """
    if latest_data.empty or not layout_tracking_config.get('enabled', False):
        return {}
    
    # Inject project_structure into layout_tracking_config for use by sub-functions
    if project_structure:
        layout_tracking_config = layout_tracking_config.copy()
        layout_tracking_config['project_structure'] = project_structure
    
    # Filter to only layout drawings based on detection patterns
    detection = layout_tracking_config.get('detection', {})
    
    mask = pd.Series([False] * len(latest_data), index=latest_data.index)
    
    # Filter by file type
    for file_type in detection.get('file_type_patterns', []):
        mask |= latest_data['File Type'].fillna('').str.contains(file_type, case=False, na=False)
    
    # Filter by doc ref patterns
    if 'Doc Ref' in latest_data.columns:
        for pattern in detection.get('doc_ref_patterns', []):
            mask |= latest_data['Doc Ref'].fillna('').str.contains(pattern, case=False, na=False, regex=True)
    
    # Exclude patterns
    for exclude_pattern in detection.get('exclude_patterns', []):
        mask &= ~latest_data['Doc Title'].fillna('').str.contains(exclude_pattern, case=False, na=False)
    
    layout_drawings = latest_data[mask].copy()
    
    if layout_drawings.empty:
        return {'total_layouts': 0, 'message': 'No layout drawings found'}
    
    # CRITICAL: Exclude withdrawn documents
    # Check multiple columns for withdrawn status
    withdrawn_mask = pd.Series([False] * len(layout_drawings), index=layout_drawings.index)
    
    # Check doc title for "Withdrawn"
    withdrawn_mask |= layout_drawings['Doc Title'].fillna('').str.contains('Withdrawn', case=False, na=False)
    
    # Check status column if it exists
    if 'Status' in layout_drawings.columns:
        withdrawn_mask |= layout_drawings['Status'].fillna('').str.contains('Withdrawn', case=False, na=False)
    
    # Check purpose of issue if it exists
    if 'Purpose of Issue' in layout_drawings.columns:
        withdrawn_mask |= layout_drawings['Purpose of Issue'].fillna('').str.contains('Withdrawn', case=False, na=False)
    
    # Count withdrawn for reporting
    withdrawn_count = withdrawn_mask.sum()
    
    # Remove withdrawn documents
    layout_drawings = layout_drawings[~withdrawn_mask].copy()
    
    if layout_drawings.empty:
        return {'total_layouts': 0, 'withdrawn_count': withdrawn_count, 'message': 'No non-withdrawn layout drawings found'}
    
    # Categorize layouts
    categorized = categorize_layouts(layout_drawings, layout_tracking_config, accommodation_data)
    
    # Calculate progress
    apartment_progress = calculate_apartment_layout_progress(categorized, layout_tracking_config, accommodation_data)
    communal_progress = calculate_communal_layout_progress(categorized, layout_tracking_config, accommodation_data)
    
    # Count uncategorized
    uncategorized = categorized[categorized['category'].isna()]
    
    return {
        'total_layouts': len(layout_drawings),
        'withdrawn_count': withdrawn_count,
        'categorized': len(categorized[categorized['category'].notna()]),
        'uncategorized': len(uncategorized),
        'apartment_progress': apartment_progress,
        'communal_progress': communal_progress,
        'categorized_data': categorized
    }
