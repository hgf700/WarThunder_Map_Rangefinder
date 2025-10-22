from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

class SimpleOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(500, 300, 50, 50)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 200)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(0, 0, 50, 50)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    overlay = SimpleOverlay()
    overlay.show()  # na początku pokazujemy overlay

    # Przykład: ukryj overlay po 3 sekundach
    QtCore.QTimer.singleShot(3000, overlay.hide)

    # Przykład: pokaż overlay po 5 sekundach
    QtCore.QTimer.singleShot(5000, overlay.show)

    app.exec_()
