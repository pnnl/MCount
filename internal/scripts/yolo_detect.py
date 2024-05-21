from ultralytics import YOLO
import pandas as pd
import styleframe
import time
import os
import shutil
from pathlib import Path

def yolo_detect(model_path, name_of_count):
    cwd = (os.getcwd()).replace("\\", "/")

    input_dir = cwd + "/external/detections/" + name_of_count + "/images/bounding"
    output_dir = cwd + "/external/detections/" + name_of_count + "/images/bounding"

    conf = 0.35
    model = YOLO(model_path)

    names_array = []
    total_sum_array = []
    for sub_dir in os.listdir(input_dir):
        print(os.path.join(input_dir, sub_dir))
        count = 0
        for img in Path(os.path.join(input_dir, sub_dir)).glob("*.png"):
            print(img)
            # Run AI predictions
            model.predict(source=img, save=True, conf=conf, save_txt=True)

            # Find mussel count through text results
            txt_path = "runs/detect/predict/labels/"+ os.path.splitext(os.path.basename(img))[0] + ".txt"
            try:
                with open(txt_path) as txt:
                    for line in txt:
                        count+=1
            except FileNotFoundError:
                pass
            
            # Move annotated image file to /external/
            shutil.move("runs/detect/predict/" + os.path.basename(img), os.path.join(output_dir, sub_dir, img))
        
        names_array.append(sub_dir)
        total_sum_array.append(count)
    
    # Delete redundant runs folder
    if os.path.exists(cwd + "/runs"):
        shutil.rmtree(cwd + "/runs")

    # Write the total coupon sums spreadsheet
    df_coupon_count = pd.DataFrame({"Image": names_array, "Count": total_sum_array})
    excel_path = cwd + "/external/detections/" + name_of_count + "/spreadsheets/overall_counts.xlsx"
    writer = pd.ExcelWriter(excel_path, mode="a", engine = "openpyxl")

    # Write dataframe to excel
    sf = styleframe.StyleFrame(df_coupon_count)
    sf.to_excel(excel_writer=writer, sheet_name="Bounding", best_fit=["Image", "Count"], row_to_add_filters=0, index=False)
    
    # Save the excel
    writer.close()
    print('\n DataFrame successfully written to Excel File.\n')
    print("Detection Complete!")
    print("--------------------------------------------------------------\n")
    time.sleep(3)

    return [total_sum_array, names_array]