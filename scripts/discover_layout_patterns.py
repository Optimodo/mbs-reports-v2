"""Interactive layout pattern discovery script.

This script analyzes drawings and schematics from the database to automatically
discover potential layout sets (e.g., GA, RCP, Small Power, Ventilation, etc.)
and apartment type naming patterns.

It presents suggestions to the user for review before adding them to the project config.
"""

import sys
import os
from pathlib import Path
from collections import defaultdict, Counter
import re
from typing import Dict, List, Tuple, Set
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.database import DocumentDatabase
from config import load_project_config, CONFIGS_DIR


def get_available_projects():
    """Get list of projects that have accommodation data (candidates for layout tracking)."""
    projects = []
    
    for config_file in CONFIGS_DIR.glob("*.py"):
        if config_file.name.startswith('__'):
            continue
        
        project_name = config_file.stem
        
        try:
            config = load_project_config(project_name)
            # Only include projects with accommodation data
            if config.get('ACCOMMODATION_DATA', {}).get('total_apartments', 0) > 0:
                total_apts = config['ACCOMMODATION_DATA']['total_apartments']
                total_types = len(config['ACCOMMODATION_DATA'].get('apartment_types', {}))
                projects.append((project_name, total_apts, total_types))
        except Exception:
            continue
    
    return sorted(projects)


def extract_potential_apartment_types(doc_titles: List[str]) -> Dict[str, int]:
    """
    Extract potential apartment type patterns from document titles.
    
    Looks for patterns like:
    - "Type A", "Type B1", "Type E4"
    - "APT TYPE A"
    - "Unit Type A"
    - Apartment types in the title
    """
    type_patterns = [
        r'\bType\s+([A-Z][A-Z0-9-]*)\b',
        r'\bAPT\s+TYPE\s+([A-Z][A-Z0-9-]*)\b',
        r'\bUnit\s+Type\s+([A-Z][A-Z0-9-]*)\b',
        r'\b([A-Z])\s+Type\b',
        r'\bType\s+([A-Z0-9]{1,3})\b'
    ]
    
    type_counts = Counter()
    
    for title in doc_titles:
        for pattern in type_patterns:
            matches = re.findall(pattern, title, re.IGNORECASE)
            for match in matches:
                type_counts[match.upper()] += 1
    
    return dict(type_counts)


def extract_layout_categories(doc_titles: List[str], doc_refs: List[str]) -> Dict[str, Dict]:
    """
    Identify potential layout categories by analyzing common words/patterns.
    
    Returns dict of: {category_key: {'keywords': [...], 'count': N, 'samples': [...]}}
    """
    # Common layout category keywords
    category_keywords = {
        'ga': ['GA', 'General Arrangement', 'Floor Plan', 'Layout Plan', 'Proposed'],
        'rcp': ['RCP', 'Reflected Ceiling', 'Ceiling Plan'],
        'small_power': ['Small Power', 'Power Layout', 'SP', 'Power Points', 'Socket'],
        'lighting': ['Lighting', 'Light Layout', 'LT', 'Luminaire'],
        'ventilation': ['Ventilation', 'Vent', 'MVHR', 'MEV', 'Extract'],
        'combined_services': ['Combined Services', 'Services Layout', 'CS'],
        'drainage': ['Drainage', 'Drain', 'Soil', 'Waste', 'SVP'],
        'heating': ['Heating', 'UFH', 'Underfloor Heating', 'Radiator'],
        'electrical': ['Electrical', 'Distribution', 'DB', 'Consumer Unit'],
        'plumbing': ['Plumbing', 'DHW', 'Hot Water', 'Cold Water']
    }
    
    discovered = {}
    
    for category_key, keywords in category_keywords.items():
        matching_docs = []
        
        for i, title in enumerate(doc_titles):
            # Check if any keyword matches
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', title, re.IGNORECASE):
                    matching_docs.append((title, doc_refs[i] if i < len(doc_refs) else ''))
                    break
        
        if matching_docs:
            discovered[category_key] = {
                'keywords': keywords,
                'count': len(matching_docs),
                'samples': matching_docs[:5]  # First 5 samples
            }
    
    return discovered


