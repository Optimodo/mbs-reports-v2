# Database Architecture Documentation

## Overview

The MBS Reports system uses a **SQLite database** for efficient document tracking with dynamic on-the-fly counting:
- ✅ **Fast weekly processing** (only process new files)
- ✅ **Flexible reporting** (regenerate any report anytime)
- ✅ **Dynamic filtering** (certificates, drawings, technical submittals)
- ✅ **Accurate counts** (P/C totals always match)
- ✅ **Simple schema** (only raw documents stored)
- ✅ **No server required** (file-based SQLite database)

## Architecture (Schema v3)

```
Input Files → db_manager.py → SQLite Database (raw docs) → Dynamic Counting → Reports
                                                                    ↓
                                                            Filters applied at 
                                                            report generation time
```

### Data Flow

1. **File Import**: New files detected → Load with column mapping → Store raw documents
2. **Report Generation**: Fetch raw docs → Apply filters → Dynamic count → Format report
3. **Historical Analysis**: Query any date range → Filter → Count → Report

## Database Schema v3

### Simplified Schema

Schema v3 removes all pre-calculated summary tables. Only raw data is stored; all counting happens dynamically at report generation time.

### Tables

#### `documents` (Primary Table)
Stores one record per document per snapshot. **All rows from source files are preserved**, including duplicates.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| project_name | TEXT | Project name (e.g., "NewMalden") |
| snapshot_date | DATE | Snapshot date (YYYY-MM-DD) |
| snapshot_time | TIME | Snapshot time (HH:MM) |
| doc_ref | TEXT | Document reference number |
| doc_title | TEXT | Document title |
| revision | TEXT | Revision number (P01, C01, etc.) |
| status | TEXT | Document status |
| file_type | TEXT | Standardized file type (via COLUMN_MAPPINGS) |
| purpose_of_issue | TEXT | Purpose of issue |
| date_wet | TEXT | Date from WET timezone |
| last_status_change_wet | TEXT | Last status change date |
| last_updated_wet | TEXT | Last updated date |
| doc_path | TEXT | Document path |
| created_at | TIMESTAMP | When record was inserted |

**No unique constraint** - Allows duplicate doc_ref + revision (legitimate duplicates like withdrawn versions, reissued certificates)

**Indices**:
- `idx_documents_project_date` on (project_name, snapshot_date)
- `idx_documents_status` on (status)
- `idx_documents_revision` on (revision)
- `idx_documents_file_type` on (file_type)

#### `processing_history` (File Tracking)
Tracks which files have been processed to prevent duplicate imports.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| project_name | TEXT | Project name |
| file_path | TEXT | Full path to file |
| file_name | TEXT | File name |
| snapshot_date | DATE | Snapshot date |
| snapshot_time | TIME | Snapshot time |
| processed_at | TIMESTAMP | When file was processed |
| record_count | INTEGER | Number of records imported |

**Unique constraint**: `(project_name, file_name)` - Prevents same file from being imported twice

## Dynamic Counting System

Instead of storing pre-calculated counts, reports use `analyzers/dynamic_counting.py`:

```python
from analyzers import create_summary_row
from utils.document_filters import get_main_report_data

# Get raw documents
raw_docs = db.get_latest_documents(project_name)

# Apply filters (e.g., drawings only for main report)
filtered_docs = get_main_report_data(raw_docs, config)

# Generate counts dynamically
summary_row = create_summary_row(date, time, filtered_docs, config)
# Returns: {'Date': '14-Oct-2025', 'Rev_P01': 50, 'Status_A': 25, ...}
```

### Benefits
- ✅ **Single source of truth** (no sync issues)
- ✅ **Accurate counts** (P revision total = P status total, always)
- ✅ **Flexible filtering** (change filters, counts update automatically)
- ✅ **Simpler schema** (2 tables vs 5)
- ✅ **Faster imports** (40-50% faster without summary calculation)

## Database Manager Usage

### Interactive Menu (Recommended)
```bash
python scripts/db_manager.py
```

Provides menu with options for:
1. Rebuild database schema
2. Import all projects
3. Import specific project
4. Show database statistics

### Weekly Workflow

The main script automatically imports new files before generating reports:

```bash
python main.py
```

This will:
1. Check for new files
2. Import any unprocessed files
3. Generate all reports with dynamic counting

## Python API

### Get Documents

```python
from data import DocumentDatabase

with DocumentDatabase() as db:
    # Get latest snapshot
    latest_docs = db.get_latest_documents('NewMalden')
    
    # Get specific snapshot
    snapshot_docs = db.get_documents_for_snapshot(
        'NewMalden', 
        '2025-10-14', 
        '09:30'
    )
    
    # Get all projects
    projects = db.get_all_projects()
```

