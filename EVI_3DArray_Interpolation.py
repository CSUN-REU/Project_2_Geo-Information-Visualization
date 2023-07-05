import numpy as np
import os
import imageio
import PIL 
import pandas as pd


from multiprocessing import Pool
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
day = 2     #The starting day used for naming the files
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

#This is an empty 3D array with this order: [File][ROWS][COLS]
InterpelatedArray = np.empty((15, ROWS, COLS))


#Looping though each of the EVI 
for EVI_File in range (len(FileArray)):

    #Marking down the 1st and 2nd EVI Immage that I am interpelating in between
    #Making sure that I don't go outside the bounds of the index
    if EVI_File+1 < len(FileArray)-1:
        EVI1 = FileArray[EVI_File]
        EVI2 = FileArray[EVI_File+1]
    else:
        break   #If this condition is true it means I have interpelated the last EVI file in the array
    
    #loop through pixels of the image
    for row in range(ROWS):

        for cols in range(COLS):

            #Labeling the elements needed for the interpelation
            y1 = EVI1[row][cols]
            y2 = EVI2[row][cols]
            
            #filling in the interpelation data for one pixel for the 14 days in the 3D array
            for x in range(15): 
                #I am multipling the data by 1000 to scale it and not loose the data
                InterpelatedArray[x][row][cols]= int((y1+((x+2)-1)*((y2-y1)/(16-1))) *1000)  
            
                print("Pixel Row: " + str(row) + " Pixel Column: " + str(cols) + " Pixel #: " + str(x) + " / 16")   

    print("Image Interpelation Compleate: " + str(itteration) + " / " + str(dirFile) + " ...Generating Imiges... ")
    itteration += 1

    #Generating Tiff Files Using NpArray 
    for y in range(15):
        #InterpelatedArray = InterpelatedArray.astype(np.uint16)
        Data = Image.fromarray(InterpelatedArray)
        saveName = "EVI_Interpelated" + str(day)
        saveLocation = "C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Interpelated/" + str(saveName) + ".tif"
        Data.save(str(saveLocation), 'TIFF')
        day +=1
    day +=1

            

#Meathod for interpelating 15 imiges between the two file arrays


def interpalateImiges()