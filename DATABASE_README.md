# Database Architecture Documentation

## Overview

The MBS Reports system now uses a **SQLite database** as the central data store, enabling:
- ✅ Efficient weekly processing (only process new files)
- ✅ Flexible report generation (regenerate any report anytime)
- ✅ Time-based aggregations (daily/weekly/monthly/quarterly/yearly)
- ✅ Historical data queries
- ✅ No server required (file-based database)

## Architecture

```
Input Files → db_manager.py → SQLite Database → Report Generators
                                      ↓
                              Queryable, Flexible
                              Can regenerate anytime
```

### Data Flow

1. **Weekly Processing**: New files detected → Processed → Stored in database
2. **Report Generation**: Query database → Aggregate data → Generate Excel/PDF reports
3. **Historical Analysis**: Query any date range → Create custom reports

## Database Schema

### Tables

#### `documents`
Primary table storing one record per document per snapshot.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| project_name | TEXT | Project name (e.g., "NewMalden") |
| snapshot_date | DATE | Snapshot date (YYYY-MM-DD) |
| snapshot_time | TIME | Snapshot time (HH:MM) |
| doc_ref | TEXT | Document reference number |
| doc_title | TEXT | Document title |
| revision | TEXT | Revision number (P01, C01, etc.) |
| status | TEXT | Document status |
| file_type | TEXT | File type/form |
| date_wet | TEXT | Date from WET timezone |
| doc_path | TEXT | Document path |
| ... | | (other fields) |

**Unique constraint**: `(project_name, snapshot_date, snapshot_time, doc_ref, revision)`

#### `revision_summaries`
Pre-aggregated revision counts by project and date.

| Column | Type | Description |
|--------|------|-------------|
| project_name | TEXT | Project name |
| snapshot_date | DATE | Snapshot date |
| snapshot_time | TIME | Snapshot time |
| revision_type | TEXT | Revision type (P01, P02, C01, etc.) |
| count | INTEGER | Number of documents |

#### `status_summaries`
Pre-aggregated status counts by project and date.

| Column | Type | Description |
|--------|------|-------------|
| project_name | TEXT | Project name |
| snapshot_date | DATE | Snapshot date |
| snapshot_time | TIME | Snapshot time |
| status | TEXT | Status value |
| count | INTEGER | Number of documents |

#### `file_type_summaries`
Pre-aggregated file type counts by project and date.

#### `processing_history`
Tracks which files have been processed to avoid reprocessing.

## Database Manager (`scripts/db_manager.py`)

Flexible script for managing the database with multiple modes.

### Usage

#### Initialize Database (First Time Setup)
```bash
python scripts/db_manager.py --init
```

Creates the database schema and all tables.

#### Import All Existing Files
```bash
python scripts/db_manager.py --import-all
```

Imports all historical files from all projects into the database. This populates the database with historical data.

#### Import Specific Project
```bash
python scripts/db_manager.py --import-project GP
```

Valid project codes: `OVB`, `NM`, `GP`, `HP`, `WCR`

#### Update with New Files Only
```bash
python scripts/db_manager.py --update
```

**This is the command that should be run weekly!** It only processes files that haven't been imported yet, making it very efficient.

#### Rebuild Database (Wipe and Recreate)
```bash
python scripts/db_manager.py --rebuild
```

**WARNING**: This deletes ALL data and rebuilds the schema. Use when:
- Schema changes require migration
- Database becomes corrupted
- Want to start fresh

#### Force Reimport (Override Existing)
```bash
python scripts/db_manager.py --import-all --force
```

Reimports all files even if already processed. Useful when:
- Data processing logic changed
- Need to recalculate summaries
- Found errors in previous import

#### Show Database Statistics
```bash
python scripts/db_manager.py --stats
```

Displays:
- Number of projects
- Number of snapshots per project
- Date ranges
- Document counts

### Command Options

| Option | Description |
|--------|-------------|
| `--init` | Initialize database schema |
| `--rebuild` | Wipe and rebuild database |
| `--import-all` | Import all files from all projects |
| `--import-project CODE` | Import specific project (OVB/NM/GP/HP/WCR) |
| `--update` | Update with new files only |
| `--stats` | Show database statistics |
| `--force` | Force reimport even if already processed |
| `--db-path PATH` | Custom database path (default: data/documents.db) |

## Python API Usage

### Basic Usage

```python
from data import DocumentDatabase

# Connect to database
with DocumentDatabase() as db:
    # Get summary data for reports
    summary_df = db.get_summary_dataframe('NewMalden')
    
    # Get latest documents
    latest_df = db.get_latest_documents('NewMalden')
    
    # Check if file processed
    processed = db.is_file_processed('NewMalden', 'NM Document Listing 141025.xlsx')
    
    # Get project statistics
    stats = db.get_project_stats('NewMalden')
```

### Insert Data

