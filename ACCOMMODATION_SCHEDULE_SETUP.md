# Accommodation Schedule Setup Guide

## Overview

The accommodation schedule parser extracts apartment data from project-specific Excel/CSV files and generates structured configuration data. This enables enhanced tracking, validation, and reporting capabilities.

## Benefits

### What You Get:
- **Definitive apartment lists** - Know exactly which apartments exist in each phase/block
- **Validation** - Detect invalid apartment numbers in certificates
- **Missing tracking** - Identify apartments without specific certificates
- **Automatic max counts** - No need to manually count apartments per phase/block
- **Floor information** - Track certificates by floor
- **Apartment types** - Foundation for future drawing tracking (apartment layouts)

## Standardized Filename Format

Accommodation schedule files should follow this naming pattern:
```
<ProjectCode> Accommodation Schedule <DDMMYY>.xlsx
```

Examples:
- `GP Accommodation Schedule 201025.xlsx` (Greenwich Peninsula, 20th Oct 2025)
- `HP Accommodation Schedule 151025.xlsx` (Holloway Park, 15th Oct 2025)
- `NM Accommodation Schedule 101125.xlsx` (New Malden, 10th Nov 2025)

This standardized format makes it easy to:
- Identify which project the schedule belongs to
- Track when the schedule was last updated
- Manage multiple versions of schedules

## Setup Process

### Step 1: Add Configuration to Project Config

Add `ACCOMMODATION_SCHEDULE_CONFIG` to your project's config file (e.g., `configs/ProjectName.py`):

```python
# Accommodation Schedule Configuration
ACCOMMODATION_SCHEDULE_CONFIG = {
    'enabled': True,  # Set to False to disable
    'file_path': 'GP Accomodation Schedule 201025.xlsx',  # Standard format: <ProjectCode> Accomodation Schedule <DDMMYY>.xlsx
    
    # Excel/CSV reading configuration
    'read_config': {
        'sheet_name': 0,     # Which sheet to read (0 = first)
        'skiprows': 2,       # How many rows to skip at the top
    },
    
    # Column mapping - maps standard names to actual column names
    'column_mapping': {
        'apartment': 'Unit',           # REQUIRED - Column with apartment numbers
        'phase': 'Phase',              # OPTIONAL - Phase/stage column
        'block': 'Block',              # OPTIONAL - Building block column
        'floor': 'Floor',              # OPTIONAL - Floor level column
        'apartment_type': 'Type',      # OPTIONAL - Apartment type column
        'bedrooms': 'Bedrooms'         # OPTIONAL - Number of bedrooms column
    },
    
    # Apartment number cleaning configuration
    'apartment_cleaning': {
        'remove_prefix': '',           # Remove prefix like "Apt " (optional)
        'extract_pattern': r'\d+'      # Regex to extract number part (optional)
    },
    
    # Floor cleaning configuration
    'floor_cleaning': {
        'remove_prefix': 'L',          # Remove prefix (e.g., "L01" -> "01")
        'remove_suffix': '',           # Remove suffix (optional)
        'convert_to_int': True         # Convert "01" -> 1 (True/False)
    }
}
```

### Step 2: Identify Correct Column Names

Run a quick check to see the actual column names in your schedule:

```python
import pandas as pd
df = pd.read_excel('input/YourSchedule.xlsx', skiprows=2, nrows=5)
print('Columns:', list(df.columns))
print(df.head())
```

Update the `column_mapping` section with the actual column names.

### Step 3: Run the Parser Script

```bash
python scripts/update_accommodation_data.py ProjectName
```

The script will:
1. Read the accommodation schedule
2. Extract and clean apartment data
3. Build structured data (phases, blocks, apartments, types)
4. Update the project config file with `ACCOMMODATION_DATA`

### Step 4: Review and Commit

Review the generated data in your Git diff:
- Check apartment counts are correct
- Verify phase/block assignments
- Confirm apartment types look reasonable

If everything looks good, commit the changes!

## Configuration Options

### Required Settings

- **`enabled`**: Must be `True` to enable parsing
- **`file_path`**: Path to the accommodation schedule file
- **`column_mapping.apartment`**: Column containing apartment numbers

### Optional Settings

All other column mappings are optional. If omitted, that data simply won't be extracted.

### Cleaning Configurations

#### `apartment_cleaning`
Standardizes apartment numbers from varied formats:
- **`remove_prefix`**: Remove text prefix (e.g., "Flat 101" -> "101")
- **`extract_pattern`**: Regex to extract numbers (e.g., `r'\d+'` extracts digits)

