import csv

# Input and output file paths
input_file = '/Users/manas/Documents/GitHub/trading/outputTemp.csv'
output_file = 'companyNames.txt'

with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    companies = []
    for row in reader:
        # Assuming the dictionary column is the second column (index 1)
        dictionary_str = row[1].strip()
        items = dictionary_str.strip('{}').split(', ')
        for i in range(len(items)):
            if 'Inc.' in items[i].split():
                print(items[i-1].strip("'"))
                companies.append(items[i-1].strip("'&#"))
            if 'corporation' in items[i].lower().split():
                print(items[i-1].strip("'"))
                companies.append(items[i-1].strip("'&#"))
    outfile.write(str(companies))

