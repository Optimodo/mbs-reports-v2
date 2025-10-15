"""Database manager script for initializing, updating, and maintaining the document database.

This script can be run standalone or imported by the main processing script.

Usage:
    # Initialize database
    python scripts/db_manager.py --init
    
    # Wipe and rebuild
    python scripts/db_manager.py --rebuild
    
    # Import all existing files
    python scripts/db_manager.py --import-all
    
    # Import specific project
    python scripts/db_manager.py --import-project GP
    
    # Update with new files only
    python scripts/db_manager.py --update
    
    # Show database stats
    python scripts/db_manager.py --stats
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data import DocumentDatabase
from config import load_project_config
from processors import load_document_listing
from analyzers import get_counts
from utils import get_file_timestamp, slugify


# Project folder mappings
PROJECT_FOLDERS = {
    'OVB': 'input/OVB',
    'NM': 'input/NM',
    'GP': 'input/GP',
    'HP': 'input/HP',
    'WCR': 'input/WCR'
}

PROJECT_NAMES = {
    'OVB': 'OvalBlockB',
    'NM': 'NewMalden',
    'GP': 'GreenwichPeninsula',
    'HP': 'HollowayPark',
    'WCR': 'WestCromwellRoad'
}


def initialize_database(db_path='data/documents.db'):
    """Initialize the database schema.
    
    Args:
        db_path: Path to database file
    """
    print("Initializing database...")
    with DocumentDatabase(db_path) as db:
        db.initialize_schema()
    print("✓ Database initialized successfully")


def rebuild_database(db_path='data/documents.db'):
    """Wipe and rebuild the entire database.
    
    Args:
        db_path: Path to database file
    """
    print("WARNING: This will delete ALL data in the database!")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Rebuild cancelled")
        return
    
    print("\nRebuilding database...")
    with DocumentDatabase(db_path) as db:
        db.rebuild_database()
    print("✓ Database rebuilt successfully")


def import_project_files(project_code, project_name, force=False, db_path='data/documents.db'):
    """Import all files for a specific project into the database.
    
    Args:
        project_code: Project code (OVB, NM, GP, HP, WCR)
        project_name: Full project name
        force: If True, reimport even if already processed
        db_path: Path to database file
        
    Returns:
        int: Number of files imported
    """
    input_dir = Path(PROJECT_FOLDERS[project_code])
    
    if not input_dir.exists():
        print(f"✗ Project folder {input_dir} does not exist")
        return 0
    
    print(f"\nImporting {project_name} ({project_code})...")
    
    # Determine file patterns
    is_csv_project = project_code in ['HP', 'WCR']
    file_patterns = ["*.xlsx", "*.csv"] if is_csv_project else ["*.xlsx"]
    
    # Get all files with timestamps
    files_with_timestamps = []
    for pattern in file_patterns:
        for file_path in input_dir.glob(pattern):
            if file_path.name.startswith('~$'):  # Skip temporary files
                continue
            
            # Get timestamp from file
            date_str, time_str = get_file_timestamp(file_path)
            if not date_str or not time_str:
                print(f"  ⚠ Skipping {file_path.name} - could not read timestamp")
                continue
            
            try:
                date = datetime.strptime(date_str, '%d-%b-%Y')
                time = datetime.strptime(time_str, '%H:%M').time()
                files_with_timestamps.append((file_path, date, time, date_str, time_str))
            except ValueError as e:
                print(f"  ⚠ Skipping {file_path.name} - invalid timestamp: {e}")
                continue
    
    # Sort by date
    files_with_timestamps.sort(key=lambda x: (x[1], x[2]))
    
    if not files_with_timestamps:
        print(f"  ✗ No valid files found")
        return 0
    
    files_imported = 0
    
    with DocumentDatabase(db_path) as db:
        for file_path, date, time, date_str, time_str in files_with_timestamps:
            # Check if already processed
            if not force and db.is_file_processed(project_name, file_path.name):
                print(f"  ○ Skipping {file_path.name} - already in database")
                continue
            
            try:
                # Load configuration
                config = load_project_config(project_name, file_path)
                
                # Load document listing
                print(f"  → Processing {file_path.name} ({date_str} {time_str})...")
                df = load_document_listing(file_path, config)
                
                if df is None or df.empty:
                    print(f"  ✗ No data in {file_path.name}")
                    continue
                
                # Convert date format for database (YYYY-MM-DD)
                snapshot_date = date.strftime('%Y-%m-%d')
                snapshot_time = time_str
                
                # Insert documents
                inserted = db.insert_documents(project_name, snapshot_date, snapshot_time, df)
                
                # Get and insert summary counts
                counts = get_counts(df, config)
                db.insert_summaries(project_name, snapshot_date, snapshot_time, counts)
                
                # Mark as processed
                db.mark_file_processed(project_name, file_path, file_path.name, 
                                       snapshot_date, snapshot_time, len(df))
                
                print(f"  ✓ Imported {inserted} documents from {file_path.name}")
                files_imported += 1
                
            except Exception as e:
                print(f"  ✗ Error processing {file_path.name}: {str(e)}")
                continue
    
    print(f"✓ Imported {files_imported} files for {project_name}")
    return files_imported


def import_all_projects(force=False, db_path='data/documents.db'):
    """Import all files from all projects.
    
    Args:
        force: If True, reimport even if already processed
        db_path: Path to database file
    """
    print("Importing all projects...")
    total_imported = 0
    
    for project_code, project_name in PROJECT_NAMES.items():
        try:
            imported = import_project_files(project_code, project_name, force, db_path)
            total_imported += imported
        except Exception as e:
            print(f"✗ Error importing {project_name}: {str(e)}")
            continue
    
    print(f"\n✓ Total files imported: {total_imported}")


def update_database_with_new_files(db_path='data/documents.db'):
    """Update database with any new files that haven't been processed yet.
    
    This is the function that should be called by the main script weekly.
    
    Args:
        db_path: Path to database file
        
    Returns:
        dict: Statistics about what was updated
    """
    print("Checking for new files to import...")
    
    stats = {
        'projects_updated': 0,
        'files_imported': 0,
        'documents_added': 0
    }
    
    for project_code, project_name in PROJECT_NAMES.items():
        try:
            files_imported = import_project_files(project_code, project_name, force=False, db_path=db_path)
            if files_imported > 0:
                stats['projects_updated'] += 1
                stats['files_imported'] += files_imported
        except Exception as e:
            print(f"✗ Error updating {project_name}: {str(e)}")
            continue
    
    if stats['files_imported'] == 0:
        print("✓ No new files to import - database is up to date")
    else:
        print(f"\n✓ Update complete:")
        print(f"  - Projects updated: {stats['projects_updated']}")
        print(f"  - Files imported: {stats['files_imported']}")
    
    return stats


def show_database_stats(db_path='data/documents.db'):
    """Display statistics about the database.
    
    Args:
        db_path: Path to database file
    """
    print("\n" + "="*60)
    print("DATABASE STATISTICS")
    print("="*60)
    
    with DocumentDatabase(db_path) as db:
        projects = db.get_all_projects()
        
        if not projects:
            print("Database is empty")
            return
        
        print(f"\nTotal projects: {len(projects)}\n")
        
        for project in projects:
            stats = db.get_project_stats(project)
            print(f"{project}:")
            print(f"  Snapshots: {stats['total_snapshots']}")
            print(f"  Latest document count: {stats['latest_document_count']}")
            print(f"  Date range: {stats['first_snapshot']} to {stats['last_snapshot']}")
            print()
    
    print("="*60)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Database manager for document tracking system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--init', action='store_true',
                       help='Initialize database schema')
    parser.add_argument('--rebuild', action='store_true',
                       help='Wipe and rebuild entire database')
    parser.add_argument('--import-all', action='store_true',
                       help='Import all files from all projects')
    parser.add_argument('--import-project', type=str,
                       help='Import files for specific project (OVB, NM, GP, HP, WCR)')
    parser.add_argument('--update', action='store_true',
                       help='Update database with new files only')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics')
    parser.add_argument('--force', action='store_true',
                       help='Force reimport even if already processed')
    parser.add_argument('--db-path', type=str, default='data/documents.db',
                       help='Path to database file (default: data/documents.db)')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    try:
        if args.init:
            initialize_database(args.db_path)
        
        if args.rebuild:
            rebuild_database(args.db_path)
        
        if args.import_all:
            import_all_projects(args.force, args.db_path)
        
        if args.import_project:
            project_code = args.import_project.upper()
            if project_code not in PROJECT_NAMES:
                print(f"✗ Unknown project code: {project_code}")
                print(f"Valid codes: {', '.join(PROJECT_NAMES.keys())}")
                return
            
            project_name = PROJECT_NAMES[project_code]
            import_project_files(project_code, project_name, args.force, args.db_path)
        
        if args.update:
            update_database_with_new_files(args.db_path)
        
        if args.stats:
            show_database_stats(args.db_path)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

