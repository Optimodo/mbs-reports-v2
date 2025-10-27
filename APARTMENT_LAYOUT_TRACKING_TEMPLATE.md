# Apartment Layout Tracking Configuration Template

This document defines the structure for `APARTMENT_LAYOUT_TRACKING` configuration that will be added to project config files.

## Configuration Structure

```python
APARTMENT_LAYOUT_TRACKING = {
    'enabled': True,
    
    # Global detection settings - how to identify layout drawings
    'detection': {
        # File types that contain layout drawings
        'file_type_patterns': ['Drawing', 'DR'],
        
        # Doc Ref patterns to identify layouts (e.g., "DR-A-" for architectural)
        'doc_ref_patterns': [r'DR-A-', r'DR-M-', r'DR-E-'],
        
        # Patterns to exclude from layout tracking
        'exclude_patterns': ['Schematic', 'Schedule', 'Detail', 'Section', 'Elevation'],
        
        # Optional: specific folder paths to search
        'folder_patterns': [r'\\Apartment Layouts\\', r'\\GA Drawings\\']
    },
    
    # Layout categories organized by scope (apartment-specific vs communal)
    'categories': {
        # APARTMENT-SPECIFIC LAYOUTS (per apartment TYPE, not per plot)
        'apartment_layouts': {
            'enabled': True,
            
            # Layout types to track for each apartment type
            'layout_types': {
                'ga_layout': {
                    'display_name': 'GA Layout',
                    'patterns': ['GA', 'General Arrangement', 'Floor Plan'],
                    'doc_ref_patterns': [r'DR-A-.*-GA-'],
                    'required': True,  # Flag if this is a critical layout
                    'description': 'General arrangement floor plan'
                },
                'rcp': {
                    'display_name': 'RCP (Reflected Ceiling Plan)',
                    'patterns': ['RCP', 'Reflected Ceiling'],
                    'doc_ref_patterns': [r'DR-A-.*-RCP-'],
                    'required': True,
                    'description': 'Reflected ceiling plan showing ceiling layout'
                },
                'small_power': {
                    'display_name': 'Small Power Layout',
                    'patterns': ['Small Power', 'Power Layout', 'SP'],
                    'doc_ref_patterns': [r'DR-E-.*-SP-'],
                    'required': True,
                    'description': 'Electrical small power layout'
                },
                'lighting': {
                    'display_name': 'Lighting Layout',
                    'patterns': ['Lighting', 'Light Layout', 'LT'],
                    'doc_ref_patterns': [r'DR-E-.*-LT-'],
                    'required': True,
                    'description': 'Lighting layout and controls'
                },
                'ventilation': {
                    'display_name': 'Ventilation Layout',
                    'patterns': ['Ventilation', 'Vent', 'MVHR'],
                    'doc_ref_patterns': [r'DR-M-.*-VENT-'],
                    'required': True,
                    'description': 'Ventilation and MVHR layout'
                },
                'combined_services': {
                    'display_name': 'Combined Services',
                    'patterns': ['Combined Services', 'Services Layout'],
                    'doc_ref_patterns': [r'DR-M-.*-CS-'],
                    'required': False,
                    'description': 'Combined MEP services layout'
                },
                'drainage': {
                    'display_name': 'Drainage Layout',
                    'patterns': ['Drainage', 'Drain', 'Soil & Waste'],
                    'doc_ref_patterns': [r'DR-M-.*-DR-'],
                    'required': False,
                    'description': 'Drainage and waste layout'
                },
                'heating': {
                    'display_name': 'Heating Layout',
                    'patterns': ['Heating', 'UFH', 'Underfloor Heating'],
                    'doc_ref_patterns': [r'DR-M-.*-HT-'],
                    'required': False,
                    'description': 'Heating system layout'
                }
            },
            
            # How to extract apartment type from document
            'apartment_type_detection': {
                # Look for type references in title/ref
                'title_patterns': [
                    r'Type\s+([A-Z0-9-]+)',
                    r'APT\s+TYPE\s+([A-Z0-9-]+)',
                    r'Unit\s+Type\s+([A-Z0-9-]+)'
                ],
                'doc_ref_patterns': [
                    r'-TYPE-([A-Z0-9-]+)-',
                    r'-T([A-Z0-9-]+)-'
                ],
                # Path-based detection (e.g., folder structure)
                'path_patterns': [
                    r'\\Type\s+([A-Z0-9-]+)\\',
                    r'\\([A-Z0-9-]+)\s+Type\\'
                ]
            }
        },
        
        # COMMUNAL/COMMON AREA LAYOUTS (floor or building-wide)
        'communal_layouts': {
            'enabled': True,
            
            # Communal layout types
            'layout_types': {
                'corridor_ga': {
                    'display_name': 'Corridor GA',
                    'patterns': ['Corridor', 'Common Areas GA'],
                    'doc_ref_patterns': [r'DR-A-.*-CORRIDOR-'],
                    'coverage_type': 'floor',  # 'floor', 'multi-floor', or 'building'
                    'description': 'Corridor general arrangement'
                },
                'corridor_lighting': {
                    'display_name': 'Corridor Lighting',
                    'patterns': ['Corridor Lighting', 'Common Areas Lighting'],
                    'doc_ref_patterns': [r'DR-E-.*-CORRIDOR-LT-'],
                    'coverage_type': 'floor',
                    'description': 'Corridor lighting layout'
                },
                'corridor_services': {
                    'display_name': 'Corridor Services',
                    'patterns': ['Corridor Services'],
                    'doc_ref_patterns': [r'DR-M-.*-CORRIDOR-'],
                    'coverage_type': 'floor',
                    'description': 'Corridor MEP services'
                },
                'core_services': {
                    'display_name': 'Core Services',
                    'patterns': ['Core', 'Riser', 'Lift Core'],
                    'doc_ref_patterns': [r'DR-.*-CORE-'],
                    'coverage_type': 'building',
                    'description': 'Core and riser services'
                }
            },
            
            # How to detect floor/block coverage
            'coverage_detection': {
                # Extract floor numbers from title (e.g., "Level 01-03" = floors 1,2,3)
                'floor_patterns': [
                    r'Level\s+(\d+)',
                    r'Floor\s+(\d+)',
                    r'L(\d{2})',
                    r'Levels?\s+(\d+)-(\d+)'  # Multi-floor pattern
                ],
                # Extract block/phase from path or title
                'block_patterns': [
                    r'Block\s+([A-G])',
                    r'Phase\s+([\d.]+)'
                ]
            }
        }
    },
    
    # Expected coverage validation
    'expected_coverage': {
        # For apartment layouts: expect one of each layout type per apartment type
        # This is derived from ACCOMMODATION_DATA.apartment_types
        'use_accommodation_types': True,
        
        # For communal layouts: expect coverage across all floors/blocks
        # This is derived from ACCOMMODATION_DATA.phases and blocks
        'use_accommodation_structure': True
    }
}
```

## Key Design Principles

1. **Type-based tracking**: Track layouts by apartment TYPE, not individual apartments
2. **Flexible detection**: Multiple pattern types (title, doc ref, path) for different project naming conventions
3. **Communal coverage**: Handle multi-floor layouts (e.g., "Levels 4-8 Corridor")
4. **Validation**: Cross-reference with accommodation schedule to detect missing layouts
5. **Reusable structure**: Similar to certificate tracking for consistency

## Next Steps

1. Implement layout detection logic in `document_tracker.py`
2. Add layout categorization functions
3. Create progress calculation for layout coverage
4. Integrate into summary report
5. Test with Greenwich Peninsula first


