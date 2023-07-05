import numpy as np
import os
import imageio
import PIL 
import pandas as pd


from multiprocessing import Pool
from PIL import Image 
from tifffile import imsave, imread

ROWS = 2272
COLS = 2485



directory = 'Datasets/EVI' #source directory
itteration = 1
currFile = 1
dirFile = len(os.listdir(directory))
totalFile = len(os.listdir(directory))*16
depth = 0   #Starting depth
day = 1     #The starting day used for naming the files
FileArray = np.zeros((dirFile, ROWS, COLS), int) #Array that stores all of the exsisting EVI Files




count = 0
#iterate over files and copy them into the 3D array
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #open EVI tif file & store it in array
        EVI = Image.open(f)
        EVIarray = np.array(EVI)
        FileArray[count] = EVIarray
        
        
    count += 1

currFile = 0

#This is an empty 3D array with this order: [File][ROWS][COLS]
InterpelatedArray = np.empty((15, ROWS, COLS))


#Looping though each of the EVI 
for EVI_File in range (len(FileArray)):

    print("Working on file: " + str(EVI_File))
    #Marking down the 1st and 2nd EVI Immage that I am interpelating in between
    #Making sure that I don't go outside the bounds of the index
    if EVI_File+1 < len(FileArray):
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
                
                #print(str(InterpelatedArray[x][row][cols]))
                #print("Pixel Row: " + str(row) + " Pixel Column: " + str(cols) + " Pixel #: " + str(x) + " / 16")   

    #print(InterpelatedArray[EVI_File])

    print("Image Interpelation Compleate: " + str(itteration) + " / " + str(dirFile-1) + " ...Generating Imiges... ")
    itteration += 1

    #Generating Tiff Files Using NpArray 
    for y in range(14):
        #InterpelatedArray = InterpelatedArray.astype(np.uint16)
        day +=1
        Data = Image.fromarray(InterpelatedArray[y])
        saveName = "EVI_Interpelated" + str(day)
        saveLocation = "C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Interpelated/" + str(saveName) + ".tif"
        Data.save(str(saveLocation), 'TIFF')
        
    day += 1


#Meathod for interpelating 15 imiges between the two file arrays
def interpalateImiges(f):
    f


#Set up files and pool
if __name__ == '__main__':
    currFile = 0
    totalFile = len(os.listdir(directory))
    files = []

    print("Generating the Array...")
    # iterate over files in source dir
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            #add files to array
            files.append(f)
            print("TIIF Stored: " + str(currFile) + "/" + str(dirFile))
            currFile += 1
        

    print("Generating Images...")
    pool = Pool()                   # Create a multiprocessing Pool
    pool.map(interpalateImiges, files)  # process files iterable with pool