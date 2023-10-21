
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

#importing the module cv2
import cv2
#reading the image whose dimensions are to be found using imread() function
image = cv2.imread('internal/resources/icon.jpg')
#using shape property to get the dimensions of the image
dimensions = image.shape
print(dimensions)
