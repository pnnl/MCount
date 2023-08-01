import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import os

default_font = 'Lelawadee'

def defaultUI(window):
    # Adds a title 
    window.setWindowTitle("Mussel Counter")

    # Sets app icon
    window.setWindowIcon(qtg.QIcon('icon.jpg'))

    # Sets window size
    window.resize(500, 400)


class MainWindow(qtw.QMainWindow):
    # Defines window initialization
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Sets title widget layout 
        title_layout = qtw.QVBoxLayout()
        header_widget = qtw.QWidget()
        title_layout.setSpacing(5)
        title_layout.setAlignment(qtc.Qt.AlignTop)
        title_layout.setGeometry(100, 100)
        header_widget.setLayout(title_layout)

        # Create title and author labels within layout
        title_label = qtw.QLabel("M-Count")
        title_label.setFont(qtg.QFont(default_font, 36))
        title_label.setAlignment(qtc.Qt.AlignCenter)
        title_layout.layout().addWidget(title_label)
        author_label = qtw.QLabel("By Navaj Nune and Lance Miller")
        author_label.setFont(qtg.QFont(default_font, 14))
        author_label.setAlignment(qtc.Qt.AlignCenter)
        title_layout.layout().addWidget(author_label)

        # Creates button layout
        button_widget = qtw.QWidget()
        button_layout = qtw.QVBoxLayout()
        button_layout.setSpacing(5)
        button_layout.setAlignment(qtc.Qt.AlignBottom)
        button_widget.setLayout(title_layout)

        # Creates buttons within layout
        run_button = qtw.QPushButton("Model Run")
        run_button.setFont(qtg.QFont(default_font, 14))
        run_button.clicked.connect(self.run_button_clicked)
        button_layout.addWidget(run_button)

        train_button = qtw.QPushButton("Model Gym")
        train_button.setFont(qtg.QFont(default_font, 14))
        train_button.clicked.connect(self.train_button_clicked)
        button_layout.addWidget(train_button)

        help_button = qtw.QPushButton("Help")
        help_button.setFont(qtg.QFont(default_font, 14))
        help_button.clicked.connect(self.help_button_clicked)
        button_layout.addWidget(help_button)

        # Shows window
        self.show()

    def run_button_clicked(self):
        self.rw = RunWindow()
        self.rw.show()
        self.close()

    def train_button_clicked(self):
        self.tw = TrainWindow()
        self.tw.show()
        self.close()

    def help_button_clicked(self):
        os.startfile('README.md')


class RunWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Adds the default UI elements
        defaultUI(self)

        # Sets widget layout 
        self.setLayout(qtw.QVBoxLayout())

        # Creates a label within layout
        title_label = qtw.QLabel("Run Model")
        title_label.setFont(qtg.QFont(default_font, 36))
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

        # Creates a file dialog button
        file_button = qtw.QPushButton("Select images from file explorer")
        file_button.setFont(qtg.QFont(default_font, 14))
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)
    
        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(default_font, 14))
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
        self.mw.show()
        self.close()


class TrainWindow (qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        
        defaultUI(self)

        # Sets widget layout 
        self.setLayout(qtw.QVBoxLayout())

        # Create title and author labels within layout
        title_label = qtw.QLabel("Train Model")
        title_label.setFont(qtg.QFont(default_font, 36))
        title_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(title_label)

        # Creates a file dialog button
        file_button = qtw.QPushButton("Select image configs from file explorer")
        file_button.setFont(qtg.QFont(default_font, 14))
        file_button.clicked.connect(self.file_button_clicked)
        self.layout().addWidget(file_button)

        # Creates a back button
        back_button = qtw.QPushButton("Cancel")
        back_button.setFont(qtg.QFont(default_font, 14))
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
        self.mw.show()
        self.close()




# Constructs app
app = qtw.QApplication([])

# Constructs window
mw = MainWindow()

# Runs the app 
app.exec_()