
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

path = r"C:\Users\mill286\Desktop\new.xlsx"

x1 = np.random.randn(100, 2)
df1 = pd.DataFrame(x1)

x2 = np.random.randn(100, 2)
df2 = pd.DataFrame(x2)

writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
df1.to_excel(writer, sheet_name = 'x1')
df2.to_excel(writer, sheet_name = 'x2')
writer.close()

book = pd.load_workbook(path)
writer = pd.ExcelWriter(path, engine = 'openpyxl')
writer.book = book

x3 = np.random.randn(100, 2)
df3 = pd.DataFrame(x3)

x4 = np.random.randn(100, 2)
df4 = pd.DataFrame(x4)

df3.to_excel(writer, sheet_name = 'x3')
df4.to_excel(writer, sheet_name = 'x4')
writer.close()