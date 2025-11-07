from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from pynput import mouse
import sys
import time

FILENAME = "test.txt"

class MouseThread(QThread):
    click = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self._stop = False
        self.last_time = 0

    def run(self):
        def on_click(x, y, button, pressed):
            if not pressed or self._stop:
                return

            now = time.time()
            # Debounce: max 1 kliknięcie co 80ms
            if now - self.last_time < 0.08:
                return
            self.last_time = now

            # Emit w głównym wątku
            self.click.emit(int(x), int(y))

        with mouse.Listener(on_click=on_click) as listener:
            self.listener = listener
            # WAŻNE: pętla z processEvents
            while not self._stop:
                time.sleep(0.01)
                QtWidgets.QApplication.processEvents()

    def stop(self):
        self._stop = True
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.quit()
        self.wait(1000)


class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(0,0,0,60);")
        self.showFullScreen()

        self.pos = None

        # Uruchom wątek
        self.thread = MouseThread()
        self.thread.click.connect(self.set_click)
        self.thread.start()

    def set_click(self, x, y):
        self.pos = (x, y)
        with open(FILENAME, "w") as f:
            f.write(f"{x},{y}\n")
        self.update()  # odśwież

    def paintEvent(self, event):
        if not self.pos:
            return

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        x, y = self.pos
        r1, r2 = 20, 14
        pen = QtGui.QPen()
        pen.setWidth(3)

        # Pomarańczowe kółko
        pen.setColor(QtGui.QColor(255, 165, 0, 180))
        p.setPen(pen)
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawEllipse(x - r1//2, y - r1//2, r1, r1)

        # Zielone kółko
        pen.setColor(QtGui.QColor(39, 250, 0, 180))
        p.setPen(pen)
        p.drawEllipse(x - r2//2, y - r2//2, r2, r2)

    def closeEvent(self, e):
        self.thread.stop()
        super().closeEvent(e)


# === URUCHOMIENIE ===
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Overlay()
    win.show()
    print("Klikaj – działa bez limitu!")
    sys.exit(app.exec_())