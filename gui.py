import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

import threading
import json
import sys
import os
import re
import subprocess
import time

from subprocess import Popen

import config as cfg
import internal.scripts.thresholdingClumpCount as thcc
import internal.scripts.createSavableCountingDirectory as cscd
import internal.scripts.makeListOfImages as mloi

cwd = os.getcwd()

def defaultUI(window):
    # Adds a title 
    window.setWindowTitle("MCount")

    # Sets app icon
    window.setWindowIcon(qtg.QIcon(cwd + '/internal/resources/icon.jpg'))

    # Sets default layout for entire window
    window.setLayout(qtw.QVBoxLayout())
    window.layout().setSpacing(15)
    
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
        self.file_button = qtw.QPushButton("Select images folder from file explorer")
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
        
        #Checks if images were chosen
        if image_dir != "":
            # Removes file button and back button
            self.file_button.setParent(None)
            self.back_button.setParent(None)

            # Creates checkboxes for thresholding and spreadsheet
            self.thresh_button = qtw.QCheckBox("Run Mussel Thresholding")
            self.thresh_button.setChecked(True)
            self.layout().addWidget(self.thresh_button)
            self.sheet_button = qtw.QCheckBox("Create Excel Spreadsheet with Counts")
            self.sheet_button.setChecked(True)
            self.layout().addWidget(self.sheet_button)

            # Creates a run button
            self.run_button = qtw.QPushButton("Run Model")
            self.run_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
            self.run_button.clicked.connect(self.run_button_clicked)
            self.layout().addWidget(self.run_button)

            # Adds the back button
            self.layout().addWidget(self.back_button)

    def back_button_clicked (self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()

    def run_button_clicked(self):
        #name the count
        name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name this counting:')
        name_of_the_count = "temp"
        if name and done:
            self.close()
            name_of_the_count = name


        if (done):
            listImages = mloi.listImage(image_dir)
            cscd.creatCountDirectorySaving(listImages, name_of_the_count)
            # Removes widgets from the layout
            self.thresh_button.setParent(None)
            self.sheet_button.setParent(None)
            self.back_button.setParent(None)
            self.run_button.setParent(None)
            # Changes title text
            self.title_label.setText("Count in Progress...")
            self.layout().addWidget(self.back_button)

            #if thresh button is checked run the file
            if (self.thresh_button.checkState()):
                thcc.threshFunction(image_dir, name_of_the_count)

            self.title_label.setText("Done")



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
        self.xml_button = qtw.QPushButton("Select image configs from file explorer")
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
            self.labelmap_button = qtw.QPushButton("Select labelmap from file explorer")
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
    
    def ckpt_parse(self):
        # Parses ckpts and chooses the highest one
        files = os.listdir(self.model_dir)
        num_check = re.compile(r'\d+')
        ckpt_files = []
        for file in files:
            match = num_check.findall(file)
            if match:
                ckpt_files.append((int(match[0]), file))
        self.last_ckpt = os.path.splitext(max(ckpt_files, key = lambda x: x[0])[1])[0]
        
        # Writes tfrecord and ckpt paths in pipeline.config
        with open(self.pipeline_dir, "r") as f:
            config = json.load(f)
        config["train_config"]["fine_tune_checkpoint"] = self.model_dir + "/" + self.last_ckpt
        config["train_input_reader"]["label_map_path"] = self.labelmap
        config["train_input_reader"]["tf_record_input_reader"]["input_path"] = self.tfrecord_dir + f"{self.name}.record"
        with open (self.pipeline_dir, "w") as f:
            json.dump(config, f)

    def train_button_clicked(self):
        self.name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name this training:')
        if self.name != "" and done:
            # Closes the window
            self.close()
            
            # Defines paths to model folders/files
            with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            self.tfrecord_dir = cwd + "/external/training/"
            script_name = "internal/scripts/generate_tfrecord.py"
            self.model_dir = model_dict["current_model_directory"]
            self.pipeline_dir = self.model_dir + "/pipeline.config"
            
            self.ckpt_parse()
            
            # Opens CMD and runs tfrecord generation, then begins training (I don't know a good way to seperate these processes)
            subprocess.Popen(["start", "cmd", "/k" "python", script_name, "-x", self.xml_dir, "-l", self.labelmap, "-o", self.tfrecord_dir + f"{self.name}.record", "-i", self.xml_dir, "-c", self.tfrecord_dir + f"{self.name}.csv"], shell=True)
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
        file_button = qtw.QPushButton("Add model folder from file explorer")
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