def validate_against_accommodation_types(discovered_types: Dict[str, int], 
                                         accommodation_types: Set[str]) -> Dict:
    """
    Compare discovered types against accommodation schedule types.
    
    Returns validation info: matched types, unmatched discovered, unmatched accommodation.
    """
    discovered_set = set(discovered_types.keys())
    accom_set = set(accommodation_types)
    
    matched = discovered_set & accom_set
    discovered_only = discovered_set - accom_set
    accom_only = accom_set - discovered_set
    
    return {
        'matched': sorted(list(matched)),
        'discovered_only': sorted(list(discovered_only)),
        'accommodation_only': sorted(list(accom_only)),
        'match_percentage': (len(matched) / len(accom_set) * 100) if accom_set else 0
    }


def analyze_project_layouts(project_name: str) -> Dict:
    """
    Analyze a project's drawings to discover layout patterns.
    
    Returns analysis results including discovered types and categories.
    """
    print(f"\n{'='*80}")
    print(f"🔍 Analyzing: {project_name}")
    print(f"{'='*80}")
    
    # Load project config
    config = load_project_config(project_name)
    accommodation_data = config.get('ACCOMMODATION_DATA', {})
    accommodation_types = set(accommodation_data.get('apartment_types', {}).keys())
    
    print(f"📊 Accommodation Schedule Info:")
    print(f"   Total Apartments: {accommodation_data.get('total_apartments', 0)}")
    print(f"   Apartment Types: {len(accommodation_types)}")
    if accommodation_types:
        sample_types = sorted(list(accommodation_types))[:10]
        print(f"   Sample Types: {', '.join(sample_types)}{' ...' if len(accommodation_types) > 10 else ''}")
    
    # Get latest documents from database
    with DocumentDatabase() as db:
        latest_docs = db.get_latest_documents(project_name)
    
    if latest_docs.empty:
        print(f"❌ No documents found in database for {project_name}")
        return None
    
    print(f"\n📄 Total Documents: {len(latest_docs)}")
    
    # Filter to drawings only (exclude certificates, submittals, etc.)
    # Look for common drawing file type patterns
    drawing_patterns = ['DR', 'Drawing']
    
    # Filter by file type - use regex OR pattern
    mask = latest_docs['File Type'].fillna('').str.contains('DR', case=False, na=False)
    drawings = latest_docs[mask].copy()
    
    # Include only layout-related drawings (positive filter first)
    # Look for keywords that indicate this is a layout drawing
    layout_keywords = ['Layout', 'Plan', 'GA', 'RCP', 'Arrangement', 'Setting Out']
    layout_mask = pd.Series([False] * len(drawings), index=drawings.index)
    for keyword in layout_keywords:
        layout_mask |= drawings['Doc Title'].fillna('').str.contains(keyword, case=False, na=False)
    
    drawings = drawings[layout_mask].copy()
    
    # Then exclude specific non-layout documents
    exclude_patterns = [
        'Schedule', 'Detail', 'Section', 'Elevation'
    ]
    
    for pattern in exclude_patterns:
        drawings = drawings[
            ~drawings['Doc Title'].fillna('').str.contains(pattern, case=False, na=False)
        ]
    
    print(f"📐 Layout Drawings (after filtering): {len(drawings)}")
    
    if drawings.empty:
        print(f"❌ No layout drawings found")
        return None
    
    # Extract data
    doc_titles = drawings['Doc Title'].fillna('').tolist()
    doc_refs = drawings['Doc Ref'].fillna('').tolist() if 'Doc Ref' in drawings.columns else []
    
    # Discover apartment types in drawings
    print(f"\n🔍 Discovering Apartment Types in Drawings...")
    discovered_types = extract_potential_apartment_types(doc_titles)
    print(f"   Found {len(discovered_types)} potential apartment types")
    
    # Validate against accommodation schedule
    if accommodation_types:
        validation = validate_against_accommodation_types(discovered_types, accommodation_types)
        print(f"\n✓ Validation Against Accommodation Schedule:")
        print(f"   Match Rate: {validation['match_percentage']:.1f}%")
        print(f"   Matched Types: {len(validation['matched'])}")
        print(f"   Types in drawings only: {len(validation['discovered_only'])}")
        print(f"   Types in accommodation only: {len(validation['accommodation_only'])}")
        
        if validation['discovered_only']:
            print(f"\n   ⚠️  Types found in drawings but not in accommodation schedule:")
            print(f"      {', '.join(validation['discovered_only'][:20])}")
    else:
        validation = None
        print(f"   ⚠️  No accommodation types to validate against")
    
    # Discover layout categories
    print(f"\n🔍 Discovering Layout Categories...")
    discovered_categories = extract_layout_categories(doc_titles, doc_refs)
    print(f"   Found {len(discovered_categories)} potential layout categories:")
    
    for cat_key, cat_data in sorted(discovered_categories.items(), key=lambda x: -x[1]['count']):
        print(f"\n   📁 {cat_key.upper()} ({cat_data['count']} documents)")
        print(f"      Keywords: {', '.join(cat_data['keywords'][:3])}")
        print(f"      Samples:")
        for title, ref in cat_data['samples'][:2]:
            preview = title[:80] + '...' if len(title) > 80 else title
            print(f"        • {preview}")
    
    return {
        'project_name': project_name,
        'config': config,
        'total_drawings': len(drawings),
        'discovered_types': discovered_types,
        'discovered_categories': discovered_categories,
        'validation': validation,
        'accommodation_types': accommodation_types
    }


