"""Generic document tracking system for certificates and drawings.

This module provides flexible tracking for different document categories
(e.g., apartment certificates, communal certificates, apartment layouts)
with configurable detection patterns and progress visualization.

Supports optional phase and block tracking for projects completed in multiple phases.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Optional


def extract_apartment_number(doc_title: str, doc_ref: str = "", doc_path: str = "", category: str = None) -> Optional[int]:
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
    
    # Pattern 3: "Apt XXX" or "APT XXX"
    apt_match = re.search(r'APT\s+(\d{1,4})', search_text)
    if apt_match:
        return int(apt_match.group(1))
    
    # Pattern 4: "Flat XXX" or "FLAT XXX" (lower priority - might be postal address)
    flat_match = re.search(r'FLAT\s+(\d{1,4})', search_text)
    if flat_match:
        return int(flat_match.group(1))
    
    # PRIMARY FILTER: Use document path to distinguish landlord/communal vs apartment certificates
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
    if df.empty:
        return df
    
    result_df = df.copy()
    result_df['category'] = None  # Don't assign default category - only assign if valid match found
    result_df['apartment_number'] = None
    result_df['phase'] = None
    result_df['block'] = None
    
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
        
        # Extract apartment numbers for matching documents and only categorize if apartment number exists
        for idx in df[mask].index:
            apartment_num = extract_apartment_number(
                df.loc[idx, 'Doc Title'],
                df.loc[idx, 'Doc Ref'] if 'Doc Ref' in df.columns else "",
                df.loc[idx, 'Doc Path'] if 'Doc Path' in df.columns else "",
                category_name
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
            'progress_percentage': round(progress_pct, 1),
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
        'overall_progress_percentage': round(overall_progress, 1)
    }


def calculate_progress_by_phase_block(categorized_df: pd.DataFrame, tracking_config: Dict, 
                                      full_tracking_config: Dict, accommodation_data: Dict = None) -> Dict:
    """
    Calculate progress broken down by phase and block.
    
    Args:
        categorized_df: DataFrame with categorized documents (must include 'phase' and 'block' columns)
        tracking_config: Configuration dictionary with category definitions
        full_tracking_config: Full tracking configuration including phases definition
        accommodation_data: Accommodation data from config (optional, provides accurate counts)
        
    Returns:
        Dictionary with progress statistics by phase and block
    """
    phase_block_progress = {}
    
    # Prefer accommodation data phases if available
    if accommodation_data and 'phases' in accommodation_data:
        phases_source = accommodation_data['phases']
        using_accom_data = True
    else:
        phases_source = full_tracking_config.get('phases', {})
        using_accom_data = False
    
    if not phases_source:
        return phase_block_progress
    
    # Calculate progress for each phase
    for phase_id, phase_config in phases_source.items():
        if using_accom_data:
            phase_display = f"Phase {phase_id}"
            phase_apartment_count = phase_config.get('apartment_count', 0)
            phase_blocks = phase_config.get('blocks', [])  # blocks is already a list in accommodation data
        else:
            phase_display = phase_config.get('display_name', phase_id)
            phase_apartment_count = phase_config.get('apartment_count', 0)
            phase_blocks = phase_config.get('blocks', [])
        
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
                'progress_percentage': round((apartments_with_docs / phase_apartment_count * 100), 1) if phase_apartment_count > 0 else 0
            }
        
        # Calculate progress for each block in this phase
        block_stats = {}
        for block_id in phase_blocks:
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
                                      full_tracking_config: Dict = None, accommodation_data: Dict = None) -> Dict:
    """
    Get detailed summary of apartment certificate progress.
    
    Args:
        categorized_df: DataFrame with categorized documents
        tracking_config: Configuration dictionary
        full_tracking_config: Full tracking configuration including phase/block definitions (optional)
        
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
        apartment_groups = category_docs.groupby('apartment_number').size()
        
        apartment_details[category_name] = {
            'apartments_with_docs': sorted(apartment_groups.index.tolist()),
            'apartments_missing': [],  # Could be calculated if we had the full apartment list
            'documents_per_apartment': apartment_groups.to_dict()
        }
    
    # Calculate phase/block progress if configured
    phase_block_progress = {}
    if full_tracking_config:
        phase_block_progress = calculate_progress_by_phase_block(
            categorized_df, tracking_config, full_tracking_config, accommodation_data
        )
    
    return {
        'progress_stats': progress_stats,
        'overall_progress': overall_progress,
        'apartment_details': apartment_details,
        'phase_block_progress': phase_block_progress
    }
