import numpy as np
from PIL import Image
import os
import imageio

ROWS = 2272
COLS = 2485
TotalFilesTemp = 320


directory = 'Datasets/EVI' #source directory

currFile = 0
totalFile = len(os.listdir(directory))*16

print("Generating the Array...")

#This is a 3D array with this order: [ROWS][COLS][DEPTH]
InterpelatedArray = np.empty((ROWS, COLS,TotalFilesTemp))
depth = 0   #Starting depth

FileArray = np.zeros(len(os.listdir(directory)))    

#iterate over files and copy them into the 3D array
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print("TIIF Stored: " + str(currFile) + "/" + '231')
        #open EVI tif file
        EVI = Image.open(f)
        FileArray[filename] = EVI

#Looping though each of the EVI 
for EVI_File in range len(FileArray):
    #loop through pixels of the image
    for row in range(ROWS):

        #Making sure that I don't go outside the bounds of the index
        if row+1 < len(FileArray)-1:
            EVI1 = FileArray[row]
            EVI2 = FileArray[row+1] 

        for cols in range(COLS):

            #traverse the rows and colloms and copy them into the new array
            InterpelatedArray[row][cols][depth] = EVIarray[row][cols]
            


#this is used to append 15 empty arrays between the avalible EVI imiges
for tempDepth in range(15):
    #used to traverse the 3D array's depth
    if(depth < TotalFilesTemp-1):
        tempEmptyArray = np.empty((ROWS, COLS, 1, like=InterpelatedArray)
        np.append(InterpelatedArray, tempEmptyArray, axis=2)
        depth += 1

            
print("Interpelating Iniges...")

#Iterpelate by each pixel and by the DEPTH array
for row in range(ROWS):
    for cols in range(COLS):
        InterpelatedArray[row][cols].interpolate(method ='linear', limit_direction ='both')

print("Image Interpelation Compleate... Generating Imiges... ")

currFile = 0
totalFile = len(totalFile = len(os.listdir(directory))) * 16


#Create an image one depth at a time
for depth in range(InterpelatedArray):
    
    print(currFile)
    print("File: " + str(currFile) + "/" + str(totalFile))

    #create blank image
    im = Image.new(mode="RGB", size=(ROWS, COLS))
    pixels = im.load()

    #open EVI tif file
    EVI = Image.open(f)
    EVIarray = np.array(EVI)


    #loop through pixels
    for row in range(ROWS):
        for col in range(COLS):
            #if EVI is valid, fill value of blank array
            if(InterpelatedArray[row][col][depth] > 0):
                value = int(((EVIarray[row][col][depth]+2000)/12000)*255)
                pixels[row,col] = (value,value,value)
            #if invalid, set to white
            else:
                pixels[row,col] = (255,255,255)
    print(f)
    #transpose image
    im = im.transpose(Image.ROTATE_270)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    #write file
    imageio.imwrite(r"C:\Users\denys\Documents\GitHub\Project_2\Datasets\EVI_Interpelated.png") #removed + f[:4]
