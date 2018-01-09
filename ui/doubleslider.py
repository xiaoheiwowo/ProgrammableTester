# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from public.datacache import SoftwareData as sw


class MDoubleSlider(QtWidgets.QWidget):
    """
    双滑块滑动条，，，
    """

    valve_changed = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(MDoubleSlider, self).__init__(parent)

        self.X_Handle2 = 800
        self.X_Handle1 = self.X_Handle2 - 100
        self.handle1_disabled = False
        self.handle2_disabled = False
        self.HandleSelected = None
        self.setFixedHeight(30)
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valve_changed.connect(self.show_valve)

    def paintEvent(self, paint_event):
        """
        绘图事件
        :param paint_event:
        :return:
        """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_slider(qp)
        qp.end()

    def draw_slider(self, qp):
        """
        绘制滑块
        :param qp:
        :return:
        """
        qp.setFont(QtGui.QFont('Serif', 7))

        pen = QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 15, self.width()-20, 15)
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.yellow)
        qp.drawRect(self.X_Handle1, 5, 10, 20)

        qp.setBrush(QtCore.Qt.red)
        qp.drawRect(self.X_Handle2, 5, 10, 20)

    def mousePressEvent(self, mouse_event):
        """

        :param mouse_event:
        :return:
        """
        if self.X_Handle1 <= mouse_event.x() < self.X_Handle1 + 10:
            if not self.handle1_disabled:
                self.HandleSelected = 1
            else:
                self.HandleSelected = None
            # print('1')
        elif self.X_Handle2 <= mouse_event.x() < self.X_Handle2 + 10:
            if not self.handle2_disabled:
                self.HandleSelected = 2
            else:
                self.HandleSelected = None
            # print('2')
        else:
            self.HandleSelected = None

    def mouseMoveEvent(self, mouse_event):
        """

        :param mouse_event:
        :return:
        """
        if self.HandleSelected == 1:
            if mouse_event.x() < 20:
                self.X_Handle1 = 20
            elif mouse_event.x() >= self.X_Handle2 - 10 - sw.sliders_interval_min:
                self.X_Handle1 = self.X_Handle2 - 10 - sw.sliders_interval_min
            else:
                self.X_Handle1 = mouse_event.x()
        elif self.HandleSelected == 2:
            if mouse_event.x() > self.width() - 30:
                self.X_Handle2 = self.width() - 30
            elif mouse_event.x() < 30 + sw.sliders_interval_min:
                self.X_Handle2 = 30 + sw.sliders_interval_min
            else:
                self.X_Handle2 = mouse_event.x()
                if self.X_Handle1 > self.X_Handle2 - 50:
                    self.X_Handle1 = self.X_Handle2 - 50
        self.update()

        start = int(100 * (self.X_Handle1 - 20) / (self.width() - 50))
        stop = int(100 * (self.X_Handle2 - 20) / (self.width() - 50))
        self.valve_changed.emit(start, stop)

    def mouseReleaseEvent(self, mouse_event):
        """

        :param mouse_event:
        :return:
        """

        start = int(100 * (self.X_Handle1 - 20)/(self.width()-50))
        stop = int(100 * (self.X_Handle2 - 20)/(self.width()-50))
        # print(self.width())
        self.valve_changed.emit(start, stop)

    @staticmethod
    def show_valve(a, b):
        """
        显示
        :param a:
        :param b:
        :return:
        """
        # print(a, b)
        pass

    def set_valve(self, val1, val2, width):
        """

        :param val1:
        :param val2:
        :return:
        """
        self.X_Handle1 = int((val1 / 100) * (width - 107 - 50)) + 21
        self.X_Handle2 = int((val2 / 100) * (width - 107 - 50)) + 20
        # self.valve_changed.emit(val1, val2)
        self.update()

    def get_valve(self):
        """

        :return:
        """
        start = int(100 * (self.X_Handle1 - 20) / (self.width() - 50))
        stop = int(100 * (self.X_Handle2 - 20) / (self.width() - 50))
        return (start, stop)

    def set_handle_disabled(self, hd1=False, hd2=False):
        """

        :param hd1:
        :param hd2:
        :return:
        """
        if hd1:
            self.handle1_disabled = True
        else:
            self.handle1_disabled = False
        if hd2:
            self.handle2_disabled = True
        else:
            self.handle2_disabled = False
