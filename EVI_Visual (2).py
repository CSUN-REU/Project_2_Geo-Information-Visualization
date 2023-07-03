import numpy as np
from PIL import Image
import os
import imageio

ROWS = 2277
COLS = 2614

directory = 'Datasets\EVI_Interpelated' #source directory

currFile = 0
totalFile = len(os.listdir(directory))
print("Generating Images...")

#iterate over files
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):

        
        print("File: " + str(currFile) + "/" + str(totalFile))

        #create blank image
        im = Image.new(mode="RGB", size=(ROWS, COLS))
        pixels = im.load()

        #open EVI tif file
        EVI = Image.open(f)
        EVIarray = np.array(EVI)

        #loop through pixels
        for r in range(ROWS):
            for c in range(COLS):

                #if EVI is valid, fill value of blank array
                if(EVIarray[r][c] > 0):
                    value = int(((EVIarray[r][c]+2000)/12000)*255)
                    pixels[r,c] = (value,value,value)
                #if invalid, set to white
                else:
                    pixels[r,c] = (255,255,255)

        print(f)
        #transpose image
        im = im.transpose(Image.ROTATE_270)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)

        #write file
        imageio.imwrite("C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Visulized" + f[4:] + ".png", im) 

        currFile += 1


