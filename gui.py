import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

import json
import sys
import os
import subprocess
import time
import textwrap
import numpy as np
import pandas as pd
from pathlib import Path

from subprocess import Popen

import config as cfg
import internal.scripts.tiling as tiling
import internal.scripts.thresholding as thresholding
import internal.scripts.directory as directory
#import internal.scripts.detections as detections

cwd = (os.getcwd()).replace("\\", "/")
print (cwd)

def defaultUI(window):
    # Adds a title 
    window.setWindowTitle("MCount")

    # Sets app icon
    window.setWindowIcon(qtg.QIcon(cwd + '/internal/resources/icon.jpg'))

    # Sets default layout for entire window
    window.setLayout(qtw.QVBoxLayout())
    window.layout().setSpacing(12)
    
    # Creates window at specific size
    window.setMinimumSize(500, 325)
    window.setMaximumSize(501, 326)


class MainWindow(qtw.QWidget):
    # Defines window initialization
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Create title and author labels within vertical layout
        self.title_label = qtw.QLabel("MCount")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignCenter)
        self.title_label.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.layout().addWidget(self.title_label)
        author_label = qtw.QLabel("By Lance Miller and Navaj Nune")
        author_label.setFont(qtg.QFont(cfg.default_font, 9))
        author_label.setAlignment(qtc.Qt.AlignCenter)
        author_label.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.layout().addWidget(author_label)

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
        self.cw = CountWindow()
        self.cw.move(self.pos())
        self.cw.show()
        self.close()

    def train_button_clicked(self):
        self.tw = TrainWindow()
        self.tw.move(self.pos())
        self.tw.show()
        self.close()
    
    def select_button_clicked(self):
        self.sw = SelectWindow()
        self.sw.move(self.pos())
        self.sw.show()
        self.close()

    def help_button_clicked(self):
        os.startfile('README.md')
    
    def quit_button_clicked(self):
        self.close()


