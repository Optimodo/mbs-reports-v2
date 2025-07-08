import pandas as pd
import sys
import os

# Add the current directory to the path so we can import configs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from configs.HollowayPark import map_holloway_park_status

# Create test data with various combinations
test_data = [
    # Status A cases
    {'Status': 'Construction', 'Design Status': ''},
    {'Status': 'Construction', 'Design Status': None},
    {'Status': 'CONSTRUCTION', 'Design Status': ''},
    
    # Status B cases
    {'Status': 'Anything', 'Design Status': 'B'},
    {'Status': 'Construction', 'Design Status': 'B'},
    {'Status': '', 'Design Status': 'B'},
    
    # Status C cases
    {'Status': 'Anything', 'Design Status': 'C'},
    {'Status': 'Construction', 'Design Status': 'C'},
    {'Status': '', 'Design Status': 'C'},
    
    # Preliminary cases
    {'Status': 'Preliminary', 'Design Status': ''},
    {'Status': 'PRELIMINARY', 'Design Status': ''},
    {'Status': 'Preliminary', 'Design Status': None},
    
    # IFC-pending cases (should be Other)
    {'Status': 'IFC-pending', 'Design Status': ''},
    {'Status': 'ifc-pending', 'Design Status': ''},
    {'Status': 'IFC-pending', 'Design Status': None},
    
    # Other cases
    {'Status': 'Information', 'Design Status': ''},
    {'Status': 'Tender', 'Design Status': ''},
    {'Status': '', 'Design Status': ''},
    {'Status': None, 'Design Status': None},
    
    # Design Status takes precedence cases
    {'Status': 'Construction', 'Design Status': 'B'},  # Should be Status B
    {'Status': 'Preliminary', 'Design Status': 'C'},   # Should be Status C
    {'Status': 'IFC-pending', 'Design Status': 'B'},   # Should be Status B
]

# Create DataFrame
df = pd.DataFrame(test_data)

print("Testing Holloway Park Status Mapping")
print("=" * 50)

# Apply status mapping
df['Mapped_Status'] = df.apply(map_holloway_park_status, axis=1)

# Debug: Let's check the first few rows in detail
print("\nDebug - First 3 rows:")
for i in range(3):
    row = df.iloc[i]
    status = row['Status'] if pd.notna(row['Status']) else 'None'
    design_status = row['Design Status'] if pd.notna(row['Design Status']) else 'None'
    mapped = row['Mapped_Status']
    
    print(f"Row {i+1}: Status='{status}' (type: {type(status)}) | Design Status='{design_status}' (type: {type(design_status)}) | Mapped='{mapped}'")
    
    # Test the function directly
    test_row = {'Status': status, 'Design Status': design_status}
    direct_result = map_holloway_park_status(test_row)
    print(f"  Direct test result: '{direct_result}'")

# Display results
for i, row in df.iterrows():
    status = row['Status'] if pd.notna(row['Status']) else 'None'
    design_status = row['Design Status'] if pd.notna(row['Design Status']) else 'None'
    mapped = row['Mapped_Status']
    
    print(f"Row {i+1:2d}: Status='{status:12s}' | Design Status='{design_status:8s}' | Mapped='{mapped}'")

print("\n" + "=" * 50)
print("Summary:")
print(df['Mapped_Status'].value_counts()) 