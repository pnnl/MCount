# MCount
### By Lance Miller and Navaj Nune
MCount is a GUI App built with PyQt5 that streamlines object detection. You can utilize a built-in computer vision model and thresholding system to accurately gather mussel larvae settlement data. Or, you can just add your own model, train it, and detect anything! 

## Installation



## How to Use MCount
You can minimize MCount anytime by clicking the - near the top right corner. 
The window cannot be enlarged to keep the formatting intact - MCount is meant to be a compact GUI app.
You can close the app anytime by clicking the X in the top right corner.
You can customize certain GUI elements (such as font or color) in the config.py file found in the same directory as MCount. 
The main menu displays MCount's five features as buttons: Count, Train Model, Select Model, Help, and Quit. 

### Count
After clicking the Count button, the main menu will disappear and the Count window will open. 

You may click "Select input images from file explorer". If you'd like to return to the main menu, click "Cancel". 

After clicking "Select input images from file explorer", a file dialog will pop up. Select the images you would like to run detections on.* The file dialog will only accept .jpg, .png, and .tif image types. 

After selecting your images, you will be prompted with two checkboxes. You may check or uncheck them depending on your use case.** "Run Mussel Thresholding" is for counting mussel clumps (along with the solo mussels). "Create Excel Spreadsheet" will create an excel spreadsheet containing the counts for each input image. The spreadsheet is stored in the ~\MCount\spreadsheets directory.

Click "Run Model" to begin the detection. This may take a while.

Once the window says "Count Complete!", you may exit out of MCount. 

To view your detected images, open them from the ~\MCount\detections directory. 

*If you're running a mussel larvae detection, these images will already need to be split into tiles. Also, the image CANNOT come from the PNNL shared drive. They must be stored locally. 

**If you're running a mussel larvae detection, keep both boxes checked.

### Train Model

### Select Model







