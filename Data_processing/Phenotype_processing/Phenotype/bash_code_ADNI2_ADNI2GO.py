import pandas as pd

# Load the file
df = pd.read_csv('DXSUM_PDXCONV_ADNI2.csv')

# Sort the dataframe by 'RID'
df_sorted = df.sort_values(by='RID')

# Save the sorted dataframe to a new CSV file
df_sorted.to_csv('sorted_DXSUM_PDXCONV_ADNI2.csv', index=False)

# Load the data
df = pd.read_csv('DXSUM_PDXCONV_ADNI2.csv')

# Select only the required columns
# Note: Using EXAMDATE as found in previous inspection
cols_to_keep = ['Phase', 'ID', 'RID', 'PTID', 'EXAMDATE', 'DXCHANGE']
df_filtered = df[cols_to_keep].copy()

# Convert EXAMDATE to datetime for proper sorting
df_filtered['EXAMDATE'] = pd.to_datetime(df_filtered['EXAMDATE'])

# Sort by RID (ascending) and then by EXAMDATE (ascending)
df_sorted_final = df_filtered.sort_values(by=['RID', 'EXAMDATE'])

# Save to a new CSV file
output_file = 'processed_ADNI2_data.csv'
df_sorted_final.to_csv(output_file, index=False)

# Load the previously processed data
df = pd.read_csv('processed_ADNI2_data.csv')

# Define the mapping for DXCHANGE to (before-phenotype, after-phenotype)
# NL = 1, MCI = 2, Dementia = 3
mapping = {
    1: (1, 1), # Stable: NL to NL
    2: (2, 2), # Stable: MCI to MCI
    3: (3, 3), # Stable: Dementia to Dementia
    4: (1, 2), # Conversion: NL to MCI
    5: (2, 3), # Conversion: MCI to Dementia
    6: (1, 3), # Conversion: NL to Dementia
    7: (2, 1), # Reversion: MCI to NL
    8: (3, 2), # Reversion: Dementia to MCI
    9: (3, 1)  # Reversion: Dementia to NL
}

# Function to extract before/after phenotype
def get_before(dx):
    return mapping.get(dx, (None, None))[0]

def get_after(dx):
    return mapping.get(dx, (None, None))[1]

# Apply the mapping
df['before-phenotype'] = df['DXCHANGE'].apply(get_before)
df['after-phenotype'] = df['DXCHANGE'].apply(get_after)

# Save the updated dataframe
output_file = 'phenotype_ADNI2_data.csv'
df.to_csv(output_file, index=False)

# Display the first few rows to verify
print(df.head(15))
print(f"\nUnique DXCHANGE values in data: {df['DXCHANGE'].unique()}")