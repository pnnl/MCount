

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

app = QApplication([])

# Get a list of font families available on the system
available_fonts = QFontDatabase().families()

print(available_fonts)