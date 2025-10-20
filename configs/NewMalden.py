"""Configuration for New Malden project."""

PROJECT_TITLE = "New Malden"

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
        "Form",
        "Number (5 digits)",
        "Last Updated (WET)",
        "Doc Path"
    ]
}

# Column mappings - Map raw Excel columns to standardized names
COLUMN_MAPPINGS = {
    'File Type': 'Form',  # New Malden uses 'Form' column for file types
    'Doc Ref': 'Doc Ref',
    'Doc Title': 'Doc Title',
    'Rev': 'Rev',
    'Status': 'Status',
    'Date (WET)': 'Date (WET)',
    'Doc Path': 'Doc Path'
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
    "column_name": "File Type",  # Standardized column name in database
    "include_in_summary": True,        # Whether to include in summary
    "summary_title": "Form Type Summary"  # Title for the summary section
} 

# Drawing Settings (for main summary report focus)
DRAWING_SETTINGS = {
    'enabled': True,
    # File type filtering (Method 1) - EXACT matches only
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Standardized column name in database
        'drawing_types': ['Drawing (DR)', 'Schematic (SM)']
    },
    # Doc Ref pattern filtering (Method 2) - 2-letter codes
    'doc_ref_filter': {
        'enabled': False,  # Enable if you want to filter by Doc Ref patterns
        'column_name': 'Doc Ref',
        'drawing_patterns': ['DR', 'SM']  # 2-letter codes to match in Doc Ref
    }
}

# Certificate Settings
CERTIFICATE_SETTINGS = {
    'enabled': True,
    # Report generation settings
    'generate_report': False,  # Set to False to disable certificate report generation
    'summary_label': 'P01-PXX (Certificates)',
    'status_suffix': ' (Certificates)',
    # File type filtering (Method 1)
    'file_type_filter': {
        'enabled': True,
        'column_name': 'Form',
        'certificate_types': ['Certificate', 'CERT']
    },
    # Doc Ref pattern filtering (Method 2)
    'doc_ref_filter': {
        'enabled': False,  # Not used for this project
        'column_name': 'Doc Ref',
        'certificate_patterns': []
    }
}

# Technical Submittal Settings
TECHNICAL_SUBMITTAL_SETTINGS = {
    'enabled': False,  # No technical submittals for this project yet
    'generate_report': False
}

# Status Mappings - Maps actual status values to standardized categories
STATUS_MAPPINGS = {
    'Status A': {
        'display_name': 'Status A',
        'color': '25E82C',  # Green
        'statuses': [
            'A - Proceed',
            'A - Proceed (Lead Reviewer)'
        ],
        'description': 'Approved to proceed'
    },
    'Status B': {
        'display_name': 'Status B',
        'color': 'EDDDA1',  # Yellow
        'statuses': [
            'B - Proceed with Comments',
            'B - Proceed with Comments (Lead Reviewer)'
        ],
        'description': 'Proceed with comments'
    },
    'Status C': {
        'display_name': 'Status C',
        'color': 'ED1111',  # Red
        'statuses': [
            'C - Rejected',
            'C - Rejected (Lead Reviewer)',
            'QC Rejected'
        ],
        'description': 'Rejected documents'
    },
    'Under Review': {
        'display_name': 'Under Review',
        'color': 'FFFFFF',  # White
        'statuses': [
            'Under Review',
            'QC Checked'
        ],
        'description': 'Under review or QC check'
    },
    'Other': {
        'display_name': 'Other',
        'color': 'D3D3D3',  # Light gray
        'statuses': [
            '---'
        ],
        'description': 'Other or unspecified status'
    }
}

# Display order for progression reports
STATUS_DISPLAY_ORDER = [
    'Status A',
    'Status B',
    'Status C',
    'Under Review',
    'Other'
]

# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,
    'file_path': 'NM Accommodation Schedule 201025.xlsx',
    'read_config': {
        'sheet_name': 0,
        'skiprows': 16,      # Skip rows 1-16, use row 17 as header
        'nrows': 456,        # Rows 18-473 (456 apartments)
        'usecols': 'A:M'     # Columns A through M
    },
    'column_mapping': {
        'apartment': 'Apt No.',          # Column B
        'floor': 'Level',                # Column C
        'block': 'Block',                # Column D
        'apartment_type': 'Apartment Type',  # Column F
        'bedrooms': 'Beds',              # Column I
        'tenure': 'Tenure'               # Column M
        # Note: No 'phase' column - will default to None
    },
    'apartment_cleaning': {
        'remove_prefix': '',             # Adjust if apartment numbers have prefixes
        'extract_pattern': r'\d+'        # Extract numeric portion
    },
    'floor_cleaning': {
        'remove_prefix': 'Level ',       # Remove "Level " prefix from floor numbers
        'remove_suffix': '',
        'convert_to_int': True
    }
}

# Accommodation Data (Auto-generated - DO NOT EDIT MANUALLY)
# Run scripts/update_accommodation_data.py to regenerate this section




