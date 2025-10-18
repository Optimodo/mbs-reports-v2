"""Document filtering utilities for certificates, technical submittals, and drawings."""

import pandas as pd
import re


def filter_certificates(df, config):
    """
    Filter documents to return only certificates based on project config.
    
    Supports two filtering methods:
    1. File type column matching (e.g., 'CT - Certificate (CT)')
    2. Doc Ref pattern matching (e.g., 2-letter codes like 'CT', 'CE')
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        
    Returns:
        DataFrame containing only certificate documents
    """
    if df.empty:
        return df
    
    cert_settings = config.get('CERTIFICATE_SETTINGS', {})
    if not cert_settings.get('enabled', False):
        return pd.DataFrame()  # Return empty DataFrame if certificates not enabled
    
    mask = pd.Series([False] * len(df), index=df.index)
    
    # Method 1: File type column filtering
    file_type_filter = cert_settings.get('file_type_filter', {})
    if file_type_filter.get('enabled', False):
        file_type_col = file_type_filter.get('column_name')
        cert_types = file_type_filter.get('certificate_types', [])
        
        if file_type_col and file_type_col in df.columns and cert_types:
            for cert_type in cert_types:
                type_mask = df[file_type_col].fillna('').astype(str).str.contains(
                    re.escape(cert_type), 
                    case=False, 
                    na=False
                )
                mask = mask | type_mask
    
    # Method 2: Doc Ref pattern filtering
    doc_ref_filter = cert_settings.get('doc_ref_filter', {})
    if doc_ref_filter.get('enabled', False):
        doc_ref_col = doc_ref_filter.get('column_name', 'Doc Ref')
        cert_patterns = doc_ref_filter.get('certificate_patterns', [])
        
        if doc_ref_col in df.columns and cert_patterns:
            for pattern in cert_patterns:
                # Create regex pattern: match the 2-letter code anywhere in Doc Ref
                # Pattern should match things like: "MBS-XXX-CT-001" or "PROJECT-CE-001"
                regex_pattern = rf'\b{re.escape(pattern)}\b'
                ref_mask = df[doc_ref_col].fillna('').astype(str).str.contains(
                    regex_pattern,
                    case=False,
                    na=False,
                    regex=True
                )
                mask = mask | ref_mask
    
    return df[mask].copy()


def filter_technical_submittals(df, config):
    """
    Filter documents to return only technical submittals based on project config.
    
    Supports two filtering methods:
    1. File type column matching (e.g., 'TX - Technical Submittals (TX)')
    2. Doc Ref pattern matching (e.g., 2-letter codes like 'TX', 'TS')
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        
    Returns:
        DataFrame containing only technical submittal documents
    """
    if df.empty:
        return df
    
    ts_settings = config.get('TECHNICAL_SUBMITTAL_SETTINGS', {})
    if not ts_settings.get('enabled', False):
        return pd.DataFrame()  # Return empty DataFrame if technical submittals not enabled
    
    mask = pd.Series([False] * len(df), index=df.index)
    
    # Method 1: File type column filtering
    file_type_filter = ts_settings.get('file_type_filter', {})
    if file_type_filter.get('enabled', False):
        file_type_col = file_type_filter.get('column_name')
        ts_types = file_type_filter.get('technical_submittal_types', [])
        
        if file_type_col and file_type_col in df.columns and ts_types:
            for ts_type in ts_types:
                type_mask = df[file_type_col].fillna('').astype(str).str.contains(
                    re.escape(ts_type),
                    case=False,
                    na=False
                )
                mask = mask | type_mask
    
    # Method 2: Doc Ref pattern filtering
    doc_ref_filter = ts_settings.get('doc_ref_filter', {})
    if doc_ref_filter.get('enabled', False):
        doc_ref_col = doc_ref_filter.get('column_name', 'Doc Ref')
        ts_patterns = doc_ref_filter.get('technical_submittal_patterns', [])
        
        if doc_ref_col in df.columns and ts_patterns:
            for pattern in ts_patterns:
                regex_pattern = rf'\b{re.escape(pattern)}\b'
                ref_mask = df[doc_ref_col].fillna('').astype(str).str.contains(
                    regex_pattern,
                    case=False,
                    na=False,
                    regex=True
                )
                mask = mask | ref_mask
    
    return df[mask].copy()


