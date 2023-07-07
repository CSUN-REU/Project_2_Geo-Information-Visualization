import numpy as np
import os
import imageio
import PIL 
import pandas as pd

from multiprocessing import Pool
from PIL import Image 
from tifffile import imsave, imread

# Constants for the source
ROWS = 2272
COLS = 2485

directory = 'Datasets/EVI' #source directory
itteration = 1
currFile = 1
dirFile = len(os.listdir(directory))
FileArray = ["" for x in range(dirFile)] #Array that will store all of the exsisting EVI Files Path FIles But it is empy for now
count = 0


#Meathod for interpelating 15 imiges between the two file arrays
def interpalateImiges(parameterArray):

    #This is an empty 3D array with this order: [File][ROWS][COLS]
    InterpelatedArray = np.empty((15, ROWS, COLS))

    print("Working on files: " + str(parameterArray[0]) + " and " + str(parameterArray[1]))
    
    #open EVI tif file & store the array and the file name
    EVI1 = Image.open(parameterArray[0])
    EVIarray1 = np.array(EVI1)
    EVI2 = Image.open(parameterArray[1])
    EVIarray2 = np.array(EVI2)
    
    #loop through pixels of the image
    for row in range(ROWS):

        for cols in range(COLS):

            #Labeling the elements needed for the interpelation
            y1 = EVIarray1[row][cols]
            y2 = EVIarray2[row][cols]
            
            #filling in the interpelation data for one pixel for the 14 days in the 3D array
            for x in range(len(InterpelatedArray)): 
                #I am multipling the data by 1000 to scale it and not loose the data
                InterpelatedArray[x][row][cols]= int((y1+((x+2)-1)*((y2-y1)/(17-1))) *1000)     


    #Generating Tiff Files Using NpArray 
    pathCounter = 1
    for y in range(15):
        Data = Image.fromarray(InterpelatedArray[y])
        FilePathName = parameterArray[0]
        IntigerIndex = FilePathName.index("doy") + 3
        print(str(IntigerIndex))
        intigerPath = str(int(FilePathName[IntigerIndex:IntigerIndex+7]) + pathCounter)
        print(intigerPath)
        pathCounter += 1
        saveName =  "MOD13A1.061__500m_16_days_EVI_doy" + str(intigerPath) + str(parameterArray[53:])
        saveLocation = "C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Interpelated/" + str(saveName) + ".tif"
        Data.save(str(saveLocation), 'TIFF')
    print("Done with 1 batch of files!")
        


#Set up files and pool
if __name__ == '__main__':

    count = 0
    #iterate over files and copy them into the 3D array
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            FileArray[count] = f
            print("TIIF Stored: " + str(currFile) + "/" + str(dirFile))
            currFile += 1
        count += 1
    currFile = 0

    #storing filePath Names in a tupple to pass as a parameter in the Interpelate Imiges method 
    #and to use to name the output
    print("Creating Parameter Array")

    parameterArray = ["" for x in range(len(FileArray)) ]
    for i in range(len(FileArray)-1):
        EVI1 = FileArray[i]
        EVI2 = FileArray[i+1]
        parameterArray[i] = (EVI1, EVI2)
        print(str(int(EVI1[46:53])+1))
        print(EVI1[53:])
        
    
    print("Generating Images...")

    pool = Pool()                   # Create a multiprocessing Pool
    pool.map(interpalateImiges, parameterArray)  # process files iterable with pool
