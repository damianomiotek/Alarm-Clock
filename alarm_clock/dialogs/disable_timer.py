from PyQt6.QtWidgets import QMessageBox


class DisableTimerDialog(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Wyłączenie minutnika")
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(f"Czy na pewno chcesz wyłączyć minutnik?")
        self.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        self.addButton("Nie", QMessageBox.ButtonRole.NoRole)