def filter_drawings_and_schematics(df, config):
    """
    Filter documents to return only drawings and schematics based on project config.
    
    This is the main document type that the summary report focuses on.
    Supports two filtering methods:
    1. File type column exact matching (e.g., 'DR - Drawings (DR)')
    2. Doc Ref pattern matching (e.g., 2-letter codes like 'DR', 'DRG')
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        
    Returns:
        DataFrame containing only drawing and schematic documents
    """
    if df.empty:
        return df
    
    drawing_settings = config.get('DRAWING_SETTINGS', {})
    if not drawing_settings.get('enabled', False):
        return df  # If not configured, return all documents (backwards compatible)
    
    mask = pd.Series([False] * len(df), index=df.index)
    
    # Method 1: File type column filtering (EXACT matches)
    file_type_filter = drawing_settings.get('file_type_filter', {})
    if file_type_filter.get('enabled', False):
        file_type_col = file_type_filter.get('column_name')
        drawing_types = file_type_filter.get('drawing_types', [])
        
        if file_type_col and file_type_col in df.columns and drawing_types:
            # Use .isin() for exact matching instead of .contains()
            type_mask = df[file_type_col].fillna('').astype(str).isin(drawing_types)
            mask = mask | type_mask
    
    # Method 2: Doc Ref pattern filtering
    doc_ref_filter = drawing_settings.get('doc_ref_filter', {})
    if doc_ref_filter.get('enabled', False):
        doc_ref_col = doc_ref_filter.get('column_name', 'Doc Ref')
        drawing_patterns = doc_ref_filter.get('drawing_patterns', [])
        
        if doc_ref_col in df.columns and drawing_patterns:
            for pattern in drawing_patterns:
                # Create regex pattern: match the 2-letter code anywhere in Doc Ref
                regex_pattern = rf'\b{re.escape(pattern)}\b'
                ref_mask = df[doc_ref_col].fillna('').astype(str).str.contains(
                    regex_pattern,
                    case=False,
                    na=False,
                    regex=True
                )
                mask = mask | ref_mask
    
    # If no filters were configured or no matches, return all documents (backwards compatible)
    if not mask.any():
        return df
    
    return df[mask].copy()


def get_main_report_data(df, config):
    """
    Get filtered data for main summary report.
    
    This excludes certificates and technical submittals, focusing on
    drawings and schematics (the main document types for the summary report).
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        
    Returns:
        DataFrame containing documents for main summary report
        (excludes certificates and technical submittals)
    """
    if df.empty:
        return df
    
    # Start with all documents
    filtered_df = df.copy()
    
    # Remove certificates
    cert_df = filter_certificates(df, config)
    if not cert_df.empty:
        filtered_df = filtered_df[~filtered_df.index.isin(cert_df.index)]
    
    # Remove technical submittals
    ts_df = filter_technical_submittals(df, config)
    if not ts_df.empty:
        filtered_df = filtered_df[~filtered_df.index.isin(ts_df.index)]
    
    # Optionally filter to only drawings/schematics if configured
    drawing_settings = config.get('DRAWING_SETTINGS', {})
    if drawing_settings.get('enabled', False):
        filtered_df = filter_drawings_and_schematics(filtered_df, config)
    
    return filtered_df


def get_document_type_summary(df, config):
    """
    Get a summary of document types for debugging/logging.
    
    Args:
        df: DataFrame containing document data
        config: Project configuration dictionary
        
    Returns:
        Dictionary with counts for each document type category
    """
    summary = {
        'total': len(df),
        'certificates': len(filter_certificates(df, config)),
        'technical_submittals': len(filter_technical_submittals(df, config)),
        'main_report_docs': len(get_main_report_data(df, config))
    }
    
    return summary

