from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from pynput import mouse
import sys

FILENAME = "test.txt"

class ClickListener(QObject):
    click_signal = pyqtSignal(int, int)  # sygnał do przekazywania kliknięć

    def __init__(self):
        super().__init__()
        self.listener = None

    def start(self):
        def on_click(x, y, button, pressed):
            if pressed:
                self.click_signal.emit(x, y)

        self.listener = mouse.Listener(on_click=on_click)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()


class SimpleOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # ustawienia okna
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # ważne dla przezroczystości
        self.setStyleSheet("background-color: rgba(0, 0, 0, 50);")
        self.showFullScreen()

        self.click_positions = []
        print("Overlay utworzony")

        # Listener w osobnym wątku
        self.click_listener = ClickListener()
        self.click_listener.click_signal.connect(self.add_click)
        self.click_listener.start()

    def add_click(self, x, y):
        """Dodaje kliknięcie (wywoływane w głównym wątku)"""
        print(f"Kliknięcie: x={x}, y={y}")
        self.click_positions.append((x, y))

        # zapis do pliku
        with open(FILENAME, "a") as f:
            f.write(f"{x},{y}\n")

        # bezpieczne odświeżenie
        self.update()  # teraz bezpieczne, bo w głównym wątku

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen_width = 3
        kolo1 = 17
        kolo2 = 12
        alpha = 150
        kolorkolo1 = [255, 165, 0]  # pomarańczowe
        kolorkolo2 = [39, 250, 0]   # zielone

        for x, y in self.click_positions:
            # pierwsze kółko
            pen = QtGui.QPen(QtGui.QColor(*kolorkolo1, alpha))
            pen.setWidth(pen_width)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawEllipse(x - kolo1//2, y - kolo1//2, kolo1, kolo1)

            # drugie kółko
            pen = QtGui.QPen(QtGui.QColor(*kolorkolo2, alpha))
            pen.setWidth(pen_width)
            painter.setPen(pen)
            painter.drawEllipse(x - kolo2//2, y - kolo2//2, kolo2, kolo2)

    def closeEvent(self, event):
        self.click_listener.stop()
        super().closeEvent(event)


# Uruchomienie
app = QtWidgets.QApplication(sys.argv)
overlay = SimpleOverlay()
overlay.show()
print("Overlay uruchomiony")

sys.exit(app.exec_())