class CountWindow(qtw.QWidget):
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
        self.title_label.setAlignment(qtc.Qt.AlignCenter)
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
        self.begin_button.setParent(None)
        self.past_counts_button.setParent(None)
        self.back_button.setParent(None)

        # Changes title text
        self.title_label.setText("New Count")
        
        # Creates a file dialog button
        self.file_button = qtw.QPushButton("Select Input Images Folder")
        self.file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(self.file_button)

        # Creates a back button
        self.back_button = qtw.QPushButton("Cancel")
        self.back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(self.back_button)


    def file_button_clicked(self):
        global image_dir

        # Opens file explorer to choose images
        image_dir = qtw.QFileDialog.getExistingDirectory(self, "Open Images Folder", cfg.initial_directory)

        with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
            model_dict = json.load(f)
            current_model_name = model_dict[model_dict["current_model_directory"]]
        
        if image_dir and current_model_name == "MCount Mussel Detector":
            # Bypasses the labelmap file dialog
            global labelmap_bypass
            labelmap_bypass = True
            self.default_labelmap = cwd + "/internal/model/annotations/labelmap.pbtxt"
            self.labelmap = self.default_labelmap
            
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
        if labelmap_bypass == False:
            self.labelmap, _ = qtw.QFileDialog.getOpenFileName(self, "Open Label Map File", cfg.initial_directory, "Protocol Buffer Text File (*.pbtxt)")
        if self.labelmap or labelmap_bypass == True:
            # Does formatting stuff
            self.labelmap_button.setParent(None)
            self.back_button.setParent(None)

            # Creates checkboxes for thresholding and spreadsheet
            self.thresh_button = qtw.QCheckBox("Run Thresholding")
            self.thresh_button.setChecked(True)
            self.layout().addWidget(self.thresh_button)
            self.sheet_button = qtw.QCheckBox("Create Excel Spreadsheet with Counts")
            self.sheet_button.setChecked(True)
            #self.layout().addWidget(self.sheet_button)

            # Creates a run button
            self.next_button = qtw.QPushButton("Next")
            self.next_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.next_button.clicked.connect(self.select_images)
            self.layout().addWidget(self.next_button)
            
            # Adds the back button
            self.layout().addWidget(self.back_button)

    def select_images(self):
        if (self.thresh_button.checkState()):
            self.thresh_button.setParent(None)
            self.next_button.setParent(None)

            self.title_label.setText("Select Images\nTo Save")

            
            # Creates help/quit button split at bottom
            self.menu_split1 = qtw.QHBoxLayout()
            self.menu_split1.setSpacing(10)
            self.layout().addLayout(self.menu_split1)
            self.menu_split2 = qtw.QHBoxLayout()
            self.menu_split2.setSpacing(10)
            self.layout().addLayout(self.menu_split2)
            self.menu_split3 = qtw.QHBoxLayout()
            self.menu_split3.setSpacing(10)
            self.layout().addLayout(self.menu_split3)
            self.menu_split4 = qtw.QHBoxLayout()
            self.menu_split4.setSpacing(10)
            self.layout().addLayout(self.menu_split4)
            self.menu_split5 = qtw.QHBoxLayout()
            self.menu_split5.setSpacing(10)
            self.layout().addLayout(self.menu_split5)

            
            # Creates checkboxes for saving images
            self.image1_buttontest = qtw.QCheckBox("#1 Original")
            self.image1_buttontest.setChecked(True)
            self.menu_split1.addWidget(self.image1_buttontest)

            self.image2_buttontest = qtw.QCheckBox("#2 Red Segmentation")
            self.image2_buttontest.setChecked(False)
            self.menu_split2.addWidget(self.image2_buttontest)

            self.image3_buttontest = qtw.QCheckBox("#3 Grayscale")
            self.image3_buttontest.setChecked(False)
            self.menu_split3.addWidget(self.image3_buttontest)

            self.image4_buttontest = qtw.QCheckBox("#4 Blurred")
            self.image4_buttontest.setChecked(False)
            self.menu_split4.addWidget(self.image4_buttontest)

            self.image5_buttontest = qtw.QCheckBox("#5 Thresholding")
            self.image5_buttontest.setChecked(True)
            self.menu_split5.addWidget(self.image5_buttontest)

            self.image6_buttontest = qtw.QCheckBox("#6 Closing")
            self.image6_buttontest.setChecked(False)
            self.menu_split1.addWidget(self.image6_buttontest)

            self.image7_buttontest = qtw.QCheckBox("#7 Lay Over")
            self.image7_buttontest.setChecked(True)
            self.menu_split2.addWidget(self.image7_buttontest)

            self.image8_buttontest = qtw.QCheckBox("#8 Extra")
            self.image8_buttontest.setChecked(False)
            self.menu_split3.addWidget(self.image8_buttontest)

            self.image9_buttontest = qtw.QCheckBox("#9 Unused")
            self.image9_buttontest.setChecked(False)
            self.menu_split4.addWidget(self.image9_buttontest)

            # Creates a run button
            self.run_button = qtw.QPushButton("Run Model")
            self.run_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.run_button.clicked.connect(self.run_button_clicked)
            self.layout().addWidget(self.run_button)

            #fixes location of start button
            self.layout().addWidget(self.back_button)

    def view_past(self):
        # Removes file button and back button
        self.title_label.setParent(None)
        self.begin_button.setParent(None)
        self.past_counts_button.setParent(None)

        self.selection = ""

        self.title_label = qtw.QLabel("View Past\nDetection Counts")
        self.title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a horizontal layout for the label and dropdown menu to reside in
        self.dropdown_layout = qtw.QHBoxLayout()
        self.dropdown_layout.setSpacing(10)
        verticalSpacer = qtw.QSpacerItem(20, 30, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.layout().addLayout(self.dropdown_layout)
        self.layout().addSpacerItem(verticalSpacer)
        
        # Adds a past counts label 
        self.model_label = qtw.QLabel(f"Past Count:")
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.model_label.setSizePolicy(size_policy)
        self.model_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_label.setAlignment(qtc.Qt.AlignCenter)
        self.dropdown_layout.addWidget(self.model_label)
        
        # Creates a dropdown menu of available counts
        self.model_dropdown = qtw.QComboBox()
        self.model_dropdown.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_dropdown.currentIndexChanged.connect(self.model_dropdown_changed)
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.model_dropdown.setSizePolicy(size_policy)
        self.dropdown_layout.addWidget(self.model_dropdown)

        # Pulls models from modeldict.json and adds them to the dropdown
        directory = cwd + "/external/detections"
        dirs = os.listdir(directory)
        dirs.remove("placeholder")
        for item in dirs:
            self.model_dropdown.addItem(item)
           

        if (len(dirs) > 0):
            # Creates a next button
            self.next_button = qtw.QPushButton("Next")
            self.next_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.next_button.clicked.connect(self.next_once_selected)
            self.layout().addWidget(self.next_button)
        else:
            self.model_dropdown.addItem("No Previous Counts")


        self.layout().addWidget(self.back_button)

    def next_once_selected(self, index):
        self.title_label.setText("Past Counts")
        self.back_button.setText("Main Menu")

        self.next_button.setParent(None)
        #self.model_dropdown.setParent(None)
        #self.model_label.setParent(None)
        
        # Creates an open pictures button
        self.open_pics = qtw.QPushButton("Open Detection Pictures")
        self.open_pics.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.open_pics.clicked.connect(lambda: self.open_pics_button_clicked(self.selection))
        self.layout().addWidget(self.open_pics)

        # Creates an open excell button
        self.open_sheet = qtw.QPushButton("Open Excel Count")
        self.open_sheet.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.open_sheet.clicked.connect(lambda: self.open_sheet_button_clicked(self.selection))
        self.layout().addWidget(self.open_sheet)

        # Adds the back button
        self.layout().addWidget(self.back_button)

    def model_dropdown_changed(self,index):
        # Records the new selected model (count version) anytime the dropdown menu is changed
        self.selected_model = self.model_dropdown.itemText(index)
        self.selection = self.model_dropdown.itemText(index) 
        return self.selected_model
    
    def back_button_clicked (self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()

    def open_pics_button_clicked (self, countName):
        #subprocess.Popen(f'explorer /select,"{cwd}/external/detections/{countName}/images"')
        paths = "external\\detections\\"+  countName + "\\images"
        os.startfile(paths)

    def open_sheet_button_clicked (self, countName):
        paths = "external\\detections\\"+  countName + "\\spreadsheets"
        os.startfile(paths)

    def run_button_clicked(self):
        #name the count
        name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name this counting:')
        name_of_count = "Unamed"
        if name and done:
            name_of_count = name
        
        #print(name_of_the_count)

        if done:
            list_images = self.list_image(image_dir)
            directory.creatCountDirectorySaving(list_images[1], name_of_count)
            # Removes widgets from the layout
            self.thresh_button.setParent(None)
            self.sheet_button.setParent(None)
            self.back_button.setParent(None)
            self.run_button.setParent(None)
            # Changes title text
            self.title_label.setText("Count in Progress ...")
            self.layout().addWidget(self.back_button)

            tiling.tile(input_image_list=list_images[0], output_tiles_dir=f"{cwd}/external/detections/{name_of_count}/images/segmentation")

            with open (f"{cwd}/internal/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            #detections.detect(model_path=model_dict["current_model_directory"], name_of_count=name_of_count, labelmap_path=self.labelmap)
            
            # if thresh button is checked run the file
            if (self.thresh_button.checkState()):
                thresholding.threshFunction(image_dir, name_of_count, list_images[0],
                                            self.image1_buttontest,
                                            self.image2_buttontest,
                                            self.image3_buttontest,
                                            self.image4_buttontest,
                                            self.image5_buttontest,
                                            self.image6_buttontest,
                                            self.image7_buttontest,
                                            self.image8_buttontest,
                                            self.image9_buttontest)

            self.title_label.setText("Detection\nComplete")
            self.back_button.setText("Main Menu")

            # Creates an open pictures button
            self.open_pics = qtw.QPushButton("Open Detection Pictures")
            self.open_pics.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.open_pics.clicked.connect(lambda: self.open_pics_button_clicked(name_of_count))
            self.layout().addWidget(self.open_pics)

            # Creates an open excell button
            self.open_sheet = qtw.QPushButton("Open Excel Count")
            self.open_sheet.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.open_sheet.clicked.connect(lambda: self.open_sheet_button_clicked(name_of_count))
            self.layout().addWidget(self.open_sheet)

            # Adds the back button
            self.layout().addWidget(self.back_button)

    
    def list_image (self, image_dir_counting):
        images = []

        images1 = Path(image_dir_counting).glob('*.tif')
        for i in images1:
            images.append(i)
        images1 = Path(image_dir_counting).glob('*.jpg')
        for i in images1:
            images.append(i)
        images1 = Path(image_dir_counting).glob('*.png')
        for i in images1:
            images.append(i)

        names = []
        
        for i in images:
            #temp = ntpath.abspath(i)
            #thingImage = temp.split("\\")
            #useThing = thingImage[len(thingImage)-1][0:len(thingImage[len(thingImage)-1])-4]
            useThing = os.path.basename(i)
            
            names.append(useThing)

        return [images, names]


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
        self.title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a file dialog button
        self.xml_button = qtw.QPushButton("Select Image Configs (.xml)")
        self.xml_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.xml_button.clicked.connect(self.xml_button_clicked)
        self.layout().addWidget(self.xml_button)

        # Creates a back button
        self.back_button = qtw.QPushButton("Cancel")
        self.back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(self.back_button)

        # Shows window
        self.show()
        
    def xml_button_clicked(self):
        # Opens file explorer to choose images
        self.xml_dir = qtw.QFileDialog.getExistingDirectory(self, "Open Image Config Folder", cfg.initial_directory)
        
        # Checks if images were chosen
        if self.xml_dir:
            self.xml_button.setParent(None)
            self.back_button.setParent(None)
            self.labelmap_button = qtw.QPushButton("Select Labelmap (.pbtxt)")
            self.labelmap_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.labelmap_button.clicked.connect(self.labelmap_button_clicked)
            self.layout().addWidget(self.labelmap_button)
            self.layout().addWidget(self.back_button)

    def labelmap_button_clicked(self):
        self.labelmap, _ = qtw.QFileDialog.getOpenFileName(self, "Open Label Map File", cfg.initial_directory, "Protocol Buffer Text File (*.pbtxt)")
        if self.labelmap:
            self.labelmap_button.setParent(None)
            self.back_button.setParent(None)
            self.train_button = qtw.QPushButton("Begin Model Training")
            self.train_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.train_button.clicked.connect(self.train_button_clicked)
            self.layout().addWidget(self.train_button)
            self.layout().addWidget(self.back_button)
    
    def config_parse(self):
        # Sets important config keys
        key1 = "input_path:"
        key2 = "label_map_path:"
        key3 = "fine_tune_checkpoint:"

        # Reads the  config file and processes lines
        with open(self.model_dir + "/pipeline.config", "r") as file:
            lines = file.readlines()

        # Changes lines that contain the right keys to give correct paths 
        for i, line in enumerate(lines):
            if key1 in line:
                lines[i] = textwrap.indent(f'{key1} "{self.tfrecord_dir}" \n', "    ")
            
            elif key2 in line:
                lines[i] = textwrap.indent(f'{key2} "{self.labelmap}" \n', "  ")

            elif key3 in line:
                lines[i] = textwrap.indent(f'{key3} "{self.ckpt_path}" \n', "  ")
            
        # Writes the modified lines back to the file
        with open(self.model_dir + "/pipeline.config", "w") as file:
            file.writelines(lines)

    def train_button_clicked(self):
        self.name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name this training:')
        if self.name != "" and done:
            # Closes the window
            self.close()
            
            # Defines paths to model folders/files
            with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            self.tfrecord_dir = cwd + "/external/training/"+ f"{self.name}.record"
            self.csv_path = cwd + "/external/training/"+ f"{self.name}.csv"
            self.script_name = cwd + "/internal/scripts/tefrecord_generation.py"
            self.model_dir = model_dict["current_model_directory"]
            self.ckpt_path = self.model_dir + "/reference_model/checkpoint/ckpt-0"
            self.pipeline_dir = self.model_dir + "/pipeline.config"
            
            self.config_parse()
            
            # Opens CMD and runs tfrecord generation, then begins training (I don't know a good way to seperate these processes)
            subprocess.Popen(["start", "cmd", "/k", "python", self.script_name, "-x", self.xml_dir, "-l", self.labelmap, "-o", self.tfrecord_dir, "-i", self.xml_dir, "-c", self.csv_path], shell=True)
            time.sleep(5)
            subprocess.Popen(["start", "cmd", "/k", "python", f"{cwd}/internal/scripts/model_main_tf2.py", f"--model_dir={self.model_dir}", f"--pipeline_config_path={self.model_dir}/pipeline.config"], shell=True)
    
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
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.title_label.setSizePolicy(size_policy)
        self.title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        self.title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(self.title_label)

        # Creates a horizontal layout for the label and dropdown menu to reside in
        self.dropdown_layout = qtw.QHBoxLayout()
        self.dropdown_layout.setSpacing(10)
        verticalSpacer = qtw.QSpacerItem(20, 30, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.layout().addLayout(self.dropdown_layout)
        self.layout().addSpacerItem(verticalSpacer)
        
        # Adds a current model label 
        self.model_label = qtw.QLabel(f"Current Model:")
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.model_label.setSizePolicy(size_policy)
        self.model_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_label.setAlignment(qtc.Qt.AlignCenter)
        self.dropdown_layout.addWidget(self.model_label)
        
        # Creates a dropdown menu of available models
        self.model_dropdown = qtw.QComboBox()
        self.model_dropdown.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_dropdown.currentIndexChanged.connect(self.model_dropdown_changed)
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.model_dropdown.setSizePolicy(size_policy)
        self.dropdown_layout.addWidget(self.model_dropdown)

        # Pulls models from modeldict.json and adds them to the dropdown
        with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
            model_dict = json.load(f)
            values = list(model_dict.values())
        directory = model_dict["current_model_directory"]
        model_name = model_dict[directory]
        self.model_dropdown.addItem(model_name)
        for item in values[1:]:
            if item != model_name:
                self.model_dropdown.addItem(item)
        
        # Creates a file dialog button
        file_button = qtw.QPushButton("Add Model Folder")
        file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        file_button.setSizePolicy(size_policy)
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)
        
        # Creates help/quit button split at bottom of window
        self.menu_split = qtw.QHBoxLayout()
        self.menu_split.setSpacing(10)
        self.layout().addLayout(self.menu_split)

        # Creates a save button
        save_button = qtw.QPushButton("Save")
        save_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        save_button.setSizePolicy(size_policy)
        save_button.clicked.connect(self.save_button_clicked)
        self.menu_split.addWidget(save_button)

        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        back_button.setSizePolicy(size_policy)
        back_button.clicked.connect(self.back_button_clicked)
        self.menu_split.addWidget(back_button)

    def model_dropdown_changed(self,index):
        # Records the new selected model anytime the dropdown menu is changed
        self.selected_model = self.model_dropdown.itemText(index)
        return self.selected_model
    
    def file_button_clicked(self):
        # Opens file explorer to choose a directory
        self.folderpath = qtw.QFileDialog.getExistingDirectory(self, 'Select Model Folder', cfg.initial_directory)
        with open(fr"{cwd}\internal/resources\modeldict.json", "r") as f:
            model_dict = json.load(f)
        # Checks if a folder was returned and if the folder is already in modeldict.json
        if self.folderpath != "" and self.folderpath not in model_dict:
            self.name_model()
            
    def name_model(self):
        name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name your model:')
        if done and name != "":
            with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            model_dict[self.folderpath] = name
            with open(f"{cwd}/internal/resources/modeldict.json", "w") as f:
                json.dump(model_dict, f, indent=4)
            self.model_dropdown.addItem(name)

    def save_button_clicked(self):
        # Changes the current model in modeldict.json to the selected one in the dropdown
        with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
            model_dict = json.load(f)
        selected_model_dir = list(model_dict.keys())[list(model_dict.values()).index(self.selected_model)]
        model_dict["current_model_directory"] = selected_model_dir
        with open(f"{cwd}/internal/resources/modeldict.json", "w") as f:
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
app.exec_()