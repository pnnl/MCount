from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

app = QApplication([])

# Get a list of font families available on the system
available_fonts = "\n".join(QFontDatabase().families())

print(available_fonts)
