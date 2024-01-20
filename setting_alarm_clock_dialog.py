from PyQt6.QtWidgets import QMessageBox


def yes_button_str():
    return "Tak"


class SettingAlarmClockDialog(QMessageBox):
    def __init__(self, parent, time):
        super().__init__(parent)

        self.setWindowTitle("Ustawianie budzika")
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(f"Czy na pewno chcesz ustawić budzik na {time.toString('hh:mm')}?")
        self.addButton(yes_button_str(), QMessageBox.ButtonRole.YesRole)
        self.addButton("Nie", QMessageBox.ButtonRole.NoRole)
