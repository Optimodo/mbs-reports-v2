"""Configuration for Greenwich Peninsula project."""

PROJECT_TITLE = "Greenwich Peninsula"

# Accommodation Schedule Configuration
# Used by scripts/update_accommodation_data.py to parse the accommodation schedule
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,  # Set to False to disable accommodation schedule parsing
    'file_path': 'GP Accommodation Schedule 201025.xlsx',  # Standard format: <ProjectCode> Accommodation Schedule <DDMMYY>.xlsx
    
    # Excel/CSV reading configuration
    'read_config': {
        'sheet_name': 0,  # First sheet
        'skiprows': 3,    # Skip first 3 rows (headers are on row 4, data starts row 5)
        'nrows': 476,     # Read 476 rows (data ends at row 480, which is 476 rows after row 4)
        'usecols': 'B:M'  # Only read columns A through N (O onwards can be ignored)
    },
    
    # Column mapping - maps standard names to actual column names in the schedule
    'column_mapping': {
        'apartment': 'Unit Ref',         # REQUIRED - Column containing apartment/unit numbers
        'phase': 'Phase',                # OPTIONAL - Column containing phase information
        'block': 'Building',             # OPTIONAL - Column containing block information  
        'floor': 'Floor',                # OPTIONAL - Column containing floor information
        'apartment_type': 'FRA Unit Type Ref',  # OPTIONAL - Column containing apartment type
        'bedrooms': 'Beds',              # OPTIONAL - Column containing number of bedrooms
        'tenure': 'Tenure'               # OPTIONAL - Column containing tenure type (e.g., Private, Rented, Shared Ownership)
    },
    
    # Apartment number cleaning configuration
    'apartment_cleaning': {
        'remove_prefix': '',  # Remove prefix like "Apt " or "Flat " (if any)
        'extract_pattern': r'\d+'  # Extract just the number part (optional regex)
    },
    
    # Floor cleaning configuration
    'floor_cleaning': {
        'remove_prefix': 'L',  # Remove "L" from "L01" -> "01"
        'remove_suffix': '',   # Remove suffix if needed
        'convert_to_int': True  # Convert "01" -> 1 (set False to keep as string)
    }
}

# Excel processing settings
EXCEL_SETTINGS = {
    "sheet_name": 0,  # First sheet by default
    "skiprows": 6,    # Skip the first 6 rows
    "usecols": [
        "Doc Title",
        "Doc Ref",
        "Rev",
        "Status",
        "Purpose of Issue",
        "Date (WET)",
        "Last Status Change (WET)",
        "File Type",
        "File Number",
        "Last Updated (WET)",
        "Doc Path",
        "Publisher"
    ]
}

# Column mappings - Map raw Excel columns to standardized names
COLUMN_MAPPINGS = {
    'File Type': 'File Type',  # Already standardized
    'Doc Ref': 'Doc Ref',
    'Doc Title': 'Doc Title',
    'Rev': 'Rev',
    'Status': 'Status',
    'Date (WET)': 'Date (WET)',
    'Doc Path': 'Doc Path',
    'Publisher': 'Publisher'
}

# Change detection settings
CHANGE_DETECTION = {
    "track_columns": [
        "Status",
        "Doc Ref",
        "Doc Title",
        "Rev",
        "Date (WET)",
        "Last Status Change (WET)"
    ],
    "ignore_columns": [
        "Last Status Change (WET)"
    ]
}

# Report settings
REPORT_SETTINGS = {
    "weekly_summary": True,
    "change_report": True,
    "output_format": "excel",  # Options: excel, pdf, html
    "include_charts": True
} 

# File type settings
FILE_TYPE_SETTINGS = {
    "column_name": "File Type",  # Column name for file type
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "File Type Summary"  # Title for the summary section
} 

# Drawing Settings (for main summary report focus)
DRAWING_SETTINGS = {
    'enabled': True,
    # File type filtering (Method 1) - EXACT matches only
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',
        'drawing_types': ['DR - Drawing (DR)', 'SC - Schematic Drawings (SC)']
    },
    # Doc Ref pattern filtering (Method 2) - 2-letter codes
    'doc_ref_filter': {
        'enabled': False,  # Enable if you want to filter by Doc Ref patterns
        'column_name': 'Doc Ref',
        'drawing_patterns': ['DR', 'SC']  # 2-letter codes to match in Doc Ref
    }
}

# Certificate Settings
CERTIFICATE_SETTINGS = {
    'enabled': True,
    # Report generation settings
    'generate_report': True,  # Set to False to disable certificate report generation
    'summary_label': 'P01-PXX (Certificates)',
    'status_suffix': ' (Certificates)',
    # File type filtering (Method 1)
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',
        'certificate_types': ['CE - Certificate (CE)']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': True,
        'column_name': 'Doc Ref',
        'certificate_patterns': ['CE']  # 2-letter codes to match in Doc Ref
    }
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': True,
    # Report generation settings
    'generate_report': False,  # Set to True when ready to create technical submittal reports
    # File type filtering (Method 1)
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Standardized column name in database
        'technical_submittal_types': ['TS - Technical submission (TS)']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': False,
        'column_name': 'Doc Ref',
        'technical_submittal_patterns': ['TS', 'TX']
    }
}

