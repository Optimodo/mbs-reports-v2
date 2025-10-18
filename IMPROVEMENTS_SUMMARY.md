# MBS Reports v2 - Improvements Summary

This document lists all the quality-of-life improvements and architectural enhancements that were implemented. Use this as a guide for incremental reimplementation after rollback.

---

## 🎯 High Priority Improvements (Implement First)

### 1. **Column Mapping Architecture** ✨
**Status**: Core architectural improvement
**Files**: `processors/data_loader.py`, all config files

**Problem Solved**: 
- Different projects use different raw column names ('Form', 'OVL - File Type', etc.)
- Hard to maintain consistency across projects

**Implementation**:
```python
# In each project config file (e.g., configs/NewMalden.py)
COLUMN_MAPPINGS = {
    'File Type': 'Form',  # Standard name: Raw column name
    'Doc Ref': 'Doc Ref',
    'Doc Title': 'Doc Title',
    'Rev': 'Rev',
    'Status': 'Status',
    # ... etc
}
```

**In `processors/data_loader.py`**:
- Apply mappings for BOTH Excel and CSV files
- Apply mappings BEFORE any other processing
- This ensures database always has consistent column names

**Benefits**:
- Database has standardized column names
- Filters work consistently across all projects
- Easy to add new projects with different column structures

**Testing**: After implementation, verify `'File Type'` column exists in database for all projects

---

### 2. **Multi-Report-Type Database System** 🗂️
**Status**: Major feature enhancement
**Files**: `data/schema.py`, `data/database.py`, `analyzers/counting.py`, `scripts/db_manager.py`

**Problem Solved**:
- Need separate counts for main report (drawings only) vs certificates vs technical submittals
- Previously mixed all document types together

**Schema Changes**:
```sql
-- Added report_type column to all summary tables
ALTER TABLE revision_summaries ADD COLUMN report_type TEXT DEFAULT 'main';
ALTER TABLE status_summaries ADD COLUMN report_type TEXT DEFAULT 'main';
ALTER TABLE file_type_summaries ADD COLUMN report_type TEXT DEFAULT 'main';

-- Updated UNIQUE constraints
UNIQUE(project_name, snapshot_date, snapshot_time, report_type, revision_type)
UNIQUE(project_name, snapshot_date, snapshot_time, report_type, status)
UNIQUE(project_name, snapshot_date, snapshot_time, report_type, file_type)
```

**Implementation Flow**:
1. During import, for each snapshot:
   ```python
   main_counts = get_counts(df, config, report_type='main')
   db.insert_summaries(project, date, time, main_counts, report_type='main')
   
   cert_counts = get_counts(df, config, report_type='certificate')
   db.insert_summaries(project, date, time, cert_counts, report_type='certificate')
   
   ts_counts = get_counts(df, config, report_type='technical_submittal')
   db.insert_summaries(project, date, time, ts_counts, report_type='technical_submittal')
   
   all_counts = get_counts(df, config, report_type='all')
   db.insert_summaries(project, date, time, all_counts, report_type='all')
   ```

2. When generating reports:
   ```python
   summary_df = db.get_summary_dataframe(project_name, report_type='main')
   ```

**Benefits**:
- Accurate counts for each report type
- Can generate specialized reports (certificates, tech submittals)
- Historical data for all report types

**Testing**: Query database to verify all 4 report_type values exist for each snapshot

---

### 3. **Robust Document Filtering System** 🎯
**Status**: Critical for accurate reporting
**Files**: `utils/document_filters.py`, all config files

**Problem Solved**:
- Need to filter documents by type (drawings, certificates, tech submittals)
- Different projects identify documents differently (file type column vs doc ref patterns)

**Implementation**:

**Create `utils/document_filters.py`**:
```python
def filter_certificates(df, config):
    """Filter for certificate documents using project-specific settings."""
    cert_settings = config.get('CERTIFICATE_SETTINGS', {})
    if not cert_settings.get('enabled', False):
        return pd.DataFrame()
    
    # Method 1: File type exact match
    if cert_settings.get('file_type_filter', {}).get('enabled', False):
        # ... implementation
    
    # Method 2: Doc Ref pattern match (2-letter codes)
    if cert_settings.get('doc_ref_filter', {}).get('enabled', False):
        # ... implementation

def filter_drawings_and_schematics(df, config):
    """Filter for drawing/schematic documents only."""
    # Similar dual-method approach

def get_main_report_data(df, config):
    """Get data for main report (drawings only)."""
    return filter_drawings_and_schematics(df, config)
```

