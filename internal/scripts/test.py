
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

num = 2

for i in range(0, 10):
    print(len(str(num)))
    num = num*num