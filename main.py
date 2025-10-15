"""Main orchestration script for Asite Document Reporter.

This module handles the high-level workflow and menu interface for processing
document listings and generating reports.
"""

import warnings
import pandas as pd
from datetime import datetime
from pathlib import Path
from config import load_project_config

# Suppress openpyxl warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
warnings.filterwarnings('ignore', category=FutureWarning)

# Import from new modular structure
from processors import load_document_listing
from analyzers import get_counts
from reports import (
    save_excel_with_retry,
    generate_progression_report,
    fill_empty_cells_with_zeros_in_file
)
from utils import (
    load_processed_files_per_project,
    save_processed_files_per_project,
    get_project_files_with_timestamps,
    detect_project_files,
    slugify,
    get_file_timestamp
)
from data import DocumentDatabase
from scripts.db_manager import update_database_with_new_files


def show_menu():
    """Display the main menu and get user choice.
    
    Returns:
        str: User's menu choice
    """
    print("\n" + "="*60)
    print("Document Register Processor")
    print("="*60)
    print("1. Process latest file (legacy)")
    print("2. Process all projects (incremental - legacy)")
    print("3. Process single project (legacy)")
    print("4. Detect files only")
    print("5. Generate standalone report")
    print("6. Process from DATABASE (recommended)")
    print("7. Regenerate all reports from scratch (legacy)")
    print("8. Exit")
    print("="*60)
    print("\n💡 TIP: Use option 6 for database-powered processing")
    
    choice = input("\nEnter your choice (1-8): ").strip()
    return choice


def get_project_selection():
    """Get project selection from user.
    
    Returns:
        tuple: (project_name, project_code)
    """
    print("\nAvailable projects:")
    print("1. Oval Block B (OVB)")
    print("2. New Malden (NM)")
    print("3. Greenwich Peninsula (GP)")
    print("4. Holloway Park (HP)")
    print("5. West Cromwell Road (WCR)")
    
    choice = input("\nSelect project (1-5): ").strip()
    
    project_map = {
        '1': ('OvalBlockB', 'OVB'),
        '2': ('NewMalden', 'NM'),
        '3': ('GreenwichPeninsula', 'GP'),
        '4': ('HollowayPark', 'HP'),
        '5': ('WestCromwellRoad', 'WCR')
    }
    
    return project_map.get(choice, ('NewMalden', 'NM'))


def get_standalone_input():
    """Get input file path for standalone report generation.
    
    Returns:
        tuple: (input_file_path, project_name)
    """
    print("\nGenerate Standalone Report")
    print("-" * 60)
    
    input_path = input("Enter the full path to the Excel file: ").strip().strip('"')
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")
    
    print("\nSelect project for this file:")
    project_name, _ = get_project_selection()
    
    return input_file, project_name


