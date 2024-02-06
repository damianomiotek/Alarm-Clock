import time

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout

from utilities import get_current_date
from other_widgets.analog_clock import AnalogClock


class Clock(QWidget):
    def __init__(self):
        super(Clock, self).__init__()

        self.base_layout = QVBoxLayout()
        self.display_date = QLabel(get_current_date())
        self.display_date_timer = QTimer()
        self.display_date_timer.start(1000)
        self.display_date_timer.timeout.connect(self.display_date_timer_timeout)

        self.analog_clock = AnalogClock()

        self.display_time = QLineEdit()
        self.display_time_timer = QTimer()
        self.display_time_timer.start(1000)
        self.display_time_timer.timeout.connect(self.display_time_timer_timeout)

        self.edit_widgets()

        self.base_layout.addWidget(self.display_date, stretch=1)
        self.base_layout.addSpacing(24)
        self.base_layout.addWidget(self.analog_clock, stretch=7)
        self.base_layout.addSpacing(14)
        self.base_layout.addWidget(self.display_time, stretch=2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.display_date.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.display_date.setStyleSheet("font-size: 34pt; color : #4b280a")

        self.display_time.setReadOnly(True)
        self.display_time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        display_time_font = self.display_time.font()
        display_time_font.setPointSize(26)
        self.display_time.setFont(display_time_font)
        current_time = time.strftime("%H:%M:%S")
        self.display_time.setText(current_time)
        self.display_time.setMaximumWidth(300)
        self.display_time.setMinimumHeight(55)

    def display_date_timer_timeout(self):
        if self.display_date.text() != get_current_date():
            self.display_date.setText(get_current_date())

    def display_time_timer_timeout(self):
        current_time = time.strftime("%H:%M:%S")
        self.display_time.setText(current_time)

