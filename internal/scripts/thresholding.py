import numpy as np
import cv2
import ntpath
import pandas as pd

import os
import styleframe

from PIL import Image

from PIL import Image

from PIL import Image

def threshFunction (image_dir_counting, countName, images,
                    image1_buttontest,
                    image2_buttontest,
                    image3_buttontest,
                    image4_buttontest,
                    image5_buttontest,
                    image6_buttontest,
                    image7_buttontest,
                    image8_buttontest,
                    image9_buttontest):

    filenames = []
    mussel_counts = []
    black_pixels = []

    pixels_per_mussel = 143.8

    # iterate over files in that directory

    print("\n\n========= thresholding beginns")
    print(image_dir_counting)

        
    for image in images:
        print ("\n--------- next picture\n")
        
        print("image: ", image)

        image_path = ntpath.abspath(image)

        img = cv2.imread(image_path) #read image

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert to hsv

        # Range for lower red
        lower_red = np.array([0, 65, 0])
        upper_red = np.array([100, 255, 255])
        mask = cv2.inRange(hsv_img, lower_red, upper_red)
        
        # Range for upper range
        lower_red = np.array([180,180,190])
        upper_red = np.array([170,155,110])
        
        # Get image in red pixel only
        red_img = cv2.bitwise_and(img.copy(), img.copy(), mask = mask)
        

        
        gray = cv2.cvtColor(red_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5,5),0)
        

        _, thresh = cv2.threshold(blurred,1,255,cv2.THRESH_BINARY_INV)
        
        alt_thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3, 8)
        
        
        kernel = np.ones((15,15),np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        
        negative = cv2.bitwise_not(closing) # OR
        
        kernel = np.ones((15,15),np.uint8)
        closing2 = cv2.morphologyEx(negative, cv2.MORPH_CLOSE, kernel)
        
        regular = cv2.bitwise_not(closing2)
        
        final = closing

        #saving all the pictures in individual folders from each step    

        endname = os.path.splitext(os.path.basename(image_path))[0]

        path = "detections/"+  countName + "/images/thresholding"

        full_path = path + "/"+ endname
        print ("Paths of directories made:", full_path)
        # try:
        os.mkdir(full_path)
        # except:
            # print("skipped making new directories")
        cv2.imwrite((full_path + "/1_og.jpg"), img)
        if (image2_buttontest):
            cv2.imwrite((full_path + "/2_red_image.jpg"), red_img)
        if (image3_buttontest):
            cv2.imwrite((full_path + "/3_gray.jpg"), gray)
        if (image4_buttontest):
            cv2.imwrite((full_path + "/4_blurred.jpg"), blurred)
        if (image5_buttontest):
            cv2.imwrite((full_path + "/5_thresh.jpg"), thresh)
        if (image6_buttontest):
            cv2.imwrite((full_path + "/6_closing.jpg"), closing)
        cv2.imwrite((full_path + "/7_my_final_use.jpg"), final)
        if (image8_buttontest):
            cv2.imwrite((full_path+"/extra_the_img_test_alt_thresh.jpg"), alt_thresh)
        if (image9_buttontest):
            cv2.imwrite((full_path + "/notUsed_closing2.jpg"), closing2)
            cv2.imwrite((full_path + "/notUsed_regular.jpg"), regular)
            cv2.imwrite((full_path + "/notUsed7_negative.jpg"), negative)
        
        trans = Image.open(full_path + "/7_my_final_use.jpg")
        trans.putalpha(75)
        
        layover = Image.open(full_path + "/1_og.jpg")
        
        layover.paste(trans, (0,0), mask=trans)
        layover = layover.save(full_path+"/8_layOver.jpg")

        if (not image1_buttontest):
            os.remove((full_path + "/1_og.jpg"))
        if (not image7_buttontest):
            os.remove((full_path + "/7_my_final_use.jpg"))
        
        number_of_black_pixels = np.sum(final == 0)
        
        print ("Black pixels: ", number_of_black_pixels)
        
        mussel = round(number_of_black_pixels/pixels_per_mussel)
        
        print ("number of mussels in clumps: ", mussel)

        filenames.append(endname)
        mussel_counts.append(mussel)
        black_pixels.append(number_of_black_pixels)

    excel_dir = "detections/"+  countName + "/spreadsheets"
    countSheet = pd.ExcelWriter(excel_dir + "/" + 'overall_counts.xlsx', mode="a", engine='openpyxl')
    df = pd.DataFrame({'Image': filenames, 'Clump Mussel Count': mussel_counts, 'Black Pixels': black_pixels})
    sf = styleframe.StyleFrame(df)
    sf.to_excel(excel_writer=countSheet, best_fit=["Image", "Clump Mussel Count", "Black Pixels"], sheet_name="Thresholding", columns_and_rows_to_freeze='B2', row_to_add_filters=0)
    countSheet.close()


    print ("\n^^^^^^^^^^^^thresholding completed^^^^^^^^^^^^")

    return [mussel_counts, filenames]

