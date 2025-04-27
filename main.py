from PyQt6.QtWidgets import QApplication
import sys

from GUI.StartWindow import StartWindow


app = QApplication(sys.argv)
win = StartWindow()
win.show()
sys.exit(app.exec())
