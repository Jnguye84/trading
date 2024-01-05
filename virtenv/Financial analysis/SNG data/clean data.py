import csv

# Input and output file paths
input_file = '/Users/manas/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/output.csv'
output_file = 'outputTemp.csv'

with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        # Assuming the dictionary column is the second column (index 1)
        dictionary_str = row[1].strip()

        # Check if the dictionary is empty
        if dictionary_str == '':
            row[1] = "'{}'"  # Replace empty dictionary with '{}' within quotes
        else:
            # Keeping the original line if the dictionary is not empty
            pass

        writer.writerow(row)

print(f"Processing complete. Result written to {output_file}")
