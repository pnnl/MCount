
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

seg_count_and_names = [[1, 2, 3, 4], ["first", "second", "third", "fourth"]]

thresh_count_and_names = [[7, 9, 12, 3], ["second", "first", "fourth", "third"]]

total_count_array = []

# Combines the segmentation and thresholding counts to give a total mussel count
for i in range(len(seg_count_and_names[1])):
    for p in range(len(thresh_count_and_names[1])):
        if seg_count_and_names[1][i] == thresh_count_and_names[1][p]:
            seg_element = i
            thresh_element = p
    total_count_array.append(seg_count_and_names[0][seg_element] + thresh_count_and_names[0][thresh_element])

print(total_count_array)