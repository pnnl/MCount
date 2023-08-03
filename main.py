import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

import json
import os

import config as cfg



cwd = os.getcwd()

def defaultUI(window):
    # Adds a title 
    window.setWindowTitle("Mussel Counter")

    # Sets app icon
    window.setWindowIcon(qtg.QIcon(r'C:\Users\mill286\OneDrive - PNNL\Desktop\Mussel-Counting-AI-App\\resources\icon.jpg'))

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
        run_button = qtw.QPushButton("Count Mussels")
        run_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        run_button.clicked.connect(self.run_button_clicked)
        self.layout().addWidget(run_button)
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

    def run_button_clicked(self):
        self.rw = RunWindow()
        self.rw.move(self.pos())
        self.rw.show()
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


class RunWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Creates a title label within layout
        title_label = qtw.QLabel("Run Model")
        title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

        # Creates a file dialog button
        file_button = qtw.QPushButton("Select input images from file explorer")
        file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)
    
        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(back_button)

    def file_button_clicked(self):
        # Opens file explorer to choose images
        file_names, _ = qtw.QFileDialog.getOpenFileNames(self, "Open Images", "", "Image Files (*.png *.jpg *.tif)")
        
        #Checks if images were chosen
        if file_names == ([], ''):
            pass
        else: 
            for i in range(len(file_names)):
                os.startfile(file_names[i])

    def back_button_clicked (self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()


class TrainWindow (qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        
        defaultUI(self)

        # Create title and author labels within layout
        title_label = qtw.QLabel("Train Model")
        title_label.setFont(qtg.QFont(cfg.default_font, cfg.header_font_size))
        title_label.setStyleSheet(f'color: {cfg.header_color}; font-weight: bold;')
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

        # Creates a file dialog button
        file_button = qtw.QPushButton("Select image configs from file explorer")
        file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)

        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(back_button)

        # Shows window
        self.show()
    
    def file_button_clicked(self):
        # Opens file explorer to choose images
        file_names, _ = qtw.QFileDialog.getOpenFileNames(self, "Open Image Config Files", "", "XML Files (*.xml)")
        
        # Checks if images were chosen
        if file_names == ([], ''):
            pass
        else: 
            for i in range(len(file_names)):
                os.startfile(file_names[i])
    
    def back_button_clicked (self):
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
        with open(fr"{cwd}\resources\modeldict.json", "r") as f:
            model_dict = json.load(f)
        directory = model_dict["current_model_directory"]
        model_name = model_dict[directory]
        
        # Adds a current model label 
        self.model_label = qtw.QLabel(f"Current Model: {model_name}")
        self.model_label.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        self.model_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(self.model_label)

        # Creates a file dialog button
        file_button = qtw.QPushButton("Add a new model folder from file explorer")
        file_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)
    
        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(cfg.default_font, cfg.button_font_size))
        back_button.clicked.connect(self.back_button_clicked)
        self.layout().addWidget(back_button)

    def file_button_clicked(self):
        # Opens file explorer to choose a directory
        self.folderpath = qtw.QFileDialog.getExistingDirectory(self, 'Select Folder')
        with open(fr"{cwd}\resources\modeldict.json", "r") as f:
            model_dict = json.load(f)
        # Checks if a folder was chosen
        if self.folderpath == "":
            pass
        elif self.folderpath in model_dict:
            # Records the new model directory in json
            with open(f"{cwd}/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            model_dict["current_model_directory"] = self.folderpath
            with open(f"{cwd}/resources/modeldict.json", "w") as f:
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
            with open(f"{cwd}/resources/modeldict.json", "r") as f:
                model_dict = json.load(f)
            model_dict["current_model_directory"] = self.folderpath
            model_dict[self.folderpath] = name
            with open(f"{cwd}/resources/modeldict.json", "w") as f:
                json.dump(model_dict, f, indent=4)
            self.model_label.setText(f"Current Model: {name}")

    def back_button_clicked (self):
        self.mw = MainWindow()
        self.mw.move(self.pos())
        self.mw.show()
        self.close()


# Constructs app
app = qtw.QApplication([])

# Constructs window
mw = MainWindow()

# Runs the app 
app.exec_()