from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

import subprocess

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox

import textwrap
import os
import re
from pathlib import Path

cwd = (os.getcwd()).replace("\\", "/")

model_path = cwd + "/internal/model"
