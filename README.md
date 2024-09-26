<img src="https://i.postimg.cc/X729HZs9/logrefined-final.png"/>

## What is MCount?
MCount is a GUI App built with PyQt6 that streamlines object detection. It utilizes a built-in computer vision model and thresholding system to accurately gather mussel larvae settlement data. It can also run or train any YOLOv8 object detection model! 

## Installation
To install MCount, simply download and extract the latest <a href="https://www.mediafire.com/file/p7j0r2jbe0kvevi/MCount.zip/file">distribution</a>. No additional packages need to be installed. 

## How to Use MCount
You can minimize MCount anytime by clicking the - near the top right corner.

You can close the app anytime by clicking the X in the top right corner.
 
The main menu displays MCount's five features as buttons: Count, Train Model, Select Model, Help, and Quit. 

### Count
After clicking the Count button, the main menu will disappear and the Count window will open. 

You may click "Begin New Count" to start a new detection. You may click "View Past Detections" to view detection images or spreadsheets from previous detections. If you'd like to return to the main menu, click "Cancel". 

Clicking "Begin New Count" will make a "Select input images from file explorer" button appear. You may click on this button to select the images you would like to run detections on. Otherwise, click "Cancel" to return to the main menu.  

After clicking "Select input images from file explorer", a file dialog will pop up. Select the images you would like to run detections on.* The file dialog will only accept .jpg, .png, and .tif image types. 

After selecting your images (and potentially your labelmap), you will be prompted with two checkboxes. You may check or uncheck them depending on your use case.** "Run Mussel Thresholding" is for mussel clump detection. "Create Excel Spreadsheet" will create an excel spreadsheet containing the counts for each input image. The spreadsheet is stored in the ~/MCount/detections/[name of count]/spreadsheets directory.

Click "Run Model" to begin the detection. This may take a while.

Once complete, you may view the detection images by clicking on "Open Detection Pictures". Each input image is separated into folders. If you're running the MCount Mussel Detector, each image will be split into smaller tiles.

You may also open the Count spreadsheet on Excel by clicking "Open Count Spreadsheet on Excel". A total count will be shown for each image. Each detection type is separated into sheets with counts for each image as well. 

You may view previous Count spreadsheets or images by clicking "View Past Detections" from the Count window. Or, you can just navigate to the ~/MCount/detections/[name of count] directory.

Once you're done with viewing your detection images or spreadsheets, click "Main Menu" to return to the main window of MCount.

*These images must be stored locally on your computer. 

**If you're running a mussel larvae detection, keep both boxes checked.

### Train Model
After clicking the Train button, the main menu will disappear and the Train window will open.

You may select your training's config file by clicking the "Select Training Config" button. You will need to select a YAML file containing the correct object classes and training directories, as described in the additional training setup section.

After selecting the config file, you will need to set some of the parameters for your training. MCount will prompt you to input the number of epochs (loops of training through your image set), the image size of your dataset, and the name for this training. 

Once you've provided the parameters for your training, MCount will close and the training will complete in the terminal. Please note that this process may take a long time, and closing the terminal will cause the training to end early. 

After the training is completed, you may view the training results in the ~/MCount/training/[name of training] directory. It will contain the training evaluation metrics and the resulting model weights file. 

## Additional Training Setup
In order to run training on a new model, you need to set up a directory with annotated images and an object classes YAML file. 

The training images must be stored in a directory named "images", and must share a parent directory with another directory called "labels". 

All image annotations must be saved in the proper YOLO text file format (.txt), and have file names which match the image they are annotating. The recommended image annotation tool for MCount is LabelImg.

Example directory tree:

```
parent_directory
├── images
    ├── image_1.jpg
    ├── image_2.jpg
    ├── image_3.jpg
    ├── ...
├── labels
    ├── image_1.txt
    ├── image_2.txt
    ├── image_3.txt
    ├── ...
```

The object classes YAML file is needed to tell the YOLO model what labels it is training on and where the training, validation, and test images are stored.

The object classes YAML file (or the training config file) should be formatted as the following: 

```
# Names of labels used in annotations
names:
   0: Object_name_1
   1: Object_name_2
   2: Object_name_3
   ...

# Image directory paths (only training directory path is absolutely neccessary)
train: "training_directory_path"
val: "validation_directory_path"
test: "testing_directory_path"
```

### Select Model
After clicking the Select Model button, the main menu will disappear and the Select Model window will open. 

The current model will be displayed at the center of the screen. If you haven't changed the model yet, it should be "MCount Default model". The MCount default model is built to only detect solo mussel larvae. 

If you'd like to change the model, click "Select model folder from file explorer". If you'd like to return to the main menu, click "Back to Main Menu". 

After clicking "Select model folder from file explorer", a file dialog will open. Select the folder in which your model checkpoints and pipeline config file reside. If the folder contains multiple checkpoints, the newest one will always be selected. 

After selecting the model folder, a text input dialog will pop up. Type the name of your model in the field and click OK. This name simply exists for future reference, so make it recognizable. 

After entering the name of the model, the current model will change to the one you just selected. Now this model will be used whenever you train or run detections in MCount.*

If you've changed folder location of an added model, it will not work. To remove or change the path to an added model, remove it from the dict in ~/MCount/internal/resources/modeldict.json

*Currently, only Yolov8 models are compatible with MCount. 

## DISCLAIMER
This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed, or
represents that its use would not infringe privately owned rights.
 
Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.
```
PACIFIC NORTHWEST NATIONAL LABORATORY operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY under Contract DE-AC05-76RL01830
```


