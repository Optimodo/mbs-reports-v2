"""
Parse accommodation schedule and update project configuration with apartment data.

This script reads a project's accommodation schedule (Excel/CSV) and generates
structured apartment data that gets inserted into the project's config file.

Usage:
    # Interactive menu mode (recommended)
    python scripts/update_accommodation_data.py
    
    # Command line mode (for automation)
    python scripts/update_accommodation_data.py <ProjectName>
    
Examples:
    python scripts/update_accommodation_data.py                    # Show interactive menu
    python scripts/update_accommodation_data.py GreenwichPeninsula # Update specific project
    
Standardized Filename Format:
    <ProjectCode> Accommodation Schedule <DDMMYY>.xlsx
    Examples:
        GP Accommodation Schedule 201025.xlsx (Greenwich Peninsula, 20th Oct 2025)
        HP Accommodation Schedule 151025.xlsx (Holloway Park, 15th Oct 2025)
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CONFIGS_DIR, INPUT_DIR


def clean_floor_number(floor_value, config):
    """
    Clean and standardize floor numbers based on project-specific format.
    
    Args:
        floor_value: Raw floor value from schedule
        config: Floor cleaning configuration
        
    Returns:
        Cleaned floor number/identifier
    """
    if pd.isna(floor_value):
        return None
    
    floor_str = str(floor_value).strip()
    
    # Apply prefix removal if configured (e.g., "L01" -> "01")
    prefix_to_remove = config.get('remove_prefix')
    if prefix_to_remove and floor_str.startswith(prefix_to_remove):
        floor_str = floor_str[len(prefix_to_remove):]
    
    # Apply suffix removal if configured
    suffix_to_remove = config.get('remove_suffix')
    if suffix_to_remove and floor_str.endswith(suffix_to_remove):
        floor_str = floor_str[:-len(suffix_to_remove)]
    
    # Convert to integer if configured
    if config.get('convert_to_int', False):
        try:
            return int(floor_str)
        except ValueError:
            return floor_str
    
    return floor_str


def clean_apartment_number(apt_value, config):
    """
    Clean and standardize apartment numbers based on project-specific format.
    
    Args:
        apt_value: Raw apartment value from schedule
        config: Apartment cleaning configuration
        
    Returns:
        Cleaned apartment number
    """
    if pd.isna(apt_value):
        return None
    
    apt_str = str(apt_value).strip()
    
    # Remove any configured prefix (e.g., "Apt " or "Flat ")
    prefix_to_remove = config.get('remove_prefix')
    if prefix_to_remove:
        apt_str = apt_str.replace(prefix_to_remove, '')
    
    # Extract number using regex if configured
    extract_pattern = config.get('extract_pattern')
    if extract_pattern:
        match = re.search(extract_pattern, apt_str)
        if match:
            apt_str = match.group(1) if match.groups() else match.group(0)
    
    # Convert to integer
    try:
        return int(apt_str)
    except ValueError:
        return apt_str


def parse_accommodation_schedule(project_name):
    """
    Parse accommodation schedule for a project and generate structured data.
    
    Args:
        project_name: Name of the project (e.g., 'GreenwichPeninsula')
        
    Returns:
        Dictionary with structured accommodation data
    """
    # Load the project's existing config to get accommodation schedule settings
    config_file = CONFIGS_DIR / f"{project_name}.py"
    if not config_file.exists():
        print(f"❌ Error: Config file not found: {config_file}")
        return None
    
    # Import the project config
    import importlib.util
    spec = importlib.util.spec_from_file_location(project_name, config_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get accommodation schedule configuration
    if not hasattr(module, 'ACCOMMODATION_SCHEDULE_CONFIG'):
        print(f"❌ Error: ACCOMMODATION_SCHEDULE_CONFIG not found in {project_name}.py")
        print("\nYou need to add ACCOMMODATION_SCHEDULE_CONFIG to the project config.")
        print("See the example configuration in the script comments.")
        return None
    
    schedule_config = module.ACCOMMODATION_SCHEDULE_CONFIG
    
    # Check if enabled
    if not schedule_config.get('enabled', False):
        print(f"ℹ️  Accommodation schedule parsing is disabled for {project_name}")
        return None
    
    # Get file path (can be absolute or relative to INPUT_DIR)
    file_path = schedule_config.get('file_path')
    if not file_path:
        print(f"❌ Error: file_path not specified in ACCOMMODATION_SCHEDULE_CONFIG")
        return None
    
    # Resolve file path
    if not os.path.isabs(file_path):
        file_path = INPUT_DIR / file_path
    else:
        file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Error: Accommodation schedule file not found: {file_path}")
        return None
    
    print(f"📖 Reading accommodation schedule: {file_path}")
    
    # Read the Excel/CSV file
    read_config = schedule_config.get('read_config', {})
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path, **read_config)
    else:
        df = pd.read_excel(file_path, **read_config)
    
    print(f"   Loaded {len(df)} rows")
    
    # Get column mappings
    column_mapping = schedule_config.get('column_mapping', {})
    
    # Required columns
    apartment_col = column_mapping.get('apartment')
    if not apartment_col or apartment_col not in df.columns:
        print(f"❌ Error: Apartment column '{apartment_col}' not found in schedule")
        print(f"   Available columns: {list(df.columns)}")
        return None
    
    # Optional columns
    phase_col = column_mapping.get('phase')
    block_col = column_mapping.get('block')
    floor_col = column_mapping.get('floor')
    type_col = column_mapping.get('apartment_type')
    bedrooms_col = column_mapping.get('bedrooms')
    tenure_col = column_mapping.get('tenure')
    
    # Get cleaning configurations
    apartment_cleaning = schedule_config.get('apartment_cleaning', {})
    floor_cleaning = schedule_config.get('floor_cleaning', {})
    
    # Build structured data
    accommodation_data = {
        'total_apartments': 0,
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'source_file': str(file_path.name),
        'phases': {},
        'apartment_types': {},
        'apartment_lookup': {}
    }
    
    # Track phase/block statistics
    phase_stats = {}
    block_stats = {}
    type_stats = {}
    tenure_stats = {}
    
    # Process each row
    valid_apartments = 0
    for idx, row in df.iterrows():
        # Extract and clean apartment number
        apt_num = clean_apartment_number(row.get(apartment_col), apartment_cleaning)
        if not apt_num:
            continue
        
        valid_apartments += 1
        
        # Extract other attributes
        phase = str(row.get(phase_col)).strip() if phase_col and pd.notna(row.get(phase_col)) else None
        block = str(row.get(block_col)).strip().upper() if block_col and pd.notna(row.get(block_col)) else None
        floor = clean_floor_number(row.get(floor_col), floor_cleaning) if floor_col else None
        apt_type = str(row.get(type_col)).strip() if type_col and pd.notna(row.get(type_col)) else None
        tenure = str(row.get(tenure_col)).strip() if tenure_col and pd.notna(row.get(tenure_col)) else None
        
        # Parse bedrooms (handle non-numeric values)
        bedrooms = None
        if bedrooms_col and pd.notna(row.get(bedrooms_col)):
            try:
                bedrooms = int(row.get(bedrooms_col))
            except (ValueError, TypeError):
                pass  # Skip non-numeric bedroom values
        
        # Store in apartment lookup
        accommodation_data['apartment_lookup'][apt_num] = {
            'phase': phase,
            'block': block,
            'floor': floor,
            'type': apt_type,
            'bedrooms': bedrooms,
            'tenure': tenure
        }
        
        # Update phase statistics
        if phase:
            if phase not in phase_stats:
                phase_stats[phase] = {
                    'apartments': [],
                    'blocks': {}
                }
            phase_stats[phase]['apartments'].append(apt_num)
            
            # Update block statistics within phase
            if block:
                if block not in phase_stats[phase]['blocks']:
                    phase_stats[phase]['blocks'][block] = {
                        'apartments': [],
                        'floors': set()
                    }
                phase_stats[phase]['blocks'][block]['apartments'].append(apt_num)
                # Include floor even if it's 0 (but not if it's None)
                if floor is not None:
                    phase_stats[phase]['blocks'][block]['floors'].add(floor)
        
        # Update apartment type statistics
        if apt_type:
            if apt_type not in type_stats:
                type_stats[apt_type] = {
                    'apartments': [],
                    'bedrooms': bedrooms
                }
            type_stats[apt_type]['apartments'].append(apt_num)
        
        # Update tenure statistics
        if tenure:
            if tenure not in tenure_stats:
                tenure_stats[tenure] = {
                    'apartments': []
                }
            tenure_stats[tenure]['apartments'].append(apt_num)
    
    accommodation_data['total_apartments'] = valid_apartments
    print(f"✓ Processed {valid_apartments} valid apartments")
    
    # Build phases structure
    for phase, stats in phase_stats.items():
        phase_data = {
            'apartment_count': len(stats['apartments']),
            'apartments': sorted(stats['apartments']),
            'blocks': {}
        }
        
        for block, block_data in stats['blocks'].items():
            phase_data['blocks'][block] = {
                'apartment_count': len(block_data['apartments']),
                'apartments': sorted(block_data['apartments']),
                'floors': sorted(list(block_data['floors']))
            }
        
        accommodation_data['phases'][phase] = phase_data
    
    # Build apartment types structure
    for apt_type, stats in type_stats.items():
        accommodation_data['apartment_types'][apt_type] = {
            'count': len(stats['apartments']),
            'bedrooms': stats['bedrooms'],
            'apartments': sorted(stats['apartments'])
        }
    
    # Build tenure structure
    accommodation_data['tenures'] = {}
    for tenure, stats in tenure_stats.items():
        accommodation_data['tenures'][tenure] = {
            'count': len(stats['apartments']),
            'apartments': sorted(stats['apartments'])
        }
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Total apartments: {accommodation_data['total_apartments']}")
    print(f"   Phases: {len(accommodation_data['phases'])}")
    for phase, data in accommodation_data['phases'].items():
        print(f"      {phase}: {data['apartment_count']} apartments, {len(data['blocks'])} blocks")
    if accommodation_data['apartment_types']:
        print(f"   Apartment types: {len(accommodation_data['apartment_types'])}")
    if accommodation_data['tenures']:
        print(f"   Tenures: {len(accommodation_data['tenures'])}")
        for tenure, data in accommodation_data['tenures'].items():
            print(f"      {tenure}: {data['count']} apartments")
    
    return accommodation_data


def update_config_file(project_name, accommodation_data):
    """
    Update the project config file with accommodation data.
    
    Args:
        project_name: Name of the project
        accommodation_data: Structured accommodation data dictionary
    """
    config_file = CONFIGS_DIR / f"{project_name}.py"
    
    print(f"\n📝 Updating config file: {config_file}")
    
    # Read existing config
    with open(config_file, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    # Generate ACCOMMODATION_DATA section
    data_section = f"\n# Accommodation Data - Auto-generated by update_accommodation_data.py\n"
    data_section += f"# Last updated: {accommodation_data['last_updated']}\n"
    data_section += f"# Source: {accommodation_data['source_file']}\n"
    data_section += f"ACCOMMODATION_DATA = {{\n"
    data_section += f"    'total_apartments': {accommodation_data['total_apartments']},\n"
    data_section += f"    'last_updated': '{accommodation_data['last_updated']}',\n"
    data_section += f"    'source_file': '{accommodation_data['source_file']}',\n"
    data_section += f"    \n"
    data_section += f"    'phases': {{\n"
    
    for phase, phase_data in accommodation_data['phases'].items():
        data_section += f"        '{phase}': {{\n"
        data_section += f"            'apartment_count': {phase_data['apartment_count']},\n"
        data_section += f"            'apartments': {phase_data['apartments']},\n"
        data_section += f"            'blocks': {{\n"
        
        for block, block_data in phase_data['blocks'].items():
            data_section += f"                '{block}': {{\n"
            data_section += f"                    'apartment_count': {block_data['apartment_count']},\n"
            data_section += f"                    'apartments': {block_data['apartments']},\n"
            data_section += f"                    'floors': {block_data['floors']}\n"
            data_section += f"                }},\n"
        
        data_section += f"            }}\n"
        data_section += f"        }},\n"
    
    data_section += f"    }},\n"
    data_section += f"    \n"
    
    # Add apartment types if present
    if accommodation_data['apartment_types']:
        data_section += f"    'apartment_types': {{\n"
        for apt_type, type_data in accommodation_data['apartment_types'].items():
            data_section += f"        '{apt_type}': {{\n"
            data_section += f"            'count': {type_data['count']},\n"
            data_section += f"            'bedrooms': {type_data.get('bedrooms')},\n"
            data_section += f"            'apartments': {type_data['apartments']}\n"
            data_section += f"        }},\n"
        data_section += f"    }},\n"
        data_section += f"    \n"
    
    # Add tenures if present
    if accommodation_data.get('tenures'):
        data_section += f"    'tenures': {{\n"
        for tenure, tenure_data in accommodation_data['tenures'].items():
            data_section += f"        '{tenure}': {{\n"
            data_section += f"            'count': {tenure_data['count']},\n"
            data_section += f"            'apartments': {tenure_data['apartments']}\n"
            data_section += f"        }},\n"
        data_section += f"    }},\n"
        data_section += f"    \n"
    
    # Add apartment lookup (but abbreviated for readability)
    data_section += f"    'apartment_lookup': {{\n"
    data_section += f"        # Full apartment lookup dictionary with {len(accommodation_data['apartment_lookup'])} apartments\n"
    for apt_num, apt_data in accommodation_data['apartment_lookup'].items():
        data_section += f"        {apt_num}: {apt_data},\n"
    data_section += f"    }}\n"
    data_section += f"}}\n"
    
    # Check if ACCOMMODATION_DATA already exists in the file
    if 'ACCOMMODATION_DATA = {' in config_content:
        # Replace existing ACCOMMODATION_DATA section
        # Find the start of ACCOMMODATION_DATA
        start_marker = '# Accommodation Data - Auto-generated'
        end_marker = '\n}\n'
        
        start_idx = config_content.find(start_marker)
        if start_idx == -1:
            start_idx = config_content.find('ACCOMMODATION_DATA = {')
        
        if start_idx != -1:
            # Find the end of the dictionary
            end_idx = config_content.find(end_marker, start_idx)
            if end_idx != -1:
                end_idx += len(end_marker)
                # Replace the section
                config_content = config_content[:start_idx] + data_section + config_content[end_idx:]
            else:
                print("⚠️  Warning: Could not find end of ACCOMMODATION_DATA section")
                print("   Please manually review and update the config file")
        else:
            print("⚠️  Warning: Could not find ACCOMMODATION_DATA section to replace")
            print("   Appending to end of file instead")
            config_content += '\n' + data_section
    else:
        # Append to end of file
        config_content += '\n' + data_section
    
    # Write updated config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✓ Config file updated successfully")
    print(f"\n💡 Next steps:")
    print(f"   1. Review the changes in your Git diff")
    print(f"   2. Verify the accommodation data looks correct")
    print(f"   3. Commit the changes when satisfied")


def get_available_projects():
    """
    Get list of available projects that have accommodation schedule configs.
    
    Returns:
        Dictionary mapping project names to their accommodation schedule paths
    """
    projects = {}
    
    # Scan all config files
    for config_file in CONFIGS_DIR.glob("*.py"):
        if config_file.name.startswith('__'):
            continue
        
        project_name = config_file.stem
        
        # Try to load the config
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(project_name, config_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if it has accommodation schedule config
            if hasattr(module, 'ACCOMMODATION_SCHEDULE_CONFIG'):
                accom_config = module.ACCOMMODATION_SCHEDULE_CONFIG
                if accom_config.get('enabled', False):
                    file_path = accom_config.get('file_path', '')
                    projects[project_name] = file_path
        except Exception:
            continue
    
    return projects


def show_menu():
    """Display interactive menu for selecting projects to update."""
    print("\n" + "=" * 80)
    print("🏢  ACCOMMODATION SCHEDULE UPDATER")
    print("=" * 80)
    print("\nThis tool parses accommodation schedules and updates project configurations")
    print("with apartment data (phases, blocks, types, tenures, etc.)")
    
    # Get available projects
    available_projects = get_available_projects()
    
    if not available_projects:
        print("\n❌ No projects found with accommodation schedule configuration enabled")
        print("\nTo enable a project:")
        print("  1. Add ACCOMMODATION_SCHEDULE_CONFIG to the project's config file")
        print("  2. Set 'enabled': True in the configuration")
        print("  3. Specify the accommodation schedule file path")
        return None
    
    print(f"\n📋 Available Projects ({len(available_projects)}):")
    print("-" * 80)
    
    project_list = sorted(available_projects.keys())
    for i, project_name in enumerate(project_list, 1):
        file_path = available_projects[project_name]
        print(f"  {i}. {project_name:25} → {file_path}")
    
    print(f"  {len(project_list) + 1}. Update ALL projects")
    print("  0. Exit")
    print("-" * 80)
    
    while True:
        try:
            choice = input("\nSelect project (0 to exit): ").strip()
            
            if not choice:
                continue
            
            choice_num = int(choice)
            
            if choice_num == 0:
                print("\n👋 Exiting...")
                return None
            elif choice_num == len(project_list) + 1:
                return project_list  # Return all projects
            elif 1 <= choice_num <= len(project_list):
                return [project_list[choice_num - 1]]  # Return single project as list
            else:
                print(f"❌ Invalid choice. Please select 0-{len(project_list) + 1}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            return None


def main():
    """Main entry point for the script."""
    # Check if project name provided as command line argument
    if len(sys.argv) >= 2:
        # Command line mode
        project_name = sys.argv[1]
        projects_to_update = [project_name]
    else:
        # Interactive menu mode
        projects_to_update = show_menu()
        
        if not projects_to_update:
            sys.exit(0)
    
    # Update selected projects
    success_count = 0
    fail_count = 0
    
    for project_name in projects_to_update:
        print(f"\n{'=' * 80}")
        print(f"🏢 Updating accommodation data for: {project_name}")
        print("=" * 80)
        
        try:
            # Parse the accommodation schedule
            accommodation_data = parse_accommodation_schedule(project_name)
            
            if not accommodation_data:
                print(f"\n❌ Failed to parse accommodation schedule for {project_name}")
                fail_count += 1
                continue
            
            # Update the config file
            update_config_file(project_name, accommodation_data)
            
            print(f"\n✅ {project_name} accommodation data updated successfully!")
            success_count += 1
            
        except Exception as e:
            print(f"\n❌ Error updating {project_name}: {str(e)}")
            fail_count += 1
    
    # Summary
    if len(projects_to_update) > 1:
        print(f"\n{'=' * 80}")
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"  ✅ Successfully updated: {success_count} project(s)")
        if fail_count > 0:
            print(f"  ❌ Failed: {fail_count} project(s)")
        print("=" * 80)
    
    print("\n💡 Next steps:")
    print("   1. Review the changes in your Git diff")
    print("   2. Verify the accommodation data looks correct")
    print("   3. Commit the changes when satisfied")
    
    if fail_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()

