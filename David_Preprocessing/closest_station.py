import csv
import sys
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
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

def find_nearest_observation(date, latitude, longitude):
    input_file = 'filtered_wind_data.csv'
    min_distance = float('inf')
    nearest_observation = None

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row

        for row in reader:
            obs_date = row[5]
            if obs_date == date:
                obs_lat = float(row[2])
                obs_lon = float(row[3])
                distance = calculate_distance(latitude, longitude, obs_lat, obs_lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_observation = row[6]
    if not nearest_observation:
        return 0
    return nearest_observation

# Usage example
if len(sys.argv) != 4:
    print("Usage: python script.py <date> <latitude> <longitude>")
    sys.exit(1)

input_date = sys.argv[1]
input_latitude = float(sys.argv[2])
input_longitude = float(sys.argv[3])

nearest_wind_observation = find_nearest_observation(input_date, input_latitude, input_longitude)
print(nearest_wind_observation)
