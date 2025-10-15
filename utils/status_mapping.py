"""Status mapping utilities for project-specific status categorization."""


def get_status_category(status_value, config):
    """Get the status category for a given status value based on project config.
    
    Args:
        status_value: The actual status value from the data
        config: Project configuration dictionary containing STATUS_MAPPINGS
        
    Returns:
        str: The category name (e.g., 'Status A', 'Status B') or None if not found
    """
    if not config or 'STATUS_MAPPINGS' not in config:
        return None
    
    status_mappings = config['STATUS_MAPPINGS']
    
    # Search through all categories to find which one contains this status
    for category, mapping_info in status_mappings.items():
        if status_value in mapping_info.get('statuses', []):
            return category
    
    return None


def get_status_color(category, config):
    """Get the color for a status category.
    
    Args:
        category: The status category name (e.g., 'Status A')
        config: Project configuration dictionary containing STATUS_MAPPINGS
        
    Returns:
        str: Hex color code or None if not found
    """
    if not config or 'STATUS_MAPPINGS' not in config:
        return None
    
    status_mappings = config['STATUS_MAPPINGS']
    
    if category in status_mappings:
        return status_mappings[category].get('color')
    
    return None


def get_status_display_name(category, config):
    """Get the display name for a status category.
    
    Args:
        category: The status category name (e.g., 'Status A')
        config: Project configuration dictionary containing STATUS_MAPPINGS
        
    Returns:
        str: Display name or the category itself if not found
    """
    if not config or 'STATUS_MAPPINGS' not in config:
        return category
    
    status_mappings = config['STATUS_MAPPINGS']
    
    if category in status_mappings:
        return status_mappings[category].get('display_name', category)
    
    return category


def get_grouped_status_counts(df, config):
    """Group status counts by category according to project's STATUS_MAPPINGS.
    
    Args:
        df: DataFrame containing document data with 'Status' column
        config: Project configuration dictionary containing STATUS_MAPPINGS
        
    Returns:
        dict: Dictionary mapping category names to counts
    """
    if not config or 'STATUS_MAPPINGS' not in config:
        # Fallback to raw status counts if no mappings defined
        return df['Status'].value_counts().to_dict()
    
    # Get actual status counts from data
    status_counts = df['Status'].value_counts()
    
    # Initialize category counts
    grouped_counts = {}
    status_mappings = config['STATUS_MAPPINGS']
    
    for category in status_mappings.keys():
        grouped_counts[category] = 0
    
    # Map each status to its category and sum counts
    for status_value, count in status_counts.items():
        category = get_status_category(status_value, config)
        if category:
            grouped_counts[category] += count
        else:
            # If status not mapped, add to "Other" if it exists, otherwise track separately
            if 'Other' in grouped_counts:
                grouped_counts['Other'] += count
            else:
                # Create unmapped category if Other doesn't exist
                if 'Unmapped' not in grouped_counts:
                    grouped_counts['Unmapped'] = 0
                grouped_counts['Unmapped'] += count
    
    # Remove categories with zero counts for cleaner output
    grouped_counts = {k: v for k, v in grouped_counts.items() if v > 0}
    
    return grouped_counts


def get_status_display_order(config):
    """Get the display order for status categories.
    
    Args:
        config: Project configuration dictionary containing STATUS_DISPLAY_ORDER
        
    Returns:
        list: Ordered list of status category names
    """
    if not config:
        return []
    
    # Return the configured display order, or default to STATUS_MAPPINGS keys order
    if 'STATUS_DISPLAY_ORDER' in config:
        return config['STATUS_DISPLAY_ORDER']
    elif 'STATUS_MAPPINGS' in config:
        return list(config['STATUS_MAPPINGS'].keys())
    
    return []

