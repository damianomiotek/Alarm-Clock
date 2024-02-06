import time

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTimeEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer, QTime, QDate

from dialogs.disable_alarm_clock_dialog import DisableAlarmClockDialog
from dialogs.setting_alarm_clock_dialog import SettingAlarmClockDialog
from dialogs.take_nap_dialog import TakeNapDialog, nap_button_str, disable_alarm_button_str
from utilities import Utilities, get_current_date, get_radio_buttons_for_days_of_week, yes_button_str
from other_widgets.switch_button import SwitchButton


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

        self.display_date_and_time = QLabel()
        self.display_timer = QTimer()
        self.display_timer.start(1000)
        self.display_timer.timeout.connect(self.display_timer_timeout)

        self.edit_time = QTimeEdit()

        self.middle_layout = QHBoxLayout()
        self.days_of_week_radio_btns = get_radio_buttons_for_days_of_week()

        self.bottom_layout = QHBoxLayout()
        self.select_alarm_sound = QPushButton("Wybierz dźwięk budzika")
        self.select_alarm_sound.clicked.connect(self.select_alarm_sound_clicked)
        self.set_button = QPushButton("Ustaw")
        self.set_button.clicked.connect(self.set_button_clicked)
        self.switch_button = SwitchButton()
        self.switch_button.clicked.connect(self.switch_button_clicked)

        self.edit_widgets()
        self.edit_layouts()

        self.base_layout.addSpacing(125)
        self.base_layout.addWidget(self.display_date_and_time)
        self.base_layout.addWidget(self.edit_time)
        self.base_layout.addLayout(self.middle_layout)
        self.base_layout.addSpacing(40)
        self.base_layout.addLayout(self.bottom_layout)
        self.base_layout.addSpacing(40)

        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.display_date_and_time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.display_date_and_time.setTextFormat(Qt.TextFormat.RichText)
        current_date = get_current_date()
        current_time = time.strftime("%H:%M:%S")
        current_date_and_time = (
            f'<span style="font-size:26pt;">{current_date}</span><br> <span style="font-size:60pt; font-weight:900; font-style:oblique; '
            f'font-family:Arial, sans-serif;">{current_time}</span>')
        self.display_date_and_time.setText(current_date_and_time)
        self.edit_time.setMaximumHeight(38)
        self.edit_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_time.setStyleSheet("font-size : 18pt")
        self.edit_time.setDisplayFormat("hh:mm")
        self.select_alarm_sound.setStyleSheet("border-radius : 5; border : 1px solid black;"
                                              "background-color : rgb(221, 221, 221); font-size : 11pt")
        self.select_alarm_sound.setMinimumSize(180, 30)
        self.set_button.setMinimumSize(100, 40)
        self.set_button.setStyleSheet("font-size : 11pt")

    def edit_layouts(self):
        for radio_button in self.days_of_week_radio_btns:
            self.middle_layout.addWidget(radio_button)
        self.bottom_layout.addWidget(self.select_alarm_sound, alignment=Qt.AlignmentFlag.AlignLeft)
        self.bottom_layout.addWidget(self.set_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.switch_button, alignment=Qt.AlignmentFlag.AlignRight)

    def display_timer_timeout(self):
        current_date = get_current_date()
        current_time = time.strftime("%H:%M:%S")
        current_date_and_time = (f'<span style="font-size:26pt;">{current_date}</span><br> <span style="font-size:60pt; font-weight:900; font-style:oblique; '
                         f'font-family:Arial, sans-serif;">{current_time}</span>')
        self.display_date_and_time.setText(current_date_and_time)

    def set_button_clicked(self):
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
            self.set_button_clicked()
        else:
            disable_alarm_dialog = DisableAlarmClockDialog(self)
            disable_alarm_dialog.exec()
            if disable_alarm_dialog.clickedButton().text() == yes_button_str():
                self.alarm_timer.stop()
                self.alarm_only_once = False
                self.alarm_in_days.clear()
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

    def select_alarm_sound_clicked(self):
        self.utilities.select_alarm_sound()
