import os
from tensorflow import *
import pandas as pd
import cv2 
import numpy as np
import re
import styleframe
import time

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from matplotlib import pyplot as plt
from pathlib import Path

from colorama import *
from termcolor import * 
from pyfiglet import *

def tf_detect(model_path, name_of_count, labelmap_path):
    print(f"\nBeginning detection named {name_of_count}...")
    print("----------------------------------------------------\n")


    cwd = (os.getcwd()).replace("\\", "/")

    # Get a list of files in the folder
    files = os.listdir(model_path)

    # Extract numeric values from file names using regular expressions
    ckpts = []
    pattern = re.compile(r'\d+')
    for file in files:
        match = pattern.findall(file)
        if match:
            ckpts.append((int(match[0]), file))

    # Find the file name with the highest number
    max_number_ckpt = os.path.splitext(max(ckpts, key=lambda x: x[0])[1])[0]

    # Load pipeline config and build a detection model
    configs = config_util.get_configs_from_pipeline_file(f"{model_path}/pipeline.config")
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    ckpt = compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(f"{model_path}/{max_number_ckpt}").expect_partial()

    # # Define the function "detect_fn" that you will be using
    @function
    def detect_fn(image):
        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)
        return detections
    category_index = label_map_util.create_category_index_from_labelmap(labelmap_path)

    # # Use the object detection function

    # # Make sure it still works, and then go through and change some of the names. Like get rid of DIR_PATH_NAME. And change DIR_PATH_NAME to RAW_PATH_NAME.



    #for_counting - this means the array is formatted for counting detection boxes, not for visualizing the detection boxes 
    #for_visualization - this means the array is formatted to be used for visualizing detection boxes, not counting detection boxes

    # index array - this means the array contains the list indeces of the detection boxes in question, not their coordinates
    # coordinate array - this means the array contains the image coordinates of the detection boxes in question, not their list indeces
    #[y1,x1,y2,x2]

    # size filtered - this means this data has been filtered to remove boxes that have an area above a certain threshold and below a certain threshold
    # size and overlap filtered - this means the data has been size filtered and also filtered to remove boxes that overlap other boxes by at least a certain amount
    # Everything that is 'size filtered' and 'size and overlap filtered' is by default also confidence filtered.


    # For solo mussels only

    DIR_PATH_NAME = cwd + "/external/detections/" + name_of_count + "/images/bounding"
    DETECTED_PATH_NAME = cwd + "/external/detections/" + name_of_count + "/images/bounding" # Defines the folder where the post-detection tiles will be saved
    score_thresh = 0.05 # *** Enter here the confidence score, from 0 to 1, above which you will accept a detection. For our difficult-to-see mussels, we use 0.1.

    total_sum_array = [] # Initializes the array that will store the mussel totals for each COUPON (not tile).
    names_array = []   # Initializes the array that will store the coupon names (that will be linked to the mussel totals)
    for sub_dir in os.walk(DIR_PATH_NAME): # Starts the loop that walks through across every coupon-specific folder in the "tiles raw" subfolder
        for i in range(len(sub_dir[1])): # Starts the loop that walks through every tile in the coupon folders within the "tiles raw" subfolder 
            DETECTED_COUPON_PATH_NAME = DETECTED_PATH_NAME + '/' + sub_dir[1][i] # Defines the name of the coupon-specific folder that the detected tile images will go into.
            if not os.path.exists(DETECTED_COUPON_PATH_NAME):
                os.mkdir(DETECTED_COUPON_PATH_NAME)             # Creates the detected tile folder specific to this coupon in the "tiles detected" folder
            tile_count = np.array([0,0]) # Initializes the array that will contain the mussel count for a specific tile.
            SUB_PATH_NAME = DIR_PATH_NAME + '\\' + sub_dir[1][i] # Defines the name of the coupon-specific folder where the raw tiles are.
            SUB_PATH = Path(SUB_PATH_NAME).glob('*.png') # Prepares the coupons-specific raw tile folder to be looped through.
            for pic in SUB_PATH: # Loop through the tiles in the folder for the current coupon.
                name = str(pic)  # Converts the tile name to string format.
                img = cv2.imread(name) # Reads the tile as an image.
                image_np = np.array(img) # Converts the image data to a numpy array.
                input_tensor = convert_to_tensor(np.expand_dims(image_np, 0), dtype=float32) # Converts the numpy array to a tensor.
                detections = detect_fn(input_tensor) # Executes the object detection function on the image tensor. Results are stored in the array called "detections"
                                                    # Num_detections will always be 100 - it's not the number of actual detections, it's the limit I think.
                num_detections = int(detections.pop('num_detections')) # I don't understand
                detections = {key: value[0, :num_detections].numpy() # I don't understand
                        for key, value in detections.items()} # I don't understand
                detections['num_detections'] = num_detections # I don't understand
                # detection_classes should be ints. 
                detections['detection_classes'] = detections['detection_classes'].astype(np.int64) # I don't understand
                label_id_offset = 1 # I don't understand 
                image_np_with_detections = image_np.copy() # I don't understand

                # Collect the main outputs of the detection into easily callable arrays. We're just pulling specific chunks of information and giving them easier names.
                # Detection_scores contains the confidence levels for each detection box. The boxes displayed in the detected image will be governed by the confidence threshold defined above ...
                # ... but we can "manually" filter the detections that we count using our own threshold here. But we like to use the same threshold as definied above, so we just call that ...
                # variable "score_thresh" and apply it in both places.
                # Detection_classes contains the class of each detection box. Class means the kind of object detected. In our case, we only have one class (solo mussel) so all classes are 1.
                # Detection_boxes contains the two X-coordinates and two Y-coordinates that bound the detection boxes. It goes X1, Y1, X2, Y2. Or something like that. Not X1,X2,Y1,Y2.
                # And remember that everything is indexed starting at 0, so if there are four values, their indeces are 0,1,2,3.

                # Filter only the detection positions that are above a minimum confidence threshold
                index_array__boxes_above_confidence = np.where(detections['detection_scores']>score_thresh) # This contains the indeces for all the detections that have a confidence level above our defined threshold.
                for pos in index_array__boxes_above_confidence:
                    coordinate_array__confidence_only_filtered = detections['detection_boxes'][pos] # This defines the array as the detection box coordinate sets that have a confidence above our defined threshold. ((((((((((unnecessary?)))))))))))
                
                ## Remove boxes that are too large or too small
                area_list = []  # Instantiate the list that will become the array of detection box areas that we calculate areas for
                for j in range(0,len(coordinate_array__confidence_only_filtered)): # Loop through the detection boxes that are above the confidence threshold  ((((((((((((((((Switch to len(positions)? ))))))))))))))) Might have tried that but it didn't work????????
                    area = 320*(detections['detection_boxes'][j][3] - detections['detection_boxes'][j][1])*320*(detections['detection_boxes'][j][2] - detections['detection_boxes'][j][0]) # Calculate the area of each box (in pixels)
                    area_list.append(area) # Add each box to the list of box areas
                area_array = np.array(area_list) # Convert the area list to a numpy array
                small_filter_positions = np.where(area_array>100) # Find the positions in the area array that are above a minimum threshold
                small_filter_list = list(small_filter_positions[0]) # Create a list of the boxes that are a above the minimum area threshold
                big_filter_positions = np.where(area_array<300) # Find the positions in the original area array that are below a maximum threshold
                big_filter_list = list(big_filter_positions[0]) # Create a list of the boxes that are below the maximum threshold
                indeces_of_areas_above_minimum_and_below_maximum = set(small_filter_list) & set(big_filter_list) # Collect the positions of common boxes that are above the minimum and below the maximum
                coordinates_of_boxes_size_filtered__for_counting = []
                for z in list(indeces_of_areas_above_minimum_and_below_maximum):
                    coordinates_of_boxes_size_filtered__for_counting.append(coordinate_array__confidence_only_filtered[z]) # This is an array of the box coordinates that have been size filtered. We will need the box coordinates for the overlap filter coming next.
                box2 = coordinates_of_boxes_size_filtered__for_counting
            
                    
    # Convert the filtered list into a format that is equivalent to the detections['detection_boxes'] format. This is only necessary if you are trying to display ONLY the filtered detection boxes, not the original set of detection boxes.
    # The detection_boxes coordinates are in the format of: [y1,x1,y2,x2]
                coordinates_of_boxes_size_filtered_for_visualization = [0,0,0,0]
                for h in coordinates_of_boxes_size_filtered__for_counting:
                    coordinates_of_boxes_size_filtered_for_visualization = np.vstack((coordinates_of_boxes_size_filtered_for_visualization,h))
                coordinates_of_boxes_size_filtered_for_visualization = np.delete(coordinates_of_boxes_size_filtered_for_visualization,(0), axis = 0)
                b = coordinates_of_boxes_size_filtered_for_visualization.shape
                if len(b)<2: 
                    detections['detection_scores'] = np.array([0,0,0,0])   # I have to do this because when I filter the detection boxes, I'm not filtering the detection scores, and this becomes a problem when I try to visualize a tile that has had all of the boxes filtered away, leaving only a single [0,0,0,0] array behind, and this is only a problem when there are scores that are above the minimum score threshold but all the detection boxes have been filtered out, in which case the matrix shape is [4,] instead of [1,x] so I just replace the scores array with a blank dummy array. It's a sloppy fix and I should probabbly just filter the detection scores and classes the same as I filter the deteciton boxes, but this seems to work fine.
                    

    # Remove overlapping boxes
                dict = {'P':[],
                        'Q':[]}   # Instatiate a list that will be the list of boxes that overlap. P and Q are the indeces of the boxes that overlap. For example, if the first row lists 2 and 5, that means boxes 2 and 5 overlap.
                df_overlap = pd.DataFrame(dict) # Instantiate a dataframe from the dict list above.
                cushion = 0.02 # !!!! **** This is the overlap parameter. Larger value allows more overlap. I usually use 0.2. I thought this was a multiple of the total tile size (320 px) but it doesn't quite match up.
                        
                for p in range(len(box2)):
                    for q in range(len(box2)):
                        if ((box2[p][3]>box2[q][1]) and (box2[p][3]<box2[q][3]) and (box2[p][2]>box2[q][0]) and (box2[p][2]<box2[q][2]) and ((box2[p][3]-box2[q][1])>cushion) and ((box2[p][2]-box2[q][0])>cushion)):
                            df_overlap.loc[len(df_overlap.index)] = [p,q]   # 
                        elif ((box2[p][1]>box2[q][1]) and (box2[p][1]<box2[q][3]) and (box2[p][2]>box2[q][0]) and (box2[p][2]<box2[q][2]) and ((box2[q][3]-box2[p][1])>cushion) and ((box2[p][2]-box2[q][0])>cushion)):
                            df_overlap.loc[len(df_overlap.index)] = [p,q] 
                        elif ((box2[p][3]>box2[q][1]) and (box2[p][3]<box2[q][3]) and (box2[p][0]>box2[q][0]) and (box2[p][0]<box2[q][2]) and ((box2[p][3]-box2[q][1])>cushion) and ((box2[q][2]-box2[p][0])>cushion)):
                            df_overlap.loc[len(df_overlap.index)] = [p,q] 
                        elif ((box2[p][1]>box2[q][1]) and (box2[p][1]<box2[q][3]) and (box2[p][0]>box2[q][0]) and (box2[p][0]<box2[q][2]) and ((box2[q][3]-box2[p][1])>cushion) and ((box2[q][2]-box2[p][0])>cushion)):
                            df_overlap.loc[len(df_overlap.index)] = [p,q] 
            
                overlap_array = df_overlap.to_numpy() # This is a list of the sets of boxes that overlap.
                overlap_column = overlap_array[:,0]
                overlaps = list(overlap_column) # This is a list of just the first column of the sets that overlap. I'm arbitrarily selecting the first (P-column) box of each overlapping pair to delete.
                box2_all = []
                for w in range(len(box2)):
                    box2_all.append(w) # Builds an array from 1 (or 0?) to the length of the size of the original Box2. This just provides a means of looping through the array of detection boxes.
                
                index_array__size_and_overlap_filtered__for_counting = []
                for element in box2_all:
                    if element not in overlaps:
                        index_array__size_and_overlap_filtered__for_counting.append(element)  # This "index_array__size_and_overlap_filtered__for_counting" array is a list of indeces of the elements in the "box2" array (the size-filtered detection boxes) that are not on the overlap list. Thus, this is 
                                                    # ... a list that is both size-filtered and overlap-filtered.
                
                coordinate_array__size_and_overlap_filtered__for_visualization=np.array([0,0,0,0])
                for x in index_array__size_and_overlap_filtered__for_counting:
                    box_take = box2[x]      # box_take is just the name of the single-line array in this loop. I'm just looking at the positions listed in index_array__size_and_overlap_filtered__for_counting, and grabbing the box coordinates that are in those positions and putting them in a new array, coordinate_array__size_and_overlap_filtered__for_visualization
                    coordinate_array__size_and_overlap_filtered__for_visualization = np.vstack((coordinate_array__size_and_overlap_filtered__for_visualization,box_take))
                a = coordinate_array__size_and_overlap_filtered__for_visualization.shape

                if len(a)<2:
                    detections['detection_scores']=np.array([0,0,0,0])                                           # ... array. It is in a format that can be plugged into the image display algorithm to display the filtered, not original, boxes.

                detections['detection_boxes'] = coordinate_array__size_and_overlap_filtered__for_visualization            # !!!! Use this line to see displayed below the boxes overlap_filtered and size_filtered.  
                #detections['detection_boxes'] = coordinates_of_boxes_size_filtered_for_visualization   # !!!! Use this line to see displayed below the boxes only size_filtered.                
                                                                    # Or comment out both lines above to see original unfiltered boxes                       
                                                                    # But if you comment out both lines, you also have to comment out the if len(a)<2.. and if len(b)<2... commands
                viz_utils.visualize_boxes_and_labels_on_image_array(   # This clump of code configured the displaying of the detected tiles in the window below. Don't change anything, unless you want to make the box lines a little thicker (line_thickness).
                        image_np_with_detections,
                        detections['detection_boxes'],
                        detections['detection_classes']+label_id_offset,
                        detections['detection_scores'],  # The only reason this works - after having filtered the 'detection_boxes' but not 'detection_scores' - is because you already filtered by detection scores in the above code, keeping only the boxes that are above the minimum threshold defined by score_thresh. So here, you only have detection boxes that are above the score thresh. So, say for example, it tries here to remove boxes 83 through 100 because they are below the score threshold. But you've already removed those boxes - there are only 82 boxes left in the detection_boxes array (in this example). That's the only way I can think why this is actually working.
                        category_index,
                        use_normalized_coordinates=True,
                        skip_scores=True, #removes scores
                        skip_labels=True, #removes labels
                        max_boxes_to_draw=10000,
                        min_score_thresh=score_thresh,
                        agnostic_mode=False,
                        line_thickness=1,
                        )
            
                # Save the mussel count for each tile after the name of each tile. This clump of code is important because it adds up the mussel counts!!! And if ...
                # ... you pull the mussel counts from the wrong section of code, you will get the wrong counts.
                base_name0 = os.path.basename(name) #Gets rid of the folder path part of the file name.
                base_name = os.path.splitext(base_name0)[0]     # Gets rid of the .png part of the file name 
                tile_count = np.vstack([tile_count,[base_name,len(index_array__size_and_overlap_filtered__for_counting)]]) # !!!! Use this line if you want to count the size_and_overlap_filtered boxes
                #tile_count = np.vstack([tile_count,[base_name,len(list(indeces_of_areas_above_minimum_and_below_maximum))]]) # !!!!! Use this line if you want to count the size_filtered boxes. Stacks the tile mussels counts into a list of the tile mussel counts
                plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB)) # Shows the image below
                
                # Save the detected tile image
                cv2.imwrite(os.path.join(DETECTED_COUPON_PATH_NAME,base_name0),image_np_with_detections) #saves the tile as an image in the tiles detected folder
            
            
            solos_sum = tile_count[:, 1].astype(float).sum() # Adds up the tile mussel counts to get a total coupon mussel count.
            names_array.append(sub_dir[1][i]) # Creates an array of the coupon names so the coupon total counts can be tabulated in a single spreadsheet
            total_sum = solos_sum # + light_clump_sum + heavy_clump_sum . This was originally for adding the clump counts, but we don't count clumps any more. This doesn't initialize the total_sum_array.
            total_sum_array.append(total_sum) # Stacks the total coupon sums into an array. I don't know why I didn't have to initialize the array first.
        print("\n Image Successfully Detected. \n")

    # Writes the total coupon sums spreadsheet.
    df_coupon_count = pd.DataFrame({"Image": names_array, "Count": total_sum_array})
    excel_path = cwd + "/external/detections/" + name_of_count + "/spreadsheets/overall_counts.xlsx"
    writer = pd.ExcelWriter(excel_path, mode="a", engine = "openpyxl")
    # write dataframe to excel
    sf = styleframe.StyleFrame(df_coupon_count)
    sf.to_excel(excel_writer=writer, sheet_name="Bounding", best_fit=["Image", "Count"], columns_and_rows_to_freeze='B2', row_to_add_filters=0, index=False)
    # save the excel
    writer.close()
    print('\n DataFrame successfully written to Excel File.\n')
    print("Detection Complete!")
    print("--------------------------------------------------------------\n")
    time.sleep(3)

    return [total_sum_array, names_array]