Examples:
```python
# Extract numbers from "Flat 101"
'apartment_cleaning': {
    'remove_prefix': 'Flat ',
    'extract_pattern': r'\d+'
}

# Handle "Unit-205"
'apartment_cleaning': {
    'extract_pattern': r'\d+'
}
```

#### `floor_cleaning`
Standardizes floor identifiers:
- **`remove_prefix`**: Remove letter prefix (e.g., "L01" -> "01")
- **`remove_suffix`**: Remove suffix (e.g., "01F" -> "01")
- **`convert_to_int`**: Convert to integer (e.g., "01" -> 1)

Examples:
```python
# "L01" -> 1
'floor_cleaning': {
    'remove_prefix': 'L',
    'convert_to_int': True
}

# "Floor 10" -> "10"
'floor_cleaning': {
    'remove_prefix': 'Floor ',
    'convert_to_int': False  # Keep as string
}
```

## Generated Data Structure

The script generates `ACCOMMODATION_DATA` in your project config:

```python
ACCOMMODATION_DATA = {
    'total_apartments': 476,
    'last_updated': '2025-10-20',
    'source_file': 'Project - Accommodation schedule.xlsx',
    
    'phases': {
        '18.02': {
            'apartment_count': 222,
            'apartments': [1, 2, 3, ...],
            'blocks': {
                'A': {
                    'apartment_count': 85,
                    'apartments': [1, 2, 3, ...],
                    'floors': [1, 2, 3, ...]
                },
                # ... more blocks
            }
        },
        # ... more phases
    },
    
    'apartment_types': {
        'Type A': {
            'count': 120,
            'bedrooms': 2,
            'apartments': [1, 5, 12, ...]
        },
        # ... more types
    },
    
    'apartment_lookup': {
        1: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': 'Type A', 'bedrooms': 2},
        2: {'phase': '18.02', 'block': 'A', 'floor': 1, 'type': 'Type B', 'bedrooms': 1},
        # ... all apartments
    }
}
```

## Using the Data

### In Certificate Tracking

```python
from config import load_project_config

config = load_project_config('GreenwichPeninsula')
accom_data = config.get('ACCOMMODATION_DATA')

if accom_data:
    # Get all valid apartments
    all_apartments = set(accom_data['apartment_lookup'].keys())
    
    # Find missing certificates
    apartments_with_fire_alarm = get_apartments_with_fire_alarm_certs()
    missing_fire_alarm = all_apartments - apartments_with_fire_alarm
    
    # Get phase-specific max count
    phase_18_02_count = accom_data['phases']['18.02']['apartment_count']
```

### In Reports

The accommodation data enables:
- "90/100 apartments have Fire Alarm certificates (10 missing)"
- "Phase 18.02: 85/222 apartments complete"
- "Block A: 100% complete, Block B: 45% complete"
- List specific missing apartments: "Missing: 105, 207, 310"

## Updating Data

When you receive a new accommodation schedule:

1. Replace the Excel file in the `input/` folder
2. Run: `python scripts/update_accommodation_data.py ProjectName`
3. Review the Git diff to see what changed
4. Commit if changes look correct

## Troubleshooting

### "Column not found" Error
- Run the column check command (Step 2) to see actual column names
- Update `column_mapping` with correct names
- Remember column names are case-sensitive

### Wrong Apartment Count
- Check `skiprows` setting - you might be skipping too many/few rows
- Check if there are header rows being counted as apartments
- Verify `apartment_cleaning` regex is extracting numbers correctly

### Phase/Block Not Detected
- Verify the column names are correct
- Check if the data in those columns matches expected format
- Add debug print to see what values are being read

### Floor Numbers Wrong
- Adjust `floor_cleaning` prefix/suffix settings
- Set `convert_to_int` to False if you want to keep as strings
- Check the actual format in the Excel file

### Multi-Floor Apartments (Duplexes, Tri-levels)
Currently, the system stores one floor per apartment. For multi-floor apartments:
- The floor stored will be the first floor encountered in the schedule
- Future enhancement: Could store as list `[floor1, floor2]` if needed
- Workaround: Use the lowest floor number for the apartment

### Houses vs Apartments
- Houses typically don't have floor designations (set floor to None or leave empty)
- The system handles missing floor data gracefully
- Houses can be in their own block for separate tracking

## Project-Specific Notes

### Greenwich Peninsula
- Uses "L" prefix for floors (L01, L02, etc.)
- Has phases 18.02 and 18.03
- Blocks A-G split across phases
- 476 total apartments

### Other Projects
Add your project-specific notes here as you configure them.

