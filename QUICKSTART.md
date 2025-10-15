# Quick Start Guide - Database-Powered MBS Reports

## 🚀 First Time Setup

### 1. Initialize the Database

```bash
# Navigate to project directory
cd C:\Users\mikem\Projects\mbs-reports-v2

# Activate virtual environment
.\venv\Scripts\activate

# Initialize database schema
python scripts/db_manager.py --init
```

### 2. Populate Database with Historical Data

```bash
# Import all existing files from all projects (one-time operation)
python scripts/db_manager.py --import-all
```

This will:
- Scan all input folders (OVB, NM, GP, HP, WCR)
- Import ~73 historical files
- Store document data and summaries in SQLite database
- Take 2-5 minutes depending on file count

### 3. Verify Database Population

```bash
# Check database statistics
python scripts/db_manager.py --stats
```

You should see:
```
DATABASE STATISTICS
============================================================
Total projects: 5

OvalBlockB:
  Snapshots: 18
  Latest document count: 1400
  Date range: 2025-06-06 to 2025-10-13

NewMalden:
  Snapshots: 21
  Latest document count: 1049
  Date range: 2025-06-06 to 2025-10-13

...
```

---

## 📊 Generate Reports from Database

### Option A: Using Main Script (Recommended)

```bash
# Run main script
python main.py

# Select option 6: Process from DATABASE
# This will:
# - Check for new files and import them
# - Query database for all snapshots
# - Generate reports from database
```

### Option B: Update Database Only

```bash
# When you add new files weekly, just run:
python scripts/db_manager.py --update

# Then generate reports:
python main.py
# Select option 6
```

---

## 📅 Weekly Workflow

Every Monday when new files arrive:

### Step 1: Add New Files
```bash
# Place new document listings in appropriate folders:
# - input/OVB/OVB Document Listing DDMMYY.xlsx
# - input/NM/NM Document Listing DDMMYY.xlsx
# - input/GP/GP Document Listing DDMMYY.xlsx
# - input/HP/HP Document Listing DDMMYY.csv
# - input/WCR/WCR Document Listing DDMMYY.csv
```

### Step 2: Process Everything
```bash
python main.py
# Select option 6: Process from DATABASE
```

That's it! The system will:
1. ✅ Detect new files
2. ✅ Import them into database
3. ✅ Query database for all snapshots
4. ✅ Generate updated reports with new data

---

## 🔄 Regenerate Reports

If you make changes to report layouts or configurations:

### Method 1: From Database (Fast - Recommended)
```bash
python main.py
# Select option 6: Process from DATABASE
```

This regenerates all reports from database instantly (no file reading needed).

### Method 2: From Files (Slow - Legacy)
```bash
python main.py
# Select option 7: Regenerate all reports from scratch
```

This re-reads all input files and regenerates reports.

---

## 🛠️ Advanced Database Operations

### Rebuild Database Completely

If schema changes or corruption occurs:

```bash
# WARNING: This deletes all data!
python scripts/db_manager.py --rebuild

# Then reimport all files
python scripts/db_manager.py --import-all
```

### Force Reimport All Files

If processing logic changed:

```bash
python scripts/db_manager.py --import-all --force
```

### Import Specific Project

```bash
# Only import one project
python scripts/db_manager.py --import-project GP

# Valid codes: OVB, NM, GP, HP, WCR
```

---

## 📂 Output Files

After running reports, you'll find in `output/` folder:

### Summary Reports
- `GreenwichPeninsula_summary.xlsx` - Overall summary with charts
- `GreenwichPeninsula_summary.pdf` - PDF export
- `NewMalden_summary.xlsx`
- `OvalBlockB_summary.xlsx`
- `HollowayPark_summary.xlsx`
- `WestCromwellRoad_summary.xlsx`

### Progression Reports
- `GreenwichPeninsula_progression.xlsx` - Week-by-week progression
- `GreenwichPeninsula_progression.pdf` - PDF export
- (Same for all projects)

---

## 🔍 Troubleshooting

### "No data in database" Error

Solution:
```bash
python scripts/db_manager.py --import-all
```

### "ModuleNotFoundError: No module named 'openpyxl'"

Solution:
```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Reports show old data

Solution:
```bash
# Update database with new files
python scripts/db_manager.py --update

# Then regenerate reports
python main.py  # Select option 6
```

### Database locked error

- Close any Python processes
- Close database browser tools
- Restart terminal

---

## 📊 What's New: Database vs Legacy

| Feature | Legacy (Options 1-3) | Database (Option 6) |
|---------|---------------------|---------------------|
| Data Source | Read files directly | Query database |
| Speed | Slow (reads 73 files) | Fast (queries database) |
| Flexibility | Can't regenerate | Regenerate anytime |
| New Files | Process one by one | Batch import to DB |
| Custom Reports | Hard to add | Easy (just query DB) |
| Monthly Summaries | Not possible | Easy SQL query |
| Date Ranges | Fixed (weekly) | Flexible (any range) |

---

## 💡 Benefits of Database Approach

### 1. **Faster Processing**
- Only read new files once
- Reports query database (milliseconds vs minutes)

### 2. **Flexible Reporting**
- Change report layout? Regenerate instantly
- Add new chart? No need to reprocess files
- Monthly reports? Simple query

### 3. **Better Data Management**
- Single source of truth
- Queryable with SQL
- Easy backups (just copy .db file)

### 4. **Future Features**
- Web dashboard
- Custom date ranges
- Trend analysis
- Email automation
- API endpoints

---

## 📝 Example Queries

For advanced users, you can query the database directly:

```python
from data import DocumentDatabase
import pandas as pd

with DocumentDatabase() as db:
    # Get all September data
    query = """
        SELECT * FROM documents
        WHERE project_name = 'NewMalden'
          AND snapshot_date BETWEEN '2025-09-01' AND '2025-09-30'
    """
    df = pd.read_sql_query(query, db.conn)
    
    # Get monthly status counts
    query = """
        SELECT 
            strftime('%Y-%m', snapshot_date) as month,
            status,
            SUM(count) as total
        FROM status_summaries
        WHERE project_name = 'NewMalden'
        GROUP BY month, status
    """
    monthly_df = pd.read_sql_query(query, db.conn)
```

---

## 🎯 Recommended Workflow Summary

**First Time:**
1. `python scripts/db_manager.py --init`
2. `python scripts/db_manager.py --import-all`
3. `python scripts/db_manager.py --stats` (verify)

**Every Week:**
1. Add new files to input folders
2. `python main.py` → Select option 6
3. Check output folder for updated reports

**When Changing Layouts:**
1. Edit report code
2. `python main.py` → Select option 6
3. Reports regenerate instantly from database

---

## 📞 Need Help?

- Check `DATABASE_README.md` for detailed database documentation
- Review `REFACTORING_SUMMARY.md` for architecture details
- Check error messages carefully
- Verify virtual environment is activated
- Ensure database is populated before generating reports

