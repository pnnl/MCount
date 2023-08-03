from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

import json

# Load the JSON data from the file
with open(r'C:\Users\mill286\OneDrive - PNNL\Desktop\Mussel-Counting-AI-App\resources\data.json', 'r') as file:
    data = json.load(file)

# Check if the key "name" exists in the JSON data
if 'name' in data:
    print("The key 'name' exists in the JSON data.")
    print("Value of 'name':", data['name'])
else:
    print("The key 'name' does not exist in the JSON data.")
