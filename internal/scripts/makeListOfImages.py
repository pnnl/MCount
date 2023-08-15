import numpy as np
import ntpath
import pandas as pd
import os
from pathlib import Path

def listImage (image_dir_counting):
    images = []

    images1 = Path(image_dir_counting).glob('*.tif')
    for i in images1:
        images.append(i)
    images1 = Path(image_dir_counting).glob('*.jpg')
    for i in images1:
        images.append(i)
    images1 = Path(image_dir_counting).glob('*.png')
    for i in images1:
        images.append(i)

    names = []

    for i in images:
        temp = ntpath.abspath(i)
        thingImage = temp.split("\\")
        useThing = thingImage[len(thingImage)-1][0:len(thingImage[len(thingImage)-1])-4]
        
        names.append(useThing)

    return names


