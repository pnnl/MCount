from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

import subprocess

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox

# creating a new dictionary
my_dict ={"Java":100, "Python":112, "C":11}
 
# one-liner
print("One line Code Key value: ", list(my_dict.keys())[list(my_dict.values()).index(100)])