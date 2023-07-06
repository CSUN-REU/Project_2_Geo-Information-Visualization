import pandas as pd
import sys
import numpy as np
import time
from PIL import Image
import os
import imageio
from multiprocessing import Pool


ROWS = 1137
COLS = 1243

directory = 'MISSINGTA'


def process_image(f):

    from tifffile import imread, imsave

    expand = [[0 for col in range(COLS*2-1)] for row in range(ROWS*2-2)]
    im = Image.open(f)
    imarray = np.array(im)

    for r in range(ROWS-1):
        for c in range(COLS):
            value = imarray[r][c]
            expand[r*2][c*2] = value
            expand[r*2+1][c*2] = value
            if(c != COLS-1):
                expand[r*2][c*2+1] = value
                expand[r*2+1][c*2+1] = value
    saveLocation = "C:/Users/Connor/Desktop/Data/AppEARS_TA/TA/missingexpanded/" + f[13:] + ".tif"
    imageio.imwrite(saveLocation, expand)        
    im = imread(saveLocation)
    imsave(saveLocation, im, compress=6)

if __name__ == '__main__':

    print("Expanding Files...")
    files = []
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            
          files.append(f)

    pool = Pool()
    pool.map(process_image, files)
