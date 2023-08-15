import ntpath
import pandas as pd
import os
import urllib.request
from pathlib import Path

def creatCountDirectorySaving (countName):
    locationForThis = "external\\detections\\"+  countName
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skiped")

    
    locationForThis = "external\\detections\\"+  countName + "\\images"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skiped")

    
    locationForThis = "external\\detections\\"+  countName + "\\images\\segmentation"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skiped")

    
    locationForThis = "external\\detections\\"+  countName + "\\images\\thresholding"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skiped")

    
    locationForThis = "external\\detections\\"+  countName + "\\spreadsheets"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skiped")

