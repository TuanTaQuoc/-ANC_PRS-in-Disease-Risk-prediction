

import pandas as pd

# Load the dataset
file_path = 'DXSUM_PDXCONV_ADNI1_sorted.csv'
df = pd.read_csv(file_path)

# Display column names to verify exact spelling
print("Columns in the dataset:")
print(df.columns.tolist())

# Inspect the first few rows
print("\nFirst 5 rows of the original dataset:")
print(df.head())

# Define the columns to keep
columns_to_keep = ['Phase', 'ID', 'RID', 'PTID', 'EXAMDATE', 'DXCURREN']

# Select columns and create a copy
processed_df = df[columns_to_keep].copy()

# Add Phenotype column
processed_df['Phenotype'] = processed_df['DXCURREN']

# Save the resulting DataFrame
output_file = 'processed_phenotype_data.csv'
processed_df.to_csv(output_file, index=False)

# Show the first 5 rows of the result
# print(processed_df.head())
# Load the previously processed data
df = pd.read_csv('processed_phenotype_data.csv')

# Convert EXAMDATE to datetime for correct sorting
df['EXAMDATE_DT'] = pd.to_datetime(df['EXAMDATE'])

# Sorting:
# 1. RID: group by patient
# 2. Phenotype: descending (highest first)
# 3. EXAMDATE_DT: descending (most recent first)
df_sorted = df.sort_values(by=['RID', 'Phenotype', 'EXAMDATE_DT'], ascending=[True, False, False])

# Drop duplicates keeping only the first row for each RID
df_final = df_sorted.drop_duplicates(subset=['RID'], keep='first')

# Remove the temporary datetime column
df_final = df_final.drop(columns=['EXAMDATE_DT'])

# Save the result
output_file = 'final_patient_phenotypes.csv'
df_final.to_csv(output_file, index=False)

# Display some results to verify
print(f"Original unique RIDs: {df['RID'].nunique()}")
print(f"Final rows (unique RIDs): {len(df_final)}")
print("\nFirst 10 rows of the final dataset:")
print(df_final.head(10))


