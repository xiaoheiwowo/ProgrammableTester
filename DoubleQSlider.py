#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets


class MDoubleSlider(QtWidgets.QWidget):
    '''
    双滑块滑动条，，，
    '''
    OutputValve = QtCore.pyqtSignal(int,int)
    def __init__(self, parent = None):
        super(MDoubleSlider, self).__init__(parent)

        self.X_Handle1 = 10
        self.X_Handle2 = 50
        self.Handle1Selected = None

        self.setFixedHeight(30)
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawbutton(qp)
        qp.end()

    def drawbutton(self, qp):
        qp.setFont(QtGui.QFont('Serif', 7))

        pen = QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 10, self.width(), 10)

        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.yellow)
        qp.drawRect(self.X_Handle1, 0, 10, 20)

        qp.setBrush(QtCore.Qt.red)
        qp.drawRect(self.X_Handle2, 0, 10, 20)

    def mousePressEvent(self, QMouseEvent):
        if self.X_Handle1 <= QMouseEvent.x() < self.X_Handle1 + 10:
            self.Handle1Selected = 1
            print('1')
        elif self.X_Handle2 <= QMouseEvent.x() < self.X_Handle2 + 10:
            self.Handle1Selected = 0
            print('2')
        else:
            self.Handle1Selected = None



    def mouseMoveEvent(self, QMouseEvent):
        if self.Handle1Selected == 1:
            self.X_Handle1 = QMouseEvent.x()
        elif self.Handle1Selected == 0:
            self.X_Handle2 = QMouseEvent.x()

        if self.X_Handle1 + 10 > self.X_Handle2:
            self.X_Handle1 = self.X_Handle2 - 10

        if self.X_Handle1 > 0 and self.X_Handle2 < self.width() - 10:
            self.update()
        else:
            if self.X_Handle1 < 1:
                self.X_Handle1 = 1
            else:
                self.X_Handle2 > self.width() - 10
                self.X_Handle2 = self.width() - 11
        # print(self.xx, self.xx2)

    def mouseReleaseEvent(self, QMouseEvent):
        if self.X_Handle1 <= QMouseEvent.x() < self.X_Handle1 + 10 or self.X_Handle2 <= QMouseEvent.x() < self.X_Handle2 + 10:
            self.OutputValve.emit(self.X_Handle1, self.X_Handle2)
        else:
            pass
        self.OutputValve.connect(self.showv)

    def showv(self,a,b):
        print(a,b)