# Accommodation Data - Auto-generated by update_accommodation_data.py
# Last updated: 2025-10-21
# Source: NM Accommodation Schedule 201025.xlsx
ACCOMMODATION_DATA = {
    'total_apartments': 456,
    'last_updated': '2025-10-21',
    'source_file': 'NM Accommodation Schedule 201025.xlsx',
    
    'phases': {
        'Default': {
            'apartment_count': 456,
            'apartments': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760],
            'blocks': {
                'A': {
                    'apartment_count': 95,
                    'apartments': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                },
                'B': {
                    'apartment_count': 78,
                    'apartments': [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                },
                'C': {
                    'apartment_count': 40,
                    'apartments': [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8]
                },
                'D': {
                    'apartment_count': 45,
                    'apartments': [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445],
                    'floors': [1, 2, 3, 4, 5, 6, 7]
                },
                'E': {
                    'apartment_count': 94,
                    'apartments': [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                },
                'F': {
                    'apartment_count': 44,
                    'apartments': [601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8]
                },
                'G': {
                    'apartment_count': 60,
                    'apartments': [701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760],
                    'floors': [1, 2, 3, 4, 5, 6, 7, 8]
                },
            }
        },
    },
    
    'apartment_types': {
        '2B TYPE E4': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [101]
        },
        '2B TYPE E5': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [102]
        },
        '1B TYPE C2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [103]
        },
        '1B TYPE B2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [104]
        },
        '2B TYPE C4': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [105]
        },
        '1B TYPE D2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [106]
        },
        '2B TYPE B2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [107]
        },
        '2B TYPE B3': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [108]
        },
        '2B TYPE A1': {
            'count': 9,
            'bedrooms': 2,
            'apartments': [109, 118, 127, 136, 145, 154, 163, 172, 181]
        },
        '2B TYPE E1': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [110, 119, 128, 137, 146, 155, 164, 173]
        },
        '2B TYPE E2': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [111, 120, 129, 138, 147, 156, 165, 174]
        },
        '1B TYPE C1': {
            'count': 8,
            'bedrooms': 1,
            'apartments': [112, 121, 130, 139, 148, 157, 166, 175]
        },
        '1B TYPE B1': {
            'count': 14,
            'bedrooms': 1,
            'apartments': [113, 122, 131, 140, 149, 158, 167, 176, 210, 219, 228, 237, 246, 255]
        },
        '2B TYPE C1': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [114, 123, 132, 141, 150, 159, 168, 177]
        },
        '1B TYPE D1': {
            'count': 8,
            'bedrooms': 1,
            'apartments': [115, 124, 133, 142, 151, 160, 169, 178]
        },
        '2B TYPE B7': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [116, 125, 134, 143, 152, 161, 170, 179]
        },
        '2B TYPE B1': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [117, 126, 135, 144, 153, 162, 171, 180]
        },
        '3B TYPE B1': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [182]
        },
        '1B TYPE F1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [183]
        },
        '1B TYPE E1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [184]
        },
        '1B TYPE G1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [185]
        },
        '3B TYPE A1': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [186]
        },
        '3B TYPE B2': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [187]
        },
        '2B TYPE C3': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [188]
        },
        '1B TYPE H1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [189]
        },
        '1B TYPE G2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [190]
        },
        '3B TYPE A2': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [191]
        },
        '3B TYPE B3': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [192]
        },
        '2B TYPE C5': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [193]
        },
        '3B TYPE C1': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [194]
        },
        '3B TYPE A3': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [195]
        },
        '1B TYPE B3': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [201]
        },
        '1B TYPE C4': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [202]
        },
        '2B TYPE E6': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [203]
        },
        '2B TYPE D2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [204]
        },
        '2B TYPE A2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [205]
        },
        '2B TYPE B4': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [206]
        },
        '2B TYPE B5': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [207]
        },
        '1B TYPE A2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [208]
        },
        '2B TYPE C6': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [209]
        },
        '1B TYPE C3': {
            'count': 6,
            'bedrooms': 1,
            'apartments': [211, 220, 229, 238, 247, 256]
        },
        '2B TYPE E3 M4(3)': {
            'count': 3,
            'bedrooms': 2,
            'apartments': [212, 221, 230]
        },
        '2B TYPE D1': {
            'count': 6,
            'bedrooms': 2,
            'apartments': [213, 222, 231, 240, 249, 258]
        },
        '2B TYPE A3': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [214, 223, 232, 241, 250, 259, 265, 271]
        },
        '2B TYPE B8': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [215, 224, 233, 242, 251, 260, 266]
        },
        '2B TYPE B6': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [216, 225, 234, 243, 252, 261, 267]
        },
        '1B TYPE A1': {
            'count': 7,
            'bedrooms': 1,
            'apartments': [217, 226, 235, 244, 253, 262, 268]
        },
        '2B TYPE C7': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [218, 227, 236, 245, 254, 263, 269, 275]
        },
        '2B TYPE E3': {
            'count': 3,
            'bedrooms': 2,
            'apartments': [239, 248, 257]
        },
        '2B TYPE F1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [264]
        },
        '2B TYPE F2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [270]
        },
        '2B TYPE G2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [272]
        },
        '2B TYPE G1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [273]
        },
        '1B TYPE A3': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [274]
        },
        '3B TYPE H2': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [276]
        },
        '2B TYPE H1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [277]
        },
        '2B TYPE C2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [278]
        },
        '3B TYPE W2': {
            'count': 8,
            'bedrooms': 3,
            'apartments': [301, 306, 311, 316, 321, 326, 331, 336]
        },
        '2B TYPE Y2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [302]
        },
        '2B TYPE Z1': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [303]
        },
        '3B TYPE Z2': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [304]
        },
        '3B TYPE Z3': {
            'count': 8,
            'bedrooms': 3,
            'apartments': [305, 310, 315, 320, 325, 330, 335, 340]
        },
        '2B TYPE Y3': {
            'count': 4,
            'bedrooms': 2,
            'apartments': [307, 312, 317, 322]
        },
        '3B TYPE W1': {
            'count': 7,
            'bedrooms': 3,
            'apartments': [308, 313, 318, 323, 328, 333, 338]
        },
        '3B TYPE Z1': {
            'count': 7,
            'bedrooms': 3,
            'apartments': [309, 314, 319, 324, 329, 334, 339]
        },
        '2B TYPE Y1': {
            'count': 4,
            'bedrooms': 2,
            'apartments': [327, 332, 337, 714]
        },
        '2B TYPE S3': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [401]
        },
        '2B TYPE S2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [402]
        },
        '2B TYPE T3': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [403]
        },
        '2B TYPE U2': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [404]
        },
        '2B TYPE X1': {
            'count': 2,
            'bedrooms': 2,
            'apartments': [405, 601]
        },
        '2B TYPE V2': {
            'count': 2,
            'bedrooms': 2,
            'apartments': [406, 501]
        },
        '2B TYPE T5': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [407, 414, 421, 428, 435, 441, 445]
        },
        '2B TYPE S1': {
            'count': 10,
            'bedrooms': 2,
            'apartments': [408, 409, 415, 416, 422, 423, 429, 430, 436, 437]
        },
        '2B TYPE T1': {
            'count': 6,
            'bedrooms': 2,
            'apartments': [410, 417, 424, 431, 438, 442]
        },
        '2B TYPE U1': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [411, 418, 425, 432, 439, 443, 705]
        },
        '3B TYPE X1': {
            'count': 3,
            'bedrooms': 3,
            'apartments': [412, 419, 426]
        },
        '2B TYPE V1': {
            'count': 10,
            'bedrooms': 2,
            'apartments': [413, 420, 427, 434, 612, 618, 624, 630, 636, 641]
        },
        '2B TYPE W1': {
            'count': 2,
            'bedrooms': 2,
            'apartments': [433, 545]
        },
        '2B TYPE U3': {
            'count': 2,
            'bedrooms': 2,
            'apartments': [440, 444]
        },
        '1B TYPE I1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [502]
        },
        '1B TYPE K': {
            'count': 2,
            'bedrooms': 1,
            'apartments': [503, 604]
        },
        '1B TYPE I5': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [504]
        },
        '2B TYPE V8': {
            'count': 11,
            'bedrooms': 2,
            'apartments': [505, 512, 519, 526, 533, 540, 547, 554, 561, 568, 575]
        },
        '2B TYPE T': {
            'count': 22,
            'bedrooms': 2,
            'apartments': [506, 507, 513, 514, 520, 521, 527, 528, 534, 535, 541, 542, 548, 549, 555, 556, 562, 563, 569, 570, 576, 577]
        },
        '2B TYPE V': {
            'count': 10,
            'bedrooms': 2,
            'apartments': [508, 515, 522, 529, 536, 543, 550, 557, 564, 571]
        },
        '1B TYPE I': {
            'count': 24,
            'bedrooms': 1,
            'apartments': [509, 511, 516, 518, 523, 525, 530, 532, 537, 539, 544, 546, 551, 553, 558, 560, 565, 567, 572, 574, 579, 581, 586, 588]
        },
        '2B TYPE W': {
            'count': 10,
            'bedrooms': 2,
            'apartments': [510, 517, 524, 531, 538, 610, 616, 622, 628, 634]
        },
        '2B TYPE W2': {
            'count': 6,
            'bedrooms': 2,
            'apartments': [552, 559, 566, 573, 580, 587]
        },
        '3B TYPE I': {
            'count': 2,
            'bedrooms': 3,
            'apartments': [578, 585]
        },
        '3B TYPE I2': {
            'count': 2,
            'bedrooms': 3,
            'apartments': [582, 589]
        },
        '1B TYPE M': {
            'count': 4,
            'bedrooms': 1,
            'apartments': [583, 584, 590, 591]
        },
        '3B TYPE K': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [592]
        },
        '3B TYPE H3': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [593]
        },
        '3B TYPE H': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [594]
        },
        '2B TYPE V7': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [602, 608, 614, 620, 626, 632, 638]
        },
        '1B TYPE L2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [603]
        },
        '1B TYPE L1': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [605]
        },
        '2B TYPE V3': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [606]
        },
        '2B TYPE X': {
            'count': 6,
            'bedrooms': 2,
            'apartments': [607, 613, 619, 625, 631, 637]
        },
        '1B TYPE L': {
            'count': 12,
            'bedrooms': 1,
            'apartments': [609, 611, 615, 617, 621, 623, 627, 629, 633, 635, 639, 640]
        },
        '2B TYPE S': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [642]
        },
        '3B TYPE J': {
            'count': 1,
            'bedrooms': 3,
            'apartments': [643]
        },
        '2B TYPE V4': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [644]
        },
        '2B TYPE T2': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [701, 709, 717, 725, 733, 741, 749, 755]
        },
        '2B TYPE T4': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [702, 710, 718, 726, 734, 742, 750, 756]
        },
        '2B TYPE V9': {
            'count': 8,
            'bedrooms': 2,
            'apartments': [703, 711, 719, 727, 735, 743, 751, 757]
        },
        '1B TYPE I4': {
            'count': 6,
            'bedrooms': 1,
            'apartments': [704, 712, 720, 728, 736, 744]
        },
        '2B TYPE Z': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [706]
        },
        '1B TYPE J2': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [707]
        },
        '2B TYPE V6': {
            'count': 1,
            'bedrooms': 2,
            'apartments': [708]
        },
        '2B TYPE U': {
            'count': 5,
            'bedrooms': 2,
            'apartments': [713, 721, 729, 737, 745]
        },
        '1B TYPE J': {
            'count': 4,
            'bedrooms': 1,
            'apartments': [715, 723, 731, 739]
        },
        '2B TYPE V5': {
            'count': 7,
            'bedrooms': 2,
            'apartments': [716, 724, 732, 740, 748, 754, 760]
        },
        '2B TYPE Y': {
            'count': 4,
            'bedrooms': 2,
            'apartments': [722, 730, 738, 746]
        },
        '1B TYPE J3': {
            'count': 1,
            'bedrooms': 1,
            'apartments': [747]
        },
        '1B TYPE I2': {
            'count': 2,
            'bedrooms': 1,
            'apartments': [752, 758]
        },
        '1B TYPE J1': {
            'count': 2,
            'bedrooms': 1,
            'apartments': [753, 759]
        },
    },
    
    'tenures': {
        'Private': {
            'count': 311,
            'apartments': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644]
        },
        'Rented': {
            'count': 85,
            'apartments': [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445]
        },
        'S/O': {
            'count': 60,
            'apartments': [701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760]
        },
    },
    
    'apartment_lookup': {
        # Full apartment lookup dictionary with 456 apartments
        101: {'phase': None, 'block': 'A', 'floor': 1, 'type': '2B TYPE E4', 'bedrooms': 2, 'tenure': 'Private'},
        102: {'phase': None, 'block': 'A', 'floor': 1, 'type': '2B TYPE E5', 'bedrooms': 2, 'tenure': 'Private'},
        103: {'phase': None, 'block': 'A', 'floor': 1, 'type': '1B TYPE C2', 'bedrooms': 1, 'tenure': 'Private'},
        104: {'phase': None, 'block': 'A', 'floor': 1, 'type': '1B TYPE B2', 'bedrooms': 1, 'tenure': 'Private'},
        105: {'phase': None, 'block': 'A', 'floor': 1, 'type': '2B TYPE C4', 'bedrooms': 2, 'tenure': 'Private'},
        106: {'phase': None, 'block': 'A', 'floor': 1, 'type': '1B TYPE D2', 'bedrooms': 1, 'tenure': 'Private'},
        107: {'phase': None, 'block': 'A', 'floor': 1, 'type': '2B TYPE B2', 'bedrooms': 2, 'tenure': 'Private'},
        108: {'phase': None, 'block': 'A', 'floor': 1, 'type': '2B TYPE B3', 'bedrooms': 2, 'tenure': 'Private'},
        109: {'phase': None, 'block': 'A', 'floor': 1, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        110: {'phase': None, 'block': 'A', 'floor': 2, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        111: {'phase': None, 'block': 'A', 'floor': 2, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        112: {'phase': None, 'block': 'A', 'floor': 2, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        113: {'phase': None, 'block': 'A', 'floor': 2, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        114: {'phase': None, 'block': 'A', 'floor': 2, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        115: {'phase': None, 'block': 'A', 'floor': 2, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        116: {'phase': None, 'block': 'A', 'floor': 2, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        117: {'phase': None, 'block': 'A', 'floor': 2, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        118: {'phase': None, 'block': 'A', 'floor': 2, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        119: {'phase': None, 'block': 'A', 'floor': 3, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        120: {'phase': None, 'block': 'A', 'floor': 3, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        121: {'phase': None, 'block': 'A', 'floor': 3, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        122: {'phase': None, 'block': 'A', 'floor': 3, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        123: {'phase': None, 'block': 'A', 'floor': 3, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        124: {'phase': None, 'block': 'A', 'floor': 3, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        125: {'phase': None, 'block': 'A', 'floor': 3, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        126: {'phase': None, 'block': 'A', 'floor': 3, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        127: {'phase': None, 'block': 'A', 'floor': 3, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        128: {'phase': None, 'block': 'A', 'floor': 4, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        129: {'phase': None, 'block': 'A', 'floor': 4, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        130: {'phase': None, 'block': 'A', 'floor': 4, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        131: {'phase': None, 'block': 'A', 'floor': 4, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        132: {'phase': None, 'block': 'A', 'floor': 4, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        133: {'phase': None, 'block': 'A', 'floor': 4, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        134: {'phase': None, 'block': 'A', 'floor': 4, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        135: {'phase': None, 'block': 'A', 'floor': 4, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        136: {'phase': None, 'block': 'A', 'floor': 4, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        137: {'phase': None, 'block': 'A', 'floor': 5, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        138: {'phase': None, 'block': 'A', 'floor': 5, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        139: {'phase': None, 'block': 'A', 'floor': 5, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        140: {'phase': None, 'block': 'A', 'floor': 5, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        141: {'phase': None, 'block': 'A', 'floor': 5, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        142: {'phase': None, 'block': 'A', 'floor': 5, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        143: {'phase': None, 'block': 'A', 'floor': 5, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        144: {'phase': None, 'block': 'A', 'floor': 5, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        145: {'phase': None, 'block': 'A', 'floor': 5, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        146: {'phase': None, 'block': 'A', 'floor': 6, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        147: {'phase': None, 'block': 'A', 'floor': 6, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        148: {'phase': None, 'block': 'A', 'floor': 6, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        149: {'phase': None, 'block': 'A', 'floor': 6, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        150: {'phase': None, 'block': 'A', 'floor': 6, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        151: {'phase': None, 'block': 'A', 'floor': 6, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        152: {'phase': None, 'block': 'A', 'floor': 6, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        153: {'phase': None, 'block': 'A', 'floor': 6, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        154: {'phase': None, 'block': 'A', 'floor': 6, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        155: {'phase': None, 'block': 'A', 'floor': 7, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        156: {'phase': None, 'block': 'A', 'floor': 7, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        157: {'phase': None, 'block': 'A', 'floor': 7, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        158: {'phase': None, 'block': 'A', 'floor': 7, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        159: {'phase': None, 'block': 'A', 'floor': 7, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        160: {'phase': None, 'block': 'A', 'floor': 7, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        161: {'phase': None, 'block': 'A', 'floor': 7, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        162: {'phase': None, 'block': 'A', 'floor': 7, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        163: {'phase': None, 'block': 'A', 'floor': 7, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        164: {'phase': None, 'block': 'A', 'floor': 8, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        165: {'phase': None, 'block': 'A', 'floor': 8, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        166: {'phase': None, 'block': 'A', 'floor': 8, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        167: {'phase': None, 'block': 'A', 'floor': 8, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        168: {'phase': None, 'block': 'A', 'floor': 8, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        169: {'phase': None, 'block': 'A', 'floor': 8, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        170: {'phase': None, 'block': 'A', 'floor': 8, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        171: {'phase': None, 'block': 'A', 'floor': 8, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        172: {'phase': None, 'block': 'A', 'floor': 8, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        173: {'phase': None, 'block': 'A', 'floor': 9, 'type': '2B TYPE E1', 'bedrooms': 2, 'tenure': 'Private'},
        174: {'phase': None, 'block': 'A', 'floor': 9, 'type': '2B TYPE E2', 'bedrooms': 2, 'tenure': 'Private'},
        175: {'phase': None, 'block': 'A', 'floor': 9, 'type': '1B TYPE C1', 'bedrooms': 1, 'tenure': 'Private'},
        176: {'phase': None, 'block': 'A', 'floor': 9, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        177: {'phase': None, 'block': 'A', 'floor': 9, 'type': '2B TYPE C1', 'bedrooms': 2, 'tenure': 'Private'},
        178: {'phase': None, 'block': 'A', 'floor': 9, 'type': '1B TYPE D1', 'bedrooms': 1, 'tenure': 'Private'},
        179: {'phase': None, 'block': 'A', 'floor': 9, 'type': '2B TYPE B7', 'bedrooms': 2, 'tenure': 'Private'},
        180: {'phase': None, 'block': 'A', 'floor': 9, 'type': '2B TYPE B1', 'bedrooms': 2, 'tenure': 'Private'},
        181: {'phase': None, 'block': 'A', 'floor': 9, 'type': '2B TYPE A1', 'bedrooms': 2, 'tenure': 'Private'},
        182: {'phase': None, 'block': 'A', 'floor': 10, 'type': '3B TYPE B1', 'bedrooms': 3, 'tenure': 'Private'},
        183: {'phase': None, 'block': 'A', 'floor': 10, 'type': '1B TYPE F1', 'bedrooms': 1, 'tenure': 'Private'},
        184: {'phase': None, 'block': 'A', 'floor': 10, 'type': '1B TYPE E1', 'bedrooms': 1, 'tenure': 'Private'},
        185: {'phase': None, 'block': 'A', 'floor': 10, 'type': '1B TYPE G1', 'bedrooms': 1, 'tenure': 'Private'},
        186: {'phase': None, 'block': 'A', 'floor': 10, 'type': '3B TYPE A1', 'bedrooms': 3, 'tenure': 'Private'},
        187: {'phase': None, 'block': 'A', 'floor': 11, 'type': '3B TYPE B2', 'bedrooms': 3, 'tenure': 'Private'},
        188: {'phase': None, 'block': 'A', 'floor': 11, 'type': '2B TYPE C3', 'bedrooms': 2, 'tenure': 'Private'},
        189: {'phase': None, 'block': 'A', 'floor': 11, 'type': '1B TYPE H1', 'bedrooms': 1, 'tenure': 'Private'},
        190: {'phase': None, 'block': 'A', 'floor': 11, 'type': '1B TYPE G2', 'bedrooms': 1, 'tenure': 'Private'},
        191: {'phase': None, 'block': 'A', 'floor': 11, 'type': '3B TYPE A2', 'bedrooms': 3, 'tenure': 'Private'},
        192: {'phase': None, 'block': 'A', 'floor': 12, 'type': '3B TYPE B3', 'bedrooms': 3, 'tenure': 'Private'},
        193: {'phase': None, 'block': 'A', 'floor': 12, 'type': '2B TYPE C5', 'bedrooms': 2, 'tenure': 'Private'},
        194: {'phase': None, 'block': 'A', 'floor': 12, 'type': '3B TYPE C1', 'bedrooms': 3, 'tenure': 'Private'},
        195: {'phase': None, 'block': 'A', 'floor': 12, 'type': '3B TYPE A3', 'bedrooms': 3, 'tenure': 'Private'},
        201: {'phase': None, 'block': 'B', 'floor': 1, 'type': '1B TYPE B3', 'bedrooms': 1, 'tenure': 'Private'},
        202: {'phase': None, 'block': 'B', 'floor': 1, 'type': '1B TYPE C4', 'bedrooms': 1, 'tenure': 'Private'},
        203: {'phase': None, 'block': 'B', 'floor': 1, 'type': '2B TYPE E6', 'bedrooms': 2, 'tenure': 'Private'},
        204: {'phase': None, 'block': 'B', 'floor': 1, 'type': '2B TYPE D2', 'bedrooms': 2, 'tenure': 'Private'},
        205: {'phase': None, 'block': 'B', 'floor': 1, 'type': '2B TYPE A2', 'bedrooms': 2, 'tenure': 'Private'},
        206: {'phase': None, 'block': 'B', 'floor': 1, 'type': '2B TYPE B4', 'bedrooms': 2, 'tenure': 'Private'},
        207: {'phase': None, 'block': 'B', 'floor': 1, 'type': '2B TYPE B5', 'bedrooms': 2, 'tenure': 'Private'},
        208: {'phase': None, 'block': 'B', 'floor': 1, 'type': '1B TYPE A2', 'bedrooms': 1, 'tenure': 'Private'},
        209: {'phase': None, 'block': 'B', 'floor': 1, 'type': '2B TYPE C6', 'bedrooms': 2, 'tenure': 'Private'},
        210: {'phase': None, 'block': 'B', 'floor': 2, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        211: {'phase': None, 'block': 'B', 'floor': 2, 'type': '1B TYPE C3', 'bedrooms': 1, 'tenure': 'Private'},
        212: {'phase': None, 'block': 'B', 'floor': 2, 'type': '2B TYPE E3 M4(3)', 'bedrooms': 2, 'tenure': 'Private'},
        213: {'phase': None, 'block': 'B', 'floor': 2, 'type': '2B TYPE D1', 'bedrooms': 2, 'tenure': 'Private'},
        214: {'phase': None, 'block': 'B', 'floor': 2, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        215: {'phase': None, 'block': 'B', 'floor': 2, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        216: {'phase': None, 'block': 'B', 'floor': 2, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        217: {'phase': None, 'block': 'B', 'floor': 2, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        218: {'phase': None, 'block': 'B', 'floor': 2, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        219: {'phase': None, 'block': 'B', 'floor': 3, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        220: {'phase': None, 'block': 'B', 'floor': 3, 'type': '1B TYPE C3', 'bedrooms': 1, 'tenure': 'Private'},
        221: {'phase': None, 'block': 'B', 'floor': 3, 'type': '2B TYPE E3 M4(3)', 'bedrooms': 2, 'tenure': 'Private'},
        222: {'phase': None, 'block': 'B', 'floor': 3, 'type': '2B TYPE D1', 'bedrooms': 2, 'tenure': 'Private'},
        223: {'phase': None, 'block': 'B', 'floor': 3, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        224: {'phase': None, 'block': 'B', 'floor': 3, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        225: {'phase': None, 'block': 'B', 'floor': 3, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        226: {'phase': None, 'block': 'B', 'floor': 3, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        227: {'phase': None, 'block': 'B', 'floor': 3, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        228: {'phase': None, 'block': 'B', 'floor': 4, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        229: {'phase': None, 'block': 'B', 'floor': 4, 'type': '1B TYPE C3', 'bedrooms': 1, 'tenure': 'Private'},
        230: {'phase': None, 'block': 'B', 'floor': 4, 'type': '2B TYPE E3 M4(3)', 'bedrooms': 2, 'tenure': 'Private'},
        231: {'phase': None, 'block': 'B', 'floor': 4, 'type': '2B TYPE D1', 'bedrooms': 2, 'tenure': 'Private'},
        232: {'phase': None, 'block': 'B', 'floor': 4, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        233: {'phase': None, 'block': 'B', 'floor': 4, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        234: {'phase': None, 'block': 'B', 'floor': 4, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        235: {'phase': None, 'block': 'B', 'floor': 4, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        236: {'phase': None, 'block': 'B', 'floor': 4, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        237: {'phase': None, 'block': 'B', 'floor': 5, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        238: {'phase': None, 'block': 'B', 'floor': 5, 'type': '1B TYPE C3', 'bedrooms': 1, 'tenure': 'Private'},
        239: {'phase': None, 'block': 'B', 'floor': 5, 'type': '2B TYPE E3', 'bedrooms': 2, 'tenure': 'Private'},
        240: {'phase': None, 'block': 'B', 'floor': 5, 'type': '2B TYPE D1', 'bedrooms': 2, 'tenure': 'Private'},
        241: {'phase': None, 'block': 'B', 'floor': 5, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        242: {'phase': None, 'block': 'B', 'floor': 5, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        243: {'phase': None, 'block': 'B', 'floor': 5, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        244: {'phase': None, 'block': 'B', 'floor': 5, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        245: {'phase': None, 'block': 'B', 'floor': 5, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        246: {'phase': None, 'block': 'B', 'floor': 6, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        247: {'phase': None, 'block': 'B', 'floor': 6, 'type': '1B TYPE C3', 'bedrooms': 1, 'tenure': 'Private'},
        248: {'phase': None, 'block': 'B', 'floor': 6, 'type': '2B TYPE E3', 'bedrooms': 2, 'tenure': 'Private'},
        249: {'phase': None, 'block': 'B', 'floor': 6, 'type': '2B TYPE D1', 'bedrooms': 2, 'tenure': 'Private'},
        250: {'phase': None, 'block': 'B', 'floor': 6, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        251: {'phase': None, 'block': 'B', 'floor': 6, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        252: {'phase': None, 'block': 'B', 'floor': 6, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        253: {'phase': None, 'block': 'B', 'floor': 6, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        254: {'phase': None, 'block': 'B', 'floor': 6, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        255: {'phase': None, 'block': 'B', 'floor': 7, 'type': '1B TYPE B1', 'bedrooms': 1, 'tenure': 'Private'},
        256: {'phase': None, 'block': 'B', 'floor': 7, 'type': '1B TYPE C3', 'bedrooms': 1, 'tenure': 'Private'},
        257: {'phase': None, 'block': 'B', 'floor': 7, 'type': '2B TYPE E3', 'bedrooms': 2, 'tenure': 'Private'},
        258: {'phase': None, 'block': 'B', 'floor': 7, 'type': '2B TYPE D1', 'bedrooms': 2, 'tenure': 'Private'},
        259: {'phase': None, 'block': 'B', 'floor': 7, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        260: {'phase': None, 'block': 'B', 'floor': 7, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        261: {'phase': None, 'block': 'B', 'floor': 7, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        262: {'phase': None, 'block': 'B', 'floor': 7, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        263: {'phase': None, 'block': 'B', 'floor': 7, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        264: {'phase': None, 'block': 'B', 'floor': 8, 'type': '2B TYPE F1', 'bedrooms': 2, 'tenure': 'Private'},
        265: {'phase': None, 'block': 'B', 'floor': 8, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        266: {'phase': None, 'block': 'B', 'floor': 8, 'type': '2B TYPE B8', 'bedrooms': 2, 'tenure': 'Private'},
        267: {'phase': None, 'block': 'B', 'floor': 8, 'type': '2B TYPE B6', 'bedrooms': 2, 'tenure': 'Private'},
        268: {'phase': None, 'block': 'B', 'floor': 8, 'type': '1B TYPE A1', 'bedrooms': 1, 'tenure': 'Private'},
        269: {'phase': None, 'block': 'B', 'floor': 8, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        270: {'phase': None, 'block': 'B', 'floor': 9, 'type': '2B TYPE F2', 'bedrooms': 2, 'tenure': 'Private'},
        271: {'phase': None, 'block': 'B', 'floor': 9, 'type': '2B TYPE A3', 'bedrooms': 2, 'tenure': 'Private'},
        272: {'phase': None, 'block': 'B', 'floor': 9, 'type': '2B TYPE G2', 'bedrooms': 2, 'tenure': 'Private'},
        273: {'phase': None, 'block': 'B', 'floor': 9, 'type': '2B TYPE G1', 'bedrooms': 2, 'tenure': 'Private'},
        274: {'phase': None, 'block': 'B', 'floor': 9, 'type': '1B TYPE A3', 'bedrooms': 1, 'tenure': 'Private'},
        275: {'phase': None, 'block': 'B', 'floor': 9, 'type': '2B TYPE C7', 'bedrooms': 2, 'tenure': 'Private'},
        276: {'phase': None, 'block': 'B', 'floor': 10, 'type': '3B TYPE H2', 'bedrooms': 3, 'tenure': 'Private'},
        277: {'phase': None, 'block': 'B', 'floor': 10, 'type': '2B TYPE H1', 'bedrooms': 2, 'tenure': 'Private'},
        278: {'phase': None, 'block': 'B', 'floor': 10, 'type': '2B TYPE C2', 'bedrooms': 2, 'tenure': 'Private'},
        301: {'phase': None, 'block': 'C', 'floor': 1, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        302: {'phase': None, 'block': 'C', 'floor': 1, 'type': '2B TYPE Y2', 'bedrooms': 2, 'tenure': 'Rented'},
        303: {'phase': None, 'block': 'C', 'floor': 1, 'type': '2B TYPE Z1', 'bedrooms': 2, 'tenure': 'Rented'},
        304: {'phase': None, 'block': 'C', 'floor': 1, 'type': '3B TYPE Z2', 'bedrooms': 3, 'tenure': 'Rented'},
        305: {'phase': None, 'block': 'C', 'floor': 1, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        306: {'phase': None, 'block': 'C', 'floor': 2, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        307: {'phase': None, 'block': 'C', 'floor': 2, 'type': '2B TYPE Y3', 'bedrooms': 2, 'tenure': 'Rented'},
        308: {'phase': None, 'block': 'C', 'floor': 2, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        309: {'phase': None, 'block': 'C', 'floor': 2, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        310: {'phase': None, 'block': 'C', 'floor': 2, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        311: {'phase': None, 'block': 'C', 'floor': 3, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        312: {'phase': None, 'block': 'C', 'floor': 3, 'type': '2B TYPE Y3', 'bedrooms': 2, 'tenure': 'Rented'},
        313: {'phase': None, 'block': 'C', 'floor': 3, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        314: {'phase': None, 'block': 'C', 'floor': 3, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        315: {'phase': None, 'block': 'C', 'floor': 3, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        316: {'phase': None, 'block': 'C', 'floor': 4, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        317: {'phase': None, 'block': 'C', 'floor': 4, 'type': '2B TYPE Y3', 'bedrooms': 2, 'tenure': 'Rented'},
        318: {'phase': None, 'block': 'C', 'floor': 4, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        319: {'phase': None, 'block': 'C', 'floor': 4, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        320: {'phase': None, 'block': 'C', 'floor': 4, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        321: {'phase': None, 'block': 'C', 'floor': 5, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        322: {'phase': None, 'block': 'C', 'floor': 5, 'type': '2B TYPE Y3', 'bedrooms': 2, 'tenure': 'Rented'},
        323: {'phase': None, 'block': 'C', 'floor': 5, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        324: {'phase': None, 'block': 'C', 'floor': 5, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        325: {'phase': None, 'block': 'C', 'floor': 5, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        326: {'phase': None, 'block': 'C', 'floor': 6, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        327: {'phase': None, 'block': 'C', 'floor': 6, 'type': '2B TYPE Y1', 'bedrooms': 2, 'tenure': 'Rented'},
        328: {'phase': None, 'block': 'C', 'floor': 6, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        329: {'phase': None, 'block': 'C', 'floor': 6, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        330: {'phase': None, 'block': 'C', 'floor': 6, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        331: {'phase': None, 'block': 'C', 'floor': 7, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        332: {'phase': None, 'block': 'C', 'floor': 7, 'type': '2B TYPE Y1', 'bedrooms': 2, 'tenure': 'Rented'},
        333: {'phase': None, 'block': 'C', 'floor': 7, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        334: {'phase': None, 'block': 'C', 'floor': 7, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        335: {'phase': None, 'block': 'C', 'floor': 7, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        336: {'phase': None, 'block': 'C', 'floor': 8, 'type': '3B TYPE W2', 'bedrooms': 3, 'tenure': 'Rented'},
        337: {'phase': None, 'block': 'C', 'floor': 8, 'type': '2B TYPE Y1', 'bedrooms': 2, 'tenure': 'Rented'},
        338: {'phase': None, 'block': 'C', 'floor': 8, 'type': '3B TYPE W1', 'bedrooms': 3, 'tenure': 'Rented'},
        339: {'phase': None, 'block': 'C', 'floor': 8, 'type': '3B TYPE Z1', 'bedrooms': 3, 'tenure': 'Rented'},
        340: {'phase': None, 'block': 'C', 'floor': 8, 'type': '3B TYPE Z3', 'bedrooms': 3, 'tenure': 'Rented'},
        401: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE S3', 'bedrooms': 2, 'tenure': 'Rented'},
        402: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE S2', 'bedrooms': 2, 'tenure': 'Rented'},
        403: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE T3', 'bedrooms': 2, 'tenure': 'Rented'},
        404: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE U2', 'bedrooms': 2, 'tenure': 'Rented'},
        405: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE X1', 'bedrooms': 2, 'tenure': 'Rented'},
        406: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE V2', 'bedrooms': 2, 'tenure': 'Rented'},
        407: {'phase': None, 'block': 'D', 'floor': 1, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        408: {'phase': None, 'block': 'D', 'floor': 2, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        409: {'phase': None, 'block': 'D', 'floor': 2, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        410: {'phase': None, 'block': 'D', 'floor': 2, 'type': '2B TYPE T1', 'bedrooms': 2, 'tenure': 'Rented'},
        411: {'phase': None, 'block': 'D', 'floor': 2, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'Rented'},
        412: {'phase': None, 'block': 'D', 'floor': 2, 'type': '3B TYPE X1', 'bedrooms': 3, 'tenure': 'Rented'},
        413: {'phase': None, 'block': 'D', 'floor': 2, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Rented'},
        414: {'phase': None, 'block': 'D', 'floor': 2, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        415: {'phase': None, 'block': 'D', 'floor': 3, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        416: {'phase': None, 'block': 'D', 'floor': 3, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        417: {'phase': None, 'block': 'D', 'floor': 3, 'type': '2B TYPE T1', 'bedrooms': 2, 'tenure': 'Rented'},
        418: {'phase': None, 'block': 'D', 'floor': 3, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'Rented'},
        419: {'phase': None, 'block': 'D', 'floor': 3, 'type': '3B TYPE X1', 'bedrooms': 3, 'tenure': 'Rented'},
        420: {'phase': None, 'block': 'D', 'floor': 3, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Rented'},
        421: {'phase': None, 'block': 'D', 'floor': 3, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        422: {'phase': None, 'block': 'D', 'floor': 4, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        423: {'phase': None, 'block': 'D', 'floor': 4, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        424: {'phase': None, 'block': 'D', 'floor': 4, 'type': '2B TYPE T1', 'bedrooms': 2, 'tenure': 'Rented'},
        425: {'phase': None, 'block': 'D', 'floor': 4, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'Rented'},
        426: {'phase': None, 'block': 'D', 'floor': 4, 'type': '3B TYPE X1', 'bedrooms': 3, 'tenure': 'Rented'},
        427: {'phase': None, 'block': 'D', 'floor': 4, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Rented'},
        428: {'phase': None, 'block': 'D', 'floor': 4, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        429: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        430: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        431: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE T1', 'bedrooms': 2, 'tenure': 'Rented'},
        432: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'Rented'},
        433: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE W1', 'bedrooms': 2, 'tenure': 'Rented'},
        434: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Rented'},
        435: {'phase': None, 'block': 'D', 'floor': 5, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        436: {'phase': None, 'block': 'D', 'floor': 6, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        437: {'phase': None, 'block': 'D', 'floor': 6, 'type': '2B TYPE S1', 'bedrooms': 2, 'tenure': 'Rented'},
        438: {'phase': None, 'block': 'D', 'floor': 6, 'type': '2B TYPE T1', 'bedrooms': 2, 'tenure': 'Rented'},
        439: {'phase': None, 'block': 'D', 'floor': 6, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'Rented'},
        440: {'phase': None, 'block': 'D', 'floor': 6, 'type': '2B TYPE U3', 'bedrooms': 2, 'tenure': 'Rented'},
        441: {'phase': None, 'block': 'D', 'floor': 6, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        442: {'phase': None, 'block': 'D', 'floor': 7, 'type': '2B TYPE T1', 'bedrooms': 2, 'tenure': 'Rented'},
        443: {'phase': None, 'block': 'D', 'floor': 7, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'Rented'},
        444: {'phase': None, 'block': 'D', 'floor': 7, 'type': '2B TYPE U3', 'bedrooms': 2, 'tenure': 'Rented'},
        445: {'phase': None, 'block': 'D', 'floor': 7, 'type': '2B TYPE T5', 'bedrooms': 2, 'tenure': 'Rented'},
        501: {'phase': None, 'block': 'E', 'floor': 1, 'type': '2B TYPE V2', 'bedrooms': 2, 'tenure': 'Private'},
        502: {'phase': None, 'block': 'E', 'floor': 1, 'type': '1B TYPE I1', 'bedrooms': 1, 'tenure': 'Private'},
        503: {'phase': None, 'block': 'E', 'floor': 1, 'type': '1B TYPE K', 'bedrooms': 1, 'tenure': 'Private'},
        504: {'phase': None, 'block': 'E', 'floor': 1, 'type': '1B TYPE I5', 'bedrooms': 1, 'tenure': 'Private'},
        505: {'phase': None, 'block': 'E', 'floor': 1, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        506: {'phase': None, 'block': 'E', 'floor': 1, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        507: {'phase': None, 'block': 'E', 'floor': 1, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        508: {'phase': None, 'block': 'E', 'floor': 2, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        509: {'phase': None, 'block': 'E', 'floor': 2, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        510: {'phase': None, 'block': 'E', 'floor': 2, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        511: {'phase': None, 'block': 'E', 'floor': 2, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        512: {'phase': None, 'block': 'E', 'floor': 2, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        513: {'phase': None, 'block': 'E', 'floor': 2, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        514: {'phase': None, 'block': 'E', 'floor': 2, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        515: {'phase': None, 'block': 'E', 'floor': 3, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        516: {'phase': None, 'block': 'E', 'floor': 3, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        517: {'phase': None, 'block': 'E', 'floor': 3, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        518: {'phase': None, 'block': 'E', 'floor': 3, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        519: {'phase': None, 'block': 'E', 'floor': 3, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        520: {'phase': None, 'block': 'E', 'floor': 3, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        521: {'phase': None, 'block': 'E', 'floor': 3, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        522: {'phase': None, 'block': 'E', 'floor': 4, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        523: {'phase': None, 'block': 'E', 'floor': 4, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        524: {'phase': None, 'block': 'E', 'floor': 4, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        525: {'phase': None, 'block': 'E', 'floor': 4, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        526: {'phase': None, 'block': 'E', 'floor': 4, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        527: {'phase': None, 'block': 'E', 'floor': 4, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        528: {'phase': None, 'block': 'E', 'floor': 4, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        529: {'phase': None, 'block': 'E', 'floor': 5, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        530: {'phase': None, 'block': 'E', 'floor': 5, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        531: {'phase': None, 'block': 'E', 'floor': 5, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        532: {'phase': None, 'block': 'E', 'floor': 5, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        533: {'phase': None, 'block': 'E', 'floor': 5, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        534: {'phase': None, 'block': 'E', 'floor': 5, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        535: {'phase': None, 'block': 'E', 'floor': 5, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        536: {'phase': None, 'block': 'E', 'floor': 6, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        537: {'phase': None, 'block': 'E', 'floor': 6, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        538: {'phase': None, 'block': 'E', 'floor': 6, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        539: {'phase': None, 'block': 'E', 'floor': 6, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        540: {'phase': None, 'block': 'E', 'floor': 6, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        541: {'phase': None, 'block': 'E', 'floor': 6, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        542: {'phase': None, 'block': 'E', 'floor': 6, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        543: {'phase': None, 'block': 'E', 'floor': 7, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        544: {'phase': None, 'block': 'E', 'floor': 7, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        545: {'phase': None, 'block': 'E', 'floor': 7, 'type': '2B TYPE W1', 'bedrooms': 2, 'tenure': 'Private'},
        546: {'phase': None, 'block': 'E', 'floor': 7, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        547: {'phase': None, 'block': 'E', 'floor': 7, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        548: {'phase': None, 'block': 'E', 'floor': 7, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        549: {'phase': None, 'block': 'E', 'floor': 7, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        550: {'phase': None, 'block': 'E', 'floor': 8, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        551: {'phase': None, 'block': 'E', 'floor': 8, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        552: {'phase': None, 'block': 'E', 'floor': 8, 'type': '2B TYPE W2', 'bedrooms': 2, 'tenure': 'Private'},
        553: {'phase': None, 'block': 'E', 'floor': 8, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        554: {'phase': None, 'block': 'E', 'floor': 8, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        555: {'phase': None, 'block': 'E', 'floor': 8, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        556: {'phase': None, 'block': 'E', 'floor': 8, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        557: {'phase': None, 'block': 'E', 'floor': 9, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        558: {'phase': None, 'block': 'E', 'floor': 9, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        559: {'phase': None, 'block': 'E', 'floor': 9, 'type': '2B TYPE W2', 'bedrooms': 2, 'tenure': 'Private'},
        560: {'phase': None, 'block': 'E', 'floor': 9, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        561: {'phase': None, 'block': 'E', 'floor': 9, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        562: {'phase': None, 'block': 'E', 'floor': 9, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        563: {'phase': None, 'block': 'E', 'floor': 9, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        564: {'phase': None, 'block': 'E', 'floor': 10, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        565: {'phase': None, 'block': 'E', 'floor': 10, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        566: {'phase': None, 'block': 'E', 'floor': 10, 'type': '2B TYPE W2', 'bedrooms': 2, 'tenure': 'Private'},
        567: {'phase': None, 'block': 'E', 'floor': 10, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        568: {'phase': None, 'block': 'E', 'floor': 10, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        569: {'phase': None, 'block': 'E', 'floor': 10, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        570: {'phase': None, 'block': 'E', 'floor': 10, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        571: {'phase': None, 'block': 'E', 'floor': 11, 'type': '2B TYPE V', 'bedrooms': 2, 'tenure': 'Private'},
        572: {'phase': None, 'block': 'E', 'floor': 11, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        573: {'phase': None, 'block': 'E', 'floor': 11, 'type': '2B TYPE W2', 'bedrooms': 2, 'tenure': 'Private'},
        574: {'phase': None, 'block': 'E', 'floor': 11, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        575: {'phase': None, 'block': 'E', 'floor': 11, 'type': '2B TYPE V8', 'bedrooms': 2, 'tenure': 'Private'},
        576: {'phase': None, 'block': 'E', 'floor': 11, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        577: {'phase': None, 'block': 'E', 'floor': 11, 'type': '2B TYPE T', 'bedrooms': 2, 'tenure': 'Private'},
        578: {'phase': None, 'block': 'E', 'floor': 12, 'type': '3B TYPE I', 'bedrooms': 3, 'tenure': 'Private'},
        579: {'phase': None, 'block': 'E', 'floor': 12, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        580: {'phase': None, 'block': 'E', 'floor': 12, 'type': '2B TYPE W2', 'bedrooms': 2, 'tenure': 'Private'},
        581: {'phase': None, 'block': 'E', 'floor': 12, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        582: {'phase': None, 'block': 'E', 'floor': 12, 'type': '3B TYPE I2', 'bedrooms': 3, 'tenure': 'Private'},
        583: {'phase': None, 'block': 'E', 'floor': 12, 'type': '1B TYPE M', 'bedrooms': 1, 'tenure': 'Private'},
        584: {'phase': None, 'block': 'E', 'floor': 12, 'type': '1B TYPE M', 'bedrooms': 1, 'tenure': 'Private'},
        585: {'phase': None, 'block': 'E', 'floor': 13, 'type': '3B TYPE I', 'bedrooms': 3, 'tenure': 'Private'},
        586: {'phase': None, 'block': 'E', 'floor': 13, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        587: {'phase': None, 'block': 'E', 'floor': 13, 'type': '2B TYPE W2', 'bedrooms': 2, 'tenure': 'Private'},
        588: {'phase': None, 'block': 'E', 'floor': 13, 'type': '1B TYPE I', 'bedrooms': 1, 'tenure': 'Private'},
        589: {'phase': None, 'block': 'E', 'floor': 13, 'type': '3B TYPE I2', 'bedrooms': 3, 'tenure': 'Private'},
        590: {'phase': None, 'block': 'E', 'floor': 13, 'type': '1B TYPE M', 'bedrooms': 1, 'tenure': 'Private'},
        591: {'phase': None, 'block': 'E', 'floor': 13, 'type': '1B TYPE M', 'bedrooms': 1, 'tenure': 'Private'},
        592: {'phase': None, 'block': 'E', 'floor': 14, 'type': '3B TYPE K', 'bedrooms': 3, 'tenure': 'Private'},
        593: {'phase': None, 'block': 'E', 'floor': 14, 'type': '3B TYPE H3', 'bedrooms': 3, 'tenure': 'Private'},
        594: {'phase': None, 'block': 'E', 'floor': 14, 'type': '3B TYPE H', 'bedrooms': 3, 'tenure': 'Private'},
        601: {'phase': None, 'block': 'F', 'floor': 1, 'type': '2B TYPE X1', 'bedrooms': 2, 'tenure': 'Private'},
        602: {'phase': None, 'block': 'F', 'floor': 1, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        603: {'phase': None, 'block': 'F', 'floor': 1, 'type': '1B TYPE L2', 'bedrooms': 1, 'tenure': 'Private'},
        604: {'phase': None, 'block': 'F', 'floor': 1, 'type': '1B TYPE K', 'bedrooms': 1, 'tenure': 'Private'},
        605: {'phase': None, 'block': 'F', 'floor': 1, 'type': '1B TYPE L1', 'bedrooms': 1, 'tenure': 'Private'},
        606: {'phase': None, 'block': 'F', 'floor': 1, 'type': '2B TYPE V3', 'bedrooms': 2, 'tenure': 'Private'},
        607: {'phase': None, 'block': 'F', 'floor': 2, 'type': '2B TYPE X', 'bedrooms': 2, 'tenure': 'Private'},
        608: {'phase': None, 'block': 'F', 'floor': 2, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        609: {'phase': None, 'block': 'F', 'floor': 2, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        610: {'phase': None, 'block': 'F', 'floor': 2, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        611: {'phase': None, 'block': 'F', 'floor': 2, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        612: {'phase': None, 'block': 'F', 'floor': 2, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Private'},
        613: {'phase': None, 'block': 'F', 'floor': 3, 'type': '2B TYPE X', 'bedrooms': 2, 'tenure': 'Private'},
        614: {'phase': None, 'block': 'F', 'floor': 3, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        615: {'phase': None, 'block': 'F', 'floor': 3, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        616: {'phase': None, 'block': 'F', 'floor': 3, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        617: {'phase': None, 'block': 'F', 'floor': 3, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        618: {'phase': None, 'block': 'F', 'floor': 3, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Private'},
        619: {'phase': None, 'block': 'F', 'floor': 4, 'type': '2B TYPE X', 'bedrooms': 2, 'tenure': 'Private'},
        620: {'phase': None, 'block': 'F', 'floor': 4, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        621: {'phase': None, 'block': 'F', 'floor': 4, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        622: {'phase': None, 'block': 'F', 'floor': 4, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        623: {'phase': None, 'block': 'F', 'floor': 4, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        624: {'phase': None, 'block': 'F', 'floor': 4, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Private'},
        625: {'phase': None, 'block': 'F', 'floor': 5, 'type': '2B TYPE X', 'bedrooms': 2, 'tenure': 'Private'},
        626: {'phase': None, 'block': 'F', 'floor': 5, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        627: {'phase': None, 'block': 'F', 'floor': 5, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        628: {'phase': None, 'block': 'F', 'floor': 5, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        629: {'phase': None, 'block': 'F', 'floor': 5, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        630: {'phase': None, 'block': 'F', 'floor': 5, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Private'},
        631: {'phase': None, 'block': 'F', 'floor': 6, 'type': '2B TYPE X', 'bedrooms': 2, 'tenure': 'Private'},
        632: {'phase': None, 'block': 'F', 'floor': 6, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        633: {'phase': None, 'block': 'F', 'floor': 6, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        634: {'phase': None, 'block': 'F', 'floor': 6, 'type': '2B TYPE W', 'bedrooms': 2, 'tenure': 'Private'},
        635: {'phase': None, 'block': 'F', 'floor': 6, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        636: {'phase': None, 'block': 'F', 'floor': 6, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Private'},
        637: {'phase': None, 'block': 'F', 'floor': 7, 'type': '2B TYPE X', 'bedrooms': 2, 'tenure': 'Private'},
        638: {'phase': None, 'block': 'F', 'floor': 7, 'type': '2B TYPE V7', 'bedrooms': 2, 'tenure': 'Private'},
        639: {'phase': None, 'block': 'F', 'floor': 7, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        640: {'phase': None, 'block': 'F', 'floor': 7, 'type': '1B TYPE L', 'bedrooms': 1, 'tenure': 'Private'},
        641: {'phase': None, 'block': 'F', 'floor': 7, 'type': '2B TYPE V1', 'bedrooms': 2, 'tenure': 'Private'},
        642: {'phase': None, 'block': 'F', 'floor': 8, 'type': '2B TYPE S', 'bedrooms': 2, 'tenure': 'Private'},
        643: {'phase': None, 'block': 'F', 'floor': 8, 'type': '3B TYPE J', 'bedrooms': 3, 'tenure': 'Private'},
        644: {'phase': None, 'block': 'F', 'floor': 8, 'type': '2B TYPE V4', 'bedrooms': 2, 'tenure': 'Private'},
        701: {'phase': None, 'block': 'G', 'floor': 1, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        702: {'phase': None, 'block': 'G', 'floor': 1, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        703: {'phase': None, 'block': 'G', 'floor': 1, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        704: {'phase': None, 'block': 'G', 'floor': 1, 'type': '1B TYPE I4', 'bedrooms': 1, 'tenure': 'S/O'},
        705: {'phase': None, 'block': 'G', 'floor': 1, 'type': '2B TYPE U1', 'bedrooms': 2, 'tenure': 'S/O'},
        706: {'phase': None, 'block': 'G', 'floor': 1, 'type': '2B TYPE Z', 'bedrooms': 2, 'tenure': 'S/O'},
        707: {'phase': None, 'block': 'G', 'floor': 1, 'type': '1B TYPE J2', 'bedrooms': 1, 'tenure': 'S/O'},
        708: {'phase': None, 'block': 'G', 'floor': 1, 'type': '2B TYPE V6', 'bedrooms': 2, 'tenure': 'S/O'},
        709: {'phase': None, 'block': 'G', 'floor': 2, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        710: {'phase': None, 'block': 'G', 'floor': 2, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        711: {'phase': None, 'block': 'G', 'floor': 2, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        712: {'phase': None, 'block': 'G', 'floor': 2, 'type': '1B TYPE I4', 'bedrooms': 1, 'tenure': 'S/O'},
        713: {'phase': None, 'block': 'G', 'floor': 2, 'type': '2B TYPE U', 'bedrooms': 2, 'tenure': 'S/O'},
        714: {'phase': None, 'block': 'G', 'floor': 2, 'type': '2B TYPE Y1', 'bedrooms': 2, 'tenure': 'S/O'},
        715: {'phase': None, 'block': 'G', 'floor': 2, 'type': '1B TYPE J', 'bedrooms': 1, 'tenure': 'S/O'},
        716: {'phase': None, 'block': 'G', 'floor': 2, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
        717: {'phase': None, 'block': 'G', 'floor': 3, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        718: {'phase': None, 'block': 'G', 'floor': 3, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        719: {'phase': None, 'block': 'G', 'floor': 3, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        720: {'phase': None, 'block': 'G', 'floor': 3, 'type': '1B TYPE I4', 'bedrooms': 1, 'tenure': 'S/O'},
        721: {'phase': None, 'block': 'G', 'floor': 3, 'type': '2B TYPE U', 'bedrooms': 2, 'tenure': 'S/O'},
        722: {'phase': None, 'block': 'G', 'floor': 3, 'type': '2B TYPE Y', 'bedrooms': 2, 'tenure': 'S/O'},
        723: {'phase': None, 'block': 'G', 'floor': 3, 'type': '1B TYPE J', 'bedrooms': 1, 'tenure': 'S/O'},
        724: {'phase': None, 'block': 'G', 'floor': 3, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
        725: {'phase': None, 'block': 'G', 'floor': 4, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        726: {'phase': None, 'block': 'G', 'floor': 4, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        727: {'phase': None, 'block': 'G', 'floor': 4, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        728: {'phase': None, 'block': 'G', 'floor': 4, 'type': '1B TYPE I4', 'bedrooms': 1, 'tenure': 'S/O'},
        729: {'phase': None, 'block': 'G', 'floor': 4, 'type': '2B TYPE U', 'bedrooms': 2, 'tenure': 'S/O'},
        730: {'phase': None, 'block': 'G', 'floor': 4, 'type': '2B TYPE Y', 'bedrooms': 2, 'tenure': 'S/O'},
        731: {'phase': None, 'block': 'G', 'floor': 4, 'type': '1B TYPE J', 'bedrooms': 1, 'tenure': 'S/O'},
        732: {'phase': None, 'block': 'G', 'floor': 4, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
        733: {'phase': None, 'block': 'G', 'floor': 5, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        734: {'phase': None, 'block': 'G', 'floor': 5, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        735: {'phase': None, 'block': 'G', 'floor': 5, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        736: {'phase': None, 'block': 'G', 'floor': 5, 'type': '1B TYPE I4', 'bedrooms': 1, 'tenure': 'S/O'},
        737: {'phase': None, 'block': 'G', 'floor': 5, 'type': '2B TYPE U', 'bedrooms': 2, 'tenure': 'S/O'},
        738: {'phase': None, 'block': 'G', 'floor': 5, 'type': '2B TYPE Y', 'bedrooms': 2, 'tenure': 'S/O'},
        739: {'phase': None, 'block': 'G', 'floor': 5, 'type': '1B TYPE J', 'bedrooms': 1, 'tenure': 'S/O'},
        740: {'phase': None, 'block': 'G', 'floor': 5, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
        741: {'phase': None, 'block': 'G', 'floor': 6, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        742: {'phase': None, 'block': 'G', 'floor': 6, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        743: {'phase': None, 'block': 'G', 'floor': 6, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        744: {'phase': None, 'block': 'G', 'floor': 6, 'type': '1B TYPE I4', 'bedrooms': 1, 'tenure': 'S/O'},
        745: {'phase': None, 'block': 'G', 'floor': 6, 'type': '2B TYPE U', 'bedrooms': 2, 'tenure': 'S/O'},
        746: {'phase': None, 'block': 'G', 'floor': 6, 'type': '2B TYPE Y', 'bedrooms': 2, 'tenure': 'S/O'},
        747: {'phase': None, 'block': 'G', 'floor': 6, 'type': '1B TYPE J3', 'bedrooms': 1, 'tenure': 'S/O'},
        748: {'phase': None, 'block': 'G', 'floor': 6, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
        749: {'phase': None, 'block': 'G', 'floor': 7, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        750: {'phase': None, 'block': 'G', 'floor': 7, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        751: {'phase': None, 'block': 'G', 'floor': 7, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        752: {'phase': None, 'block': 'G', 'floor': 7, 'type': '1B TYPE I2', 'bedrooms': 1, 'tenure': 'S/O'},
        753: {'phase': None, 'block': 'G', 'floor': 7, 'type': '1B TYPE J1', 'bedrooms': 1, 'tenure': 'S/O'},
        754: {'phase': None, 'block': 'G', 'floor': 7, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
        755: {'phase': None, 'block': 'G', 'floor': 8, 'type': '2B TYPE T2', 'bedrooms': 2, 'tenure': 'S/O'},
        756: {'phase': None, 'block': 'G', 'floor': 8, 'type': '2B TYPE T4', 'bedrooms': 2, 'tenure': 'S/O'},
        757: {'phase': None, 'block': 'G', 'floor': 8, 'type': '2B TYPE V9', 'bedrooms': 2, 'tenure': 'S/O'},
        758: {'phase': None, 'block': 'G', 'floor': 8, 'type': '1B TYPE I2', 'bedrooms': 1, 'tenure': 'S/O'},
        759: {'phase': None, 'block': 'G', 'floor': 8, 'type': '1B TYPE J1', 'bedrooms': 1, 'tenure': 'S/O'},
        760: {'phase': None, 'block': 'G', 'floor': 8, 'type': '2B TYPE V5', 'bedrooms': 2, 'tenure': 'S/O'},
    }
}