def generate_standalone_report(input_file, output_file, config):
    """Generate a standalone report from a single input file.
    
    Args:
        input_file: Path to input Excel file
        output_file: Path to output report file
        config: Project configuration dictionary
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the input file
        current_df = load_document_listing(input_file, config)
        if current_df is None:
            return False
        
        # Get counts for summary
        counts = get_counts(current_df, config)
        
        # Create summary DataFrame with single row
        summary_data = [{
            'Date': datetime.now().strftime('%d-%b-%Y'),
            'Time': datetime.now().strftime('%H:%M')
        }]
        for key in sorted(counts.keys()):
            summary_data[0][key] = counts.get(key, 0)
        
        summary_df = pd.DataFrame(summary_data)
        
        # Create empty changes DataFrame since this is a standalone report
        changes_df = pd.DataFrame(columns=list(current_df.columns) + ['Change Type', 'Change Details'])
        
        # Save to Excel
        if save_excel_with_retry(summary_df, changes_df, current_df, output_file, config):
            print(f"\nStandalone report generated in {output_file}")
            return True
        else:
            print("\nPlease close any open Excel files and try again.")
            return False
            
    except Exception as e:
        print(f"Error generating standalone report: {str(e)}")
        return False


def process_project_files(project_name, project_input_dir, output_dir, processed_files):
    """Process all files for a single project.
    
    Args:
        project_name: Name of the project
        project_input_dir: Path to project input directory
        output_dir: Path to output directory
        processed_files: Dictionary tracking which files have been processed
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not project_input_dir.exists():
        print(f"Project folder {project_input_dir} does not exist")
        return False
    
    # Get all files with their timestamps
    files_with_timestamps = get_project_files_with_timestamps(project_input_dir)
    
    if not files_with_timestamps:
        print(f"No valid files found in {project_input_dir}")
        return False
    
    # Initialize project in processed_files if not exists
    project_slug = slugify(project_name)
    if project_slug not in processed_files:
        processed_files[project_slug] = {}
    
    # Track all counts and latest data
    all_counts = {}
    latest_data_df = None
    previous_latest_data = None
    files_processed = False
    config = None
    
    # Process files in chronological order
    project_output_file = output_dir / f"{project_slug}_summary.xlsx"
    
    for file_path, date, time, date_str, time_str in files_with_timestamps:
        # Check if already processed
        file_key = f"{date_str}_{time_str}"
        if file_path.name in processed_files[project_slug] and processed_files[project_slug][file_path.name] == file_key:
            print(f"Skipping already processed: {file_path.name} ({date_str} {time_str})")
            # Still need to load the data for counts
            config = load_project_config(project_name, file_path)
            current_df = load_document_listing(file_path, config)
            if current_df is not None:
                counts = get_counts(current_df, config)
                all_counts[(date, time)] = counts
                latest_data_df = current_df.copy()
            continue
        
        # Process this file
        print(f"\nProcessing: {file_path.name} ({date_str} {time_str})")
        config = load_project_config(project_name, file_path)
        
        try:
            # Load the document listing
            current_df = load_document_listing(file_path, config)
            if current_df is None:
                continue
            
            # Get counts
            try:
                counts = get_counts(current_df, config)
                all_counts[(date, time)] = counts
            except Exception as e:
                print(f"Error getting counts: {str(e)}")
                raise
            
            # Mark as processed
            processed_files[project_slug][file_path.name] = file_key
            latest_data_df = current_df.copy()
            previous_latest_data = current_df.copy()
            files_processed = True
            
            # Generate progression report for this file (add new column)
            progression_output = output_dir / f"{project_slug}_progression.xlsx"
            
            # Create a single-row summary DataFrame for this file
            file_summary_data = [{
                'Date': date.strftime('%d-%b-%Y'),
                'Time': time.strftime('%H:%M')
            }]
            for key in sorted(counts.keys()):
                file_summary_data[0][key] = counts.get(key, 0)
            file_summary_df = pd.DataFrame(file_summary_data)
            
            print(f"Adding progression data for {date_str} {time_str}...")
            if generate_progression_report(file_summary_df, progression_output, config, current_df):
                print(f"Progression report updated with new column")
            else:
                print("Failed to update progression report")
                
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
            continue
    
    # Guard: If nothing was processed, don't continue
    if not files_processed or latest_data_df is None or config is None:
        print("No new files processed for this project.")
        return False
    
    # Create summary DataFrame from all counts
    summary_data = []
    for (date, time) in sorted(all_counts.keys()):
        row = {
            'Date': date.strftime('%d-%b-%Y'),
            'Time': time.strftime('%H:%M')
        }
        counts = all_counts[(date, time)]
        for key in sorted(counts.keys()):
            row[key] = counts.get(key, 0)
        summary_data.append(row)
    summary_df = pd.DataFrame(summary_data)
    
    # Save to Excel (summary only)
    if save_excel_with_retry(summary_df, None, latest_data_df, project_output_file, config):
        print(f"\nSummary updated in {project_output_file}")
    else:
        print("\nPlease close any open Excel files and try again.")
        return False
    
    # After all files are processed, fill empty cells in the progression report
    progression_output = output_dir / f"{project_slug}_progression.xlsx"
    fill_empty_cells_with_zeros_in_file(str(progression_output))
    
    return True


