import numpy as np
import cv2
import ntpath
import pandas as pd

import os
import styleframe

from PIL import Image

from PIL import Image

from PIL import Image

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
    """
    Created on Wed Jul 28 07:07:59 2023

    @author: nune265

    Alt Method for Counting Object in Image
    Using excel to save values
    Calculates and changes the red thresh layer
    """

    fileNameAry = []
    musselCountAry = []
    blackPxlAry = []

    numPixPerMussle = 143.8

    # iterate over files in that directory
    images = imagess

    print("\n\n========= thresholding beginns")
    print(image_dir_counting)

        
    for image in images:
        print ("\n--------- next picture\n")
        
        print("image: ", image)

        imageUse = ntpath.abspath(image)

        img = cv2.imread(imageUse) #read image

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert to hsv

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
        

        
        gray = cv2.cvtColor(redImage, cv2.COLOR_BGR2GRAY)
        blured = cv2.GaussianBlur(gray,(5,5),0)
        

        ret, thresh = cv2.threshold(blured,1,255,cv2.THRESH_BINARY_INV)
        
        theImgTestAltThresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3, 8)
            
        tempppp = thresh
        
        
        kernel = np.ones((15,15),np.uint8)
        closing = cv2.morphologyEx(tempppp, cv2.MORPH_CLOSE, kernel)
        
        
        negative = cv2.bitwise_not(closing) # OR
        
        kernel = np.ones((15,15),np.uint8)
        closing2 = cv2.morphologyEx(negative, cv2.MORPH_CLOSE, kernel)
        
        regular = cv2.bitwise_not(closing2)
        
        myFinalUse = closing

        #saving all the pictures in individual folders from each step    

        endname = os.path.splitext(os.path.basename(imageUse))[0]

        locationForThis = "external/detections/"+  countName + "/images/thresholding"

        place = locationForThis + "/"+ endname
        print ("file paths of directories made:", place)
        try:
            os.mkdir(ntpath.abspath(place))
        except:
            print("skipped making new directories")
        cv2.imwrite((place+"/1_og.jpg"), img)
        if (image2_buttontest):
            cv2.imwrite((place+"/2_red_image.jpg"), redImage)
        if (image3_buttontest):
            cv2.imwrite((place+"/3_gray.jpg"), gray)
        if (image4_buttontest):
            cv2.imwrite((place+"/4_blurred.jpg"), blured)
        if (image5_buttontest):
            cv2.imwrite((place+"/5_thresh.jpg"), tempppp)
        if (image6_buttontest):
            cv2.imwrite((place+"/6_closing.jpg"), closing)
        cv2.imwrite((place+"/7_my_final_use.jpg"), myFinalUse)
        if (image8_buttontest):
            cv2.imwrite((place+"/extra_the_img_test_alt_thresh.jpg"), theImgTestAltThresh)
        if (image9_buttontest):
            cv2.imwrite((place+"/notUsed_closing2.jpg"), closing2)
            cv2.imwrite((place+"/notUsed_regular.jpg"), regular)
            cv2.imwrite((place+"/notUsed7_negative.jpg"), negative)

        
        
        trans = Image.open(place+"/7_my_final_use.jpg")
        trans.putalpha(75)
        
        layOver = Image.open(place+"/1_og.jpg")
        
        layOver.paste(trans, (0,0), mask=trans)
        layOver = layOver.save(place+"/8_layOver.jpg")

        if (not image1_buttontest):
            os.remove((place+"/1_og.jpg"))
        if (not image7_buttontest):
            os.remove((place+"/7_my_final_use.jpg"))
        
        number_of_white_pix = cv2.countNonZero(myFinalUse)
        number_of_black_pix = np.sum(myFinalUse == 0)
        total = np.sum(myFinalUse)
        
        print ("black pixels: ", number_of_black_pix)
        
        mussel = round(number_of_black_pix/numPixPerMussle)
        
        print ("number of mussels in clumps: ", mussel)

        fileNameAry.append(endname)
        musselCountAry.append(mussel)
        blackPxlAry.append(number_of_black_pix)

    locationForThis = "external/detections/"+  countName + "/spreadsheets"
    countSheet = pd.ExcelWriter(locationForThis + "/" + 'overall_counts.xlsx', mode="a", engine='openpyxl')
    df = pd.DataFrame({'Image': fileNameAry, 'Clump Mussel Count': musselCountAry, 'Black Pixels': blackPxlAry})
    sf = styleframe.StyleFrame(df)
    sf.to_excel(excel_writer=countSheet, best_fit=["Image", "Clump Mussel Count", "Black Pixels"], sheet_name="Thresholding", columns_and_rows_to_freeze='B2', row_to_add_filters=0)
    countSheet.close()


    print ("\n^^^^^^^^^^^^thresholding completed^^^^^^^^^^^^")

    return [musselCountAry, fileNameAry]

