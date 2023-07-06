from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import imageio

#tiff dimensions
ROWS = 2272
COLS = 2485
directory = 'Interpoalted' #source

upper = 9000
lower = 6000



#Image processing function (EDIT THIS)
def process_image(f):
    #generate blank image to be edited
    im = Image.new(mode="RGB", size=(COLS, ROWS))
    pixels = im.load()

    #open source tiff file
    LST = Image.open(f)
    LSTarray = np.array(LST)

    #assign values to pixels(output) according to source tiff file
    for r in range(ROWS):
        for c in range(COLS):
            val = (LSTarray[r][c]-7500)
            if(val < lower and val > 0):
                val = 0
            elif(val > upper):
                val = 255
            else:
                val = int(((val-lower)/(upper-lower)) * 255)
            if(val >= 0):
                pixels[c,r] = (val,0,255-val)
            else:
                pixels[c,r] = (0,0,0)

    #Add text
    year = f[36:40]
    day = f[40:43]
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 75)
    draw.text((1600, 50), "Year: " + year + ", Day: " + day, font = font, fill=(255, 255, 255))

    #Write to destination
    imageio.imwrite("C:/Users/Connor/Desktop/Data/AppEARS_LST/ColorInter/" + f[13:] + ".png", im) 
    


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

    
