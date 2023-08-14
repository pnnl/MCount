# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 07:07:59 2023

@author: nune265

Alt Method for Counting Object in Image
Using excel to save values
Calculates and changes the red thresh layer
"""


# import important librarys

import numpy as np
import cv2
import math
import ntpath
import pandas as pd

import os

import urllib.request
from PIL import Image
from patchify import patchify

from PIL import Image, ImageDraw, ImageFilter

from PIL import Image, ImageEnhance

import gui
#from gui import image_dir

import config

#import getpixel
#from google.colab.patches import cv2_imshow

# import required module
from pathlib import Path

# get the path/directory
folder_dir = gui.image_dir_counting

#sheet=pd.read_excel("musselCountingTest.xlsx")
countSheet = pd.ExcelWriter('musselCountingTest.xlsx', engine='xlsxwriter')

fileNameAry = []
musselCountAry = []
blackPxlAry = []

numPixPerMussle = 150

# iterate over files in
# that directory
images = Path(folder_dir).glob('*.tif')  


print("\n\n ---------------------------------- ")
print(folder_dir)