def process_single_project(project_name, project_code):
    """Process all files for a specific project in chronological order.
    
    Args:
        project_name: Name of the project
        project_code: Project code (OVB, NM, GP, HP)
    """
    print(f"\n{'='*60}")
    print(f"Processing project: {project_name}")
    print(f"{'='*60}")
    
    # Setup directories
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Define project folders
    project_folders = {
        'OVB': input_dir / 'OVB',
        'NM': input_dir / 'NM',
        'GP': input_dir / 'GP',
        'HP': input_dir / 'HP',
        'WCR': input_dir / 'WCR'
    }
    
    # Load processed files record
    processed_files = load_processed_files_per_project()
    
    # Process this project
    success = process_project_files(project_name, project_folders[project_code], output_dir, processed_files)
    
    if success:
        print(f"Successfully processed project: {project_name}")
    else:
        print(f"Failed to process project: {project_name}")
    
    # Save processed files record
    save_processed_files_per_project(processed_files)
    print(f"\n{'='*60}")
    print(f"Project {project_name} processed!")
    print(f"{'='*60}")


def process_all_projects():
    """Process all projects in their respective input folders."""
    # Setup directories
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Define project folders with consistent naming
    project_folders = {
        'OVB': input_dir / 'OVB',
        'NM': input_dir / 'NM',
        'GP': input_dir / 'GP',
        'HP': input_dir / 'HP',
        'WCR': input_dir / 'WCR'
    }
    
    # Project name mapping
    project_names = {
        'OVB': 'OvalBlockB',
        'NM': 'NewMalden',
        'GP': 'GreenwichPeninsula',
        'HP': 'HollowayPark',
        'WCR': 'WestCromwellRoad'
    }
    
    # Load processed files record
    processed_files = load_processed_files_per_project()
    
    # Process each project
    for project_code, project_input_dir in project_folders.items():
        project_name = project_names[project_code]
        
        print(f"\n{'='*60}")
        print(f"Processing project: {project_name}")
        print(f"{'='*60}")
        
        if not project_input_dir.exists():
            print(f"Project folder {project_input_dir} does not exist, skipping...")
            continue
        
        success = process_project_files(project_name, project_input_dir, output_dir, processed_files)
        
        if success:
            print(f"Successfully processed project: {project_name}")
        else:
            print(f"Failed to process project: {project_name}")
    
    # Save processed files record
    save_processed_files_per_project(processed_files)
    print(f"\n{'='*60}")
    print("All projects processed!")
    print(f"{'='*60}")


