import csv
from datetime import date, timedelta
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import imageio
from multiprocessing import Pool


start_date = date(2013,1,1)
end_date = date(2022,12,31)
total_days = (end_date-start_date).days

west_long = -124.479171862164
east_long = -114.13149647518
north_lat = 41.9949864769535
south_lat = 32.5299007372903

rows = 2272
cols = 2485

data_file = "mapdataall.csv"

def date_to_num(d):
    year = int(d[:d.index("-")])
    d = d[d.index("-")+1:]
    month = int(d[:d.index("-")])
    day = int(d[d.index("-")+1:])
    return (date(year,month,day)-start_date).days


def LL_to_RC(long, lat):
    long_diff = east_long - west_long
    long_step = long_diff / cols
    col = int((float(long) - west_long)/long_step)

    lat_diff = south_lat - north_lat
    lat_step = lat_diff / rows
    row = int((float(lat) - north_lat)/lat_step)
    return row, col

def extract_data(csv_file):

    fire_data = {
        "date": [],
        "coord": [],
        "area": []
    }
    with open(csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            try:
                acres = int(row["incident_acres_burned"])
            except:
                acres = 0
            r, c = LL_to_RC(row["incident_longitude"], row["incident_latitude"])
            fire_data["date"].append(date_to_num(row["incident_dateonly_created"]))
            fire_data["area"].append(acres)
            fire_data["coord"].append((r,c))
            
            line_count += 1
        print(f'Processed {line_count} lines.')
    return fire_data

#takes in area in acres, draws in km
def draw_circle(tifs, area, coord):
    area = area * 0.0040468564224 #in km
    radius = math.sqrt(area/math.pi) * 2 #in pixel lengths (500m)
    args = []
    for tif in tifs:
        args.append((tif,radius,coord))
    pool = Pool()
    output = pool.starmap(parallel_draw, args)
    return output

def parallel_draw(tif, radius, coord):
    pixels = tif.load()
    for r in range(rows):
        for c in range(cols):
            dist = math.sqrt((coord[0] - r)**2 + (coord[1]-c)**2)
            if(dist <= radius and pixels[c,r] != (255,255,255)):
                pixels[c,r] = (255,0,0)
    return tif


def generate_visual():
    
    directory = "fire_visual"
    leading_days = 30
    tifs = []
    fire_data = extract_data(data_file)
    print(fire_data)
    finished_files = 0
    for i in range(total_days):
        im = Image.open("grass.png")
        tifs.append(im)
        while(fire_data["date"].count(i) > 0):
            index = fire_data["date"].index(i)
            print(str(fire_data["area"][index]) + " " + str(fire_data["date"][index]))
            tifs = draw_circle(tifs, fire_data["area"][index], fire_data["coord"][index])
            del fire_data["date"][index]
            del fire_data["area"][index]
            del fire_data["coord"][index]
        if(len(tifs) > leading_days):
            cur_date = start_date + timedelta(days=finished_files)
            draw = ImageDraw.Draw(tifs[0])
            font = ImageFont.truetype("arial.ttf", 75)
            draw.text((1600, 50), str(cur_date), font = font, fill=(255, 255, 255))
            imageio.imwrite("C:/Users/Connor/Desktop/Data/CALFIRE_INCIDENTS/output" + str(finished_files) + ".png", tifs[0])
            del tifs[0]
            finished_files += 1
    for tif in tifs:
        imageio.imwrite("C:/Users/Connor/Desktop/Data/CALFIRE_INCIDENTS/output" + str(finished_files) + ".png", tif)
        finished_files += 1

if __name__ == '__main__':
    generate_visual()
        

