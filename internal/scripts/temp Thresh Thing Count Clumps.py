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



#import getpixel
#from google.colab.patches import cv2_imshow

# import required module
from pathlib import Path

# get the path/directory
folder_dir = 'raw tif img'

#sheet=pd.read_excel("musselCountingTest.xlsx")
countSheet = pd.ExcelWriter('musselCountingTest3.xlsx', engine='xlsxwriter')

fileNameAry = []
musselCountAry = []
blackPxlAry = []

numPixPerMussle = 150

# iterate over files in
# that directory
images = Path(folder_dir).glob('*.tif')
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
    
    
    kernel = np.ones((8,8),np.uint8)
    closing = cv2.morphologyEx(tempppp, cv2.MORPH_CLOSE, kernel)
    #cv2.imwrite((place+"/6_closing.jpg"), closing)
    
    #cv2.imwrite("temp.jpg", closing)
    
    
    negative = cv2.bitwise_not(closing) # OR
    #cv2.imwrite((place+"/7_negative.jpg"), negative)
    
    kernel = np.ones((15,15),np.uint8)
    closing2 = cv2.morphologyEx(negative, cv2.MORPH_CLOSE, kernel)
    
    regular = cv2.bitwise_not(closing2)
    
    
    #atempt #1
    """
    
    removeSoloPatch = closing
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closing, connectivity=8)

    areas = stats[:, cv2.CC_STAT_AREA]
    
    # Set your desired threshold here (you may need to adjust this value)
    threshold_area = 10000
    small_patch_indices = areas < threshold_area
    
    
    #print (removeSoloPatch.dtype)
    
    new_color = (0, 255, 255)  # (B, G, R)
    #new_color_array = np.array(new_color, dtype=removeSoloPatch.dtype)

    print(removeSoloPatch.ndim)
    
    
    #img_arr = negative
    #print(img_arr)


    
    for label in range(1, num_labels):  # Start from 1 to ignore the background label
        if small_patch_indices[label]:
            mask = labels == label
            coordinates = np.argwhere(mask)
            for coord in coordinates:
                x, y = coord
                removeSoloPatch[x][y] = 0

    """
    
    #attempt #2
    """
    
    totalChange = 0
    count = 0
    posititons = {
        "arr1": [],
        "arr2": []
        }
    
    for i in closing:
        for p in i:
            if (p == 0):
                count+=1
                posititons["arr1"].append(i)
                posititons["arr2"].append(p)
                print("count++")
            if (p == 255):
                if (count<= 100 and count > 0):
                    for b in posititons["arr1"]:
                        for v in posititons["arr2"]:
                            closing[b][v] = 255
                            totalChange+=1
                            print("change++")
                count = 0
                posititons = {
                    "arr1": [],
                    "arr2": []
                    }
    
    print("Total Change: " , totalChange)

    """
    
    #saving all the pictures in individual folders from each step    
    
    thingImage = imageUse.split("\\")
    useThing = ""
    placeNum = 0
    
    for i in thingImage:
        temp = list(i)
        temp = temp[:4]
        if (temp == ["T", "a", "n", "k"]):
            useThing = i
        placeNum += 1
            
    print(useThing)
    print(placeNum)
    
    placeNum-=1
    
    myFinalUse = closing
    
    
    
    
    place = "final thresh\\"+thingImage[placeNum][0:len(thingImage[placeNum])-4]
    print (place)
    try:
        os.mkdir(ntpath.abspath(place))
    except:
        print("skiped")
    #os.replace(ntpath.abspath(place))

    cv2.imwrite((place+"/1_og.jpg"), img)
    cv2.imwrite((place+"/2_redImage.jpg"), redImage)
    cv2.imwrite((place+"/3_gray.jpg"), gray)
    cv2.imwrite((place+"/4_blured.jpg"), blured)
    cv2.imwrite((place+"/6_thresh.jpg"), tempppp)
    cv2.imwrite((place+"/extra_theImgTestAltThresh.jpg"), theImgTestAltThresh)
    cv2.imwrite((place+"/7_closing.jpg"), closing)
    cv2.imwrite((place+"/8_negative.jpg"), negative)
    cv2.imwrite((place+"/notUsed_closing2.jpg"), closing2)
    cv2.imwrite((place+"/notUsed_regular.jpg"), regular)
    cv2.imwrite((place+"/9_myFinalUse.jpg"), myFinalUse)
    
    
    trans = Image.open(place+"/9_myFinalUse.jpg")
    trans.putalpha(75)
    
    layOver = Image.open(place+"/1_og.jpg")
    
    layOver.paste(trans, (0,0), mask=trans)
    
    #cv2.imwrite("during files/9_layerOver.jpg", layOver)
    
    #layOver.show()
    
    layOver = layOver.save(place+"/12_layOver.jpg")

    
    
    number_of_white_pix = cv2.countNonZero(myFinalUse)
    number_of_black_pix = np.sum(myFinalUse == 0)
    total = np.sum(myFinalUse)
    
    
    print ("white pixles: ", number_of_white_pix)
    print ("black pixles: ", number_of_black_pix)
    
    mussel = number_of_black_pix/numPixPerMussle
    
    print ("Number of Mussels in clumps: ", mussel)
    
    print ("done")
    
    print("\n\n\n\n\n\ntotal (added): ", number_of_white_pix+number_of_black_pix)
    print("the toal number of pixels in a picture of a coupon is 2170 * 2170 = 4708900")
    
    print("total (actual): nvm not true", total)
    
    fileNameAry.append(useThing)
    musselCountAry.append(mussel)
    blackPxlAry.append(number_of_black_pix)
        