def process_projects_from_database():
    """Process all projects using database as data source.
    
    This function:
    1. Updates database with any new files
    2. Queries database for all snapshots per project
    3. Generates reports from database data (simulating file processing loop)
    """
    print("\n" + "="*60)
    print("PROCESSING FROM DATABASE")
    print("="*60)
    
    # Step 1: Update database with any new files
    print("\nStep 1: Checking for new files to import into database...")
    try:
        stats = update_database_with_new_files()
        if stats['files_imported'] > 0:
            print(f"✓ Imported {stats['files_imported']} new files")
        else:
            print("✓ Database is up to date")
    except Exception as e:
        print(f"✗ Error updating database: {str(e)}")
        print("Continuing with existing database data...")
    
    # Step 2: Generate reports from database
    print("\nStep 2: Generating reports from database...")
    
    # Setup directories
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Project name mapping
    project_names = {
        'OvalBlockB': 'OvalBlockB',
        'NewMalden': 'NewMalden',
        'GreenwichPeninsula': 'GreenwichPeninsula',
        'HollowayPark': 'HollowayPark',
        'WestCromwellRoad': 'WestCromwellRoad'
    }
    
    with DocumentDatabase() as db:
        # Get all projects from database
        db_projects = db.get_all_projects()
        
        if not db_projects:
            print("✗ No data in database. Please run db_manager.py --import-all first")
            return
        
        print(f"Found {len(db_projects)} projects in database")
        
        # Process each project
        for project_name in db_projects:
            print(f"\n{'='*60}")
            print(f"Processing: {project_name}")
            print(f"{'='*60}")
            
            try:
                # Load project configuration
                config = load_project_config(project_name)
                
                # Get summary data from database (all snapshots)
                summary_df = db.get_summary_dataframe(project_name)
                
                if summary_df.empty:
                    print(f"✗ No data for {project_name}")
                    continue
                
                print(f"Found {len(summary_df)} snapshots")
                
                # Get latest documents
                latest_data_df = db.get_latest_documents(project_name)
                
                # Project output files
                project_slug = slugify(project_name)
                summary_output = output_dir / f"{project_slug}_summary.xlsx"
                progression_output = output_dir / f"{project_slug}_progression.xlsx"
                
                # Delete existing progression report to rebuild from scratch
                if progression_output.exists():
                    progression_output.unlink()
                    print(f"Deleted existing progression report")
                
                # Process each snapshot (simulating file-by-file processing)
                print(f"\nProcessing {len(summary_df)} snapshots...")
                
                for idx, row in summary_df.iterrows():
                    snapshot_date = row['Date']
                    snapshot_time = row['Time']
                    
                    # Create single-row summary for this snapshot
                    snapshot_summary = pd.DataFrame([row])
                    
                    # Generate progression report (adds one column per snapshot)
                    if generate_progression_report(snapshot_summary, progression_output, config, latest_data_df):
                        print(f"  ✓ Added column: {snapshot_date} {snapshot_time}")
                    else:
                        print(f"  ✗ Failed to add column: {snapshot_date} {snapshot_time}")
                
                # Generate summary report with all data
                if save_excel_with_retry(summary_df, None, latest_data_df, summary_output, config):
                    print(f"\n✓ Summary saved: {summary_output}")
                else:
                    print(f"\n✗ Failed to save summary")
                
                # Fill empty cells in progression report
                fill_empty_cells_with_zeros_in_file(str(progression_output))
                print(f"✓ Progression completed: {progression_output}")
                
            except Exception as e:
                print(f"✗ Error processing {project_name}: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
    
    print(f"\n{'='*60}")
    print("Database processing complete!")
    print(f"{'='*60}")


def regenerate_all_reports():
    """Regenerate all reports from scratch using all available input files.
    
    This function:
    1. Deletes existing progression reports
    2. Processes ALL files in each project folder (ignoring processed files tracking)
    3. Regenerates reports completely from all available data
    """
    print("\n" + "="*60)
    print("REGENERATE ALL REPORTS FROM SCRATCH")
    print("="*60)
    print("\nThis will:")
    print("  - Delete existing progression reports")
    print("  - Process ALL files in input folders")
    print("  - Regenerate reports from scratch")
    print("\nExisting summary reports will be overwritten.")
    
    response = input("\nAre you sure you want to continue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Regeneration cancelled")
        return
    
    # Setup directories
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Define project folders
    project_folders = {
        'OVB': input_dir / 'OVB',
        'NM': input_dir / 'NM',
        'GP': input_dir / 'GP',
        'HP': input_dir / 'HP',
        'WCR': input_dir / 'WCR'
    }
    
    # Project name mapping
    project_names = {
        'OVB': 'OvalBlockB',
        'NM': 'NewMalden',
        'GP': 'GreenwichPeninsula',
        'HP': 'HollowayPark',
        'WCR': 'WestCromwellRoad'
    }
    
    # Delete existing progression reports
    print("\nDeleting existing progression reports...")
    for project_code, project_name in project_names.items():
        project_slug = slugify(project_name)
        progression_file = output_dir / f"{project_slug}_progression.xlsx"
        progression_pdf = output_dir / f"{project_slug}_progression.pdf"
        
        if progression_file.exists():
            progression_file.unlink()
            print(f"  Deleted {progression_file.name}")
        if progression_pdf.exists():
            progression_pdf.unlink()
            print(f"  Deleted {progression_pdf.name}")
    
    print("\nRegenerating reports...")
    
    # Process each project
    for project_code, project_input_dir in project_folders.items():
        project_name = project_names[project_code]
        
        print(f"\n{'='*60}")
        print(f"Regenerating: {project_name}")
        print(f"{'='*60}")
        
        if not project_input_dir.exists():
            print(f"Project folder {project_input_dir} does not exist, skipping...")
            continue
        
        # Get all files with timestamps
        files_with_timestamps = get_project_files_with_timestamps(project_input_dir)
        
        if not files_with_timestamps:
            print(f"No valid files found in {project_input_dir}")
            continue
        
        # Track all counts and latest data
        all_counts = {}
        latest_data_df = None
        config = None
        
        # Project output files
        project_slug = slugify(project_name)
        project_output_file = output_dir / f"{project_slug}_summary.xlsx"
        
        # Process ALL files in chronological order
        for file_path, date, time, date_str, time_str in files_with_timestamps:
            print(f"\nProcessing: {file_path.name} ({date_str} {time_str})")
            config = load_project_config(project_name, file_path)
            
            try:
                # Load the document listing
                current_df = load_document_listing(file_path, config)
                if current_df is None:
                    print(f"  Warning: No data in {file_path.name}")
                    continue
                
                # Get counts
                try:
                    counts = get_counts(current_df, config)
                    all_counts[(date, time)] = counts
                except Exception as e:
                    print(f"  Error getting counts: {str(e)}")
                    continue
                
                latest_data_df = current_df.copy()
                
                # Generate progression report for this file (add new column)
                progression_output = output_dir / f"{project_slug}_progression.xlsx"
                
                # Create a single-row summary DataFrame for this file
                file_summary_data = [{
                    'Date': date.strftime('%d-%b-%Y'),
                    'Time': time.strftime('%H:%M')
                }]
                for key in sorted(counts.keys()):
                    file_summary_data[0][key] = counts.get(key, 0)
                file_summary_df = pd.DataFrame(file_summary_data)
                
                print(f"  Adding to progression report...")
                if generate_progression_report(file_summary_df, progression_output, config, current_df):
                    print(f"  ✓ Added column for {date_str} {time_str}")
                else:
                    print(f"  ✗ Failed to update progression report")
                    
            except Exception as e:
                print(f"  ✗ Error processing {file_path.name}: {str(e)}")
                continue
        
        # Create summary DataFrame from all counts
        if all_counts and latest_data_df is not None and config is not None:
            summary_data = []
            for (date, time) in sorted(all_counts.keys()):
                row = {
                    'Date': date.strftime('%d-%b-%Y'),
                    'Time': time.strftime('%H:%M')
                }
                counts = all_counts[(date, time)]
                for key in sorted(counts.keys()):
                    row[key] = counts.get(key, 0)
                summary_data.append(row)
            summary_df = pd.DataFrame(summary_data)
            
            # Save summary report
            if save_excel_with_retry(summary_df, None, latest_data_df, project_output_file, config):
                print(f"\n✓ Summary saved to {project_output_file}")
            else:
                print(f"\n✗ Failed to save summary")
            
            # Fill empty cells in progression report
            progression_output = output_dir / f"{project_slug}_progression.xlsx"
            fill_empty_cells_with_zeros_in_file(str(progression_output))
            print(f"✓ Progression report completed: {progression_output}")
        else:
            print(f"\n✗ No data processed for {project_name}")
    
    print(f"\n{'='*60}")
    print("All reports regenerated!")
    print(f"{'='*60}")


def main():
    """Main function with interactive menu."""
    # Setup directories
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            # Process latest file (original behavior)
            print("\nProcessing latest file...")
            print("Note: This option processes a single latest file from the input directory.")
            print("For project-specific processing, use option 2 or 3.")
            
            # Get the previous latest data
            previous_latest_data = None
            output_file = output_dir / 'summary.xlsx'
            
            # Find the most recent file based on timestamps
            latest_file = None
            latest_timestamp = None
            
            for file_path in input_dir.glob("*.xlsx"):
                if file_path.name.startswith('~$'):  # Skip temporary files
                    continue
                    
                # Get timestamp from B4
                date_str, time_str = get_file_timestamp(file_path)
                if not date_str or not time_str:
                    print(f"Skipping {file_path.name} - could not read timestamp")
                    continue
                    
                # Convert to datetime for comparison
                try:
                    date = datetime.strptime(date_str, '%d-%b-%Y')
                    time = datetime.strptime(time_str, '%H:%M').time()
                    if latest_timestamp is None or (date, time) > latest_timestamp:
                        latest_timestamp = (date, time)
                        latest_file = file_path
                except ValueError as e:
                    print(f"Warning: Could not parse date/time from {file_path.name}: {str(e)}")
                    continue
            
            if latest_file is None:
                print("No valid files found to process")
                input("\nPress Enter to continue...")
                continue
            
            print(f"\nProcessing latest file: {latest_file.name}")
            
            # Load project configuration based on the latest file
            config = load_project_config(None, latest_file)
            
            # Read the latest file
            try:
                current_df = load_document_listing(latest_file, config)
                if current_df is None:
                    input("\nPress Enter to continue...")
                    continue
                
                # Get counts for summary
                try:
                    counts = get_counts(current_df, config)
                    all_counts = {latest_timestamp: counts}
                except Exception as e:
                    print(f"Error getting counts: {str(e)}")
                    input("\nPress Enter to continue...")
                    continue
                
            except Exception as e:
                print(f"Error processing {latest_file.name}: {str(e)}")
                input("\nPress Enter to continue...")
                continue
            
            # Create summary DataFrame
            summary_data = []
            for (date, time) in sorted(all_counts.keys()):
                row = {
                    'Date': date.strftime('%d-%b-%Y'),
                    'Time': time.strftime('%H:%M')
                }
                counts = all_counts[(date, time)]
                for key in sorted(counts.keys()):
                    row[key] = counts.get(key, 0)
                summary_data.append(row)
            
            summary_df = pd.DataFrame(summary_data)
            
            # Create empty changes DataFrame
            changes_df = pd.DataFrame(columns=list(current_df.columns) + ['Change Type', 'Change Details'])
            
            # Save to Excel
            project_slug = slugify(config.get('PROJECT_TITLE', 'summary'))
            output_file = output_dir / f"{project_slug}_summary.xlsx"
            
            if save_excel_with_retry(summary_df, changes_df, current_df, output_file, config):
                print(f"\nSummary updated in {output_file}")
                
                # Generate progression report
                progression_output = output_dir / f"{project_slug}_progression.xlsx"
                if generate_progression_report(summary_df, progression_output, config, current_df):
                    print(f"Progression report generated in {progression_output}")
                else:
                    print("Failed to generate progression report")
            else:
                print("\nPlease close any open Excel files and try again.")
            
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # Process all projects
            print("\nProcessing all projects...")
            process_all_projects()
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Process single project
            project_name, project_code = get_project_selection()
            print(f"\nProcessing single project: {project_name}")
            process_single_project(project_name, project_code)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Detect files only
            print("\nDetecting files in project folders...")
            detect_project_files()
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            # Generate standalone report
            try:
                input_file, project = get_standalone_input()
                
                # Load project configuration based on input file
                config = load_project_config(project, input_file)
                
                # Generate output filename
                project_slug = slugify(config.get('PROJECT_TITLE', 'standalone_report'))
                output_file = output_dir / f"{project_slug}_standalone_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                
                if generate_standalone_report(input_file, output_file, config):
                    print(f"\nStandalone report generated successfully!")
                else:
                    print("\nFailed to generate standalone report.")
                    
            except KeyboardInterrupt:
                print("\nCancelled.")
            except Exception as e:
                print(f"\nError: {str(e)}")
            
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            # Process from database (recommended workflow)
            process_projects_from_database()
            input("\nPress Enter to continue...")
            
        elif choice == '7':
            # Regenerate all reports from scratch (legacy)
            regenerate_all_reports()
            input("\nPress Enter to continue...")
            
        elif choice == '8':
            # Exit
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
