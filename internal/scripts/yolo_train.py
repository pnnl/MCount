from ultralytics import YOLO
import os

def new_train(model_path, yaml, loops, img_size):
    model = YOLO(model_path)

    results = model.train(data=yaml, epochs=loops, imgsz=img_size)