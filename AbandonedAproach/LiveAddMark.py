# UsableProgram/ClickOverlay.py
import os
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from pynput import mouse
from typing import Tuple, Optional, List


# === KONFIGURACJA PLIKÓW ===
class Config:
    SETTINGS_FOLDER = os.path.join(os.path.dirname(__file__), "settings")
    SETTINGS_FILE = "settings.txt"
    OUTPUT_FILE = "click_position.txt"

    @staticmethod
    def get_settings_path() -> str:
        os.makedirs(Config.SETTINGS_FOLDER, exist_ok=True)
        return os.path.join(Config.SETTINGS_FOLDER, Config.SETTINGS_FILE)

    @staticmethod
    def get_output_path() -> str:
        return os.path.join(Config.SETTINGS_FOLDER, Config.OUTPUT_FILE)


# === ZARZĄDZANIE USTAWIENIAMI ===
class SettingsManager:
    DEFAULT = [0, 0, 0, 0, 1920, 1080]

    @staticmethod
    def load() -> List[int]:
        path = Config.get_settings_path()
        if not os.path.exists(path):
            return SettingsManager.DEFAULT.copy()
        try:
            with open(path, "r", encoding="utf-8") as f:
                values = list(map(int, f.readline().strip().split()))
                return values if len(values) == 6 else SettingsManager.DEFAULT.copy()
        except:
            return SettingsManager.DEFAULT.copy()

    @staticmethod
    def get_bounding_box() -> Tuple[int, int, int, int]:
        _, _, min_x, min_y, max_x, max_y = SettingsManager.load()
        return int(min_x), int(min_y), int(max_x), int(max_y)


# === WĄTEK NASŁUCHIWANIA MYSZY (TYLKO LPM, BEZ PRZEPEŁNIENIA) ===
class MouseListener(QThread):
    clicked = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self._running = True
        self._last_click = 0.0
        self._debounce = 0.08
        self._listener = None

    def run(self):
        def on_click(x, y, button, pressed):
            # TYLKO LEWY PRZYCISK
            if button != mouse.Button.left:
                return
            if not pressed or not self._running:
                return
            now = time.time()
            if now - self._last_click < self._debounce:
                return
            self._last_click = now
            self.clicked.emit(int(x), int(y))

        with mouse.Listener(on_click=on_click) as listener:
            self._listener = listener
            # BEZ join() → GUI ŻYJE
            while self._running:
                time.sleep(0.01)
                QtWidgets.QApplication.processEvents()

    def stop(self):
        self._running = False
        if self._listener:
            self._listener.stop()
        self.quit()
        self.wait(1000)


# === OVERLAY KLIKÓW ===
class ClickOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WA_TransparentForMouseEvents  # kliki przechodzą do gry
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(0,0,0,60);")
        self.showFullScreen()

        self.click_pos: Optional[Tuple[int, int]] = None
        self.min_x, self.min_y, self.max_x, self.max_y = SettingsManager.get_bounding_box()

        self.listener = MouseListener()
        self.listener.clicked.connect(self.on_click)
        self.listener.start()

        print(f"Overlay aktywny: klikaj w minimapie [{self.min_x}, {self.min_y}] → [{self.max_x}, {self.max_y}]")

    def on_click(self, x: int, y: int):
        if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y:
            self.click_pos = (x, y)
            self._save_position(x, y)
            self.update()

    def _save_position(self, x: int, y: int):
        try:
            with open(Config.get_output_path(), "w", encoding="utf-8") as f:
                f.write(f"{x},{y}\n")
            print(f"Zapisano kliknięcie na minimapie: ({x}, {y})")
        except Exception as e:
            print(f"Błąd zapisu: {e}")

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        # Rysuj obszar minimapy (żółty prostokąt)
        rect = QtCore.QRect(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)
        p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0, 180), 2))
        p.setBrush(QtGui.QColor(255, 255, 0, 30))
        p.drawRect(rect)

        # Rysuj kliknięcie (pomarańczowe + zielone kółko)
        if self.click_pos:
            x, y = self.click_pos
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

    def closeEvent(self, event):
        self.listener.stop()
        super().closeEvent(event)


# === URUCHOMIENIE ===
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    overlay = ClickOverlay()
    overlay.show()
    print("Klikaj LPM na minimapie – współrzędne zapisują się w settings/click_position.txt")
    print("PPM i inne przyciski są ignorowane.")
    sys.exit(app.exec_())