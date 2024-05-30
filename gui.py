from colorama import *
from termcolor import * 
from pyfiglet import *
import time

cprint(figlet_format("MCount", font="standard"), attrs=["bold"])

time.sleep(1)

print("Open the README for complete app instructions.\n")

time.sleep(1)

import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

import json
import sys
import os
import re
import pandas as pd
import styleframe
from pathlib import Path
import openpyxl

import config as cfg
import internal.scripts.tiling as tiling
import internal.scripts.thresholding as thresholding
import internal.scripts.directories as dirs
import internal.scripts.yolo_detect as yd
import internal.scripts.yolo_train as yt

# Gets the current working directory and replaces the backslashes to prevent parsing issues later on
cwd = (os.getcwd()).replace("\\", "/")

# Makes the GUI agree better with OS window scaling 
os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"]             = "1"

# Opens the model dict
with open(dirs.dict, "r") as f:
    model_dict = json.load(f)
try:
    # Checks if this is the first time the user has opened this dict
    if model_dict["first_time"]:
        model_dict["current_model_directory"] = dirs.model
        model_dict[dirs.model] = "MCount Mussel Detector"
        model_dict.pop("first_time")

        with open(dirs.dict, "w") as f:
            json.dump(model_dict, f, indent=4)
except:
    pass

def defaultUI(window):
    # Adds a title 
    window.setWindowTitle("MCount")

    # Sets app icon
    window.setWindowIcon(qtg.QIcon(cwd + '/internal/resources/icon.jpg'))

    # Sets default layout for entire window
    window.setLayout(qtw.QVBoxLayout())
    window.layout().setSpacing(12)
    
    # Creates window at specific size
    if cfg.small_screen:
        window.setMinimumSize(400, 300)
        window.setMaximumSize(401, 301)
    else:
        window.setMinimumSize(500, 350)
        window.setMaximumSize(501, 351)


