import ntpath
import pandas as pd
import os
import urllib.request
from pathlib import Path

def creatCountDirectorySaving (imageList, countName):
    #the follwing will make all the folders to organize the fidderent parts of detection and counting and will skip making the forlder if it already exists 
    cwd = os.getcwd()

    locationForThis = cwd + "\\external\\detections\\"+  countName
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "\\external\\detections\\"+  countName + "\\images"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "\\external\\detections\\"+  countName + "\\images\\segmentation"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "\\external\\detections\\"+  countName + "\\images\\thresholding"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "\\external\\detections\\"+  countName + "\\spreadsheets"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")


    #this creates the main excel sheet
    location = "external\\detections\\"+  countName + "\\spreadsheets"
    musselSheet = pd.ExcelWriter(location + "\\" + 'overall_counts.xlsx', engine='xlsxwriter')

    dfFull = pd.DataFrame({'File Name': imageList, })

    #adds the names of the pictuers in this count set
    dfFull.to_excel(musselSheet, sheet_name='Total', index=False)

    musselSheet.close()