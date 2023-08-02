import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Buttons in Centered Horizontal Layout')

        # Create the main vertical box layout
        main_layout = QVBoxLayout(self)

        # Add any other widgets you want above the horizontal button layout
        label = QLabel('This is above the buttons')
        main_layout.addWidget(label)

        # Create a horizontal box layout to hold the buttons
        button_layout = QHBoxLayout()

        # Create two buttons
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')

        # Add the buttons to the horizontal layout
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        # Add a vertical spacer item to center the horizontal layout at the bottom
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(vertical_spacer)

        # Add the horizontal layout to the vertical layout
        main_layout.addLayout(button_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())