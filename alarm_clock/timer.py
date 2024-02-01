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
        self.empty_label = QLabel()
        self.time = QTimeEdit()
        self.control_panel = QHBoxLayout()
        self.add_ten_minutes = QPushButton("+10")
        self.add_ten_minutes.clicked.connect(self.handle_add_ten_minutes)
        self.add_one_minute = QPushButton("+1")
        self.add_one_minute.clicked.connect(self.handle_add_one_minute)
        self.start_hold = QPushButton("Start")
        self.start_hold.clicked.connect(self.handle_start_hold)
        self.subtract_one_minute = QPushButton("-1")
        self.subtract_one_minute.clicked.connect(self.handle_subtract_one_minute)
        self.subtract_ten_minutes = QPushButton("-10")
        self.subtract_ten_minutes.clicked.connect(self.handle_subtract_ten_minutes)

        self.edit_widgets()
        self.edit_layouts()

        self.base_layout.addLayout(self.top_panel, Qt.AlignmentFlag.AlignTop)
        self.base_layout.addWidget(self.time)
        self.base_layout.addLayout(self.control_panel)

        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.time.setDisplayFormat("hh:mm:ss")
        self.time.setMaximumHeight(40)

        self.select_sound.setMaximumSize(110, 50)
        select_sound_font = self.select_sound.font()
        select_sound_font.setPointSize(11)
        self.select_sound.setFont(select_sound_font)
        self.select_sound.setStyleSheet("background-color :rgb(230, 230, 230)")

        turn_off_font = self.turn_off.font()
        turn_off_font.setPointSize(11)
        self.turn_off.setFont(turn_off_font)
        self.turn_off.setMaximumSize(70, 70)
        self.turn_off.setStyleSheet("border-radius : 35; border : 1px solid black; background-color: orange")

        self.start_hold.setStyleSheet("background-color : green")

    def edit_layouts(self):
        self.top_panel.addWidget(self.select_sound, Qt.AlignmentFlag.AlignLeft)
        self.top_panel.addStretch()
        self.top_panel.addWidget(self.turn_off, Qt.AlignmentFlag.AlignRight)

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
            self.start_hold.setStyleSheet("background-color : orange")
            self.started = True
        elif self.started and self.time.time().toString() != "00:00:00":
            self.timer.stop()
            self.time.setReadOnly(False)
            self.start_hold.setText("Start")
            self.start_hold.setStyleSheet("background-color : green")
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
        elif full_seconds == 0:
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


    def handle_add_ten_minutes(self):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()
        minutes += 10

        full_seconds = hours * 3600 + minutes * 60 + seconds
        minutes, seconds = divmod(full_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.time.setTime(QTime(hours, minutes, seconds))

    def handle_add_one_minute(self):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()
        minutes += 1

        full_seconds = hours * 3600 + minutes * 60 + seconds
        minutes, seconds = divmod(full_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.time.setTime(QTime(hours, minutes, seconds))

    def handle_subtract_one_minute(self):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()
        minutes -= 1

        full_seconds = hours * 3600 + minutes * 60 + seconds
        if full_seconds > 0:
            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes = divmod(minutes, 60)
        else:
            hours = minutes = seconds = 0

        self.time.setTime(QTime(hours, minutes, seconds))

    def handle_subtract_ten_minutes(self):
        hours = self.time.time().hour()
        minutes = self.time.time().minute()
        seconds = self.time.time().second()
        minutes -= 10

        full_seconds = hours * 3600 + minutes * 60 + seconds
        if full_seconds > 0:
            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes = divmod(minutes, 60)
        else:
            hours = minutes = seconds = 0

        self.time.setTime(QTime(hours, minutes, seconds))


