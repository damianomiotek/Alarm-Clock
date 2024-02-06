from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from utilities import Utilities, yes_button_str
from dialogs.disable_timer import DisableTimerDialog


class Timer(QWidget):
    def __init__(self):
        super(Timer, self).__init__()

        self.base_layout = QVBoxLayout()
        self.utilities = Utilities()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.started = False

        self.top_panel = QHBoxLayout()
        self.select_sound = QPushButton("Wybierz\ndźwięk")
        self.select_sound.clicked.connect(self.handle_select_sound)
        self.turn_off = QPushButton("Wyłącz\nminutnik")
        self.turn_off.clicked.connect(self.handle_turn_off)
        self.time = QTimeEdit()
        self.control_panel = QHBoxLayout()
        self.add_ten_minutes = QPushButton("+10")
        self.add_ten_minutes.clicked.connect(lambda: self.add_minutes(10))
        self.add_one_minute = QPushButton("+1")
        self.add_one_minute.clicked.connect(lambda: self.add_minutes(1))
        self.start_hold = QPushButton("Start")
        self.start_hold.clicked.connect(self.handle_start_hold)
        self.subtract_one_minute = QPushButton("-1")
        self.subtract_one_minute.clicked.connect(lambda: self.subtract_minutes(1))
        self.subtract_ten_minutes = QPushButton("-10")
        self.subtract_ten_minutes.clicked.connect(lambda: self.subtract_minutes(10))

        self.edit_widgets()
        self.edit_layouts()

        self.base_layout.addLayout(self.top_panel)
        self.base_layout.addWidget(self.time)
        self.base_layout.addSpacing(130)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(25)

        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.select_sound.setMinimumSize(120, 50)
        self.select_sound.setStyleSheet("background-color :rgb(230, 230, 230); font-size : 11pt")

        self.turn_off.setMinimumSize(75, 75)
        self.turn_off.setStyleSheet("border-radius : 37; border : 1px solid black; background-color: orange; "
                                    "font-size: 11pt")

        self.time.setDisplayFormat("hh:mm:ss")
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time.setMaximumHeight(60)
        self.time.setStyleSheet("font-size : 28pt")

        self.add_one_minute.setMaximumSize(50, 50)
        self.add_one_minute.setStyleSheet("border-radius : 25; border : 1px solid black; font-size : 12pt")
        self.add_ten_minutes.setMaximumSize(50, 50)
        self.add_ten_minutes.setStyleSheet("border-radius : 25; border : 1px solid black; font-size : 12pt")
        self.start_hold.setMaximumSize(95, 45)
        self.start_hold.setStyleSheet("background-color : green; font-size : 12pt")
        self.subtract_one_minute.setMaximumSize(50, 50)
        self.subtract_one_minute.setStyleSheet("border-radius : 25; border : 1px solid black; font-size : 12pt")
        self.subtract_ten_minutes.setMaximumSize(50, 50)
        self.subtract_ten_minutes.setStyleSheet("border-radius : 25; border : 1px solid black; font-size : 12pt")

    def edit_layouts(self):
        self.top_panel.addWidget(self.select_sound, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.top_panel.addWidget(self.turn_off, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self.control_panel.addWidget(self.add_ten_minutes)
        self.control_panel.addWidget(self.add_one_minute)
        self.control_panel.addWidget(self.start_hold)
        self.control_panel.addWidget(self.subtract_one_minute)
        self.control_panel.addWidget(self.subtract_ten_minutes)

    def handle_start_hold(self):
        if not self.started and self.time.time().toString() != "00:00:00":
            self.timer.start(1000)
            self.time.setReadOnly(True)
            self.start_hold.setText("Wstrzymaj")
            self.start_hold.setStyleSheet("background-color : orange; font-size : 12pt")
            self.started = True
        elif self.started and self.time.time().toString() != "00:00:00":
            self.timer.stop()
            self.time.setReadOnly(False)
            self.start_hold.setText("Start")
            self.start_hold.setStyleSheet("background-color : green; font-size : 12pt")
            self.started = False

    def update_timer(self):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()

        full_seconds = hours * 3600 + minutes * 60 + seconds
        if full_seconds > 0:
            full_seconds -= 1
            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            self.time.setTime(QTime(hours, minutes, seconds))
        else:
            self.utilities.play_alarm()
            self.timer.stop()
            self.time.setReadOnly(False)
            self.start_hold.setText("Start")
            self.start_hold.setStyleSheet("background-color : green")
            self.started = False
            button = QMessageBox.information(self, "Czas minął", "Czas minął. Alarm został włączony",
                                             buttons=QMessageBox.StandardButton.Ok)

            if button == QMessageBox.StandardButton.Ok:
                self.utilities.stop_alarm()

    def handle_select_sound(self):
        self.utilities.select_alarm_sound()

    def handle_turn_off(self):
        disable_timer_dialog = DisableTimerDialog(self)
        disable_timer_dialog.exec()
        if disable_timer_dialog.clickedButton().text() == yes_button_str():
            self.timer.stop()
            self.time.setTime(QTime(0, 0, 0))
            self.time.setReadOnly(False)
            self.start_hold.setText("Start")
            self.start_hold.setStyleSheet("background-color : green")
            self.started = False

    def add_minutes(self, extra_minutes):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()
        minutes += extra_minutes

        full_seconds = hours * 3600 + minutes * 60 + seconds
        minutes, seconds = divmod(full_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.time.setTime(QTime(hours, minutes, seconds))

    def subtract_minutes(self, num_minutes):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()
        minutes -= num_minutes

        full_seconds = hours * 3600 + minutes * 60 + seconds
        if full_seconds > 0:
            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes = divmod(minutes, 60)
        else:
            hours = minutes = seconds = 0

        self.time.setTime(QTime(hours, minutes, seconds))
