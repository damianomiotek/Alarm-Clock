import os
from pathlib import Path

import pygame
from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QRadioButton, QFileDialog


def yes_button_str():
    return "Tak"

#iconImage = QPixmap("../musicIcon3.png")
#musicIcon = QIcon(QPixmap("musicIcon.jpg"))


def get_current_date():
    current_date = QDateTime.currentDateTime().toString("dd.MM.yyyy")
    day = current_date[0:2]
    if day[0] == '0':
        day = day[1]
    month = current_date[3:5]
    polish_months = {"01": "Styczeń", "02": "Luty", "03": "Marzec", "04": "Kwiecień", "05": "Maj", "06": "Czerwiec",
                     "07": "Lipied", "08": "Sierpień", "09": "Wrzesień", "10": "Październik", "11": "Listopad",
                     "12": "Grudzień"}
    month = polish_months[month]
    year = current_date[-4:]
    current_date = f"{day} {month} {year}"
    return current_date


def get_radio_buttons_for_days_of_week():
    days_of_week = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]
    radio_buttons = []
    for day in range(7):
        radio_buttons.append(QRadioButton(days_of_week[day]))
        radio_buttons[-1].setAutoExclusive(False)
    return radio_buttons


month_names = {"01": "stycznia", "02": "lutego", "03": "marca", "04": "kwietnia", "05": "maja", "06": "czerwca",
               "07": "lipca", "08": "sierpnia", "09": "września", "10": "października", "11": "listopada",
               "12": "grudnia"}

weekdays = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]


class Utilities:
    def __init__(self):
        pygame.mixer.init()
        self.sound_file = "alarm_classic.mp3"
        self.sound = pygame.mixer.Sound(self.sound_file)

    def play_alarm(self):
        self.sound.play(1000)

    def stop_alarm(self):
        self.sound.stop()

    def select_alarm_sound(self):
        file_filter = 'Pliki dźwiękowe (*.mp3 *.m4a *.flac *.wav *.wma *.aac);; Wszystkie pliki (*.*)'
        file_name = QFileDialog.getOpenFileName(
            caption='Wybierz dźwięk budzika',
            directory=str(Path.home()),
            filter=file_filter
        )
        if file_name[0] != "":
            self.sound_file = file_name[0]
            self.sound = pygame.mixer.Sound(self.sound_file)
