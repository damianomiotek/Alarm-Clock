from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush
from PyQt6.QtWidgets import QPushButton


class SwitchButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(84)
        self.setMinimumHeight(26)

    def paintEvent(self, event):
        label = "WŁ" if self.isChecked() else "WYŁ"
        bg_color = QColor("green") if self.isChecked() else QColor("gray")

        radius = 10
        width = 40
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(255,255,255))

        pen = QPen(QColor("black"), 1)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignmentFlag.AlignHCenter, label)