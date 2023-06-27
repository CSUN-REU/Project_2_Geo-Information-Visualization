import numpy as np
from PIL import Image
import os
import imageio

ROWS = 2272
COLS = 2485

directory = 'Datasets/EVI' #source directory

currFile = 0
totalFile = len(os.listdir(directory))
print("Intepelating Imiges...")

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

print("Image Interpelation Compleate... Generating Imiges... ")

currFile = 0
totalFile = len(totalFile = len(os.listdir(directory))) * 16


#Create an image one depth at a time
for depth in range(InterpelatedArray)

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
            if(InterpelatedArray[row][ccol][depth] > 0):
                value = int(((EVIarray[row][col][depth]+2000)/12000)*255)
                pixels[r,c] = (value,value,value)
            #if invalid, set to white
            else:
                pixels[r,c] = (255,255,255)
    print(f)
    #transpose image
    im = im.transpose(Image.ROTATE_270)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    #write file
    imageio.imwrite("C:\Users\denys\Documents\GitHub\Project_2\Datasets\EVI_Interpelated" + ".png", im)     #removed + f[:4]
