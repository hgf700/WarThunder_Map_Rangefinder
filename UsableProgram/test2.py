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

        pen_width = 3
        kolo1=17
        kolo2=12
        alpha=150
        kolorkolo1=[255, 165, 0]
        kolorkolo2=[39, 250, 0]

        poskolo1 = 1
        poskolo2=3
#o
        pen = QtGui.QPen(QtGui.QColor(kolorkolo1[0],kolorkolo1[1], kolorkolo1[2],alpha))
        pen.setWidth(pen_width)
        pen.setCosmetic(False)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawEllipse(poskolo1,poskolo1, kolo1,kolo1)

#g
#9
        # center_x = poskolo1 + kolo1 / 2
        # center_y = poskolo1 + kolo1 / 2

        # new_x = center_x - kolo2 / 2
        # new_y = center_y - kolo2 / 2

        pen = QtGui.QPen(QtGui.QColor(kolorkolo2[0], kolorkolo2[1],kolorkolo2[2],alpha))
        pen.setWidth(pen_width)
        pen.setCosmetic(False)
        painter.setPen(pen)
        # painter.drawEllipse(new_x, new_y, kolo2, kolo2)
        painter.drawEllipse(poskolo2,poskolo2, kolo2,kolo2)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    overlay = SimpleOverlay()
    overlay.show()  
    app.exec_()
