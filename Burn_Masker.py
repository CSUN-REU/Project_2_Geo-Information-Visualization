import pandas as pd
import sys
import numpy as np
import time
from PIL import Image
import os
import imageio

ROWS = 2272
COLS = 2485

directory = 'Burn_Date'
mask = [[0 for col in range(COLS)] for row in range(ROWS)]



currFile = 0
totalFile = len(os.listdir(directory))

print("Generating Mask...")
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):


        print("File: " + str(currFile) + "/" + str(totalFile))
        im = Image.open(f)
        imarray = np.array(im)

        changeCount = 0
        for r in range(ROWS):
            for c in range(COLS):
                if(imarray[r][c] > 0):
                    mask[r][c] = 1;
                    changeCount+=1
        print("Changed: " + str(changeCount) + " pixels")

        currFile += 1

imageio.imwrite("C:/Users/Connor/Desktop/Data/AppEARS_EVI_BA/BA/mask.tif", mask) 

