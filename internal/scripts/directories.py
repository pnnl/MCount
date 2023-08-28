import ntpath
import pandas as pd
import os
cwd = (os.getcwd()).replace("\\", "/")

detections = cwd + "/external/detections"


def new_detection_directory(imageList, countName):
    # the follwing will make all the folders to organize the different parts of detection and counting and will skip making the folder if it already exists 

    locationForThis = cwd + "/external/detections/"+  countName
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "/external/detections/"+  countName + "/images"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "/external/detections/"+  countName + "/images/segmentation"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "/external/detections/"+  countName + "/images/thresholding"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")

    
    locationForThis = cwd + "/external/detections/"+  countName + "/spreadsheets"
    try:
        os.mkdir(ntpath.abspath(locationForThis))
    except:
        print("skipped")


    # this creates the main excel sheet
    location = cwd + "/external/detections/"+  countName + "/spreadsheets"
    musselSheet = pd.ExcelWriter(location + "/" + 'overall_counts.xlsx', engine='xlsxwriter')

    musselSheet.close()
