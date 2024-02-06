import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton


class Stopwatch(QWidget):
    def __init__(self):
        super(Stopwatch, self).__init__()

        self.base_layout = QVBoxLayout()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.started = False
        self.start_time = 0
        self.until_now = 0

        self.time = QLabel("00:00:00:00")
        self.control_panel = QHBoxLayout()
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.start_button_clicked)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_time)
        self.edit_widgets()

        self.base_layout.addWidget(self.time)
        self.base_layout.addSpacing(50)
        self.control_panel.addWidget(self.start_stop_button)
        self.control_panel.addWidget(self.reset_button)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(80)

        self.setLayout(self.base_layout)

    def edit_widgets(self):
        time_font = self.time.font()
        time_font.setPointSize(95)
        self.time.setFont(time_font)
        self.time.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        start_stop_button_font = self.start_stop_button.font()
        start_stop_button_font.setPointSize(20)
        self.start_stop_button.setFont(start_stop_button_font)
        self.start_stop_button.setMaximumSize(130, 130)
        self.start_stop_button.setStyleSheet("border-radius : 65; border : 2px solid black; background-color: green")

        reset_button_font = self.reset_button.font()
        reset_button_font.setPointSize(20)
        self.reset_button.setFont(reset_button_font)
        self.reset_button.setMaximumSize(130, 130)
        self.reset_button.setStyleSheet("border-radius : 65; border : 2px solid black; background-color: orange")

    def start_button_clicked(self):
        if not self.started:
            self.start_time = time.time()
            self.timer.start(10)
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setStyleSheet("background-color: red; color: white; border-radius: 60; border: 2px solid black")
            self.started = True
        elif self.started:
            self.timer.stop()
            self.until_now = time.time() - self.start_time + self.until_now
            self.start_stop_button.setText("Start")
            self.start_stop_button.setStyleSheet("background-color: green; color: black; border-radius: 60; border: 2px solid black")
            self.started = False

    def update_time(self):
        time_passed = time.time() - self.start_time + self.until_now
        secs = time_passed % 60
        mins = time_passed // 60
        hours = mins // 60
        self.time.setText(f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}:{int((time_passed % 1) * 100):02d}")

    def reset_time(self):
        self.timer.stop()
        self.until_now = 0
        self.time.setText(f"00:00:00:00")
        self.start_stop_button.setText("Start")
        self.start_stop_button.setStyleSheet(
            "background-color: green; color: black; border-radius: 60; border: 2px solid black")
        self.started = False



