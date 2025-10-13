"""Data cleaning and normalization utilities."""

import pandas as pd


def clean_revision(val):
    """Clean and normalize revision values.
    
    Args:
        val: Revision value to clean
        
    Returns:
        str: Cleaned revision string
    """
    if pd.isna(val):
        return ''
    s = str(val).replace('\u00A0', ' ').strip().upper()
    # Replace Cyrillic 'С' (U+0421) with Latin 'C'
    s = s.replace('\u0421', 'C')
    return s

