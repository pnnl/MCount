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

cwd = ((repr(os.getcwd())).replace(r"\\", "/")).replace(r"'", "")

print(cwd)

# Defines paths to model folders/files
with open(f"{cwd}/internal/resources/modeldict.json", "r") as f:
    model_dict = json.load(f)
tfrecord_dir = cwd + "/external/training/"+ f"yooo.record"
csv_path = cwd + "/external/training/"+ f"yooo.csv"
script_name = cwd + "/internal/scripts/generate_tfrecord.py"
model_dir = model_dict["current_model_directory"]
pipeline_dir = model_dir + "/pipeline.config"

files = os.listdir(model_dir)
num_check = re.compile(r'\d+')
ckpt_files = []
for file in files:
    match = num_check.findall(file)
    if match:
        ckpt_files.append((int(match[0]), file))
last_ckpt = os.path.splitext(max(ckpt_files, key = lambda x: x[0])[1])[0]
ckpt_path = cwd + "/internal/model/" + last_ckpt

# Sets important config keys
key1 = "input_path:"
key2 = "label_map_path:"
key3 = "fine_tune_checkpoint:"

# Reads the  config file and processes lines
with open(model_dir + "/pipeline.config", "r") as file:
    lines = file.readlines()

# Changes lines that contain the right keys to give correct paths 
for i, line in enumerate(lines):
    if key1 in line:
        lines[i] = textwrap.indent(f'{key1} "{tfrecord_dir}" \n', "    ")
    
    elif key2 in line:
        lines[i] = textwrap.indent(f'"{key2} "fffffffffff" \n', "  ")

    elif key3 in line:
        lines[i] = textwrap.indent(f'{key3} "{ckpt_path}" \n', "  ")
    
# Writes the modified lines back to the file
with open(model_dir + "/pipeline.config", "w") as file:
    file.writelines(lines)