def generate_type_detection_patterns(discovered_types: Dict[str, int], 
                                     sample_titles: List[str]) -> Dict:
    """
    Generate apartment type detection patterns based on discovered types.
    """
    # Analyze the titles to find the most common pattern format
    patterns = {
        'title_patterns': [
            r'Type\s+([A-Z][A-Z0-9-]*)',
            r'APT\s+TYPE\s+([A-Z][A-Z0-9-]*)',
            r'Unit\s+Type\s+([A-Z][A-Z0-9-]*)'
        ],
        'doc_ref_patterns': [
            r'-TYPE-([A-Z][A-Z0-9-]+)-',
            r'-T([A-Z][A-Z0-9-]+)-'
        ],
        'path_patterns': [
            r'\\Type\s+([A-Z][A-Z0-9-]+)\\',
            r'\\([A-Z][A-Z0-9-]+)\s+Type\\'
        ]
    }
    
    return patterns


def generate_layout_config(analysis: Dict, selected_categories: List[str]) -> str:
    """
    Generate the APARTMENT_LAYOUT_TRACKING configuration Python code.
    """
    project_name = analysis['project_name']
    discovered_categories = analysis['discovered_categories']
    
    # Build the config string
    config_lines = []
    config_lines.append("# Apartment Layout Tracking Configuration")
    config_lines.append("# Auto-generated by discover_layout_patterns.py")
    config_lines.append("# Review and adjust patterns as needed")
    config_lines.append("")
    config_lines.append("APARTMENT_LAYOUT_TRACKING = {")
    config_lines.append("    'enabled': True,")
    config_lines.append("    ")
    config_lines.append("    'detection': {")
    config_lines.append("        'file_type_patterns': ['Drawing', 'DR'],")
    config_lines.append("        'doc_ref_patterns': [r'DR-A-', r'DR-M-', r'DR-E-'],")
    config_lines.append("        'exclude_patterns': ['Schematic', 'Schedule', 'Detail', 'Section', 'Elevation'],")
    config_lines.append("    },")
    config_lines.append("    ")
    config_lines.append("    'categories': {")
    config_lines.append("        'apartment_layouts': {")
    config_lines.append("            'enabled': True,")
    config_lines.append("            ")
    config_lines.append("            'layout_types': {")
    
    # Add selected categories
    for cat_key in selected_categories:
        cat_data = discovered_categories[cat_key]
        display_name = cat_key.replace('_', ' ').title()
        keywords = cat_data['keywords'][:3]  # Top 3 keywords
        
        config_lines.append(f"                '{cat_key}': {{")
        config_lines.append(f"                    'display_name': '{display_name}',")
        config_lines.append(f"                    'patterns': {keywords},")
        config_lines.append(f"                    'doc_ref_patterns': [],  # Add specific doc ref patterns if needed")
        
        # Mark common categories as required
        required = cat_key in ['ga', 'rcp', 'small_power', 'lighting', 'ventilation']
        config_lines.append(f"                    'required': {required},")
        config_lines.append(f"                    'description': '{display_name} layout'")
        config_lines.append("                },")
    
    config_lines.append("            },")
    config_lines.append("            ")
    config_lines.append("            'apartment_type_detection': {")
    config_lines.append("                'title_patterns': [")
    config_lines.append("                    r'Type\\s+([A-Z][A-Z0-9-]*)',")
    config_lines.append("                    r'APT\\s+TYPE\\s+([A-Z][A-Z0-9-]*)',")
    config_lines.append("                    r'Unit\\s+Type\\s+([A-Z][A-Z0-9-]*)'")
    config_lines.append("                ],")
    config_lines.append("                'doc_ref_patterns': [")
    config_lines.append("                    r'-TYPE-([A-Z][A-Z0-9-]+)-',")
    config_lines.append("                    r'-T([A-Z][A-Z0-9-]+)-'")
    config_lines.append("                ],")
    config_lines.append("                'path_patterns': [")
    config_lines.append("                    r'\\\\Type\\s+([A-Z][A-Z0-9-]+)\\\\',")
    config_lines.append("                    r'\\\\([A-Z][A-Z0-9-]+)\\s+Type\\\\'")
    config_lines.append("                ]")
    config_lines.append("            }")
    config_lines.append("        },")
    config_lines.append("        ")
    config_lines.append("        'communal_layouts': {")
    config_lines.append("            'enabled': False,  # Enable and configure if needed")
    config_lines.append("            'layout_types': {},")
    config_lines.append("            'coverage_detection': {")
    config_lines.append("                'floor_patterns': [")
    config_lines.append("                    r'Level\\s+(\\d+)',")
    config_lines.append("                    r'Floor\\s+(\\d+)',")
    config_lines.append("                    r'Levels?\\s+(\\d+)-(\\d+)'")
    config_lines.append("                ]")
    config_lines.append("            }")
    config_lines.append("        }")
    config_lines.append("    }")
    config_lines.append("}")
    config_lines.append("")
    
    return '\n'.join(config_lines)


