import sys

from PyQt6.QtWidgets import QApplication
from alarm_clock.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