# Status Mappings - Maps actual status values to standardized categories
# This allows project-specific status terminology to be properly categorized
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A',
        'color': '25E82C',  # Green
        'statuses': [
            'A - Authorized and Accepted'
        ],
        'description': 'Approved/Accepted documents'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'B - Partial Sign Off (with comment)'
        ],
        'description': 'Approved with comments'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'C-Rejected'
        ],
        'description': 'Rejected documents'
    },
    'Information': {
        'display_name': 'For Information',
        'color': 'FFFFFF',  # White
        'statuses': [
            'For Information'
        ],
        'description': 'Informational or under review'
    },
    'Review': {
        'display_name': 'Under Review/For Commenting',
        'color': 'FFFFFF',  # White
        'statuses': [
            'For Status Change',
            'For Commenting',
            'Reviewed'
        ],
        'description': 'For commenting or under review'
    }

}

# Display order for progression reports (order matters for chart generation)
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'Information',
    'Review'
]

# Certificate Tracking Configuration
CERTIFICATE_TRACKING = {
    # Optional: Define project phases and blocks for granular tracking
    'phases': {
        '18.02': {
            'display_name': 'Phase 18.02',
            'blocks': ['A', 'B', 'C'],
            'apartment_count': 254  # Apartments in this phase
        },
        '18.03': {
            'display_name': 'Phase 18.03',
            'blocks': ['D', 'E', 'F', 'G'],
            'apartment_count': 222  # Apartments in this phase
        }
    },
    
    # Phase/Block detection patterns (how to identify them in document metadata)
    'phase_detection': {
        'patterns': [r'18\.02', r'18\.03'],  # Regex patterns to find phase in title/ref/path
        'doc_title_patterns': [r'Plot\s+(\d{2}\.\d{2})'],  # Extract phase from doc title
        'doc_ref_patterns': []  # Could extract from doc ref if needed
    },
    
    'block_detection': {
        'patterns': [
            r'\bBlock\s*-\s*([A-G])\b',  # Match "Block - A" or "Block -A" or "Block- A"
            r'\bBlock\s+([A-G])\b',      # Match "Block A"
            r'\b([A-G])\s+Block\b'       # Match "A Block"
        ],
        'doc_title_patterns': []  # Could extract from doc title if needed
    },
    
    # Certificate categories to track
    'apartment_certificates': {
        'part_p': {
            'patterns': ['Part P'],
            'max_count': 476,  # Total apartments (476 flats across all phases/blocks)
            'display_name': 'Part P'
        },
        'electrical_cert': {
            'patterns': ['Electrical Cert'],
            'max_count': 476,
            'display_name': 'Electrical Cert'
        },
        'mvhr_ventilation': {
            'patterns': ['MVHR Cert', 'MVHR'],
            'max_count': 476,
            'display_name': 'MVHR / Ventilation'
        },
        'apartment_flushing': {
            'patterns': ['Apartment Flushing Certificate', 'Apartment Flushing'],
            'max_count': 476,
            'display_name': 'Apartment Flushing'
        },
        'fire_alarm': {
            'patterns': ['FA Cert', 'FA CERT', 'Fire'],
            'max_count': 476,
            'display_name': 'Fire Alarm'
        },
        'data_network': {
            'patterns': ['Data Network Cert', 'DATA NETWORK'],
            'max_count': 476,
            'display_name': 'Data Network'
        },
        'irs': {
            'patterns': ['IRS Cert', 'IRS'],
            'max_count': 476,
            'display_name': 'IRS'
        },
        'hiu_heating': {
            'patterns': ['HIU Cert', 'Heat'],
            'max_count': 476,
            'display_name': 'HIU / Heating'
        },
        'water_quality': {
            'patterns': ['Water Quality Cert', 'Water Quality'],
            'max_count': 476,
            'display_name': 'Water Quality'
        }
    }
} 