**In each project config**:
```python
# Example: Greenwich Peninsula
DRAWING_SETTINGS = {
    'enabled': True,
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',  # Use MAPPED name, not raw name
        'drawing_types': ['DR - Drawing (DR)', 'SC - Schematic Drawings (SC)']
    },
    'doc_ref_filter': {
        'enabled': False,
        'column_name': 'Doc Ref',
        'drawing_patterns': ['DR', 'SC']
    }
}

CERTIFICATE_SETTINGS = {
    'enabled': True,
    'generate_report': True,
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',
        'certificate_types': ['CT - Certificate (CT)']
    },
    'doc_ref_filter': {
        'enabled': False,
        'column_name': 'Doc Ref',
        'certificate_patterns': ['CT']
    }
}
```

**Benefits**:
- Precise control over what documents appear in each report
- Dual method approach handles different project data structures
- Easy to configure per project

**Testing**: 
- Check main report only shows drawings/schematics
- Verify file type summary matches filter settings
- Ensure certificate report only shows certificates

---

### 4. **Cyrillic Character Normalization** 🔤
**Status**: Bug fix / data quality improvement
**Files**: `utils/data_cleaning.py`

**Problem Solved**:
- Cyrillic characters in revision numbers (Cyrillic 'С' looks like Latin 'C')
- Causes incorrect counting (C05 and С05 counted separately)

**Implementation**:
```python
# In utils/data_cleaning.py
def clean_revision(val):
    """Clean and normalize revision values."""
    if pd.isna(val):
        return ''
    
    s = str(val).strip().upper()
    
    # Cyrillic to Latin character mapping
    cyrillic_to_latin = {
        '\u0410': 'A',  # Cyrillic А → Latin A
        '\u0412': 'B',  # Cyrillic В → Latin B
        '\u0421': 'C',  # Cyrillic С → Latin C
        '\u0415': 'E',  # Cyrillic Е → Latin E
        '\u041D': 'H',  # Cyrillic Н → Latin H
        '\u041A': 'K',  # Cyrillic К → Latin K
        '\u041C': 'M',  # Cyrillic М → Latin M
        '\u041E': 'O',  # Cyrillic О → Latin O
        '\u0420': 'P',  # Cyrillic Р → Latin P
        '\u0422': 'T',  # Cyrillic Т → Latin T
        # Add lowercase versions too
        '\u0430': 'A',
        '\u0432': 'B',
        '\u0441': 'C',
        # ... etc
    }
    
    for cyrillic, latin in cyrillic_to_latin.items():
        s = s.replace(cyrillic, latin)
    
    return s
```

**Where to Apply**:
- In `data_loader.py` after loading data
- Before storing in database

**Benefits**:
- Accurate revision counting
- Prevents mysterious count mismatches
- Handles copy-paste from Excel (common source of Cyrillic chars)

**Testing**: Check if C05, С05 (Cyrillic) count as same revision

---

### 5. **Holloway Park Dual-Column Status Logic** 🏗️
**Status**: Project-specific custom mapping
**Files**: `configs/HollowayPark.py`, `processors/data_loader.py`

**Problem Solved**:
- HP uses TWO columns for status: 'Status' (column F) and 'Design Status' (column I)
- Design Status takes precedence when present
- Need to merge these into single normalized status

**Implementation**:

