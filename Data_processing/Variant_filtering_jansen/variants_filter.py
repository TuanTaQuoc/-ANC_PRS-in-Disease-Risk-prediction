import pandas as pd

def filter_variants(input_file, thresholds):
    # Read the input file
    try:
        data = pd.read_csv(input_file, sep="\t")
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Iterate over thresholds and filter data
    for threshold in thresholds:
        filtered_data = data[data['P'] <= threshold][['SNP', 'P', 'BETA']]
        output_file = f"filtered_variants_p_{threshold}.csv"
        
        # Save the filtered data to a new file
        try:
            filtered_data.to_csv(output_file, index=False)
            print(f"Filtered data saved to {output_file}")
        except Exception as e:
            print(f"Error saving the file {output_file}: {e}")

if __name__ == "__main__":
    input_file = "Jansen_metadata.txt"
    thresholds = [1e-4, 1e-6, 1e-8]
    filter_variants(input_file, thresholds)