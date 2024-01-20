from PyQt6.QtCore import Qt, QTimer, QTime, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QPolygon
from PyQt6.QtWidgets import QWidget


class AnalogClock(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        self.hPointer = QPolygon([QPoint(6, 7), QPoint(-6, 7), QPoint(0, -50)])
        self.mPointer = QPolygon([QPoint(6, 7), QPoint(-6, 7), QPoint(0, -70)])
        self.sPointer = QPolygon([QPoint(2, 2), QPoint(-2, 2), QPoint(0, -90)])

    def paintEvent(self, event):
        hour_color = QColor("black")
        minute_color = QColor("black")
        second_color = QColor("red")
        face_color = QColor("white")
        rim_color = QColor("black")
        rim_width = 3

        side = min(self.width(), self.height())
        x = self.width() / 2
        y = self.height() / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(x, y)
        painter.scale(side / 200, side / 200)

        painter.setPen(QPen(rim_color, rim_width))
        painter.setBrush(QBrush(face_color))
        painter.drawEllipse(-95, -95, 190, 190)

        for i in range(12):
            angle = i * 30
            painter.save()
            painter.rotate(angle)
            painter.translate(0, -90)
            painter.setPen(QPen(hour_color))
            painter.drawLine(0, 0, 0, 8)
            painter.translate(0, 90)
            if i == 0:
                painter.translate(-3, -77)
            if i == 1:
                painter.translate(-3, -77)
                painter.rotate(-30)
            elif i == 2:
                painter.translate(-5, -74)
                painter.rotate(-60)
            elif i == 3:
                painter.translate(-5, -73)
                painter.rotate(-90)
            elif i == 4:
                painter.translate(-3, -70)
                painter.rotate(-120)
            elif i == 5:
                painter.translate(-2, -68)
                painter.rotate(-150)
            elif i == 6:
                painter.translate(3, -68)
                painter.rotate(-180)
            elif i == 7:
                painter.translate(6, -70)
                painter.rotate(150)
            elif i == 8:
                painter.translate(6, -75)
                painter.rotate(120)
            elif i == 9:
                painter.translate(7, -77)
                painter.rotate(90)
            elif i == 10:
                painter.translate(3, -79)
                painter.rotate(60)
            elif i == 11:
                painter.translate(2, -79)
                painter.rotate(30)

            painter.drawText(0, 10, f"{i}")
            painter.restore()

        time = QTime.currentTime()
        hour = time.hour()
        minute = time.minute()
        second = time.second()

        painter.save()
        painter.rotate(30 * (hour + minute / 60))
        painter.setPen(QPen(hour_color, 0))
        painter.setBrush(QBrush(hour_color))
        painter.drawConvexPolygon(self.hPointer)
        painter.restore()

        painter.save()
        painter.rotate(6 * (minute + second / 60))
        painter.setPen(QPen(minute_color, 0))
        painter.setBrush(QBrush(minute_color))
        painter.drawConvexPolygon(self.mPointer)
        painter.restore()

        painter.save()
        painter.rotate(6 * second)
        painter.setPen(QPen(second_color, 0))
        painter.setBrush(QBrush(second_color))
        painter.drawConvexPolygon(self.sPointer)
        painter.restore()
