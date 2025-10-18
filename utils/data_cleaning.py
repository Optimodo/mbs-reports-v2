"""Data cleaning and normalization utilities."""

import pandas as pd


def clean_revision(val):
    """Clean and normalize revision values.
    
    Handles Cyrillic characters that look like Latin characters.
    Common issue when copy-pasting from Excel or other sources.
    
    Args:
        val: Revision value to clean
        
    Returns:
        str: Cleaned revision string with all Cyrillic characters converted to Latin
    """
    if pd.isna(val):
        return ''
    
    s = str(val).replace('\u00A0', ' ').strip().upper()
    
    # Cyrillic to Latin character mapping
    # These Cyrillic characters look identical to Latin but have different Unicode values
    cyrillic_to_latin = {
        '\u0410': 'A',  # Cyrillic А → Latin A
        '\u0412': 'B',  # Cyrillic В → Latin B  
        '\u0421': 'C',  # Cyrillic С → Latin C (most common issue)
        '\u0415': 'E',  # Cyrillic Е → Latin E
        '\u041D': 'H',  # Cyrillic Н → Latin H
        '\u041A': 'K',  # Cyrillic К → Latin K
        '\u041C': 'M',  # Cyrillic М → Latin M
        '\u041E': 'O',  # Cyrillic О → Latin O
        '\u0420': 'P',  # Cyrillic Р → Latin P
        '\u0422': 'T',  # Cyrillic Т → Latin T
        '\u0425': 'X',  # Cyrillic Х → Latin X
        # Lowercase versions (in case they appear before .upper())
        '\u0430': 'A',
        '\u0432': 'B',
        '\u0441': 'C',
        '\u0435': 'E',
        '\u043D': 'H',
        '\u043A': 'K',
        '\u043C': 'M',
        '\u043E': 'O',
        '\u0440': 'P',
        '\u0442': 'T',
        '\u0445': 'X'
    }
    
    # Replace all Cyrillic characters with Latin equivalents
    for cyrillic, latin in cyrillic_to_latin.items():
        s = s.replace(cyrillic, latin)
    
    return s

