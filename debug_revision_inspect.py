import pandas as pd

filename = 'input/GP File Export 28052025 - All Fields.xlsx'
header_row = 6  # Excel row 7
excel_rows = [1061, 1062, 109, 110]
df_indices = [r - (header_row + 1) for r in excel_rows]

df = pd.read_excel(filename, header=header_row)

print("Inspecting revision values in column F for rows 1061, 1062, 109, 110:")
for excel_row, idx in zip(excel_rows, df_indices):
    val = df.iloc[idx, 5]  # 5 is column F
    print(f"Excel Row {excel_row}: '{val}' | repr: {repr(val)} | ords: {[ord(c) for c in str(val)]}") 