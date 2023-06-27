import numpy as np
from PIL import Image
import os
import imageio

ROWS = 2272
COLS = 2485

directory = 'EVI' #source directory

currFile = 0
totalFile = len(os.listdir(directory))
print("Generating Images...")

#This is a 3D array with this order: [ROWS][COLS][DEPTH]
InterpelatedArray = [][][]
depth = 0   #Starting depth


#iterate over files and copy them into the 3D array
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):

        print("File: " + str(currFile) + "/" + str(totalFile))

        #open EVI tif file
        EVI = Image.open(f)
        EVIarray = np.array(EVI)

        #loop through pixels of the image
        for row in range(ROWS):
            for ccol in range(COLS):

                #traverse the rows and colloms and copy them into the new array
                InterpelatedArray[row][cols][depth] = EVIarray[row][cols]

            #used to traverse the EVI files
            currFile += 1

            #used to traverse the 3D array's depth
            depth += 16
            

#Iterate by each pixel and inteperating the DEPTH array
for row in range(ROWS)
    for cols in range(COLS)
        InterpelatedArray[row][cols].interpolate(method ='linear', limit_direction ='both')




