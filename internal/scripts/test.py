
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

profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)

@profile
def profiled_function():
    import os
    import tensorflow as tf
    import pandas as pd
    import openpyxl
    import cv2 
    import numpy as np
    import re
    import styleframe

    from object_detection.utils import label_map_util
    from object_detection.utils import visualization_utils as viz_utils
    from object_detection.builders import model_builder
    from object_detection.utils import config_util
    from matplotlib import pyplot as plt
    from pathlib import Path

profiled_function()