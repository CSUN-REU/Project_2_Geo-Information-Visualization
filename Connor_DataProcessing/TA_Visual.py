from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import imageio

#tiff dimensions
ROWS = 2272
COLS = 2485
directory = 'Expanded' #source


#Image processing function (EDIT THIS)
def process_image(f):
    #generate blank image to be edited
    im = Image.new(mode="RGB", size=(COLS, ROWS))
    pixels = im.load()

    #open source tiff file
    TA = Image.open(f)
    TAarray = np.array(TA)

    #assign values to pixels(output) according to source tiff file
    for r in range(ROWS):
        for c in range(COLS):
            val = TAarray[r][c]
            if(val == 3):
                pixels[c,r] = (0,0,255) #water
            elif(val == 4):
                pixels[c,r] = (255,255,255) #cloud
            elif(val == 5): #land
                pixels[c,r] = (0,255,0)
            elif(val >= 7 and val <= 9):
                pixels[c,r] = (255,0,0)
            else:
                pixels[c,r] = (0,0,0) #none

    #Add text
    year = f[30:34]
    day = f[34:37]
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 75)
    draw.text((1600, 50), "Year: " + year + ", Day: " + day, font = font, fill=(255, 255, 255))

    #Write to destination
    imageio.imwrite("C:/Users/Connor/Desktop/Data/AppEARS_TA/TA/ColorScale/" + f[8:] + ".png", im) 
    


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

