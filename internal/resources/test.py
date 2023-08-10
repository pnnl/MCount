from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

import subprocess

# List of commands to run in the new cmd window
commands = ["echo Hello", "echo World", "dir"]

# Combine the commands using the & operator
combined_commands = " & ".join(commands)

# Create the command to start a new cmd window and run the combined commands
command = ["start", "cmd", "/k", combined_commands]

# Run the combined commands in a new cmd window
subprocess.Popen(command, shell=True)