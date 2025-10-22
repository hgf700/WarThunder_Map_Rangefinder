from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
import sys

class Overlay(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)
        self.show()
        self.marker_pos = QPoint(960, 540)  # środek ekranu

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 255, 0), 3)
        painter.setPen(pen)
        painter.drawLine(self.marker_pos.x() - 10, self.marker_pos.y(),
                         self.marker_pos.x() + 10, self.marker_pos.y())
        painter.drawLine(self.marker_pos.x(), self.marker_pos.y() - 10,
                         self.marker_pos.x(), self.marker_pos.y() + 10)

    def mousePressEvent(self, event):
        self.marker_pos = event.pos()
        self.update()
        print(f"Kliknięto: {event.x()}, {event.y()}")

app = QApplication(sys.argv)
overlay = Overlay()
sys.exit(app.exec_())
