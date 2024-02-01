import requests
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QComboBox
from utilities import month_names, weekdays
from bs4 import BeautifulSoup


class WorldClock(QWidget):
    def __init__(self):
        super(WorldClock, self).__init__()

        self.base_layout = QVBoxLayout()
        self.search_in_api_str = "Wyszukaj w Abstract API"
        self.search_in_google_str = "Wyszukaj w wyszukiwarce Google"
        self.failed_search = "Nie znaleziono czasu dla: "
        self.local_gmt = 1

        self.display_result = QVBoxLayout()
        self.time = QLabel()
        self.date_and_hour_difference = QLabel()
        self.input_data = QVBoxLayout()
        self.prompt_to_enter_data = QLabel("Wprowadź nazwę miejscowości, lub nazwę miejscowości i kraj, gdzie chcesz"
                                           " otrzymać aktualny czas")
        self.place = QLineEdit()
        self.buttons = QHBoxLayout()
        self.search_button = QPushButton("Szukaj")
        self.search_button.clicked.connect(self.search_time)
        self.select_button = QComboBox()

        self.edit_widgets()
        self.edit_layouts()

        self.base_layout.addLayout(self.display_result)
        self.base_layout.addLayout(self.input_data)
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        #self.time.setMaximumHeight(800)
        time_font = self.time.font()
        time_font.setPointSize(45)
        time_font.setBold(True)
        self.time.setFont(time_font)

        self.date_and_hour_difference.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.date_and_hour_difference.setMaximumHeight(70)
        date_hour_difference_font = self.date_and_hour_difference.font()
        date_hour_difference_font.setPointSize(20)
        self.date_and_hour_difference.setFont(date_hour_difference_font)

        self.prompt_to_enter_data.setMaximumHeight(32)
        prompt_font = self.prompt_to_enter_data.font()
        prompt_font.setPointSize(13)
        self.prompt_to_enter_data.setFont(prompt_font)

        self.place.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.place.setMaximumHeight(50)
        place_font = self.place.font()
        place_font.setPointSize(12)
        self.place.setFont(place_font)

        self.search_button.setMaximumWidth(100)
        self.select_button.addItems([self.search_in_api_str, self.search_in_google_str])
        self.select_button.setMaximumWidth(220)

    def edit_layouts(self):
        self.display_result.addWidget(self.time)
        self.display_result.addWidget(self.date_and_hour_difference)
        label_for_additional_space = QLabel()
        label_for_additional_space.setMaximumHeight(160)
        self.display_result.addWidget(label_for_additional_space)

        self.input_data.addWidget(self.prompt_to_enter_data)
        self.input_data.addWidget(self.place)
        self.buttons.addWidget(self.search_button, Qt.AlignmentFlag.AlignCenter)
        self.buttons.addWidget(self.select_button, Qt.AlignmentFlag.AlignRight)
        self.input_data.addLayout(self.buttons)

    def search_time(self):
        entered_place = self.place.text()

        if not entered_place or entered_place.isspace():
            self.place.setText("Nie wprowadziłeś żadnej miejscowości")
            return

        if self.select_button.currentText() == self.search_in_api_str:
            found_time, found_date_and_hour_difference = self.search_in_api(entered_place)
        else:
            found_time, found_date_and_hour_difference = self.search_in_google(entered_place)

        if self.failed_search in found_time:
            self.date_and_hour_difference.setStyleSheet("color : red")
            self.date_and_hour_difference.setText(found_time)
            return

        self.time.setText(found_time)
        self.date_and_hour_difference.setStyleSheet("color : black")
        self.date_and_hour_difference.setText(found_date_and_hour_difference)

    def search_in_api(self, place):
        abstract_api_url = "https://timezone.abstractapi.com/v1/current_time"
        query = {"api_key": "key", "location": place}

        response = requests.request("GET", abstract_api_url, params=query)
        if response.status_code != 200:
            return self.failed_search + "\n" + place, str()

        data_json = response.json()
        found_time = data_json["datetime"].split(" ")[1]
        found_time = found_time[0:5]
        found_date = data_json["datetime"].split(" ")[0]
        year, month, day = found_date.split("-")
        found_date = f"{day} {month_names[month]} {year}\n"

        gmt_offset = data_json["gmt_offset"]
        hour_difference = abs(self.local_gmt - gmt_offset)
        found_hour_difference = self.get_found_hour_difference(hour_difference)

        if gmt_offset < self.local_gmt:
            found_hour_difference = f"{found_hour_difference} do tyłu"
        elif gmt_offset > self.local_gmt:
            found_hour_difference = f"{found_hour_difference} do przodu"

        return found_time, found_date + found_hour_difference

    def search_in_google(self, place):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "pl-PL,pl;q=0.9"}
        google_url = "https://www.google.com/search"
        params = {
            "q":    f"Aktualny czas w {place}",
            "gl":   "pl"
        }

        response = requests.get(google_url, params=params, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        if not soup.find(class_="gsrt vk_bk FzvWSb YwPhnf"):
            return self.failed_search + "\n" + place, str()

        found_time = soup.find(class_="gsrt vk_bk FzvWSb YwPhnf").get_text()
        found_date_and_gmt = soup.find(class_="vk_gy vk_sh").get_text()
        found_date = found_date_and_gmt[:found_date_and_gmt.rfind("(")]
        found_date = found_date.rstrip().lstrip() + "\n"

        found_hour = int(found_time[0:2])
        hour_in_current_place = int(datetime.now().hour)
        found_weekday = found_date.split(",")[0]
        found_weekday = weekdays.index(found_weekday)
        current_weekday = datetime.today().weekday()
        found_hour_difference = str()

        if current_weekday == found_weekday:
            hour_difference = abs(hour_in_current_place - found_hour)
            found_hour_difference = self.get_found_hour_difference(hour_difference)
            if hour_in_current_place < found_hour:
                found_hour_difference = f"{found_hour_difference} do przodu"
            elif hour_in_current_place > found_hour:
                found_hour_difference = f"{found_hour_difference} do tyłu"
        elif (current_weekday > found_weekday != 0 and current_weekday != 6
              or (current_weekday == 0 and found_weekday == 6)):
            hour_difference = 24 - found_hour + hour_in_current_place
            found_hour_difference = self.get_found_hour_difference(hour_difference)
            found_hour_difference = f"{found_hour_difference} do tyłu"
        elif current_weekday < found_weekday or (current_weekday == 6 and found_weekday == 0):
            hour_difference = 24 - hour_in_current_place + found_hour
            found_hour_difference = self.get_found_hour_difference(hour_difference)
            found_hour_difference = f"{found_hour_difference} do przodu"

        return found_time, found_date + found_hour_difference

    def get_found_hour_difference(self, hour_difference):
        found_hour_difference = str()
        if hour_difference == 1:
            found_hour_difference = f"{hour_difference} godzina"
        elif hour_difference in [2, 3, 4, 22, 23, 24]:
            found_hour_difference = f"{hour_difference} godziny"
        elif hour_difference != 0:
            found_hour_difference = f"{hour_difference} godzin"

        return found_hour_difference
