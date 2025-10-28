"""Data cleaning and normalization utilities."""

import pandas as pd


def normalize_cyrillic_to_ascii(text):
    """Convert Cyrillic characters that look like Latin to actual Latin characters.
    
    Handles the common issue where Cyrillic characters are used instead of Latin
    (e.g., when copy-pasting from Russian Excel or other sources).
    This causes pattern matching to fail since В (Cyrillic) != B (Latin).
    
    Args:
        text: String to normalize
        
    Returns:
        str: String with all Cyrillic lookalikes converted to Latin
    """
    if pd.isna(text):
        return ''
    
    s = str(text)
    
    # Cyrillic to Latin character mapping
    # These Cyrillic characters look identical to Latin but have different Unicode values
    cyrillic_to_latin = {
        # Uppercase Cyrillic → Latin
        '\u0410': 'A',  # Cyrillic А → Latin A
        '\u0412': 'B',  # Cyrillic В → Latin B  
        '\u0421': 'C',  # Cyrillic С → Latin C (most common in revisions)
        '\u0415': 'E',  # Cyrillic Е → Latin E
        '\u041D': 'H',  # Cyrillic Н → Latin H
        '\u041A': 'K',  # Cyrillic К → Latin K
        '\u041C': 'M',  # Cyrillic М → Latin M
        '\u041E': 'O',  # Cyrillic О → Latin O (common in apartment types like OO-1)
        '\u0420': 'P',  # Cyrillic Р → Latin P
        '\u0422': 'T',  # Cyrillic Т → Latin T
        '\u0425': 'X',  # Cyrillic Х → Latin X
        # Lowercase Cyrillic → Latin
        '\u0430': 'a',
        '\u0432': 'b',
        '\u0441': 'c',
        '\u0435': 'e',
        '\u043D': 'h',
        '\u043A': 'k',
        '\u043C': 'm',
        '\u043E': 'o',
        '\u0440': 'p',
        '\u0442': 't',
        '\u0445': 'x'
    }
    
    # Replace all Cyrillic characters with Latin equivalents
    for cyrillic, latin in cyrillic_to_latin.items():
        s = s.replace(cyrillic, latin)
    
    return s


def clean_revision(val):
    """Clean and normalize revision values.
    
    - Converts Cyrillic characters to Latin
    - Removes non-breaking spaces
    - Converts to uppercase
    - Removes trailing dots (used for QA reissues)
    
    Args:
        val: Revision value to clean
        
    Returns:
        str: Cleaned revision string
    """
    if pd.isna(val):
        return ''
    
    # Normalize Cyrillic characters first
    s = normalize_cyrillic_to_ascii(val)
    
    # Replace non-breaking spaces and strip
    s = s.replace('\u00A0', ' ').strip().upper()
    
    # Remove trailing dots (used by some projects for reissued QA rejected documents)
    # Example: C01. → C01, P02... → P02
    # This ensures consistent revision counting across all projects
    s = s.rstrip('.')
    
    return s


def clean_document_title(val):
    """Clean and normalize document title values.
    
    - Converts Cyrillic characters to Latin (fixes apartment types like В-2, М-1, ОО-1)
    - Removes non-breaking spaces
    - Strips whitespace
    
    Args:
        val: Document title to clean
        
    Returns:
        str: Cleaned document title
    """
    if pd.isna(val):
        return ''
    
    # Normalize Cyrillic characters (fixes В-2 → B-2, М-1 → M-1, ОО-1 → OO-1)
    s = normalize_cyrillic_to_ascii(val)
    
    # Replace non-breaking spaces and strip
    s = s.replace('\u00A0', ' ').strip()
    
    return s