```python
from data import DocumentDatabase
from datetime import datetime

with DocumentDatabase() as db:
    # Insert documents
    count = db.insert_documents(
        project_name='NewMalden',
        snapshot_date='2025-10-14',
        snapshot_time='09:30',
        documents_df=df
    )
    
    # Insert summary counts
    counts = {'Rev_P01': 50, 'Status_Status A': 25}
    db.insert_summaries(
        project_name='NewMalden',
        snapshot_date='2025-10-14',
        snapshot_time='09:30',
        counts=counts
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

### Query Data

```python
import pandas as pd
from data import DocumentDatabase

with DocumentDatabase() as db:
    # Get all documents from September 2025
    query = """
        SELECT * FROM documents
        WHERE project_name = 'NewMalden'
          AND snapshot_date BETWEEN '2025-09-01' AND '2025-09-30'
    """
    df = pd.read_sql_query(query, db.conn)
    
    # Get monthly status progression
    query = """
        SELECT 
            strftime('%Y-%m', snapshot_date) as month,
            status,
            SUM(count) as total
        FROM status_summaries
        WHERE project_name = 'NewMalden'
        GROUP BY month, status
        ORDER BY month
    """
    monthly_df = pd.read_sql_query(query, db.conn)
```

## Weekly Workflow

### Automated Workflow (Recommended)

The main script will automatically call `db_manager.update_database_with_new_files()` before generating reports.

```python
# In main.py
from scripts.db_manager import update_database_with_new_files

# Update database with any new files
stats = update_database_with_new_files()

# Then generate reports from database
# ...
```

### Manual Workflow

1. **Monday morning**: Place new files in `input/` folders
2. **Run update**: `python scripts/db_manager.py --update`
3. **Generate reports**: `python main.py` (will read from database)

## Report Generation from Database

### Current Reports (Using Database)

Reports now read from the database instead of processing files directly:

```python
from data import DocumentDatabase

with DocumentDatabase() as db:
    # Get summary data (replaces old Excel reading)
    summary_df = db.get_summary_dataframe('NewMalden')
    
    # Get latest data (replaces old file loading)
    latest_df = db.get_latest_documents('NewMalden')
    
    # Generate reports as before
    generate_progression_report(summary_df, output_file, config, latest_df)
```

### Future Report Types (Easy to Add)

With data in the database, new report types are trivial:

**Monthly Summary**:
```python
# Group by month instead of week
SELECT 
    strftime('%Y-%m', snapshot_date) as month,
    ...
FROM documents
GROUP BY month
```

**Quarterly Comparison**:
```python
# Compare Q3 vs Q4
SELECT ... WHERE snapshot_date BETWEEN '2025-07-01' AND '2025-09-30'
UNION
SELECT ... WHERE snapshot_date BETWEEN '2025-10-01' AND '2025-12-31'
```

**Custom Date Range**:
```python
# Any date range
SELECT ... WHERE snapshot_date BETWEEN ? AND ?
```

## Benefits Summary

| Feature | Before (Excel-based) | After (Database) |
|---------|---------------------|------------------|
| Weekly processing | ✅ Fast (only new files) | ✅ Fast (only new files) |
| Regenerate reports | ❌ Must reprocess 73 files | ✅ Instant from database |
| Monthly summaries | ❌ Not possible | ✅ Simple query |
| Custom date ranges | ❌ Not possible | ✅ Simple query |
| Add new features | ❌ Reprocess everything | ✅ Just update report code |
| Historical queries | ❌ Must read Excel files | ✅ SQL queries |
| Data portability | ❌ Locked in Excel | ✅ Standard SQL database |

## Maintenance

### Backup Database

```bash
# Copy database file
cp data/documents.db data/documents_backup_$(date +%Y%m%d).db
```

### Vacuum Database (Optimize)

```python
from data import DocumentDatabase

with DocumentDatabase() as db:
    db.conn.execute('VACUUM')
```

### Export to CSV

```python
import pandas as pd
from data import DocumentDatabase

with DocumentDatabase() as db:
    df = pd.read_sql_query("SELECT * FROM documents", db.conn)
    df.to_csv('export.csv', index=False)
```

## Troubleshooting

### Database is locked

- Close any open connections
- Check if another process is using the database

### Schema changes needed

1. Use `--rebuild` to recreate schema
2. Use `--import-all` to repopulate data

### Missing data

Check processing history:
```sql
SELECT * FROM processing_history WHERE project_name = 'NewMalden'
```

### Performance issues

Add indices if needed:
```sql
CREATE INDEX idx_custom ON documents(column_name);
```

## Future Enhancements

Potential additions:
- 📊 Web-based dashboard querying the database
- 📈 Real-time charts using SQL queries
- 🔍 Advanced search across all documents
- 📧 Automated email reports
- 🌐 REST API for external access
- 📱 Mobile app reading from database

