import csv
import numpy as np
import gzip
import shutil
import os
from PIL import Image
from datetime import datetime, timedelta
from multiprocessing import Pool
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Earth radius in kilometers
    earth_radius = 6371.0

    # Calculate the differences in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Haversine formula for distance calculation
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

# Size of tif files
rows = 2272
cols = 2485

# Latitude and longitude boundaries of California
north_bound = 41.99498
south_bound = 32.52990
west_bound = -124.47917
east_bound = -114.13149
# Difference between each row and col
col_diff = abs(west_bound - east_bound) / cols
row_diff = abs(north_bound - south_bound) / rows

def create_csv(current_date):

    ca_image = Image.open('MOD13A1.061__500m_16_days_EVI_doy2013017_aid0001.tif')
    ca = np.array(ca_image)

    # current_date = datetime.strptime(date_string, "%Y-%m-%d")

    # Generate the CSV filename based on the current date
    filename = str(current_date) + ".csv"
    path = '/home/davidjcastrejon/wind/wind_observations/' + filename
    nearest_observation = None
    # Write data to the CSV file
    with open(path, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over each pixel
        for r in range(rows):
            # print('Row: ' + str(r))
            for c in range(cols):

                lat1 = north_bound - row_diff * r
                lat2 = north_bound - (row_diff * (r + 1))
                lon1 = west_bound + col_diff * c
                lon2 = west_bound + (col_diff * (c + 1))
                # print(lat1, lon1)
                # ca_lon = ((west_bound + (c * col_diff)) + (west_bound + ((c + 1) * col_diff))) / 2
                # ca_lat = ((north_bound - (r * row_diff)) + (north_bound - ((r + 1) * row_diff))) / 2

                if ca[r][c] < 0:
                    row_data = [r, c, 0]
                    writer.writerow(row_data)

                else:
                    # Read .csv for day to calculate closest measurement per pixel
                    with open('sorted_wind/' + str(current_date) + '.csv', 'r') as file:
                        reader = csv.reader(file)
                        header = next(reader)
                        min_distance = 10000

                        for row in reader:
                            obs_lat = float(row[2])
                            obs_lon = float(row[3])
                            ca_lon = ((west_bound + (c * col_diff)) + (west_bound + ((c + 1) * col_diff))) / 2
                            ca_lat = ((north_bound - (r * row_diff)) + (north_bound - ((r + 1) * row_diff))) / 2
                            # print(lat1, lon1, ca_lat, ca_lon)
                            distance = calculate_distance(ca_lat, ca_lon, obs_lat, obs_lon)
                            if distance < min_distance:
                                min_distance = distance
                                nearest_observation = row[6]

                    row_data = [r, c, nearest_observation]
                    writer.writerow(row_data)
    # current_date += timedelta(days=1)
    input_file = path
    output_file = path + '.gz'
    with open(input_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    os.remove(input_file)



dates_set = set()

for year in range(2019, 2023):
    for month in range(1, 13):
        for day in range(1, 32):
            # Check if the date is valid
            if month in [4, 6, 9, 11] and day > 30:
                continue
            elif month == 2:
                if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                    if day > 29:
                        continue
                elif day > 28:
                    continue
            elif day > 31:
                continue

            # Format the date as 'YYYY-MM-DD' and add it to the set
            date = f"{year}-{month:02d}-{day:02d}"
            dates_set.add(date)

# Print the set of dates
# for date in dates_set:
#     print(date)



if __name__ == '__main__':
    print(dates_set)
    pool = Pool()
    pool.map(create_csv, dates_set)