### Insert Documents

```python
from data import DocumentDatabase

with DocumentDatabase() as db:
    # Insert documents (no summary calculation)
    count = db.insert_documents(
        project_name='NewMalden',
        snapshot_date='2025-10-14',
        snapshot_time='09:30',
        documents_df=df
    )
    
    # Mark file as processed
    db.mark_file_processed(
        project_name='NewMalden',
        file_path='/path/to/file.xlsx',
        file_name='file.xlsx',
        snapshot_date='2025-10-14',
        snapshot_time='09:30',
        record_count=100
    )
```

### Query Examples

```python
import pandas as pd
from data import DocumentDatabase

with DocumentDatabase() as db:
    # Get all drawings from September
    query = """
        SELECT * FROM documents
        WHERE project_name = 'NewMalden'
          AND file_type = 'DR - Drawings (DR)'
          AND snapshot_date BETWEEN '2025-09-01' AND '2025-09-30'
    """
    df = pd.read_sql_query(query, db.conn)
    
    # Get documents by revision type
    query = """
        SELECT doc_ref, doc_title, revision, status
        FROM documents
        WHERE project_name = 'NewMalden'
          AND revision LIKE 'P%'
        ORDER BY revision, doc_ref
    """
    p_revisions = pd.read_sql_query(query, db.conn)
```

## Report Generation

All reports now use dynamic counting:

```python
from data import DocumentDatabase
from analyzers import create_summary_row
from utils.document_filters import get_main_report_data

with DocumentDatabase() as db:
    # Get raw documents
    raw_docs = db.get_latest_documents('NewMalden')
    
    # Filter for drawings/schematics (main report)
    main_docs = get_main_report_data(raw_docs, config)
    
    # Generate dynamic counts
    summary_row = create_summary_row(date, time, main_docs, config)
    
    # Use in reports
    save_excel_with_retry(pd.DataFrame([summary_row]), ..., main_docs, ...)
```

## Configuration System

### Column Mappings

Each project config defines how to map raw Excel/CSV columns to standardized names:

```python
# configs/OvalBlockB.py
COLUMN_MAPPINGS = {
    'File Type': 'OVL - File Type',  # Standard name: Raw column name
    'Doc Ref': 'Doc Ref',
    'Rev': 'Rev',
    # ...
}
```

### Document Filters

Projects configure filters for different document types:

```python
# Drawings (main report focus)
DRAWING_SETTINGS = {
    'enabled': True,
    'file_type_filter': {
        'enabled': True,
        'column_name': 'File Type',
        'drawing_types': ['DR - Drawings (DR)', 'SC - Schematics']
    }
}

# Certificates (separate report)
CERTIFICATE_SETTINGS = {
    'enabled': True,
    'generate_report': True,
    'file_type_filter': {
        'enabled': True,
        'certificate_types': ['CT - Certificate (CT)']
    }
}
```

## Maintenance

### Rebuild Database

```bash
python scripts/db_manager.py
# Select option 1: Rebuild database schema
```

This will:
1. Drop all existing tables
2. Recreate schema v3 (2 tables only)
3. Ready for fresh import

### Repopulate All Projects

```bash
python scripts/db_manager.py
# Select option 2: Import all projects
```

### Backup Database

```bash
# Windows
copy data\documents.db data\documents_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db

# Linux/Mac
cp data/documents.db data/documents_backup_$(date +%Y%m%d).db
```

### Optimize Database

```python
from data import DocumentDatabase

with DocumentDatabase() as db:
    db.conn.execute('VACUUM')
```

## Troubleshooting

### Database locked
- Ensure no other processes are accessing the database
- Close any open database connections

### Need to change schema
1. Rebuild database: `python scripts/db_manager.py` → Option 1
2. Repopulate: Option 2

### Verify data integrity
```python
from data import DocumentDatabase

with DocumentDatabase() as db:
    stats = db.get_project_stats('NewMalden')
    print(stats)
```

## Performance

### Schema v3 vs v2

| Metric | v2 (with summaries) | v3 (dynamic) | Improvement |
|--------|---------------------|--------------|-------------|
| Database size | 100MB | 60MB | 40% smaller |
| Import speed | 10-15s/file | 5-8s/file | 50% faster |
| Tables | 5 tables | 2 tables | Simpler |
| Report speed | Instant (pre-calc) | ~1-2s (dynamic) | Negligible |

### Why Dynamic is Better

- **Accuracy**: No sync issues between raw data and summaries
- **Flexibility**: Change filters without rebuilding database
- **Simplicity**: Single source of truth, easier to maintain
- **Debugging**: Transparent - can trace from raw data to final count

---
**Schema Version**: v3  
**Last Updated**: October 2025
