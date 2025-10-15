# West Cromwell Road Project Setup

## Project Details
- **Project Name**: West Cromwell Road
- **Project Code**: WCR
- **File Format**: CSV (similar to Holloway Park)
- **Input Folder**: `input/WCR/`
- **Configuration**: `configs/WestCromwellRoad.py`

## What Was Configured

### 1. Project Code Registration
Added `'WCR': 'WestCromwellRoad'` to `config.py` in the `PROJECT_CODES` dictionary.

This enables automatic project detection when document references start with "WCR-".

### 2. Configuration File
Created `configs/WestCromwellRoad.py` with:
- **CSV Settings**: Configured to read CSV files with UTF-8 encoding
- **Column Mappings**: 
  - `Name` → `Doc Ref`
  - `Description` → `Doc Title`
  - `Revision` → `Rev`
  - `Status` → `Status`
  - `Revision Date Modified` → `Date (WET)`
- **Excel Settings**: Available as fallback for Excel files
- **Certificates**: Disabled (can be enabled later if needed)

### 3. Menu Integration
Updated `main.py` to include West Cromwell Road:
- Added to project selection menu (option 5)
- Added WCR to project folders mapping
- Added to "Process All Projects" workflow

### 4. Input Folder
Created `input/WCR/` directory for document listing files.

**Existing file detected**: `WCR Document Listing 141025.csv`

## CSV File Format

The CSV files should have the following columns:
- **Name**: Document reference (e.g., "WCR-MBS-B2-02-DR-X-5202")
- **Revision Workflow**: Workflow status
- **Description**: Document title/description
- **Revision**: Revision number (P01, P02, C01, etc.)
- **Status**: Document status
- **Organisation Name**: Company name
- **Author**: Document author
- **Revision Date Modified**: Last modification date
- **State**: Document state (Active, Revised, etc.)

## How to Use

### Process West Cromwell Road Files

1. **Place CSV files in `input/WCR/`**
   - Name format: `WCR Document Listing DDMMYY.csv`
   - Or any naming convention with timestamps

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Select an option**:
   - **Option 2**: Process all projects (includes WCR)
   - **Option 3**: Process single project → Select 5 for WCR
   - **Option 4**: Detect files to see what's available

### Output Files

The system will generate:
- `output/WestCromwellRoad_summary.xlsx` - Overall summary with charts
- `output/WestCromwellRoad_progression.xlsx` - Week-by-week progression

## Example Document Reference

```
WCR-MBS-B2-02-DR-X-5202
│   │   │  │  │  │ └─ Document number
│   │   │  │  │  └─ Discipline (X = Mixed)
│   │   │  │  └─ Type (DR = Drawing)
│   │   │  └─ Subzone
│   │   └─ Zone (B2 = Block B2)
│   └─ Originator (MBS = Malcolm Building Services)
└─ Project Code
```

## Status Values

Based on the CSV sample, common status values include:
- "Superseded"
- "For Comments"
- "Construction"
- "QA Approved"
- "Not Approved"
- "Yes - Proceed to EA Review"

The system will categorize these into standard status groups (Status A, B, C, etc.) for reporting.

## Next Steps

1. **Review the configuration** if column names don't match exactly
2. **Add more document listings** to the `input/WCR/` folder
3. **Run the processor** to generate reports
4. **Customize status mapping** if needed (see `configs/HollowayPark.py` for advanced status mapping examples)

## Troubleshooting

If files aren't being processed:
1. Check that document references start with "WCR-"
2. Verify CSV column names match the mapping in `configs/WestCromwellRoad.py`
3. Ensure CSV files have the timestamp in a recognizable format
4. Check `processed_files_per_project.json` to see what's been processed

## Customization

To customize the configuration further, edit `configs/WestCromwellRoad.py`:
- Adjust column mappings if CSV structure differs
- Enable certificates if needed
- Add custom status mapping (see Holloway Park example)
- Configure file type filtering


