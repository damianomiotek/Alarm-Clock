from PyQt6.QtWidgets import QMainWindow, QTabWidget
from alarm_clock.alarm import Alarm
from alarm_clock.clock import Clock
from alarm_clock.stopwatch import Stopwatch
from alarm_clock.timer import Timer
from alarm_clock.world_clock import WorldClock


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)
        tabs_font = tabs.font()
        tabs_font.setPointSize(12)
        tabs.setFont(tabs_font)


        tabs.addTab(Alarm(), "Budzik")
        tabs.addTab(Stopwatch(), "Stoper")
        tabs.addTab(Timer(), "Minutnik")
        tabs.addTab(Clock(), "Aktualny czas")
        tabs.addTab(WorldClock(), "Aktualny czas na świecie")
        self.setCentralWidget(tabs)

        self.setMinimumSize(1100, 750)

        self.setWindowTitle("Zegar")
