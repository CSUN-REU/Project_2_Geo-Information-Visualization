import numpy as np
import os
import imageio

from PIL import Image
from tifffile import imsave, imread
ROWS = 2277
COLS = 2614
TotalFilesTemp = 320


directory = 'Datasets/EVI' #source directory
itteration = 1
currFile = 1
dirFile = len(os.listdir(directory))
totalFile = len(os.listdir(directory))*16
depth = 0   #Starting depth
day = 1     #The starting day used for naming the files
FileArray = np.zeros((dirFile, ROWS, COLS), int) #Array that stores all of the exsisting EVI Files


print("Generating the Array...")

count = 0
#iterate over files and copy them into the 3D array
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #open EVI tif file & store it in array
        EVI = Image.open(f)
        EVIarray = np.array(EVI)
        FileArray[count] = EVIarray
        print("TIIF Stored: " + str(currFile) + "/" + str(dirFile))
        currFile += 1
    count += 1

currFile = 0

#This is an empty 3D array with this order: [ROWS][COLS][DEPTH]
InterpelatedArray = np.empty((ROWS, COLS, 14))


#Looping though each of the EVI 
for EVI_File in range (len(FileArray)):

    
    #loop through pixels of the image
    for row in range(ROWS):
        #Making sure that I don't go outside the bounds of the index
        if row+1 < len(FileArray)-1:
            EVI1 = FileArray[row]
            EVI2 = FileArray[row+1]
        else:
            break   #If this condition is true it means I have interpelated the last EVI file in the array
        

        for cols in range(COLS):

            #Labeling the elements needed for the interpelation
            y1 = EVI1[row][cols]
            y2 = EVI2[row][cols]
            
            #filling in the interpelation data for one pixel for the 14 days in the 3D array
            for x in range(14):
                InterpelatedArray[row][cols][x]= y1+((x+2)-1)*((y2-y1)/(16-1))
    
    print("Image Interpelation Compleate: " + str(itteration) + " / " + str(dirFile) + " ...Generating Imiges... ")
    itteration += 1

    #Generating Tiff Files  
    for y in range(14):
        level = InterpelatedArray[y]
        saveName = "EVI_Interpelated" + str(day)
        saveLocation = "C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Interpelated/" + str(saveName) + ".tif"
        imageio.imwrite(saveLocation, level)
        im = imread(saveLocation)
        imsave(saveLocation, im)
        day +=1
    day +=1

            

