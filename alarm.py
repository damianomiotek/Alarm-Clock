import time

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTimeEdit, QPushButton, QLineEdit, QLabel)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate

from disable_alarm_clock_dialog import DisableAlarmClockDialog
from setting_alarm_clock_dialog import SettingAlarmClockDialog, yes_button_str
from take_nap_dialog import TakeNapDialog, nap_button_str, disable_alarm_button_str
from utilities import Utilities, get_current_date, get_radio_buttons_for_days_of_week
from switch_button import SwitchButton


class Alarm(QWidget):
    def __init__(self):
        super(Alarm, self).__init__()

        self.base_layout = QVBoxLayout()
        self.utilities = Utilities()
        self.alarm_in_days = []
        self.alarm_only_once = False

        self.alarm_timer = QTimer()
        self.alarm_timer.timeout.connect(self.check_alarm)
        self.alarm_time = QTime()
        self.nap_timer = QTimer()
        self.nap_timer.timeout.connect(self.check_alarm_after_nap)

        self.display_time = QLineEdit()
        self.display_time_layout = QHBoxLayout()
        self.display_time_timer = QTimer()
        self.display_time_timer.start(1000)
        self.display_time_timer.timeout.connect(self.display_time_timer_timeout)

        self.display_date = QLabel(get_current_date())
        self.display_date_timer = QTimer()
        self.display_date_timer.start(1000)
        self.display_date_timer.timeout.connect(self.display_date_timer_timeout)

        self.edit_time = QTimeEdit()

        self.middle_layout = QHBoxLayout()
        self.days_of_week_radio_btns = get_radio_buttons_for_days_of_week()

        self.bottom_layout = QHBoxLayout()
        self.button = QPushButton("Ustaw")
        self.button.clicked.connect(self.button_clicked)
        self.switch_button = SwitchButton()
        self.switch_button.clicked.connect(self.switch_button_clicked)

        self.edit_widgets()
        self.edit_layouts_except_base_layout()

        self.base_layout.addLayout(self.display_time_layout)
        self.base_layout.addWidget(self.display_date)
        self.base_layout.addWidget(self.edit_time)
        self.base_layout.addLayout(self.middle_layout)
        self.base_layout.addLayout(self.bottom_layout)

        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.display_time.setReadOnly(True)
        self.display_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_time = time.strftime("%H:%M:%S")
        self.display_time.setText(current_time)
        self.display_time.setMaximumSize(300, 50)
        self.display_time.setStyleSheet("background-color: rgb(221, 221, 221)")
        self.display_date.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_time.setDisplayFormat("hh:mm")
        self.button.setMaximumSize(70, 30)

    def edit_layouts_except_base_layout(self):
        self.display_time_layout.addWidget(self.display_time)
        for radio_button in self.days_of_week_radio_btns:
            self.middle_layout.addWidget(radio_button)
        self.bottom_layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)
        self.bottom_layout.addWidget(self.switch_button, alignment=Qt.AlignmentFlag.AlignRight)

    def display_time_timer_timeout(self):
        current_time = time.strftime("%H:%M:%S")
        self.display_time.setText(current_time)

    def display_date_timer_timeout(self):
        if self.display_date.text() != get_current_date():
            self.display_date.setText(get_current_date())

    def button_clicked(self):
        set_alarm_dialog = SettingAlarmClockDialog(self, self.edit_time.time())
        set_alarm_dialog.exec()

        if set_alarm_dialog.clickedButton().text() == yes_button_str():
            self.alarm_time = self.edit_time.time()
            for button_index in range(len(self.days_of_week_radio_btns)):
                if self.days_of_week_radio_btns[button_index].isChecked():
                    self.alarm_in_days.append(button_index + 1)
            if len(self.alarm_in_days) == 0:
                self.alarm_only_once = True
            self.alarm_timer.start(1000)
            self.switch_button.setChecked(True)
        else:
            self.switch_button.setChecked(False)

    def switch_button_clicked(self):
        if self.switch_button.isChecked():
            self.button_clicked()
        else:
            disable_alarm_dialog = DisableAlarmClockDialog(self)
            disable_alarm_dialog.exec()
            if disable_alarm_dialog.clickedButton().text() == yes_button_str():
                self.alarm_timer.stop()
            else:
                self.switch_button.setChecked(True)

    def check_alarm(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        current_day = QDate.currentDate().dayOfWeek()
        if self.alarm_time.toString("hh:mm:ss") == current_time:
            if current_day in self.alarm_in_days or self.alarm_only_once:
                self.alarm_only_once = False
                self.utilities.play_alarm()
                nap_alarm_dialog = TakeNapDialog(self)
                nap_alarm_dialog.exec()

                if nap_alarm_dialog.clickedButton().text() == nap_button_str():
                    self.utilities.stop_alarm()
                    self.nap_timer.start(10000)
                elif nap_alarm_dialog.clickedButton().text() == disable_alarm_button_str():
                    self.utilities.stop_alarm()
                    if len(self.alarm_in_days) == 0:
                        self.switch_button.setChecked(False)
                        self.alarm_timer.stop()

    def check_alarm_after_nap(self):
        self.nap_timer.stop()
        self.utilities.play_alarm()
        nap_alarm_dialog = TakeNapDialog(self)
        nap_alarm_dialog.exec()

        if nap_alarm_dialog.clickedButton().text() == nap_button_str():
            self.utilities.stop_alarm()
            self.nap_timer.start(10000)
        elif nap_alarm_dialog.clickedButton().text() == disable_alarm_button_str():
            self.utilities.stop_alarm()
            if len(self.alarm_in_days) == 0:
                self.switch_button.setChecked(False)
                self.alarm_timer.stop()
