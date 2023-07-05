import numpy as np
import os
import imageio
import PIL 
import pandas as pd
from PIL import Image 
from tifffile import imsave, imread

ROWS = 2272
COLS = 2485
TotalFilesTemp = 320

directory = 'Datasets/EVI' #source directory
itteration = 1
currFile = 1
dirFile = len(os.listdir(directory))
totalFile = len(os.listdir(directory))*16
depth = 0   #Starting depth
day = 2     #The starting day used for naming the files
FileArray = np.zeros((dirFile, ROWS * COLS), int) #Array that stores all of the exsisting EVI Files


print("Generating the Array...")

count = 0
#iterate over files and copy them into the 3D array
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #open EVI tif file & store it in array
        EVI = Image.open(f)
        EVIarray = np.array(EVI)
        EVIarray = EVIarray.flatten()  #This flattens the EVI Arrays
        FileArray[count] = EVIarray
        print("TIIF Stored: " + str(currFile) + "/" + str(dirFile))
        currFile += 1
    count += 1

currFile = 0

#This is an empty 3D array with this order: [File][ROWS][COLS]
InterpelatedArray = np.empty((16, ROWS * COLS), dtype='int')


#Looping though each of the EVI 
for EVI_File in range (len(FileArray)):

    #Marking down the 1st and 2nd EVI Immage that I am interpelating in between
    #Making sure that I don't go outside the bounds of the index
    if EVI_File+1 < len(FileArray)-1:

        # This Assigns the EVI Array to the first and last element of the Interpelation Array
        # to use for interpelation 
        # print(FileArray.dtype())
        InterpelatedArray[0] = FileArray[EVI_File]
        InterpelatedArray[15] = FileArray[EVI_File+1]
        
    else:
        break   #If this condition is true it means I have interpelated the last EVI file in the array
    
    #Turn InterpalatedArray from np array to pd database for interpelation to work
    PandasInterpelatedArray = pd.DataFrame(InterpelatedArray)

    #testing the data in the PandasInterpelatedArray
    
    

    PandasInterpelatedArray.interpolate(method ='linear', limit_direction ='both')
    print("EVI Interpelated: " + str(EVI_File) + "/" + str((len(FileArray))) )
    print(PandasInterpelatedArray)

    start = 1   #this is where I start to reshape the arrays 
    #Generating Tiff Files Using NpArray 
    while start < len(InterpelatedArray)-2:
        np.reshape(InterpelatedArray[start], (COLS, ROWS))
        Data = Image.fromarray(InterpelatedArray[start])
        saveName = "EVI_Interpelated" + str(day)
        saveLocation = "C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Interpelated/" + str(saveName) + ".png"
        Data.save(str(saveLocation), 'TIFF')
        start += 1
        day +=1
    day +=1

            

