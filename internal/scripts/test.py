
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
from colorama import *
from termcolor import * 
from pyfiglet import *
import line_profiler
import atexit

xml_list = []
for xml in Path(r"C:\Users\mill286\Tensorflow\workspace\images\instance 1\train").glob("*.xml"):
    xml_list.append(os.path.splitext(os.path.basename(xml)))

image_list = []
for image in Path(r"C:\Users\mill286\Tensorflow\workspace\images\instance 1\train").glob("*.png"):
    image_list.append(os.path.splitext(os.path.basename(image)))

xml_count = 0
for x in xml_list:
    xml_count +=1

image_count = 0
for i in image_list:
    image_count +=1

print(f"XMLs: {xml_count}")

print(f"PNGs: {image_count}")