**In `configs/HollowayPark.py`**:
```python
def map_holloway_park_status(row):
    """Custom status mapping for Holloway Park dual-column system."""
    status_col_f = row.get('Status', '') if pd.notna(row.get('Status', '')) else ''
    design_status_col_i = row.get('Design Status', '') if pd.notna(row.get('Design Status', '')) else ''
    
    # Clean values
    status_col_f = str(status_col_f).strip()
    design_status_col_i = str(design_status_col_i).strip()
    
    # Handle string 'nan' from pandas string conversion
    if design_status_col_i.lower() == 'nan':
        design_status_col_i = ''
    if status_col_f.lower() == 'nan':
        status_col_f = ''
    
    # Design Status takes precedence
    if design_status_col_i:
        if design_status_col_i.upper() == 'B':
            return 'Status B'
        elif design_status_col_i.upper() == 'C':
            return 'Status C'
        else:
            return 'Other'
    
    # If no Design Status, check Status column
    if status_col_f:
        if status_col_f.lower() == 'construction':
            return 'Status A'
        elif status_col_f.lower() == 'ifc-pending':
            return 'IFC-pending'
        else:
            return 'Other'
    
    return 'Other'
```

**In `processors/data_loader.py`**:
```python
# Apply custom status mapping for Holloway Park BEFORE string conversion
if config.get('PROJECT_TITLE') == 'Holloway Park':
    from configs.HollowayPark import map_holloway_park_status
    if 'Status' in df.columns or 'Design Status' in df.columns:
        df['Status'] = df.apply(map_holloway_park_status, axis=1)
        print("Applied custom Holloway Park status mapping")
```

**CRITICAL ORDER**:
1. Load CSV
2. Apply column mappings (creates 'Status' and 'Design Status' columns)
3. **Apply custom status mapping** ← BEFORE string conversion!
4. Clean revisions
5. Convert to strings

**Benefits**:
- Handles HP's unique dual-column workflow
- Normalizes to standard status categories
- Works with existing STATUS_MAPPINGS

**Testing**: Verify 'Construction' → 'Status A' and Design Status 'B' → 'Status B'

---

## 📊 Medium Priority Improvements

### 6. **Database Manager Menu System** 🎮
**Status**: UX improvement
**Files**: `scripts/db_manager.py`

**Changes**:
- Removed command-line arguments
- Added interactive console menu
- Options: Initialize, Rebuild, Import All, Update, Statistics, Exit

**Benefits**: Easier to use, no need to remember command flags

---

### 7. **Database Viewer Tool** 🔍
**Status**: New utility
**Files**: `db_viewer.py`

**Features**:
- View projects and statistics
- Browse revision/status/file type summaries by report_type
- View latest documents
- Run custom SQL queries
- Export tables to CSV

**Usage**: `python db_viewer.py`

**Benefits**: Quick database inspection without external tools

---

### 8. **Streamlined Main Menu** 🎯
**Status**: UX improvement
**Files**: `main.py`

**Changes**:
- Removed all legacy file-based processing options
- Only database-driven options:
  1. Run all projects, all reports
  2. Run single project, all reports
  3. Run specific report type
  4. Exit

**Benefits**: Cleaner, more intuitive, forces use of proper workflow

---

### 9. **Chart Color Improvements** 🎨
**Status**: Visual enhancement
**Files**: `reports/summary_report.py`

**Problem**: White/light colors in pie charts not visible

**Solution**:
```python
def get_chart_safe_color(config_color, category):
    """Convert white/light colors to visible alternatives."""
    if config_color in ['FFFFFF', 'ffffff', 'WHITE']:
        return 'F0F0F0'  # Light gray instead of white
    return config_color
```

**Benefits**: All pie chart sections visible

---

### 10. **Empty Revision Row Filtering** 📋
**Status**: Report cleanup
**Files**: `reports/summary_report.py`

**Problem**: Summary sheet shows P20-P30 even if count is 0 (from old snapshots)

**Solution**:
```python
# Only add revision row if count > 0 in latest data
if count > 0:
    # Add revision row
```

**Benefits**: Cleaner summary sheets, no clutter from old revisions

---

## 🔧 Low Priority / Nice-to-Have

### 11. **Console Output Cleanup** 🧹
**Status**: UX polish
**Files**: Various

**Changes**:
- Removed excessive debug output
- Replaced Unicode characters with ASCII (✓ → OK, ✗ → X)
- Cleaner progress messages

---

### 12. **Documentation Files** 📚
**Status**: New documentation
**Files Created**:
- `SCHEMA_V2_MIGRATION.md` - Database schema migration guide
- `CERTIFICATE_FILTERING_GUIDE.md` - Document filtering system guide
- `REBUILD_DB.md` - Architecture fix documentation
- `NEW_PROJECT_SETUP.md` - Guide for adding new projects