def interactive_category_selection(discovered_categories: Dict) -> List[str]:
    """
    Let user interactively select which layout categories to include.
    """
    print(f"\n{'='*80}")
    print("📋 SELECT LAYOUT CATEGORIES TO TRACK")
    print(f"{'='*80}")
    print("Review the discovered categories and select which ones to include in tracking.\n")
    
    categories_sorted = sorted(discovered_categories.items(), key=lambda x: -x[1]['count'])
    
    selected = []
    
    for i, (cat_key, cat_data) in enumerate(categories_sorted, 1):
        print(f"\n{i}. {cat_key.upper()} - {cat_data['count']} documents")
        print(f"   Keywords: {', '.join(cat_data['keywords'][:3])}")
        print(f"   Sample: {cat_data['samples'][0][0][:80]}...")
        
        choice = input(f"   Include this category? (Y/n): ").strip().lower()
        
        if choice != 'n':
            selected.append(cat_key)
            print(f"   ✓ Added {cat_key}")
        else:
            print(f"   ✗ Skipped {cat_key}")
    
    return selected


def update_config_file(project_name: str, config_text: str):
    """
    Add the generated configuration to the project's config file.
    """
    config_file = CONFIGS_DIR / f"{project_name}.py"
    
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return False
    
    # Read existing config
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if APARTMENT_LAYOUT_TRACKING already exists
    if 'APARTMENT_LAYOUT_TRACKING' in content:
        print(f"\n⚠️  APARTMENT_LAYOUT_TRACKING already exists in config file")
        choice = input("   Overwrite existing configuration? (y/N): ").strip().lower()
        if choice != 'y':
            print("   Cancelled - configuration not updated")
            return False
        
        # Remove old config (find and replace the entire block)
        # This is a simple approach - find the start and try to find the closing brace
        start_marker = 'APARTMENT_LAYOUT_TRACKING = {'
        start_idx = content.find(start_marker)
        if start_idx != -1:
            # Find the matching closing brace
            brace_count = 0
            idx = start_idx + len(start_marker) - 1
            while idx < len(content):
                if content[idx] == '{':
                    brace_count += 1
                elif content[idx] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found the end
                        content = content[:start_idx] + content[idx+1:]
                        break
                idx += 1
    
    # Append new config at the end
    content = content.rstrip() + '\n\n' + config_text + '\n'
    
    # Write back
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Configuration added to {config_file}")
    return True


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("🔍 APARTMENT LAYOUT PATTERN DISCOVERY")
    print("="*80)
    print("\nThis tool analyzes your project drawings to automatically discover")
    print("layout patterns and suggests configuration for layout tracking.\n")
    
    # Get available projects
    projects = get_available_projects()
    
    if not projects:
        print("❌ No projects found with accommodation data")
        print("   Run scripts/update_accommodation_data.py first")
        return
    
    print(f"📋 Projects with Accommodation Data ({len(projects)}):")
    print("-" * 80)
    for i, (name, apts, types) in enumerate(projects, 1):
        print(f"  {i}. {name:25} ({apts} apartments, {types} types)")
    print(f"  {len(projects) + 1}. Process ALL projects")
    print("  0. Exit")
    print("-" * 80)
    
    choice = input("\nSelect project (0 to exit): ").strip()
    
    if choice == '0':
        print("\n👋 Exiting...")
        return
    
    try:
        choice_num = int(choice)
        
        if choice_num == len(projects) + 1:
            # Process all projects
            projects_to_process = [p[0] for p in projects]
        elif 1 <= choice_num <= len(projects):
            # Process single project
            projects_to_process = [projects[choice_num - 1][0]]
        else:
            print(f"❌ Invalid choice")
            return
    except ValueError:
        print(f"❌ Invalid input")
        return
    
    # Process each selected project
    for project_name in projects_to_process:
        analysis = analyze_project_layouts(project_name)
        
        if not analysis:
            continue
        
        # Interactive category selection
        selected_categories = interactive_category_selection(analysis['discovered_categories'])
        
        if not selected_categories:
            print(f"\n⚠️  No categories selected - skipping configuration")
            continue
        
        print(f"\n✓ Selected {len(selected_categories)} categories: {', '.join(selected_categories)}")
        
        # Generate configuration
        config_text = generate_layout_config(analysis, selected_categories)
        
        print(f"\n{'='*80}")
        print("📝 GENERATED CONFIGURATION")
        print(f"{'='*80}")
        print(config_text[:500] + "\n... (truncated)\n")
        
        # Ask to save
        choice = input(f"Add this configuration to {project_name} config file? (Y/n): ").strip().lower()
        
        if choice != 'n':
            if update_config_file(project_name, config_text):
                print(f"\n✅ {project_name} configuration updated successfully!")
        else:
            print(f"\n⚠️  Configuration not saved")
        
        print()  # Blank line between projects
    
    print(f"\n{'='*80}")
    print("✅ DISCOVERY COMPLETE")
    print(f"{'='*80}")
    print("\nNext steps:")
    print("  1. Review the generated configurations in your config files")
    print("  2. Adjust patterns if needed based on your project's naming conventions")
    print("  3. Run 'python main.py' and generate Layout Tracking Report")
    print("  4. Review the report and refine patterns as needed")


if __name__ == '__main__':
    main()

