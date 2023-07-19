import sys
from PyQt5.QtWidgets import QApplication, QWidget
app = QApplication([])
w = QWidget()
w.resize(300,300)
w.setWindowTitle("AI App")
w.show()
sys.exit(app.exec())