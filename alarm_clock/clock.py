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
        self.display_time_layout = QHBoxLayout()
        self.display_time_layout.addWidget(self.display_time)

        self.edit_widgets()

        self.base_layout.addWidget(self.display_date)
        self.base_layout.addWidget(self.analog_clock)
        self.base_layout.addLayout(self.display_time_layout)
        self.base_layout.setStretchFactor(self.display_date, 1)
        self.base_layout.setStretchFactor(self.analog_clock, 3)
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.display_date.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = self.display_date.font()
        font.setPointSize(22)
        self.display_date.setFont(font)

        self.display_time.setReadOnly(True)
        self.display_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_time = time.strftime("%H:%M:%S")
        self.display_time.setText(current_time)
        self.display_time.setMaximumWidth(200)
        self.display_time.setMinimumHeight(35)

    def display_date_timer_timeout(self):
        if self.display_date.text() != get_current_date():
            self.display_date.setText(get_current_date())

    def display_time_timer_timeout(self):
        current_time = time.strftime("%H:%M:%S")
        self.display_time.setText(current_time)

