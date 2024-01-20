from PyQt6.QtWidgets import QMessageBox


def nap_button_str():
    return "Drzemka"


def disable_alarm_button_str():
    return "Wyłącz"


class TakeNapDialog(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Budzik")
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText("Włącz drzemkę 10 min lub wyłącz budzik")
        self.addButton(nap_button_str(), QMessageBox.ButtonRole.AcceptRole)
        self.addButton(disable_alarm_button_str(), QMessageBox.ButtonRole.RejectRole)
