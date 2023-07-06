import pandas as pd
import sys
import numpy as np
import time
from PIL import Image
import os
import imageio
from multiprocessing import Pool
from tifffile import imread, imsave

def interpolate(val1, val2, numValues):
    output = np.zeros(numValues)
    step = (val2 - val1) / (numValues + 1)
    for i in range(numValues):
        output[i] = val1 + (step*(i+1))
    return output


ROWS = 2272
COLS = 2485
numFiles = 25
directory = 'Expanded'

tiffs = np.zeros((numFiles, ROWS, COLS), int)

count = 0
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        im = Image.open(f)
        imarray = np.array(im)
        tiffs[count] = imarray
    count+=1
    if(count == numFiles):
        break
    print(count)


lastData = np.zeros((ROWS,COLS), int)
count = 0
for tif in tiffs:
    for r in range(ROWS):
        for c in range(COLS):
            val = tif[r][c]
            if(val != 0):
                last = lastData[r][c]
                if(last != 0 and last != count - 1):
                    intp = interpolate(tiffs[last][r][c], val, (count-last-1))
                    for i in range(len(intp)):
                        tiffs[last+i+1][r][c] = int(intp[i])
                lastData[r][c] = count
    print(count)
    count += 1


count = 350 #starting file
for tif in tiffs:
    saveLocation = "C:/Users/Connor/Desktop/Data/AppEARS_LST/Interpoalted/InterpolatedLST" + str(count).zfill(4) + ".tif"
    imageio.imwrite(saveLocation, tif)        
    im = imread(saveLocation)
    imsave(saveLocation, im, compress=6)
    count += 1


                