df = pd.DataFrame({'File Name': fileNameAry, 'Mussel Count (in clumps)': musselCountAry, 'Black Pixles': blackPxlAry})

df.to_excel(countSheet, sheet_name='Sheet1', index=False)


countSheet.close()






"""
contours, hierarchy = cv2.findContours(negative, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]
max_area = cv2.contourArea(contours[0])
total = 0 # total contour size
for con in contours:
     area = cv2.contourArea(con) # get contour size
     total += area
     if area > max_area:
        max_area = area
diff = 0.1 # smallest contour have to bigger than (diff * max_area)
max_area = int(max_area * diff) # smallest contour have to bigger
average = int(total / (len(contours))) # average size for contour
radius_avg = int(math.sqrt(average / 3.14)) # average radius 

average = int(average * diff)

# Remove small object
mask = np.zeros(negative.shape[:2],dtype=np.uint8)
for component in zip(contours, hierarchy):
     currentContour = component[0]
     currentHierarchy = component[1]
     area = cv2.contourArea(currentContour)
     if ((currentHierarchy[3] < 0) and (area > average)):
          cv2.drawContours(mask, [currentContour], 0, (255), -1)

res1 = img.copy()
count = 0 #result
for con in contours:
     area = cv2.contourArea(con)
     radian = int(math.sqrt(area / 3.14))
     minRad = int(radian * 0.3)
     maxRad = int(radian * 2)
     mask_temp = np.zeros(mask.shape[:2],dtype=np.uint8)
     cv2.drawContours(mask_temp, [con], 0, (255), -1)
     circles = cv2.HoughCircles(mask_temp,cv2.HOUGH_GRADIENT,1, 1.2 * radian, param1=100,param2=10,minRadius=minRad,maxRadius=maxRad)
     if circles is not None: 
          circles = np.uint16(np.around(circles))
          for i in circles[0, :]:
               radius = i[2]
               if radius > radius_avg:
                    count += 1
                    center = (i[0], i[1]) # circle center
                    cv2.putText(res1, str(count), center,      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Put text at center    
                    cv2.circle(res1, center, radius, (0, 0, 255), 3) 
print('number of object is', count)
cv2.imwrite("during files/8_result.jpg", res1)
#cv2.imwrite("result.jpg", res1)
"""

#cv2.imwrite("during files/9_myFinalUse.jpg", myFinalUse)

print ("done")



#cv2.imshow("result", res1)
#cv2_imshow(res1)

"""
# sure background area
sure_bg = cv2.erode(mask, kernel)
# Finding sure foreground area
dist_transform = cv2.distanceTransform(mask,cv2.DIST_L2,5)
cv2_imshow(dist_transform)
# Draw sure figure from distance transform
ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0) 
# 0.2 is important, the bigger it is, the object is smaller (to the object center)
sure_fg = np.uint8(sure_fg)
#Find contour for sure figure
contours, hierarchy = cv2.findContours(sure_fg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
count = 0
result = img.copy()
for i in range(len(contours)):
     if radius[i] > averageRadius * diff_average_radius:
         count += 1
         cv2.circle(result, center, radius, (0, 0, 255), 3) # Draw circle
         cv2.putText(result, str(count), center,      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Put text
cv2_imshow(result)
"""






