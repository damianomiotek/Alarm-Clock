from PyQt6.QtWidgets import QMessageBox


class DisableAlarmClockDialog(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Wyłączenie budzika")
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(f"Czy na pewno chcesz wyłączyć budzik?")
        self.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        self.addButton("Nie", QMessageBox.ButtonRole.NoRole)
