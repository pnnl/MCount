import ntpath
import pandas as pd
import os

cwd = (os.getcwd()).replace("\\", "/")

detections = cwd + "/detections"
resources = cwd + "/internal/resources"
dict = cwd + "/internal/resources/modeldict.json"
training = cwd + "/training"
scripts = cwd + "/internal/scripts"
model = cwd + "/internal/model/official_model.pt"

def new_detection_directory(count_name, thresholding):
    # Creates the neccessary directories to organize the different parts of detection and counting and will skip making the directory if it already exists
    
    path = cwd + "/detections"
    try:
        os.mkdir(ntpath.abspath(path))
    except:
        print("skipped /detections")
    
    path = cwd + "/detections/" +  count_name
    try:
        os.mkdir(ntpath.abspath(path))
    except:
        print("skipped /detections/ + count_name")

    
    path = cwd + "/detections/" + count_name + "/images"
    try:
        os.mkdir(ntpath.abspath(path))
    except:
        print("skipped")

    
    path = cwd + "/detections/"+  count_name + "/images/bounding"
    try:
        os.mkdir(ntpath.abspath(path))
    except:
        print("skipped")

    if thresholding:
        path = cwd + "/detections/"+  count_name + "/images/thresholding"
        try:
            os.mkdir(ntpath.abspath(path))
        except:
            print("skipped")

    
    path = cwd + "/detections/"+  count_name + "/spreadsheets"
    try:
        os.mkdir(ntpath.abspath(path))
    except:
        print("skipped")


    # this creates the main excel sheet
    location = cwd + "/detections/"+  count_name + "/spreadsheets"
    musselSheet = pd.ExcelWriter(location + "/" + 'overall_counts.xlsx', engine='xlsxwriter')

    musselSheet.close()

    print("Successfully created detection directories.")

def new_training_directory():
    path = cwd + "/training"
    try:
        os.mkdir(ntpath.abspath(path))
    except:
        print("skipped /training")

    print("Successfully created training directories")