from ultralytics import YOLO
import os
import shutil

def new_train(model_path, yaml, loops, img_size, name):
    print("ALL TRAINING RESULTS WILL BE MOVED THE TRAINING DIRECTORY ONCE COMPLETED")

    model = YOLO(model_path)

    results = model.train(data=yaml, epochs=loops, imgsz=img_size)

    os.rename("runs/detect/train", f"runs/detect/{name}")
    shutil.move(f"runs/detect/{name}", f"training")
    os.rmdir("runs/detect") 
    os.rmdir("runs") 
    