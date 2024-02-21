#Python script to convert the geospatial data into greyscale PNG images as an input to the Blender software

from multiprocessing import Pool
import random
import sys
import pandas as pd
import sys
import numpy as np
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import imageio



ROWS = 2272
COLS = 2485



def process_image(f):
        
    im = Image.new(mode="RGB", size=(COLS, ROWS))
    pixels = im.load()
    EVI = Image.open(f)
    EVIarray = np.array(EVI)

    for r in range(ROWS):
        for c in range(COLS):
            if(EVIarray[r][c] > 0):
                value = int(((EVIarray[r][c]+2000)/12000)*350)
                if(value > 256):
                    pixels[c,r] = (0,255,0)
                else:
                    pixels[c,r] = (255-value,value,0)
            else:
                pixels[c,r] = (255,255,255)
                EVIarray[r][c] = -3000
    #MOD13A1.061__500m_16_days_EVI_doy2012353_aid0001.tif
    year = f[37:41]
    day = f[41:44]
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 75)
    draw.text((1600, 50), "Year: " + year + ", Day: " + day, font = font, fill=(0, 0, 0))
    imageio.imwrite("C:/Users/Connor/Desktop/Data/AppEARS_EVI_BA/EVI/ColorScale/" + f[4:] + ".png", im) 
    

if __name__ == '__main__':
    directory = 'EVI'
    currFile = 0
    totalFile = len(os.listdir(directory))
    files = []

    print("Getting Files...")
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            files.append(f)

    print("Generating Images...")
    pool = Pool()                         # Create a multiprocessing Pool
    pool.map(process_image, files)  # process data_inputs iterable with pool

