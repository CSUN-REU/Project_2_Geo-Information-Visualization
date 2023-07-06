import csv
from datetime import date, timedelta
import math
import numpy
from PIL import Image, ImageDraw, ImageFont
import os
import imageio
from multiprocessing import Pool
import random
import pandas

start_date = date(2013,1,1)
end_date = date(2022,12,31)
total_days = (end_date-start_date).days

west_long = -124.479171862164
east_long = -114.13149647518
north_lat = 41.9949864769535
south_lat = 32.5299007372903

rows = 2272
cols = 2485

def RC_to_LL(r,c):
    long = ((east_long - west_long)/cols)*c + west_long
    lat = ((south_lat - north_lat)/rows)*r + north_lat
    return long, lat

def getMaskCoords():
    im = Image.open('mask.tif')
    imarray = numpy.array(im)
    coords = []
    print(imarray.shape)
    for r in range(len(imarray)):
        for c in range(len(imarray[0])):
            if(imarray[r][c] == 1):
                coords.append((r,c))
    return coords
            

def getFiles():
    directory = 'TA'
    TA = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            TA.append(f)

    directory = 'LST'
    LST = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            LST.append(f)

    directory = 'Fire'
    Fire = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            Fire.append(f)
            
    return TA, LST, Fire
    
def writeFile():
    # field names 
    fields = ['Date', 'Longitude', 'Latitude', 'EVI', 'TA', 'LST', 'Wind', 'Fire'] 
    
    # name of csv file 
    filename = "data.csv"

    coords = getMaskCoords()
    coordlen = len(coords)

    TA, LST, Fire = getFiles()

    # writing to csv file 
    with open(filename, 'w', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields)

        
        for day in range(total_days):
            print(day)
            TAarray = numpy.array(Image.open(TA[day]))
            LSTarray = numpy.array(Image.open(LST[day]))
            FirePix = Image.open(Fire[day]).load()
            
            date = start_date + timedelta(days = day)
            data = [[date] for i in range(coordlen)]
            
            for i in range(coordlen):
                r = coords[i][0]
                c = coords[i][1]
                long, lat = RC_to_LL(r, c)
                data[i].append(long)
                data[i].append(lat)
                data[i].append(-9999)
                data[i].append(TAarray[r][c])
                data[i].append(LSTarray[r][c])
                data[i].append(-9999)
                if(FirePix[c,r] != (255,0,0)):
                    data[i].append(0)
                else:
                    data[i].append(1)
        
            # writing the data rows 
            csvwriter.writerows(data)

            if(day == 10):
                break
            
    df = pandas.read_csv('data.csv')
    df.to_csv("compressed.csv", compression = 'gzip')
    
writeFile()