---

## ⚠️ Known Issues / Incomplete

### Issues Encountered During Implementation:

1. **Holloway Park Status A Missing** ❌
   - Custom status mapping applied twice
   - String conversion timing issues
   - **Root Cause**: Order of operations in `data_loader.py`
   - **Fix**: Apply custom mapping only once, before string conversion

2. **Database Double Import** ❌
   - `rebuild_database()` was calling `import_all_projects()` automatically
   - Menu option 3 also called import
   - **Fix**: Removed automatic import from `rebuild_database()`

3. **Filter Column Name Confusion** ❌
   - Filters sometimes used raw column names, sometimes mapped names
   - **Fix**: Always use mapped names in filter configs (after column mapping)

---

## 🎯 Recommended Reimplementation Order

### Phase 1: Foundation (Test After Each)
1. ✅ Column Mapping Architecture
   - Add COLUMN_MAPPINGS to all configs
   - Update `data_loader.py` to apply mappings
   - Test: Verify 'File Type' column in database

2. ✅ Cyrillic Character Normalization
   - Update `clean_revision()` function
   - Test: Check C05 vs С05 counting

### Phase 2: Core Features
3. ✅ Robust Document Filtering System
   - Create `utils/document_filters.py`
   - Add DRAWING_SETTINGS to configs
   - Test: Main report shows only drawings

4. ✅ Multi-Report-Type Database
   - Update schema (SCHEMA_VERSION = 2)
   - Update `get_counts()` to accept report_type
   - Update `insert_summaries()` to store report_type
   - Test: Query database for all 4 report types

### Phase 3: Project-Specific
5. ✅ Holloway Park Dual-Column Status
   - Implement `map_holloway_park_status()`
   - Apply in correct order (after mapping, before string conversion)
   - Test: 'Construction' → 'Status A'

### Phase 4: Polish
6. ✅ Database Manager Menu
7. ✅ Database Viewer Tool
8. ✅ Chart Colors & Empty Row Filtering
9. ✅ Streamlined Main Menu

---

## 🧪 Testing Checklist

After each phase, verify:

- [ ] Database rebuilds without errors
- [ ] All projects import successfully
- [ ] Status counts match expected values
- [ ] Revision counts are accurate
- [ ] File type counts show only filtered types
- [ ] Reports generate without errors
- [ ] Charts display correctly
- [ ] No duplicate data in database

---

## 📝 Critical Lessons Learned

1. **Test incrementally** - Each improvement should be tested before moving to next
2. **Column mapping FIRST** - Must happen before any other processing
3. **Custom mappings BEFORE string conversion** - pd.notna() doesn't work on string 'nan'
4. **Single application** - Apply transformations once, in the right place
5. **Use database viewer** - Essential for debugging count issues
6. **Verify architecture** - Reports should NEVER count, only aggregate

---

## 💡 Architecture Principles

These should guide all future development:

1. **Data flows one direction**: Raw → Normalized → Database → Reports
2. **Count once, use many**: Counting happens during import, reports just aggregate
3. **Configuration over code**: Project differences in configs, not if/else statements
4. **Consistent columns**: Database always has same column names via mapping
5. **Filter early**: Apply document type filters during counting, not reporting

---

## 🔗 Related Files

**Core Architecture**:
- `data/schema.py` - Database structure
- `data/database.py` - Database API
- `processors/data_loader.py` - Data loading & normalization
- `analyzers/counting.py` - Counting logic
- `utils/document_filters.py` - Filtering logic

**Configuration**:
- `configs/*.py` - Project-specific settings
- `config.py` - Config loader

**Tools**:
- `scripts/db_manager.py` - Database management
- `db_viewer.py` - Database inspection
- `main.py` - Report generation

---

## 📞 Support

If issues arise during reimplementation:
1. Use `db_viewer.py` to inspect database
2. Check `verify_db_after_rebuild.py` for validation
3. Review architecture principles above
4. Test each component in isolation

Good luck with the reimplementation! 🚀