class MainWindow(qtw.QWidget):
    # Function is run as soon as window is initialized
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Create title and author labels within vertical layout
        self.title_label = qtw.QLabel("MCount")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.title_font_size))
        self.title_label.setStyleSheet(f'color: {cfg.title_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        self.layout().addWidget(self.title_label)
        author_label = qtw.QLabel("By Lance Miller and Navaj Nune")
        author_label.setFont(qtg.QFont(cfg.default_font, 14))
        author_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        author_label.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.layout().addWidget(author_label)
        verticalSpacer = qtw.QSpacerItem(20, 15, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.layout().addItem(verticalSpacer)

        # Creates run, train, and select model buttons within vertical layout
        count_button = qtw.QPushButton("Count")
        count_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        count_button.clicked.connect(self.count_button_clicked)
        self.layout().addWidget(count_button)
        train_button = qtw.QPushButton("Train Model")
        train_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        train_button.clicked.connect(self.train_button_clicked)
        self.layout().addWidget(train_button)
        select_button = qtw.QPushButton("Select Model")
        select_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        select_button.clicked.connect(self.select_button_clicked)
        self.layout().addWidget(select_button)
       
        # Creates help/quit button split at bottom
        menu_split = qtw.QHBoxLayout()
        menu_split.setSpacing(10)
        self.layout().addLayout(menu_split)

        # Creates help and quit buttons within horizontal layout
        help_button = qtw.QPushButton("Help")
        help_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        help_button.clicked.connect(self.help_button_clicked)
        menu_split.addWidget(help_button)
        quit_button = qtw.QPushButton("Quit")
        quit_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        quit_button.clicked.connect(self.quit_button_clicked)
        menu_split.addWidget(quit_button)
        
        # Shows window
        self.show()

    def count_button_clicked(self):
        # Closes the main window and opens the count window
        self.cw = CountWindow()
        self.cw.move(self.pos())
        self.cw.show()
        self.close()

    def train_button_clicked(self):
        # Closes the main window and opens the train window
        self.tw = TrainWindow()
        self.tw.move(self.pos())
        self.tw.show()
        self.close()
    
    def select_button_clicked(self):
        # Closes the main window and opens the select model window
        self.sw = SelectWindow()
        self.sw.move(self.pos())
        self.sw.show()
        self.close()

    def help_button_clicked(self):
        # Opens the help document
        os.startfile('README.md')
    
    def quit_button_clicked(self):
        # Closes the GUI and ends the application runtime
        self.close()


class CountWindow(qtw.QWidget):
    # Function is run as soon as window is initialized
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Creates a title label within layout
        self.title_label = qtw.QLabel("Count")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a file dialog button
        self.begin_button = qtw.QPushButton("Begin New Count")
        self.begin_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.begin_button.clicked.connect(self.begin_button_clicked)
        self.layout().addWidget(self.begin_button)     

        # Creates a view past counts button
        self.past_counts_button = qtw.QPushButton("View Past Detection Counts")
        self.past_counts_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.past_counts_button.clicked.connect(self.view_past)
        self.layout().addWidget(self.past_counts_button)    
        
        # Creates a back button
        self.back_button = qtw.QPushButton("Cancel")
        self.back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(self.back_button)

    def begin_button_clicked(self):
        # Clears window elements
        self.begin_button.setParent(None)
        self.past_counts_button.setParent(None)
        self.back_button.setParent(None)

        # Changes title text
        self.title_label.setText("New Count")
        
        # Creates a file dialog button
        self.file_button = qtw.QPushButton("Select Input Images Folder")
        self.file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.file_button.clicked.connect(self.images_button_clicked)
        self.layout().addWidget(self.file_button)

        # Creates a back button
        self.back_button = qtw.QPushButton("Cancel")
        self.back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(self.back_button)

    def images_button_clicked(self):
        global image_dir
        # Opens file explorer to choose images
        image_dir = qtw.QFileDialog.getExistingDirectory(self, "Open Images Folder", cfg.initial_directory)

        # Pulls current model directory from modeldict.json
        with open(dirs.dict, "r") as f:
            model_dict = json.load(f)
            current_model_name = model_dict[model_dict["current_model_directory"]]
        
        # Will check if an image directory was chosen and if they have the MCount model selected
        if image_dir and current_model_name == "MCount Mussel Detector":
            # Bypasses the labelmap file dialog
            self.labelmap_bypass = True
            
            self.default_labelmap = cwd + "/internal/model/annotations/labelmap.pbtxt"

            global labelmap
            labelmap = self.default_labelmap
            
            # Does formatting stuff
            self.file_button.setParent(None)
            self.labelmap_button = qtw.QPushButton("Placeholder")

            # Continues as if labelmap button was pressed
            self.labelmap_button_clicked()

        # Checks if images were chosen
        elif image_dir:
            # Removes file button and back button
            self.file_button.setParent(None)
            self.back_button.setParent(None)

            # Creates a labelmap file dialog button
            self.labelmap_button = qtw.QPushButton("Select Labelmap (.pbtxt)")
            self.labelmap_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.labelmap_button.clicked.connect(self.labelmap_button_clicked)
            self.layout().addWidget(self.labelmap_button)

            # Adds the back button
            self.layout().addWidget(self.back_button)
    
    def labelmap_button_clicked(self):
        # Checks for labelmap_bypass
        global labelmap
        if self.labelmap_bypass == False:
            labelmap, _ = qtw.QFileDialog.getOpenFileName(self, "Open Label Map File", cfg.initial_directory, "Protocol Buffer Text File (*.pbtxt)")
        if labelmap or self.labelmap_bypass == True:
            # Does formatting stuff
            self.labelmap_button.setParent(None)
            self.back_button.setParent(None)

            # Creates checkboxes for thresholding and spreadsheet
            self.thresh_checkbox = qtw.QCheckBox("Run Thresholding")
            global run_thresh
            run_thresh = False
            # self.thresh_checkbox.setChecked(True)
            self.thresh_checkbox.stateChanged.connect(self.thresh_checkbox_changed)
            self.layout().addWidget(self.thresh_checkbox)
            self.img_selection_checkbox = qtw.QCheckBox("Download Specific Thresholding Images")
            self.img_selection_checkbox.stateChanged.connect(self.select_checkbox_changed)
            # self.layout().addWidget(self.img_selection_checkbox)

            # Creates a run button
            self.next_button = qtw.QPushButton("Run Model")
            self.next_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.next_button.clicked.connect(self.name_count)
            self.layout().addWidget(self.next_button)
            
            # Adds the back button
            self.layout().addWidget(self.back_button)

    # This function is run anytime the thresholding checkbox is checked or unchecked
    def thresh_checkbox_changed(self):
        # If the checkbox is checked, another checkbox is created for the user to select specific thresholding images
        if self.thresh_checkbox.isChecked():
            run_thresh = True
            self.layout().addWidget(self.img_selection_checkbox)
            self.layout().addWidget(self.next_button)
            self.layout().addWidget(self.back_button)

        # If the thresholding checkbox is unchecked, the selection checkbox is removed
        if not self.thresh_checkbox.isChecked():
            self.img_selection_checkbox.setChecked(False)
            self.img_selection_checkbox.setParent(None)

    # This function is run anytime the selection checkbox is checked or unchecked
    def select_checkbox_changed(self):
        # If the selection checkbox is checked, change the next button text 
        if self.img_selection_checkbox.isChecked():
            self.next_button.setText("Next")
            self.next_button.clicked.disconnect(self.name_count)
            self.next_button.clicked.connect(self.select_thresh_images)
            
        # If the selection checkbox is checked, change the next button text 
        if not self.img_selection_checkbox.isChecked():
            self.next_button.setText("Run Model")
            self.next_button.clicked.disconnect(self.select_thresh_images)
            self.next_button.clicked.connect(self.name_count)


    def name_count (self):
        # Opens an input dialog for the user to name the count (Files will be stored in a subdirectory under this name)
        name, self.done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name this counting:')
        global name_of_count
        if name == "" and self.done:
            try:
                # Finds the highest number in the unnamed folders and adds 1
                unnamed_files = []
                pattern = re.compile(r"\d+")
                for sub_dir in next(os.walk(dirs.detections))[1]:
                    if "Unnamed Detection" in sub_dir:
                        match = pattern.findall(str(sub_dir))
                        if match:
                            unnamed_files.append(int(match[0]))
                if unnamed_files != []: 
                    value = max(unnamed_files) + 1
                else:
                    value = 1
                name_of_count = f"Unnamed Detection {value}"
                
            except:
                name_of_count = f"Unnamed Detection 1"
            # Removes widgets from the layout
            self.thresh_checkbox.setParent(None)
            self.img_selection_checkbox.setParent(None)
            self.next_button.setParent(None)

            self.run_button_clicked()
        if name and self.done:
            # Sets the name
            name_of_count = name
            
            # Removes widgets from the layout
            self.thresh_checkbox.setParent(None)
            self.img_selection_checkbox.setParent(None)
            self.next_button.setParent(None)

            self.run_button_clicked()
        
        
    def select_thresh_images(self):
            # Clears previous app elements
            self.thresh_checkbox.setParent(None)
            self.img_selection_checkbox.setParent(None)
            self.next_button.setParent(None)

            # Changes title
            self.title_label.setText("Select Images\nTo Save")

            # Creates help/quit button split at bottom
            self.menu_split1 = qtw.QHBoxLayout()
            self.menu_split1.setSpacing(10)
            self.layout().addLayout(self.menu_split1)
            self.menu_split2 = qtw.QVBoxLayout()
            self.menu_split2.setSpacing(10)
            self.menu_split1.addLayout(self.menu_split2)
            self.menu_split3 = qtw.QVBoxLayout()
            self.menu_split3.setSpacing(10)
            self.menu_split1.addLayout(self.menu_split3)
            self.menu_split4 = qtw.QVBoxLayout()
            self.menu_split4.setSpacing(10)
            self.menu_split1.addLayout(self.menu_split4)
            
            # Creates checkboxes for saving images
            self.image1_buttontest = qtw.QCheckBox("#1 Original")
            self.image1_buttontest.setChecked(True)
            self.menu_split2.addWidget(self.image1_buttontest)

            self.image2_buttontest = qtw.QCheckBox("#2 Red Segmentation")
            self.image2_buttontest.setChecked(False)
            self.menu_split2.addWidget(self.image2_buttontest)

            self.image3_buttontest = qtw.QCheckBox("#3 Grayscale")
            self.image3_buttontest.setChecked(False)
            self.menu_split2.addWidget(self.image3_buttontest)

            self.image4_buttontest = qtw.QCheckBox("#4 Blurred")
            self.image4_buttontest.setChecked(False)
            self.menu_split3.addWidget(self.image4_buttontest)

            self.image5_buttontest = qtw.QCheckBox("#5 Thresholding")
            self.image5_buttontest.setChecked(True)
            self.menu_split3.addWidget(self.image5_buttontest)

            self.image6_buttontest = qtw.QCheckBox("#6 Closing")
            self.image6_buttontest.setChecked(False)
            self.menu_split3.addWidget(self.image6_buttontest)

            self.image7_buttontest = qtw.QCheckBox("#7 Final")
            self.image7_buttontest.setChecked(True)
            self.menu_split4.addWidget(self.image7_buttontest)

            self.image8_buttontest = qtw.QCheckBox("#8 Extra")
            self.image8_buttontest.setChecked(False)
            self.menu_split4.addWidget(self.image8_buttontest)

            self.image9_buttontest = qtw.QCheckBox("#9 Unused")
            self.image9_buttontest.setChecked(False)
            self.menu_split4.addWidget(self.image9_buttontest)

            # Creates a run button
            self.run_button = qtw.QPushButton("Run Model")
            self.run_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.run_button.clicked.connect(self.get_rid_of_checkboxes)
            self.layout().addWidget(self.run_button)

            # Fixes location of start button
            self.layout().addWidget(self.back_button)

    def get_rid_of_checkboxes(self):
        self.name_count()
        if self.done:
            # Removes a million widgets LOL
            self.menu_split1.setParent(None)
            self.menu_split2.setParent(None)
            self.menu_split3.setParent(None)
            self.menu_split4.setParent(None)

            self.image1_buttontest.setParent(None)
            self.image2_buttontest.setParent(None)
            self.image3_buttontest.setParent(None)
            self.image4_buttontest.setParent(None)
            self.image5_buttontest.setParent(None)
            self.image6_buttontest.setParent(None)
            self.image7_buttontest.setParent(None)
            self.image8_buttontest.setParent(None)
            self.image9_buttontest.setParent(None)

            self.run_button.setParent(None)
            
            # Begins the detections
            self.run_button_clicked()

    def run_button_clicked(self):
        # Removes widgets from the layout
        self.thresh_checkbox.setParent(None)
        self.back_button.setParent(None)
        self.next_button.setParent(None)

        # Changes title text
        self.title_label.setText("Count in Progress...")
        
        # Adds a smaller text bar
        self.process_label = qtw.QLabel("Creating directories...")
        self.process_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.process_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.process_label.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.layout().addWidget(self.process_label)
        
        # Adds a progress bar 
        self.progress_bar = qtw.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.layout().addWidget(self.progress_bar)

        # Runs the detections
        self.detection = DetectionThread()
        self.detection.start()
        self.detection.any_signal.connect(self.loading)
        self.detection.finished.connect(self.count_complete)
        
        # Sets the beginning percent for the progress bar
        self.current_percent = 0

    # This function is run any time a signal is emitted from the detection thread
    def loading (self, percent, process):
        if process == 1:
            # Updates the process label
            self.process_label.setText("Cropping images...")

            # Smoothly increases the progress bar
            for i in range(0, percent):
                self.current_percent += 1
                time.sleep(0.05)
                self.progress_bar.setValue(self.current_percent)
        
        if process == 2:
            # Updates the process label
            self.process_label.setText("Running AI detections...")

            # Smoothly increases the progress bar
            for i in range(0, percent):
                self.current_percent += 1
                time.sleep(0.05)
                self.progress_bar.setValue(self.current_percent)
        
        if process == 3:
            # Updates the process label
            self.process_label.setText("Evaluating colors...")

            # Smoothly increases the progress bar
            for i in range(0, percent):
                self.current_percent += 1
                time.sleep(0.05)
                self.progress_bar.setValue(self.current_percent)
        
        if process == 4:
            # Updates the process label
            self.process_label.setText("Wrapping up...")

            # Smoothly increases the progress bar
            for i in range(0, percent):
                self.current_percent += 1
                time.sleep(0.05)
                self.progress_bar.setValue(self.current_percent)

    def count_complete(self):
        time.sleep(1)
        
        self.progress_bar.setParent(None)
        self.process_label.setParent(None)

        # Changes the title and cancel button to fit a "complete" dialog
        self.title_label.setText("Count\n Complete")
        self.back_button.setText("Main Menu")

        # Creates an open pictures button
        self.open_pics = qtw.QPushButton("Open Detection Pictures")
        self.open_pics.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.open_pics.clicked.connect(lambda: self.open_pics_button_clicked(name_of_count))
        self.layout().addWidget(self.open_pics)

        # Creates an open excel button
        self.open_sheet = qtw.QPushButton("Open Count Spreadsheet")
        self.open_sheet.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.open_sheet.clicked.connect(lambda: self.open_sheet_button_clicked(name_of_count))
        self.layout().addWidget(self.open_sheet)

        # Adds the back button
        self.layout().addWidget(self.back_button)

    def open_pics_button_clicked (self, count_name):
        # Opens the images path 
        path = dirs.detections + "/" + count_name + "/images"
        os.startfile(path)

    def open_sheet_button_clicked (self, count_name):
        # Opens the counts spreadsheet from the spreadsheets path
        path = dirs.detections + "/" + count_name + "/spreadsheets/overall_counts.xlsx"
        os.startfile(path)

    def view_past(self):
        # Removes file button and back button
        self.title_label.setParent(None)
        self.begin_button.setParent(None)
        self.past_counts_button.setParent(None)
        self.back_button.setParent(None)

        # Adds a title label
        self.title_label = qtw.QLabel("View Past\nDetection Counts")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a horizontal layout for the label and dropdown menu to reside in
        self.dropdown_layout = qtw.QHBoxLayout()
        self.dropdown_layout.setSpacing(10)
        verticalSpacer = qtw.QSpacerItem(20, 30, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.layout().addLayout(self.dropdown_layout)
        self.layout().addSpacerItem(verticalSpacer)
        
        # Adds a past counts label 
        self.past_counts_label = qtw.QLabel(f"Past Count:")
        self.past_counts_label.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.past_counts_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.past_counts_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.dropdown_layout.addWidget(self.past_counts_label)
        
        # Creates a dropdown menu of available counts
        self.past_counts_dropdown = qtw.QComboBox()
        self.past_counts_dropdown.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.past_counts_dropdown.currentIndexChanged.connect(self.past_counts_dropdown_changed)
        self.past_counts_dropdown.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.dropdown_layout.addWidget(self.past_counts_dropdown)
        

        # Iterates through the detections
        if os.path.isdir(dirs.detections):
            sub_dirs = os.listdir(dirs.detections)
            for item in sub_dirs:
                self.past_counts_dropdown.addItem(item)
                
            if (len(sub_dirs) > 0):
                # Creates a next button
                self.next_button = qtw.QPushButton("Next")
                self.next_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
                self.next_button.clicked.connect(self.next_once_selected)
                self.layout().addWidget(self.next_button)
                self.layout().addWidget(self.back_button)
            else:
                self.past_counts_dropdown.addItem("No Previous Counts")
                self.layout().addWidget(self.back_button)
        else:
            self.past_counts_dropdown.addItem("No Previous Counts")
            self.layout().addWidget(self.back_button)
            
    def next_once_selected(self, index):
        self.title_label.setText("Past Counts")
        self.back_button.setText("Main Menu")

        self.next_button.setParent(None)

        # Creates an open pictures button
        self.open_pics = qtw.QPushButton("Open Detection Images")
        self.open_pics.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.open_pics.clicked.connect(lambda: self.open_pics_button_clicked(self.selection))
        self.layout().addWidget(self.open_pics)

        # Creates an open excel button
        self.open_sheet = qtw.QPushButton("Open Count Spreadsheet")
        self.open_sheet.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.open_sheet.clicked.connect(lambda: self.open_sheet_button_clicked(self.selection))
        self.layout().addWidget(self.open_sheet)

        # Adds the back button
        self.layout().addWidget(self.back_button)

    def past_counts_dropdown_changed(self,index):
        # Records the new selected model (count version) anytime the dropdown menu is changed
        self.selected_model = self.past_counts_dropdown.itemText(index)
        self.selection = self.past_counts_dropdown.itemText(index) 
        return self.selected_model
    
    def back_button_clicked (self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()


# Any instance of this class is run on a separate thread from the rest of the code, which means it runs concurrently with the GUI
class DetectionThread(qtc.QThread):
    # Defines which signals are transmitted to the loading function
    any_signal = qtc.pyqtSignal(int, int)

    def list_image (self, image_dir_counting):
        # Initializes the list of image paths
        images = []

        # Iterates through all the .tif, .jpg, and .png files in the image directory and adds the path to each one
        images1 = Path(image_dir_counting).glob('*.tif')
        for i in images1:
            images.append(i)
        images1 = Path(image_dir_counting).glob('*.jpg')
        for i in images1:
            images.append(i)
        images1 = Path(image_dir_counting).glob('*.png')
        for i in images1:
            images.append(i)

        # Initializes the list of image names
        names = []
        
        # Iterates through each image path and takes its file name WITHOUT the file type extension (.png, .tif, etc)
        for i in images:
            useThing = os.path.basename(i)
            names.append(useThing)

        return [images, names]
    
    def run(self):
        # Sets the initial percentage for the progress bar
        total_percent = 0 

        # Returns the paths and names of the images selected
        images_list = self.list_image(image_dir)

        # Creates required directories
        dirs.new_detection_directory(name_of_count, run_thresh)

        # Updates the percentage of the progress bar
        self.any_signal.emit(20, 1)
            
        # Breaks images into tiles
        tiling.tile(input_image_list=images_list[0], output_tiles_dir=f"{dirs.detections}/{name_of_count}/images/bounding")

        # Updates the percentage of the progress bar
        self.any_signal.emit(50, 2)

        # Runs detections
        with open (dirs.dict, "r") as f:
            model_dict = json.load(f)
        seg_count_and_names = yd.yolo_detect(model_path=model_dict["current_model_directory"], name_of_count=name_of_count)

        # Updates the percentage of the progress bar
        self.any_signal.emit(20, 3)

        # Checks if the user selected mussel thresholding or not
        if run_thresh:
            print("DETECTED TRUE!\nDETECTED TRUE!\nDETECTED TRUE!\nDETECTED TRUE!\nDETECTED TRUE!\n")
            try:
                thresh_count_and_names = thresholding.threshFunction(image_dir, name_of_count, images_list[0],
                                            CountWindow.image1_buttontest.checkState(),
                                            CountWindow.image2_buttontest.checkState(),
                                            CountWindow.image3_buttontest.checkState(),
                                            CountWindow.image4_buttontest.checkState(),
                                            CountWindow.image5_buttontest.checkState(),
                                            CountWindow.image6_buttontest.checkState(),
                                            CountWindow.image7_buttontest.checkState(),
                                            CountWindow.image8_buttontest.checkState(),
                                            CountWindow.image9_buttontest.checkState())
            except:
                thresh_count_and_names = thresholding.threshFunction(image_dir, name_of_count, images_list[0],
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,)

            total_count_array = []
            # Combines the segmentation and thresholding counts to give a total mussel count
            for i in range(len(seg_count_and_names[1])):
                for p in range(len(thresh_count_and_names[1])):
                    if seg_count_and_names[1][i] == thresh_count_and_names[1][p]:
                        seg_element = i
                        thresh_element = p
                total_count_array.append(seg_count_and_names[0][seg_element] + thresh_count_and_names[0][thresh_element])

        # Just segmentation for non-mussel counting
        else:
            total_count_array = seg_count_and_names[0]
        
        # Updates the percentage of the progress bar
        self.any_signal.emit(10, 4)

        # Takes the first sheet generated by directory.py and makes it the totals sheet
        full_path = dirs.detections + "/" + name_of_count + "/spreadsheets/overall_counts.xlsx"
        workbook = openpyxl.load_workbook(full_path)
        sheet1 = workbook["Sheet1"]
        sheet1.title = "Totals"
        workbook.save(full_path)

        # Creates a pandas dataframe with the totals, stylizes it, and then adds it to the excel spreadsheet
        print(len(images_list[1]))
        print(len(total_count_array))
        countSheet = pd.ExcelWriter(full_path, mode="a", engine='openpyxl', if_sheet_exists='replace')
        df = pd.DataFrame({"Image": images_list[1], "Total Count": total_count_array})
        sf = styleframe.StyleFrame(df)
        sf.to_excel(excel_writer=countSheet, sheet_name="Totals", best_fit=["Image", "Total Count"], columns_and_rows_to_freeze='B2', row_to_add_filters=0)
        countSheet.close()


class TrainWindow (qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Create title and author labels within layout
        self.title_label = qtw.QLabel("Train Model")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a file dialog button
        self.yaml_button = qtw.QPushButton("Select Training Config (*.yaml)")
        self.yaml_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.yaml_button.clicked.connect(self.yaml_button_clicked)
        self.layout().addWidget(self.yaml_button)

        # Creates a back button
        self.back_button = qtw.QPushButton("Cancel")
        self.back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(self.back_button)

        # Shows window
        self.show()
        
    def yaml_button_clicked(self):
        # Opens file explorer to choose images
        self.yaml, done = qtw.QFileDialog.getOpenFileName(self, "Open Training Config File", cfg.initial_directory, "YAML file (*.yaml)")

        # Checks if images were chosen
        if self.yaml != "" and done:
            self.yaml_button.setParent(None)
            self.back_button.setParent(None)
            self.train_button = qtw.QPushButton("Begin Model Training")
            self.train_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.train_button.clicked.connect(self.train_button_clicked)
            self.layout().addWidget(self.train_button)
            self.layout().addWidget(self.back_button)

    def train_button_clicked(self):
        self.epochs, done = qtw.QInputDialog.getInt(self, 'Input Dialog', 'Amount of epochs for this training:')
        if self.epochs != "" and done:
            print(self.epochs)
            self.pxsize, done = qtw.QInputDialog.getInt(self, 'Input Dialog', 'Pixel size of the images used for this training (e.g. 640):')
            
            if self.pxsize != "" and done:
                print(self.pxsize)
                self.name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name for this training:')

                if self.name != "" and done:
                    print(self.name)

                    # Closes the window
                    self.close()
                    
                    dirs.new_training_directory()

                    with open(dirs.dict, "r") as f:
                        model_dict = json.load(f)
                        current_model = model_dict["current_model_directory"]

                    yt.new_train(model_path=current_model, yaml=self.yaml, loops=self.epochs, img_size=self.pxsize, name=self.name)
    
    def back_button_clicked(self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()

class SelectWindow (qtw.QWidget): 
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Creates a label within layout
        self.title_label = qtw.QLabel("Select Model")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        self.title_label.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a horizontal layout for the label and dropdown menu to reside in
        self.dropdown_layout = qtw.QHBoxLayout()
        self.dropdown_layout.setSpacing(10)
        verticalSpacer = qtw.QSpacerItem(20, 30, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.layout().addLayout(self.dropdown_layout)
        self.layout().addSpacerItem(verticalSpacer)
        
        # Adds a current model label 
        self.model_label = qtw.QLabel(f"Current Model:")
        self.model_label.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.model_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.dropdown_layout.addWidget(self.model_label)
        
        # Creates a dropdown menu of available models
        self.model_dropdown = qtw.QComboBox()
        self.model_dropdown.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_dropdown.currentIndexChanged.connect(self.model_dropdown_changed)
        self.model_dropdown.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.dropdown_layout.addWidget(self.model_dropdown)

        # Pulls models from modeldict.json and adds them to the dropdown
        with open(dirs.dict, "r") as f:
            model_dict = json.load(f)
            values = list(model_dict.values())
            values.pop(0)
    
        for item in values:
            path = list(model_dict.keys())[list(model_dict.values()).index(item)]
            if path == model_dict["current_model_directory"]:
                self.model_dropdown.addItem(item)
                values.remove(item)

        self.model_dropdown.addItems(values)
        
        # Creates a file dialog button
        file_button = qtw.QPushButton("Add Model File")
        file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        file_button.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)
        
        # Creates button split at bottom of window
        self.menu_split = qtw.QHBoxLayout()
        self.menu_split.setSpacing(10)
        self.layout().addLayout(self.menu_split)

        # Creates a save button
        save_button = qtw.QPushButton("Save")
        save_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        save_button.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        save_button.clicked.connect(self.save_button_clicked)
        self.menu_split.addWidget(save_button)

        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        back_button.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.back_button_clicked)
        self.menu_split.addWidget(back_button)

    def model_dropdown_changed(self,index):
        # Records the new selected model anytime the dropdown menu is changed
        self.selected_model = self.model_dropdown.itemText(index)
        return self.selected_model
    
    def file_button_clicked(self):
        # Opens file explorer to choose a directory
        self.folderpath, _ = qtw.QFileDialog.getOpenFileName(self, 'Select Model File', cfg.initial_directory, "PyTorch Model File (*.pt)")
        with open(dirs.dict, "r") as f:
            model_dict = json.load(f)
        # Checks if a folder was returned and if the folder is already in modeldict.json
        if self.folderpath != "" and self.folderpath not in model_dict:
            self.name_model()
            
    def name_model(self):
        name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name your model:')
        if done and name != "":
            with open(dirs.dict, "r") as f:
                model_dict = json.load(f)
            model_dict[self.folderpath] = name
            with open(dirs.dict, "w") as f:
                json.dump(model_dict, f, indent=4)
            self.model_dropdown.addItem(name)

    def save_button_clicked(self):
        # Changes the current model in modeldict.json to the selected one in the dropdown
        with open(dirs.dict, "r") as f:
            model_dict = json.load(f)
        selected_model_dir = list(model_dict.keys())[list(model_dict.values()).index(self.selected_model)]
        model_dict["current_model_directory"] = selected_model_dir
        with open(dirs.dict, "w") as f:
            json.dump(model_dict, f, indent=4)
        for i in range(self.model_dropdown.count()):
            self.model_dropdown.removeItem(i)
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()

    def back_button_clicked(self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()

# Constructs app
app = qtw.QApplication(sys.argv)

# Constructs window
mw = MainWindow()

# Runs the app 
app.exec()