import ntpath
import pandas as pd
import os
import urllib.request
from pathlib import Path

def creatCountDirectorySaving (imageList, countName):
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


    
    location = "external\\detections\\"+  countName + "\\spreadsheets"
    musselSheet = pd.ExcelWriter(location + "\\" + 'overall_mussel_counts.xlsx', engine='xlsxwriter')

    dfFull = pd.DataFrame({'File Name': imageList, })

    dfFull.to_excel(musselSheet, sheet_name='Total', index=False)

    musselSheet.close()