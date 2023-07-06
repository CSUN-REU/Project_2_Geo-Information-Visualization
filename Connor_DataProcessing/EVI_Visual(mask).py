from multiprocessing import Pool
import random
import sys
import pandas as pd
import sys
import numpy as np
import time
from PIL import Image
import os
import imageio



ROWS = 2272
COLS = 2485

mask = Image.open("mask.tif")
maskarray = np.array(mask)

def process_image(f):
        
    im = Image.new(mode="RGB", size=(ROWS, COLS))
    pixels = im.load()
    EVI = Image.open(f)
    EVIarray = np.array(EVI)

    for r in range(ROWS):
        for c in range(COLS):
            if(EVIarray[r][c] > 0 and maskarray[r][c] > 0):
                value = int(((EVIarray[r][c]+2000)/12000)*350)
                if(value > 256):
                    pixels[r,c] = (0,255,0)
                else:
                    pixels[r,c] = (255-value,value,0)
            else:
                pixels[r,c] = (255,255,255)
                EVIarray[r][c] = -3000
    im = im.transpose(Image.ROTATE_270)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    imageio.imwrite("C:/Users/Connor/Desktop/Data/AppEARS_EVI_BA/EVI/ColorScale(mask)/" + f[4:] + ".png", im) 
    

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

