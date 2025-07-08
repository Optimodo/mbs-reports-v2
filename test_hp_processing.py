import pandas as pd
from pathlib import Path
import sys
import os

# Add the current directory to the path so we can import from configs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_hp_processing():
    """Test Holloway Park CSV processing"""
    
    print("Testing Holloway Park CSV processing...")
    
    # Import the Holloway Park config
    import configs.HollowayPark as hp_config
    
    # Test CSV file path
    csv_file = Path('input/HP/HP Document Listing 080725.csv')
    
    if not csv_file.exists():
        print(f"CSV file not found: {csv_file}")
        return False
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, **hp_config.CSV_SETTINGS)
        print(f"Successfully read CSV file with {len(df)} rows")
        
        # Test MBS filtering
        if hp_config.MBS_FILTER['enabled']:
            filter_mask = pd.Series([False] * len(df), index=df.index)
            
            for column in hp_config.MBS_FILTER['search_columns']:
                if column in df.columns:
                    case_sensitive = hp_config.MBS_FILTER['case_sensitive']
                    mask = df[column].str.contains('MBS', case=not case_sensitive, na=False)
                    filter_mask = filter_mask | mask
            
            filtered_df = df[filter_mask].copy()
            print(f"MBS filtering: {len(df)} total records -> {len(filtered_df)} MBS records")
            
            # Show some MBS examples
            print("\nSample MBS entries:")
            for idx, row in filtered_df.head(5).iterrows():
                print(f"  {row['Title']} | {row['Status']} | {row['Rev']} | {row['Date']}")
        
        # Test column mappings
        if hp_config.COLUMN_MAPPINGS:
            print(f"\nColumn mappings: {hp_config.COLUMN_MAPPINGS}")
            
            # Apply mappings
            for target_col, source_col in hp_config.COLUMN_MAPPINGS.items():
                if source_col in df.columns:
                    df[target_col] = df[source_col]
                    print(f"  Mapped {source_col} -> {target_col}")
        
        # Test revision cleaning
        if 'Rev' in df.columns:
            df['Rev'] = df['Rev'].apply(hp_config.clean_revision_hp)
            print(f"\nRevision cleaning applied")
            print(f"Unique revisions: {df['Rev'].unique()[:10]}")  # Show first 10
        
        print("\nHolloway Park CSV processing test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing Holloway Park processing: {str(e)}")
        return False

if __name__ == "__main__":
    test_hp_processing() 