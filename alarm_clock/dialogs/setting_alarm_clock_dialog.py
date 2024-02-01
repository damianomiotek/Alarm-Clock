from PyQt6.QtWidgets import QMessageBox


class SettingAlarmClockDialog(QMessageBox):
    def __init__(self, parent, time):
        super().__init__(parent)

        self.setWindowTitle("Ustawianie budzika")
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(f"Czy na pewno chcesz ustawić budzik na {time.toString('hh:mm')}?")
        self.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        self.addButton("Nie", QMessageBox.ButtonRole.NoRole)
