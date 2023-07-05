from multiprocessing import Pool
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import imageio

#tiff dimensions
ROWS = 2272
COLS = 2485
directory = 'Datasets\EVI_Interpelated' #source


#Image processing function (EDIT THIS)
def process_image(f):

    #generate blank image to be edited
    im = Image.new(mode="RGB", size=(COLS, ROWS))
    pixels = im.load()

    #open source tiff file
    EVI = Image.open(f)
    EVIarray = np.array(EVI)

    #assign values to pixels(output) according to source tiff file
    for r in range(ROWS):
        for c in range(COLS):
            if(EVIarray[r][c] > 0):
                value = int((( (EVIarray[r][c])/1000+2000)/12000)*255)
                if(value > 256):
                    pixels[c,r] = (255,255,255)
                else:
                    pixels[c,r] = (value,value,value)
            else:
                pixels[c,r] = (255,0,0)

    #Write to destination
    imageio.imwrite("Datasets/EVI_Visulized/" + str(random.random()) + ".png", im) 
    print("Done!")
    


#Set up files and pool
if __name__ == '__main__':
    currFile = 0
    totalFile = len(os.listdir(directory))
    files = []

    print("Getting Files...")
    # iterate over files in source dir
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            #add files to array
            files.append(f)

    print("Generating Images...")
    pool = Pool()                   # Create a multiprocessing Pool
    pool.map(process_image, files)  # process files iterable with pool

