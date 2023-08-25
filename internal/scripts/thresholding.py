import numpy as np
import cv2
import ntpath
import pandas as pd

import os
import styleframe

from PIL import Image

from PIL import Image

from PIL import Image

from pathlib import Path


def threshFunction (image_dir_counting, countName, imagess,
                    image1_buttontest,
                    image2_buttontest,
                    image3_buttontest,
                    image4_buttontest,
                    image5_buttontest,
                    image6_buttontest,
                    image7_buttontest,
                    image8_buttontest,
                    image9_buttontest):
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

    fileNameAry = []
    musselCountAry = []
    blackPxlAry = []

    numPixPerMussle = 143.8

    # iterate over files in
    # that directory
    images = imagess

    print("\n\n ---------------------------------- ")
    print(image_dir_counting)

        
    for image in images:
        print ("-----------------------------------------------------------")
        
        print(image)

        imageUse = ntpath.abspath(image)

        img = cv2.imread(imageUse) #read image
        #img = cv2.imread("truetest3.png") #read image
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #convert to hsv
        
        #cv2.imwrite((place+"/1_og.jpg"), img)

        # Range for lower red
        lower_red = np.array([0, 65, 0])
        upper_red = np.array([100, 255, 255])
        mask1 = cv2.inRange(hsv_img, lower_red, upper_red)
        
        # Range for upper range
        lower_red = np.array([180,180,190])
        upper_red = np.array([170,155,110])
        mask2 = cv2.inRange(hsv_img,lower_red,upper_red)
        # mask for lower and upper red
        mask = mask1# - mask2

        
        # Get image in red pixel only
        redImage = cv2.bitwise_and(img.copy(), img.copy(), mask = mask)
        ##cv2.imwrite("during files/2_redImage.jpg", redImage)
        

        
        gray = cv2.cvtColor(redImage, cv2.COLOR_BGR2GRAY)
        #cv2.imwrite((place+"/3_gray.jpg"), gray)
        blured = cv2.GaussianBlur(gray,(5,5),0)
        #cv2.imwrite((place+"/4_blured.jpg"), blured)
        

        ret, thresh = cv2.threshold(blured,1,255,cv2.THRESH_BINARY_INV)#+cv2.THRESH_OTSU)
        
        theImgTestAltThresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3, 8)
            
        #tempppp = cv2.bitwise_not(thresh)
        tempppp = thresh
        #cv2.imwrite((place+"/5_thresh.jpg"), temp)
        
        
        kernel = np.ones((15,15),np.uint8)
        closing = cv2.morphologyEx(tempppp, cv2.MORPH_CLOSE, kernel)
        #cv2.imwrite((place+"/6_closing.jpg"), closing)
        
        #cv2.imwrite("temp.jpg", closing)
        
        
        negative = cv2.bitwise_not(closing) # OR
        #cv2.imwrite((place+"/7_negative.jpg"), negative)
        
        kernel = np.ones((15,15),np.uint8)
        closing2 = cv2.morphologyEx(negative, cv2.MORPH_CLOSE, kernel)
        
        regular = cv2.bitwise_not(closing2)
        
        myFinalUse = closing

        #saving all the pictures in individual folders from each step    

        thingImage = imageUse.split("\\")
        useThing = thingImage[len(thingImage)-1][0:len(thingImage[len(thingImage)-1])-4]
        
        locationForThis = "external\\detections\\"+  countName + "\\images\\thresholding"

        place = locationForThis + "\\"+ useThing
        print (place)
        try:
            os.mkdir(ntpath.abspath(place))
        except:
            print("skiped")
        #os.replace(ntpath.abspath(place))
        cv2.imwrite((place+"/1_og.jpg"), img)
        if (image2_buttontest):
            cv2.imwrite((place+"/2_redImage.jpg"), redImage)
        if (image3_buttontest):
            cv2.imwrite((place+"/3_gray.jpg"), gray)
        if (image4_buttontest):
            cv2.imwrite((place+"/4_blured.jpg"), blured)
        if (image5_buttontest):
            cv2.imwrite((place+"/5_thresh.jpg"), tempppp)
        if (image6_buttontest):
            cv2.imwrite((place+"/6_closing.jpg"), closing)
        cv2.imwrite((place+"/7_myFinalUse.jpg"), myFinalUse)
        if (image8_buttontest):
            cv2.imwrite((place+"/extra_theImgTestAltThresh.jpg"), theImgTestAltThresh)
        if (image9_buttontest):
            cv2.imwrite((place+"/notUsed_closing2.jpg"), closing2)
            cv2.imwrite((place+"/notUsed_regular.jpg"), regular)
            cv2.imwrite((place+"/notUsed7_negative.jpg"), negative)

        
        
        trans = Image.open(place+"/7_myFinalUse.jpg")
        trans.putalpha(75)
        
        layOver = Image.open(place+"/1_og.jpg")
        
        layOver.paste(trans, (0,0), mask=trans)
        
        #cv2.imwrite("during files/9_layerOver.jpg", layOver)
        
        #layOver.show()
        
        layOver = layOver.save(place+"/8_layOver.jpg")

        if (not image1_buttontest):
            os.remove((place+"/1_og.jpg"))
        if (not image7_buttontest):
            os.remove((place+"/7_myFinalUse.jpg"))
        
        number_of_white_pix = cv2.countNonZero(myFinalUse)
        number_of_black_pix = np.sum(myFinalUse == 0)
        total = np.sum(myFinalUse)
        
        
        print ("white pixles: ", number_of_white_pix)
        print ("black pixles: ", number_of_black_pix)
        
        mussel = round(number_of_black_pix/numPixPerMussle)
        
        print ("Number of Mussels in clumps: ", mussel)
        
        print ("done")
        
        print("\n\n\n\n\n\ntotal (added): ", number_of_white_pix+number_of_black_pix)
        print("the toal number of pixels in a picture of a coupon is 2170 * 2170 = 4708900")
        
        print("total (actual): nvm not true", total)
        
        fileNameAry.append(useThing)
        musselCountAry.append(mussel)
        blackPxlAry.append(number_of_black_pix)

    locationForThis = "external\\detections\\"+  countName + "\\spreadsheets"
    countSheet = pd.ExcelWriter(locationForThis + "\\" + 'overall_counts.xlsx', mode="a", engine='openpyxl')
    df = pd.DataFrame({'File Name': fileNameAry, 'Clump Mussel Count': musselCountAry, 'Black Pixels': blackPxlAry})
    sf = styleframe.StyleFrame(df)
    sf.to_excel(excel_writer=countSheet, best_fit=["File Name", "Clump Mussel Count", "Black Pixels"], sheet_name="Thresholding", columns_and_rows_to_freeze='B2', row_to_add_filters=0)
    countSheet.close()


    print ("\ndone done done")

    return [musselCountAry, fileNameAry]

