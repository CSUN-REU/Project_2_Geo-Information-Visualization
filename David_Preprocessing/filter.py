import csv

def filter_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row

        rows_with_observation = []

        for row in reader:
            if len(row) >= 7 and row[6]:  # Check if the 7th column has a non-empty value
                rows_with_observation.append(row)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header row
        writer.writerows(rows_with_observation)

    print("Filtered CSV file created successfully.")

# Usage example
input_file = './all_wind.csv'
output_file = './filtered_wind_data.csv'

filter_csv(input_file, output_file)

