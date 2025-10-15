"""File operations and management utilities."""

import json
import re
from pathlib import Path
from datetime import datetime
from .timestamps import get_file_timestamp


def load_processed_files_per_project():
    """Load the record of processed files per project.
    
    Returns:
        dict: Dictionary of processed files by project
    """
    try:
        with open('processed_files_per_project.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_processed_files_per_project(processed_files):
    """Save the record of processed files per project.
    
    Args:
        processed_files: Dictionary of processed files by project
    """
    with open('processed_files_per_project.json', 'w') as f:
        json.dump(processed_files, f, indent=2, default=str)


def get_project_files_with_timestamps(project_input_dir):
    """Get all Excel/CSV files in a project directory with their timestamps, sorted by date.
    
    Args:
        project_input_dir: Path to project input directory
        
    Returns:
        list: List of tuples (file_path, date, time, date_str, time_str)
    """
    files_with_timestamps = []
    
    # Check if this project uses CSV files (by folder name)
    project_dir_str = str(project_input_dir).lower()
    is_csv_project = ('hp' in project_dir_str or 'holloway' in project_dir_str or 
                     'wcr' in project_dir_str or 'cromwell' in project_dir_str)
    
    # Get file patterns to search for
    if is_csv_project:
        file_patterns = ["*.xlsx", "*.csv"]
    else:
        file_patterns = ["*.xlsx"]
    
    for pattern in file_patterns:
        for file_path in project_input_dir.glob(pattern):
            if file_path.name.startswith('~$'):  # Skip temporary files
                continue
                
            # Get timestamp from B4 (Excel) or Report Created column (CSV)
            date_str, time_str = get_file_timestamp(file_path)
            if not date_str or not time_str:
                print(f"Skipping {file_path.name} - could not read timestamp")
                continue
                
            # Convert to datetime for comparison
            try:
                date = datetime.strptime(date_str, '%d-%b-%Y')
                time = datetime.strptime(time_str, '%H:%M').time()
                files_with_timestamps.append((file_path, date, time, date_str, time_str))
            except ValueError as e:
                print(f"Warning: Could not parse date/time from {file_path.name}: {str(e)}")
                continue
    
    # Sort by date and time (oldest first)
    files_with_timestamps.sort(key=lambda x: (x[1], x[2]))
    return files_with_timestamps


def detect_project_files():
    """Detect all files in project folders and update the JSON tracking file.
    
    Returns:
        dict: Dictionary of all detected files by project
    """
    print("Detecting files in project folders...")
    
    # Setup directories
    input_dir = Path('input')
    
    # Define project folders with consistent naming
    project_folders = {
        'OVB': input_dir / 'OVB',
        'NM': input_dir / 'NM', 
        'GP': input_dir / 'GP',
        'HP': input_dir / 'HP'
    }
    
    # Load existing processed files record
    processed_files = load_processed_files_per_project()
    
    # Handle legacy "NewMalden" entry by merging with "NM"
    if "NewMalden" in processed_files and "NM" not in processed_files:
        processed_files["NM"] = processed_files.pop("NewMalden")
    elif "NewMalden" in processed_files and "NM" in processed_files:
        # Merge both entries
        nm_files = processed_files.get("NM", {})
        legacy_files = processed_files.get("NewMalden", {})
        nm_files.update(legacy_files)
        processed_files["NM"] = nm_files
        del processed_files["NewMalden"]
    
    # Similar handling for other projects
    if "OvalBlockB" in processed_files and "OVB" not in processed_files:
        processed_files["OVB"] = processed_files.pop("OvalBlockB")
    elif "OvalBlockB" in processed_files and "OVB" in processed_files:
        ovb_files = processed_files.get("OVB", {})
        legacy_files = processed_files.get("OvalBlockB", {})
        ovb_files.update(legacy_files)
        processed_files["OVB"] = ovb_files
        del processed_files["OvalBlockB"]
    
    if "GreenwichPeninsula" in processed_files and "GP" not in processed_files:
        processed_files["GP"] = processed_files.pop("GreenwichPeninsula")
    elif "GreenwichPeninsula" in processed_files and "GP" in processed_files:
        gp_files = processed_files.get("GP", {})
        legacy_files = processed_files.get("GreenwichPeninsula", {})
        gp_files.update(legacy_files)
        processed_files["GP"] = gp_files
        del processed_files["GreenwichPeninsula"]
    
    if "HollowayPark" in processed_files and "HP" not in processed_files:
        processed_files["HP"] = processed_files.pop("HollowayPark")
    elif "HollowayPark" in processed_files and "HP" in processed_files:
        hp_files = processed_files.get("HP", {})
        legacy_files = processed_files.get("HollowayPark", {})
        hp_files.update(legacy_files)
        processed_files["HP"] = hp_files
        del processed_files["HollowayPark"]
    
    all_files = {}
    
    # Scan each project folder
    for project_code, folder_path in project_folders.items():
        if not folder_path.exists():
            print(f"Warning: Project folder {folder_path} does not exist")
            continue
        
        print(f"\nScanning {project_code} folder...")
        project_files = get_project_files_with_timestamps(folder_path)
        
        if not project_files:
            print(f"No valid files found in {project_code} folder")
            continue
        
        # Initialize if not exists
        if project_code not in processed_files:
            processed_files[project_code] = {}
        
        # Store files by name with their timestamp keys
        project_file_dict = {}
        for file_path, date, time, date_str, time_str in project_files:
            file_key = f"{date_str}_{time_str}"
            project_file_dict[file_path.name] = file_key
            
            # Mark unprocessed files
            if file_path.name not in processed_files[project_code]:
                print(f"  Found unprocessed: {file_path.name} ({date_str} {time_str})")
        
        all_files[project_code] = project_file_dict
    
    # Save the updated record
    save_processed_files_per_project(processed_files)
    
    print("\nFile detection complete!")
    return all_files


def slugify(text):
    """Convert text to a filesystem-safe slug.
    
    Args:
        text: Text to slugify
        
    Returns:
        str: Slugified text
    """
    return re.sub(r'[^A-Za-z0-9]+', '_', text).strip('_')