# Accommodation Data - Auto-generated by update_accommodation_data.py
# Last updated: 2025-10-20
# Source: GP Accommodation Schedule 201025.xlsx
ACCOMMODATION_DATA = {
    'total_apartments': 476,
    'last_updated': '2025-10-20',
    'source_file': 'GP Accommodation Schedule 201025.xlsx',
    
    'phases': {
        '18.02': {
            'apartment_count': 254,
            'apartments': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254],
            'blocks': {
                'A': {
                    'apartment_count': 181,
                    'apartments': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
                },
                'B': {
                    'apartment_count': 62,
                    'apartments': [182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243],
                    'floors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                },
                'C': {
                    'apartment_count': 11,
                    'apartments': [244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254],
                    'floors': [0]
                },
            }
        },
        '18.03': {
            'apartment_count': 222,
            'apartments': [255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476],
            'blocks': {
                'D': {
                    'apartment_count': 6,
                    'apartments': [255, 256, 257, 258, 259, 260],
                    'floors': [0]
                },
                'E': {
                    'apartment_count': 131,
                    'apartments': [261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
                },
                'F': {
                    'apartment_count': 61,
                    'apartments': [392, 393, 394, 395, 396, 397, 398, 403, 404, 405, 406, 407, 408, 409, 414, 415, 416, 417, 418, 419, 420, 425, 426, 427, 428, 429, 430, 431, 436, 437, 438, 439, 440, 441, 442, 447, 448, 449, 450, 451, 452, 453, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476],
                    'floors': [0, 2, 3, 4, 5, 6, 7, 8, 9]
                },
                'G': {
                    'apartment_count': 24,
                    'apartments': [399, 400, 401, 402, 410, 411, 412, 413, 421, 422, 423, 424, 432, 433, 434, 435, 443, 444, 445, 446, 454, 455, 456, 457],
                    'floors': [0, 1, 2, 3, 4, 5, 6]
                },
            }
        },
    },
    
    'apartment_types': {
        '02a': {
            'count': 25,
            'bedrooms': 2,
            'apartments': [1, 8, 15, 22, 29, 36, 43, 50, 57, 64, 261, 268, 275, 282, 289, 296, 303, 310, 317, 324, 331, 338, 345, 352, 359]
        },
        '8': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [2]
        },
        '04b': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [3]
        },
        '05a': {
            'count': 24,
            'bedrooms': 1,
            'apartments': [4, 11, 18, 25, 32, 39, 46, 53, 60, 67, 264, 271, 278, 285, 292, 299, 306, 313, 320, 327, 334, 341, 348, 355]
        },
        '06a': {
            'count': 24,
            'bedrooms': 2,
            'apartments': [5, 12, 19, 26, 33, 40, 47, 54, 61, 68, 265, 272, 279, 286, 293, 300, 307, 314, 321, 328, 335, 342, 349, 356]
        },
        '07a': {
            'count': 10,
            'bedrooms': 1,
            'apartments': [6, 13, 20, 27, 34, 41, 48, 55, 62, 69]
        },
        '01a': {
            'count': 22,
            'bedrooms': 2,
            'apartments': [7, 14, 21, 28, 35, 42, 49, 56, 63, 267, 274, 281, 288, 295, 302, 309, 316, 323, 330, 337, 344, 351]
        },
        '03a': {
            'count': 9,
            'bedrooms': 1,
            'apartments': [9, 16, 23, 30, 37, 44, 51, 58, 65]
        },
        '04a': {
            'count': 22,
            'bedrooms': 1,
            'apartments': [10, 17, 24, 31, 38, 45, 52, 59, 66, 270, 277, 284, 291, 298, 305, 312, 319, 326, 333, 340, 347, 354]
        },
        '1': {
            'count': 9,
            'bedrooms': 2,
            'apartments': [70, 77, 84, 91, 98, 105, 112, 119, 126]
        },
        '2': {
            'count': 25,
            'bedrooms': 2,
            'apartments': [71, 78, 85, 92, 99, 106, 113, 120, 127, 134, 138, 143, 148, 153, 158, 163, 168, 173, 178, 363, 368, 373, 378, 383, 388]
        },
        '3': {
            'count': 19,
            'bedrooms': 1,
            'apartments': [72, 79, 86, 93, 100, 107, 114, 121, 128, 135, 139, 144, 149, 154, 159, 164, 169, 174, 179]
        },
        '4': {
            'count': 9,
            'bedrooms': 1,
            'apartments': [73, 80, 87, 94, 101, 108, 115, 122, 129]
        },
        '5': {
            'count': 9,
            'bedrooms': 1,
            'apartments': [74, 81, 88, 95, 102, 109, 116, 123, 130]
        },
        '6': {
            'count': 9,
            'bedrooms': 2,
            'apartments': [75, 82, 89, 96, 103, 110, 117, 124, 131]
        },
        '7': {
            'count': 9,
            'bedrooms': 1,
            'apartments': [76, 83, 90, 97, 104, 111, 118, 125, 132]
        },
        '16': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [133]
        },
        '14': {
            'count': 16,
            'bedrooms': 3,
            'apartments': [136, 140, 145, 150, 155, 160, 165, 170, 175, 180, 365, 370, 375, 380, 385, 390]
        },
        '11': {
            'count': 9,
            'bedrooms': 2,
            'apartments': [137, 142, 147, 152, 157, 162, 167, 172, 177]
        },
        '15': {
            'count': 9,
            'bedrooms': 1,
            'apartments': [141, 146, 151, 156, 161, 166, 171, 176, 181]
        },
        '44': {
            'count': 2,
            'bedrooms': 3,
            'apartments': [182, 392]
        },
        '44b': {
            'count': 4,
            'bedrooms': 3,
            'apartments': [183, 184, 393, 394]
        },
        '45': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [185]
        },
        '46': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [186]
        },
        '47': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [187]
        },
        '48': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [188]
        },
        '30': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [189, 196, 203, 210, 217, 224, 231]
        },
        '31': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [190, 197, 204, 211, 218, 225, 232]
        },
        '31b': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [191, 198, 205, 212, 219, 226, 233]
        },
        '32': {
            'count': 7,
            'bedrooms': 3,
            'apartments': [192, 199, 206, 213, 220, 227, 234]
        },
        '33': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [193, 200, 207, 214, 221, 228, 235]
        },
        '35': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [194, 201, 208, 215, 222, 229, 236]
        },
        '34': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [195, 202, 209, 216, 223, 230, 237]
        },
        '57': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [238]
        },
        '53': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [239]
        },
        '54': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [240]
        },
        '55': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [241]
        },
        '56': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [242]
        },
        '52': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [243]
        },
        '61': {
            'count': 2,
            'bedrooms': 4,
            'apartments': [244, 255]
        },
        '62': {
            'count': 12,
            'bedrooms': 4,
            'apartments': [245, 246, 247, 248, 249, 250, 253, 256, 257, 258, 259, 260]
        },
        '65': {
            'count': 1,
            'bedrooms': 4,
            'apartments': [251]
        },
        '63': {
            'count': 1,
            'bedrooms': 4,
            'apartments': [252]
        },
        '64': {
            'count': 1,
            'bedrooms': 4,
            'apartments': [254]
        },
        '08a': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [262]
        },
        '04c': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [263]
        },
        '17': {
            'count': 14,
            'bedrooms': 1,
            'apartments': [266, 273, 280, 287, 294, 301, 308, 315, 322, 329, 336, 343, 350, 357]
        },
        '13a': {
            'count': 14,
            'bedrooms': 1,
            'apartments': [269, 276, 283, 290, 297, 304, 311, 318, 325, 332, 339, 346, 353, 360]
        },
        '16a': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [358]
        },
        '14a': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [361]
        },
        '12': {
            'count': 6,
            'bedrooms': 2,
            'apartments': [362, 367, 372, 377, 382, 387]
        },
        '13': {
            'count': 6,
            'bedrooms': 1,
            'apartments': [364, 369, 374, 379, 384, 389]
        },
        '18': {
            'count': 6,
            'bedrooms': 1,
            'apartments': [366, 371, 376, 381, 386, 391]
        },
        '45a': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [395]
        },
        '49': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [396]
        },
        '50': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [397]
        },
        '51': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [398]
        },
        '85': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [399]
        },
        '86': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [400]
        },
        '84': {
            'count': 6,
            'bedrooms': 1,
            'apartments': [401, 413, 424, 435, 446, 457]
        },
        '87': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [402]
        },
        '30a': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [403, 414, 425, 436, 447, 458, 465]
        },
        '31a': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [404, 415, 426, 437, 448, 459, 466]
        },
        '31c': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [405, 416, 427, 438, 449, 460, 467]
        },
        '32a': {
            'count': 7,
            'bedrooms': 3,
            'apartments': [406, 417, 428, 439, 450, 461, 468]
        },
        '33b': {
            'count': 3,
            'bedrooms': 1,
            'apartments': [407, 418, 429]
        },
        '35a': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [408, 419, 430, 441, 452, 463, 470]
        },
        '34a': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [409, 420, 431, 442, 453, 464, 471]
        },
        '82': {
            'count': 5,
            'bedrooms': 3,
            'apartments': [410, 421, 432, 443, 454]
        },
        '81': {
            'count': 5,
            'bedrooms': 1,
            'apartments': [411, 422, 433, 444, 455]
        },
        '83': {
            'count': 5,
            'bedrooms': 1,
            'apartments': [412, 423, 434, 445, 456]
        },
        '33a': {
            'count': 4,
            'bedrooms': 1,
            'apartments': [440, 451, 462, 469]
        },
        '42a': {
            'count': 1,
            'bedrooms': 4,
            'apartments': [472]
        },
        '38a': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [473]
        },
        '36a': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [474]
        },
        '37a': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [475]
        },
        '39a': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [476]
        },
    },
    
    'tenures': {
        'Shared Ownership': {
            'count': 225,
            'apartments': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361]
        },
        'Private': {
            'count': 142,
            'apartments': [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]
        },
        'Affordable Rent': {
            'count': 109,
            'apartments': [182, 183, 184, 185, 186, 187, 188, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]
        },
    },
    
    'apartment_lookup': {
        # Full apartment lookup dictionary with 476 apartments
        1: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        2: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': '8', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        3: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': '04b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        4: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        5: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        6: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        7: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        8: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        9: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        10: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        11: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        12: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        13: {'phase': '18.02', 'block': 'A', 'floor': 2, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        14: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        15: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        16: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        17: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        18: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        19: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        20: {'phase': '18.02', 'block': 'A', 'floor': 3, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        21: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        22: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        23: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        24: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        25: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        26: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        27: {'phase': '18.02', 'block': 'A', 'floor': 4, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        28: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        29: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        30: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        31: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        32: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        33: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        34: {'phase': '18.02', 'block': 'A', 'floor': 5, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        35: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        36: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        37: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        38: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        39: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        40: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        41: {'phase': '18.02', 'block': 'A', 'floor': 6, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        42: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        43: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        44: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        45: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        46: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        47: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        48: {'phase': '18.02', 'block': 'A', 'floor': 7, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        49: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        50: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        51: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        52: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        53: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        54: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        55: {'phase': '18.02', 'block': 'A', 'floor': 8, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        56: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        57: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        58: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        59: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        60: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        61: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        62: {'phase': '18.02', 'block': 'A', 'floor': 9, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        63: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        64: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        65: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '03a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        66: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        67: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        68: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        69: {'phase': '18.02', 'block': 'A', 'floor': 10, 'type': '07a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        70: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        71: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        72: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        73: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        74: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        75: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        76: {'phase': '18.02', 'block': 'A', 'floor': 11, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        77: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        78: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        79: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        80: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        81: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        82: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        83: {'phase': '18.02', 'block': 'A', 'floor': 12, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        84: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        85: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        86: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        87: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        88: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        89: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        90: {'phase': '18.02', 'block': 'A', 'floor': 13, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        91: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        92: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        93: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        94: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        95: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        96: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        97: {'phase': '18.02', 'block': 'A', 'floor': 14, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        98: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        99: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        100: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        101: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        102: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        103: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        104: {'phase': '18.02', 'block': 'A', 'floor': 15, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        105: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        106: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        107: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        108: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        109: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        110: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        111: {'phase': '18.02', 'block': 'A', 'floor': 16, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        112: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        113: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        114: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        115: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        116: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        117: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        118: {'phase': '18.02', 'block': 'A', 'floor': 17, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        119: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        120: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        121: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        122: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        123: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        124: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        125: {'phase': '18.02', 'block': 'A', 'floor': 18, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        126: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '1', 'bedrooms': 2, 'tenure': 'Private'},
        127: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        128: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        129: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '4', 'bedrooms': 1, 'tenure': 'Private'},
        130: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '5', 'bedrooms': 1, 'tenure': 'Private'},
        131: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '6', 'bedrooms': 2, 'tenure': 'Private'},
        132: {'phase': '18.02', 'block': 'A', 'floor': 19, 'type': '7', 'bedrooms': 1, 'tenure': 'Private'},
        133: {'phase': '18.02', 'block': 'A', 'floor': 20, 'type': '16', 'bedrooms': 1, 'tenure': 'Private'},
        134: {'phase': '18.02', 'block': 'A', 'floor': 20, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        135: {'phase': '18.02', 'block': 'A', 'floor': 20, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        136: {'phase': '18.02', 'block': 'A', 'floor': 20, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        137: {'phase': '18.02', 'block': 'A', 'floor': 21, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        138: {'phase': '18.02', 'block': 'A', 'floor': 21, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        139: {'phase': '18.02', 'block': 'A', 'floor': 21, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        140: {'phase': '18.02', 'block': 'A', 'floor': 21, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        141: {'phase': '18.02', 'block': 'A', 'floor': 21, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        142: {'phase': '18.02', 'block': 'A', 'floor': 22, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        143: {'phase': '18.02', 'block': 'A', 'floor': 22, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        144: {'phase': '18.02', 'block': 'A', 'floor': 22, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        145: {'phase': '18.02', 'block': 'A', 'floor': 22, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        146: {'phase': '18.02', 'block': 'A', 'floor': 22, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        147: {'phase': '18.02', 'block': 'A', 'floor': 23, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        148: {'phase': '18.02', 'block': 'A', 'floor': 23, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        149: {'phase': '18.02', 'block': 'A', 'floor': 23, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        150: {'phase': '18.02', 'block': 'A', 'floor': 23, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        151: {'phase': '18.02', 'block': 'A', 'floor': 23, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        152: {'phase': '18.02', 'block': 'A', 'floor': 24, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        153: {'phase': '18.02', 'block': 'A', 'floor': 24, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        154: {'phase': '18.02', 'block': 'A', 'floor': 24, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        155: {'phase': '18.02', 'block': 'A', 'floor': 24, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        156: {'phase': '18.02', 'block': 'A', 'floor': 24, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        157: {'phase': '18.02', 'block': 'A', 'floor': 25, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        158: {'phase': '18.02', 'block': 'A', 'floor': 25, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        159: {'phase': '18.02', 'block': 'A', 'floor': 25, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        160: {'phase': '18.02', 'block': 'A', 'floor': 25, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        161: {'phase': '18.02', 'block': 'A', 'floor': 25, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        162: {'phase': '18.02', 'block': 'A', 'floor': 26, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        163: {'phase': '18.02', 'block': 'A', 'floor': 26, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        164: {'phase': '18.02', 'block': 'A', 'floor': 26, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        165: {'phase': '18.02', 'block': 'A', 'floor': 26, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        166: {'phase': '18.02', 'block': 'A', 'floor': 26, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        167: {'phase': '18.02', 'block': 'A', 'floor': 27, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        168: {'phase': '18.02', 'block': 'A', 'floor': 27, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        169: {'phase': '18.02', 'block': 'A', 'floor': 27, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        170: {'phase': '18.02', 'block': 'A', 'floor': 27, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        171: {'phase': '18.02', 'block': 'A', 'floor': 27, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        172: {'phase': '18.02', 'block': 'A', 'floor': 28, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        173: {'phase': '18.02', 'block': 'A', 'floor': 28, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        174: {'phase': '18.02', 'block': 'A', 'floor': 28, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        175: {'phase': '18.02', 'block': 'A', 'floor': 28, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        176: {'phase': '18.02', 'block': 'A', 'floor': 28, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        177: {'phase': '18.02', 'block': 'A', 'floor': 29, 'type': '11', 'bedrooms': 2, 'tenure': 'Private'},
        178: {'phase': '18.02', 'block': 'A', 'floor': 29, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        179: {'phase': '18.02', 'block': 'A', 'floor': 29, 'type': '3', 'bedrooms': 1, 'tenure': 'Private'},
        180: {'phase': '18.02', 'block': 'A', 'floor': 29, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        181: {'phase': '18.02', 'block': 'A', 'floor': 29, 'type': '15', 'bedrooms': 1, 'tenure': 'Private'},
        182: {'phase': '18.02', 'block': 'B', 'floor': 0, 'type': '44', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        183: {'phase': '18.02', 'block': 'B', 'floor': 0, 'type': '44b', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        184: {'phase': '18.02', 'block': 'B', 'floor': 0, 'type': '44b', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        185: {'phase': '18.02', 'block': 'B', 'floor': 0, 'type': '45', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        186: {'phase': '18.02', 'block': 'B', 'floor': 0, 'type': '46', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        187: {'phase': '18.02', 'block': 'B', 'floor': 1, 'type': '47', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        188: {'phase': '18.02', 'block': 'B', 'floor': 1, 'type': '48', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        189: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        190: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        191: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        192: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        193: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        194: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        195: {'phase': '18.02', 'block': 'B', 'floor': 2, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        196: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        197: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        198: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        199: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        200: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        201: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        202: {'phase': '18.02', 'block': 'B', 'floor': 3, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        203: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        204: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        205: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        206: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        207: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        208: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        209: {'phase': '18.02', 'block': 'B', 'floor': 4, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        210: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        211: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        212: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        213: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        214: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        215: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        216: {'phase': '18.02', 'block': 'B', 'floor': 5, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        217: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        218: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        219: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        220: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        221: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        222: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        223: {'phase': '18.02', 'block': 'B', 'floor': 6, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        224: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        225: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        226: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        227: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        228: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        229: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        230: {'phase': '18.02', 'block': 'B', 'floor': 7, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        231: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '30', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        232: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '31', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        233: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '31b', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        234: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '32', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        235: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '33', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        236: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '35', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        237: {'phase': '18.02', 'block': 'B', 'floor': 8, 'type': '34', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        238: {'phase': '18.02', 'block': 'B', 'floor': 9, 'type': '57', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        239: {'phase': '18.02', 'block': 'B', 'floor': 9, 'type': '53', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        240: {'phase': '18.02', 'block': 'B', 'floor': 9, 'type': '54', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        241: {'phase': '18.02', 'block': 'B', 'floor': 9, 'type': '55', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        242: {'phase': '18.02', 'block': 'B', 'floor': 9, 'type': '56', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        243: {'phase': '18.02', 'block': 'B', 'floor': 9, 'type': '52', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        244: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '61', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        245: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        246: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        247: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        248: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        249: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        250: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        251: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '65', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        252: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '63', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        253: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        254: {'phase': '18.02', 'block': 'C', 'floor': 0, 'type': '64', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        255: {'phase': '18.03', 'block': 'D', 'floor': 0, 'type': '61', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        256: {'phase': '18.03', 'block': 'D', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        257: {'phase': '18.03', 'block': 'D', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        258: {'phase': '18.03', 'block': 'D', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        259: {'phase': '18.03', 'block': 'D', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        260: {'phase': '18.03', 'block': 'D', 'floor': 0, 'type': '62', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        261: {'phase': '18.03', 'block': 'E', 'floor': 1, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        262: {'phase': '18.03', 'block': 'E', 'floor': 1, 'type': '08a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        263: {'phase': '18.03', 'block': 'E', 'floor': 1, 'type': '04c', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        264: {'phase': '18.03', 'block': 'E', 'floor': 1, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        265: {'phase': '18.03', 'block': 'E', 'floor': 1, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        266: {'phase': '18.03', 'block': 'E', 'floor': 1, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        267: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        268: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        269: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        270: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        271: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        272: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        273: {'phase': '18.03', 'block': 'E', 'floor': 2, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        274: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        275: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        276: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        277: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        278: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        279: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        280: {'phase': '18.03', 'block': 'E', 'floor': 3, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        281: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        282: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        283: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        284: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        285: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        286: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        287: {'phase': '18.03', 'block': 'E', 'floor': 4, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        288: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        289: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        290: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        291: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        292: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        293: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        294: {'phase': '18.03', 'block': 'E', 'floor': 5, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        295: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        296: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        297: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        298: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        299: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        300: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        301: {'phase': '18.03', 'block': 'E', 'floor': 6, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        302: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        303: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        304: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        305: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        306: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        307: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        308: {'phase': '18.03', 'block': 'E', 'floor': 7, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        309: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        310: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        311: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        312: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        313: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        314: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        315: {'phase': '18.03', 'block': 'E', 'floor': 8, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        316: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        317: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        318: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        319: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        320: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        321: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        322: {'phase': '18.03', 'block': 'E', 'floor': 9, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        323: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        324: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        325: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        326: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        327: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        328: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        329: {'phase': '18.03', 'block': 'E', 'floor': 10, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        330: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        331: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        332: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        333: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        334: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        335: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        336: {'phase': '18.03', 'block': 'E', 'floor': 11, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        337: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        338: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        339: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        340: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        341: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        342: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        343: {'phase': '18.03', 'block': 'E', 'floor': 12, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        344: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        345: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        346: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        347: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        348: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        349: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        350: {'phase': '18.03', 'block': 'E', 'floor': 13, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        351: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '01a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        352: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        353: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        354: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '04a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        355: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '05a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        356: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '06a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        357: {'phase': '18.03', 'block': 'E', 'floor': 14, 'type': '17', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        358: {'phase': '18.03', 'block': 'E', 'floor': 15, 'type': '16a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        359: {'phase': '18.03', 'block': 'E', 'floor': 15, 'type': '02a', 'bedrooms': 2, 'tenure': 'Shared Ownership'},
        360: {'phase': '18.03', 'block': 'E', 'floor': 15, 'type': '13a', 'bedrooms': 1, 'tenure': 'Shared Ownership'},
        361: {'phase': '18.03', 'block': 'E', 'floor': 15, 'type': '14a', 'bedrooms': 3, 'tenure': 'Shared Ownership'},
        362: {'phase': '18.03', 'block': 'E', 'floor': 16, 'type': '12', 'bedrooms': 2, 'tenure': 'Private'},
        363: {'phase': '18.03', 'block': 'E', 'floor': 16, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        364: {'phase': '18.03', 'block': 'E', 'floor': 16, 'type': '13', 'bedrooms': 1, 'tenure': 'Private'},
        365: {'phase': '18.03', 'block': 'E', 'floor': 16, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        366: {'phase': '18.03', 'block': 'E', 'floor': 16, 'type': '18', 'bedrooms': 1, 'tenure': 'Private'},
        367: {'phase': '18.03', 'block': 'E', 'floor': 17, 'type': '12', 'bedrooms': 2, 'tenure': 'Private'},
        368: {'phase': '18.03', 'block': 'E', 'floor': 17, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        369: {'phase': '18.03', 'block': 'E', 'floor': 17, 'type': '13', 'bedrooms': 1, 'tenure': 'Private'},
        370: {'phase': '18.03', 'block': 'E', 'floor': 17, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        371: {'phase': '18.03', 'block': 'E', 'floor': 17, 'type': '18', 'bedrooms': 1, 'tenure': 'Private'},
        372: {'phase': '18.03', 'block': 'E', 'floor': 18, 'type': '12', 'bedrooms': 2, 'tenure': 'Private'},
        373: {'phase': '18.03', 'block': 'E', 'floor': 18, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        374: {'phase': '18.03', 'block': 'E', 'floor': 18, 'type': '13', 'bedrooms': 1, 'tenure': 'Private'},
        375: {'phase': '18.03', 'block': 'E', 'floor': 18, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        376: {'phase': '18.03', 'block': 'E', 'floor': 18, 'type': '18', 'bedrooms': 1, 'tenure': 'Private'},
        377: {'phase': '18.03', 'block': 'E', 'floor': 19, 'type': '12', 'bedrooms': 2, 'tenure': 'Private'},
        378: {'phase': '18.03', 'block': 'E', 'floor': 19, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        379: {'phase': '18.03', 'block': 'E', 'floor': 19, 'type': '13', 'bedrooms': 1, 'tenure': 'Private'},
        380: {'phase': '18.03', 'block': 'E', 'floor': 19, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        381: {'phase': '18.03', 'block': 'E', 'floor': 19, 'type': '18', 'bedrooms': 1, 'tenure': 'Private'},
        382: {'phase': '18.03', 'block': 'E', 'floor': 20, 'type': '12', 'bedrooms': 2, 'tenure': 'Private'},
        383: {'phase': '18.03', 'block': 'E', 'floor': 20, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        384: {'phase': '18.03', 'block': 'E', 'floor': 20, 'type': '13', 'bedrooms': 1, 'tenure': 'Private'},
        385: {'phase': '18.03', 'block': 'E', 'floor': 20, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        386: {'phase': '18.03', 'block': 'E', 'floor': 20, 'type': '18', 'bedrooms': 1, 'tenure': 'Private'},
        387: {'phase': '18.03', 'block': 'E', 'floor': 21, 'type': '12', 'bedrooms': 2, 'tenure': 'Private'},
        388: {'phase': '18.03', 'block': 'E', 'floor': 21, 'type': '2', 'bedrooms': 2, 'tenure': 'Private'},
        389: {'phase': '18.03', 'block': 'E', 'floor': 21, 'type': '13', 'bedrooms': 1, 'tenure': 'Private'},
        390: {'phase': '18.03', 'block': 'E', 'floor': 21, 'type': '14', 'bedrooms': 3, 'tenure': 'Private'},
        391: {'phase': '18.03', 'block': 'E', 'floor': 21, 'type': '18', 'bedrooms': 1, 'tenure': 'Private'},
        392: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '44', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        393: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '44b', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        394: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '44b', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        395: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '45a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        396: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '49', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        397: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '50', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        398: {'phase': '18.03', 'block': 'F', 'floor': 0, 'type': '51', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        399: {'phase': '18.03', 'block': 'G', 'floor': 0, 'type': '85', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        400: {'phase': '18.03', 'block': 'G', 'floor': 0, 'type': '86', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        401: {'phase': '18.03', 'block': 'G', 'floor': 1, 'type': '84', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        402: {'phase': '18.03', 'block': 'G', 'floor': 1, 'type': '87', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        403: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        404: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        405: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        406: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        407: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '33b', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        408: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        409: {'phase': '18.03', 'block': 'F', 'floor': 2, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        410: {'phase': '18.03', 'block': 'G', 'floor': 2, 'type': '82', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        411: {'phase': '18.03', 'block': 'G', 'floor': 2, 'type': '81', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        412: {'phase': '18.03', 'block': 'G', 'floor': 2, 'type': '83', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        413: {'phase': '18.03', 'block': 'G', 'floor': 2, 'type': '84', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        414: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        415: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        416: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        417: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        418: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '33b', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        419: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        420: {'phase': '18.03', 'block': 'F', 'floor': 3, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        421: {'phase': '18.03', 'block': 'G', 'floor': 3, 'type': '82', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        422: {'phase': '18.03', 'block': 'G', 'floor': 3, 'type': '81', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        423: {'phase': '18.03', 'block': 'G', 'floor': 3, 'type': '83', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        424: {'phase': '18.03', 'block': 'G', 'floor': 3, 'type': '84', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        425: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        426: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        427: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        428: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        429: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '33b', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        430: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        431: {'phase': '18.03', 'block': 'F', 'floor': 4, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        432: {'phase': '18.03', 'block': 'G', 'floor': 4, 'type': '82', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        433: {'phase': '18.03', 'block': 'G', 'floor': 4, 'type': '81', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        434: {'phase': '18.03', 'block': 'G', 'floor': 4, 'type': '83', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        435: {'phase': '18.03', 'block': 'G', 'floor': 4, 'type': '84', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        436: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        437: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        438: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        439: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        440: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '33a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        441: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        442: {'phase': '18.03', 'block': 'F', 'floor': 5, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        443: {'phase': '18.03', 'block': 'G', 'floor': 5, 'type': '82', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        444: {'phase': '18.03', 'block': 'G', 'floor': 5, 'type': '81', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        445: {'phase': '18.03', 'block': 'G', 'floor': 5, 'type': '83', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        446: {'phase': '18.03', 'block': 'G', 'floor': 5, 'type': '84', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        447: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        448: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        449: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        450: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        451: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '33a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        452: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        453: {'phase': '18.03', 'block': 'F', 'floor': 6, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        454: {'phase': '18.03', 'block': 'G', 'floor': 6, 'type': '82', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        455: {'phase': '18.03', 'block': 'G', 'floor': 6, 'type': '81', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        456: {'phase': '18.03', 'block': 'G', 'floor': 6, 'type': '83', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        457: {'phase': '18.03', 'block': 'G', 'floor': 6, 'type': '84', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        458: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        459: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        460: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        461: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        462: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '33a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        463: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        464: {'phase': '18.03', 'block': 'F', 'floor': 7, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        465: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '30a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        466: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '31a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        467: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '31c', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        468: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '32a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        469: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '33a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        470: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '35a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        471: {'phase': '18.03', 'block': 'F', 'floor': 8, 'type': '34a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        472: {'phase': '18.03', 'block': 'F', 'floor': 9, 'type': '42a', 'bedrooms': 4, 'tenure': 'Affordable Rent'},
        473: {'phase': '18.03', 'block': 'F', 'floor': 9, 'type': '38a', 'bedrooms': 3, 'tenure': 'Affordable Rent'},
        474: {'phase': '18.03', 'block': 'F', 'floor': 9, 'type': '36a', 'bedrooms': 1, 'tenure': 'Affordable Rent'},
        475: {'phase': '18.03', 'block': 'F', 'floor': 9, 'type': '37a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
        476: {'phase': '18.03', 'block': 'F', 'floor': 9, 'type': '39a', 'bedrooms': 2, 'tenure': 'Affordable Rent'},
    }
}
