from PyQt6.QtWidgets import QMainWindow, QTabWidget
from alarm import Alarm
from clock import Clock
from stopwatch import Stopwatch
from timer import Timer
from world_clock import WorldClock


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)

        tabs.addTab(Alarm(), "Budzik")
        tabs.addTab(Stopwatch(), "Stoper")
        tabs.addTab(Timer(), "Minutnik")
        tabs.addTab(Clock(), "Aktualny czas")
        tabs.addTab(WorldClock(), "Aktualny czas w różnych miejscach świecie")
        self.setCentralWidget(tabs)


        self.setWindowTitle("Zegar")
