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

from pathlib import Path


def threshFunction (image_dir_counting):
    # -*- coding: utf-8 -*-
    """
    Created on Wed Jul 28 07:07:59 2023

    @author: nune265

    Alt Method for Counting Object in Image
    Using excel to save values
    Calculates and changes the red thresh layer
    """


    # import important librarys

    

    #import gui
    #from gui import image_dir

    #import config

    #import getpixel
    #from google.colab.patches import cv2_imshow

    # import required module

    # get the path/directory

    #sheet=pd.read_excel("musselCountingTest.xlsx")
    countSheet = pd.ExcelWriter('musselCountingTest.xlsx', engine='xlsxwriter')

    fileNameAry = []
    musselCountAry = []
    blackPxlAry = []

    numPixPerMussle = 150

    # iterate over files in
    # that directory
    images = Path(image_dir_counting).glob('*.tif')  


    print("\n\n ---------------------------------- ")
    print(image_dir_counting)



