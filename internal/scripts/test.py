
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import json
import os
import subprocess
import sys
import textwrap
import os
import re
import cv2
from pathlib import Path
import pandas as pd
import numpy as np
import directories as dirs

seg_count_and_names = [[1, 2, 3, 4], ["first", "second", "third", "fourth"]]

thresh_count_and_names = [[7, 9, 12, 3], ["second", "first", "fourth", "third"]]

total_count_array = []

import os

dir_list = next(os.walk(dirs.detections))[1]

print(dir_list)



# Pulls models from unamedNumber.json and adds them to the dropdown
with open(f"{cwd}/internal/resources/unamedNumber.json", "r") as json_File:
    model_dict = json.load(json_File)
    value_list = list(model_dict.values())
value = value_list[0]  