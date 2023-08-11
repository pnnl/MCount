import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

import threading
import json
import sys
import os
import subprocess

import config as cfg
import thresholdingClumpCount as thcc

cwd = os.getcwd()

def defaultUI(window):
    # Adds a title 
    window.setWindowTitle("MCount")

    # Sets app icon
    window.setWindowIcon(qtg.QIcon(cwd + '/internal/resources/icon.jpg'))

    # Sets default layout for entire window
    window.setLayout(qtw.QVBoxLayout())
    window.layout().setSpacing(10)

    # window.layout().setSizeConstraint(qtw.QLayout.SetMinimumSize)
    
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
        title_label = qtw.QLabel("MCount")
        title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        title_label.setAlignment(qtc.Qt.AlignCenter)
        title_label.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.layout().addWidget(title_label)
        author_label = qtw.QLabel("By Navaj Nune and Lance Miller")
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
        title_label = qtw.QLabel("Count")
        title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

        # Creates a file dialog button
        self.file_button = qtw.QPushButton("Select input images from file explorer")
        self.file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(self.file_button)    
        
        # Creates a back button
        self.back_button = qtw.QPushButton("Cancel")
        self.back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(self.back_button)

    def file_button_clicked(self):
        # Opens file explorer to choose images
        file_names, _ = qtw.QFileDialog.getOpenFileNames(self, "Open Images", cfg.initial_directory, "Image Files (*.png *.jpg *.tif)")
        
        #Checks if images were chosen
        if file_names == []:
            pass
        else:
            print(file_names)
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
            self.run_button.clicked.connect(self.cont_button_clicked)
            self.layout().addWidget(self.run_button)

            # Adds the back button
            self.layout().addWidget(self.back_button)

            # Opens files 
            for i in range(len(file_names)):
                os.startfile(file_names[i])

    def back_button_clicked (self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()

    def cont_button_clicked(self):
        # Removes widgets from the layout
        self.thresh_button.setParent(None)
        self.sheet_button.setParent(None)
        self.back_button.setParent(None)
        self.layout().addWidget(self.back_button)


class TrainWindow (qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Create title and author labels within layout
        title_label = qtw.QLabel("Train Model")
        title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

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
            
    def train_button_clicked(self):
        self.close()
        tfrecord_dir = cwd + "/external/training"
        script_name = "internal/scripts/generate_tfrecord.py"
        subprocess.Popen(["start", "cmd", "/k", "python", script_name, "-x", self.xml_dir, "-l", self.labelmap, "-o", tfrecord_dir, "-i", self.xml_dir, "-c", tfrecord_dir], shell=True)
     
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
        title_label = qtw.QLabel("Select Model")
        title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

        # Checks json for current model directory and corresponding name
        with open(fr"{cwd}\internal\resources\modeldict.json", "r") as f:
            model_dict = json.load(f)
        directory = model_dict["current_model_directory"]
        model_name = model_dict[directory]

        # Creates a horizontal layout for the label and dropdown menu to reside in
        self.dropdown_layout = qtw.QHBoxLayout()
        self.layout().addChildLayout(self.dropdown_layout)
        
        # Adds a current model label 
        self.model_label = qtw.QLabel(f"Current Model:")
        self.model_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addChildWidget(self.model_label)
        
        # Creates a dropdown menu of available models
        self.model_dropdown = qtw.QComboBox()
        with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
            model_dict = json.load(f)
            values = list(model_dict.values())
            print(values)
        for item in values:
            self.model_dropdown.addItem(values[item])
        self.dropdown_layout.addWidget(self.model_dropdown)


        # Creates a file dialog button
        file_button = qtw.QPushButton("Add model folder from file explorer")
        file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)
    
        # Creates a back button
        back_button = qtw.QPushButton("Back to main menu")
        back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(back_button)

    def file_button_clicked(self):
        # Opens file explorer to choose a directory
        self.folderpath = qtw.QFileDialog.getExistingDirectory(self, 'Select Model Folder', cfg.initial_directory)
        with open(fr"{cwd}\internal/resources\modeldict.json", "r") as f:
            model_dict = json.load(f)
        # Checks if a folder was chosen
        if self.folderpath == "":
            pass
        elif self.folderpath in model_dict:
            # Records the new model directory in json
            with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            model_dict["current_model_directory"] = self.folderpath
            with open(f"{cwd}/internal/resources/modeldict.json", "w") as f:
                json.dump(model_dict, f, indent=4)
            self.model_label.setText(f"Current Model: {model_dict[self.folderpath]}")
        else:
            print(self.folderpath)
            print(model_dict)
            self.name_model()
    
    def name_model(self):
        name, done = qtw.QInputDialog.getText(self, 'Input Dialog', 'Name your model:')
        if done and name != "":
            # Records the new model directory and its corresponding name in json
            with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            model_dict["current_model_directory"] = self.folderpath
            model_dict[self.folderpath] = name
            with open(f"{cwd}/internal/resources/modeldict.json", "w") as f:
                json.dump(model_dict, f, indent=4)
            self.model_label.setText(f"Current Model: {name}")

    def back_button_clicked (self):
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