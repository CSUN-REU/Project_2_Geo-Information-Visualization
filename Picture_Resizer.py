import numpy as np
import os
import imageio
import PIL 
import pandas as pd


from multiprocessing import Pool
from PIL import Image 
from tifffile import imsave, imread



directory = 'Datasets/EVI' #source directory
day = 1


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #open EVI tif file & store it in array
        EVI = Image.open(f)
        EVI_Resized = EVI.resize((20, 20))
        saveName = "EVI_Interpelated" + str(day)
        saveLocation = "C:/Users/denys/Documents/GitHub/Project_2/Datasets/EVI_Interpelated/" + str(saveName) + ".tif"
        EVI_Resized.save(str(saveLocation), 'TIFF')
        day += 1