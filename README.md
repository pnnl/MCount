# MCount
MCount is a GUI App built with PyQt6 that streamlines object detection. It utilizes a built-in computer vision model and thresholding system to accurately gather mussel larvae settlement data. It can also run or train any TensorFlow object detection model! 

## Installation
TODO


## How to Use MCount
You can minimize MCount anytime by clicking the - near the top right corner.
 
The window cannot be enlarged to keep the formatting intact - MCount is meant to be a compact GUI app.

You can close the app anytime by clicking the X in the top right corner.

You can customize certain GUI elements (such as font or color) in the config.py file found in the same directory as MCount.
 
The main menu displays MCount's five features as buttons: Count, Train Model, Select Model, Help, and Quit. 

### Count
After clicking the Count button, the main menu will disappear and the Count window will open. 

You may click "Begin New Count" to start a new detection. You may click "View Past Detections" to view detection images or spreadsheets from previous detections. If you'd like to return to the main menu, click "Cancel". 

Clicking "Begin New Count" will make a "Select input images from file explorer" button appear. You may click on this button to select the images you would like to run detections on. Otherwise, click "Cancel" to return to the main menu.  

After clicking "Select input images from file explorer", a file dialog will pop up. Select the images you would like to run detections on.* The file dialog will only accept .jpg, .png, and .tif image types. 

If you're not running the Default MCount Mussel Detector, you will be prompted to select your model's labelmap with a "Select Labelmap" button.  

After selecting your images (and potentially your labelmap), you will be prompted with two checkboxes. You may check or uncheck them depending on your use case.** "Run Mussel Thresholding" is for mussel clump detection. "Create Excel Spreadsheet" will create an excel spreadsheet containing the counts for each input image. The spreadsheet is stored in the ~\MCount\spreadsheets directory.

Click "Run Model" to begin the detection. This may take a while.

Once complete, you may view the detection images by clicking on "Open Detection Pictures". Each input image is separated into folders. If you're running the MCount Mussel Detector, each image will be split into smaller tiles.

You may also open the Count spreadsheet on Excel by clicking "Open Count Spreadsheet on Excel". A total count will be shown for each image. Each detection type is separated into sheets with counts for each image as well. 

You may view previous Count spreadsheets or images by clicking "View Past Detections" from the Count window. Or, you can just navigate (with file explorer) to your named detection folder under the ~/MCount/external/detections directory.

Once you're done with viewing your detection images or spreadsheets, click "Main Menu" to return to the main window of MCount.

*These images must be stored locally on your computer. 

**If you're running a mussel larvae detection, keep both boxes checked.

### Train Model
After clicking the Train button, the main menu will disappear and the Train window will open.

In order to train your selected model, you must add your training data by clicking "Select Image Configs". A file dialog will open and you must select a folder in which both the original images AND matching labeled image configs reside. Otherwise, click "Cancel" to return to the Main Menu.

Unless you're training the Default MCount Mussel Detector, you will need to provide your model's labelmap by clicking the "Select Labelmap" button. A file dialog will open and you must select a pbtxt file that contains your model's labelmap. Otherwise, click "Cancel" to return to the Main Menu.

After selecting your input images (and potentially your labelmap), MCount will close and the training will begin in the terminal. First, a terminal will create a .record file to store all of your training data. You may close it once it completes. Then the training will begin.

All properties of the training is determined by your config file of your model. It may take a long time! Like many minutes, hours, or often days! DO NOT CLOSE THE TERMINAL OR TURN OFF YOUR COMPUTER UNTIL THE TRAINING COMPLETES.*  

Once the training is complete, you may close the terminal and test your updated model with the Count feature. 

*You can check if the training is complete by typing in the terminal. If no letters show up, the training is not done. If letters do show up, the training ended (some way or another). 

### Select Model
After clicking the Select Model button, the main menu will disappear and the Select Model window will open. 

The current model will be displayed at the center of the screen. If you haven't changed the model yet, it should be "MCount Default model". The MCount default model is built to only detect solo mussel larvae. 

If you'd like to change the model, click "Select model folder from file explorer". If you'd like to return to the main menu, click "Back to Main Menu". 

After clicking "Select model folder from file explorer", a file dialog will open. Select the folder in which your model checkpoints and pipeline config file reside. If the folder contains multiple checkpoints, the newest one will always be selected. 

After selecting the model folder, a text input dialog will pop up. Type the name of your model in the field and click OK. This name simply exists for future reference, so make it recognizable. 

After entering the name of the model, the current model will change to the one you just selected. Now this model will be used whenever you train or run detections in MCount.*

*Currently, only TensorFlow 2 Detection Model Zoo models are compatible with MCount. 







