from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

import subprocess

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox

import os
import re

def find_file_with_highest_number(folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Extract numeric values from file names using regular expressions
    numeric_files = []
    pattern = re.compile(r'\d+')
    for file in files:
        match = pattern.findall(file)
        if match:
            numeric_files.append((int(match[0]), file))

    if not numeric_files:
        return None  # No numeric files found

    # Find the file name with the highest number
    max_number_file = os.path.splitext(max(numeric_files, key=lambda x: x[0])[1])[0]

    return max_number_file

folder_path = r"C:\Users\mill286\Desktop\Mussel-Counting-AI-App\internal\model"
highest_number_file = find_file_with_highest_number(folder_path)

if highest_number_file:
    print(f"The file with the highest number is: {highest_number_file}")
else:
    print("No numeric files found in the folder.")