# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
title
"""
import time
import random

from PyQt5 import QtCore, QtGui, QtWidgets

from ui import diagram, doubleslider
from public.datacache import SoftwareData as sw


class Ui_CurrentDiagram(QtWidgets.QDialog):
    """
    introduction
    """

    def __init__(self, parent=None):
        super(Ui_CurrentDiagram, self).__init__(parent)
        self.resize(1024, 600)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电流曲线')
        self.setWindowIcon(QtGui.QIcon(":/logo.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        self.BT_Dynamic = QtWidgets.QPushButton('动态')
        self.BT_Dynamic.setFixedSize(50, 50)
        self.BT_Static = QtWidgets.QPushButton('静态')
        self.BT_Static.setFixedSize(50, 50)
        self.BT_ScreenShot = QtWidgets.QPushButton('截屏')
        self.BT_ScreenShot.setFixedSize(50, 50)
        self.BT_ZoomIn = QtWidgets.QPushButton(self)
        self.BT_ZoomIn.setFixedSize(50, 50)
        self.BT_ZoomIn.setStyleSheet('''QPushButton {background-image: url("./images/zoomin.png")}''')

        # 电流曲线区域
        self.GB_Diagram = QtWidgets.QGroupBox(self)
        self.BigDiagram = diagram.PlotWidget(self)
        self.DS_DataSlider = doubleslider.MDoubleSlider(self.GB_Diagram)
        self.Layout_Diagram = QtWidgets.QVBoxLayout(self.GB_Diagram)

        # self.refresh_time = QtCore.QTimer(self)
        # self.refresh_time.timeout.connect(self.draw_dynamic)
        # self.refresh_time.start(300)
        self.init_diagram_area()
        Layout_Other = QtWidgets.QVBoxLayout()
        Layout_Other.addWidget(self.BT_ZoomIn)
        Layout_Other.addStretch(1)
        Layout_Other.addWidget(self.BT_ScreenShot)
        Layout_Other.addWidget(self.BT_Dynamic)
        Layout_Other.addWidget(self.BT_Static)

        Layout_Main = QtWidgets.QHBoxLayout()
        Layout_Main.addWidget(self.GB_Diagram)
        Layout_Main.addLayout(Layout_Other)
        self.setLayout(Layout_Main)

        self.refresh_thread = RefreshThread(self)
        self.refresh_thread.start()

        # slider 滑块值
        self.val1 = 70
        self.val2 = 100
        # 静态标志位
        self.fg_static = 0

        # 信号
        self.BT_ZoomIn.clicked.connect(self.stop_timer_and_close)
        self.BT_Static.clicked.connect(self.static_diagram)

        self.BT_Dynamic.clicked.connect(self.dynamic_diagram)
        self.BT_ScreenShot.clicked.connect(self.screen_shot)

        self.DS_DataSlider.valve_changed.connect(self.get_dataslider_valve)
        # self.DS_DataSlider.valve_changed.connect(self.draw_static)

    def init_diagram_area(self):
        """
        初始化电流曲线区域
        :return:
        """

        self.GB_Diagram.setGeometry(10, 10, 900, 580)
        self.GB_Diagram.setTitle('动态曲线')

        self.DS_DataSlider.setMinimumHeight(50)
        self.DS_DataSlider.set_valve(70, 100, self.width())
        self.DS_DataSlider.set_handle_disabled(False, True)

        self.Layout_Diagram.addWidget(self.BigDiagram)
        self.Layout_Diagram.addWidget(self.DS_DataSlider)

    def static_diagram(self):
        """

        :return:
        """
        sw.static_current_value = sw.current_value[:]
        self.GB_Diagram.setTitle('静态曲线')
        self.DS_DataSlider.set_handle_disabled(False, False)
        self.mycid = self.BigDiagram.turn_on_cid()

        self.fg_static = 1

        # self.refresh_time.stop()
        # self.refresh_time.start(100)

    def dynamic_diagram(self):
        """

        :return:
        """
        self.fg_static = 0
        self.GB_Diagram.setTitle('动态曲线')
        try:
            self.BigDiagram.turn_off_cid(self.mycid)
        except:
            print('动态图无交互功能')
        self.DS_DataSlider.set_valve(70, 100, self.width())
        self.DS_DataSlider.set_handle_disabled(False, True)
        self.val1, self.val2 = 70, 100

        # self.refresh_time.start(300)

    def draw_dynamic(self):
        """

        :return:
        """
        if self.GB_Diagram.title() == '动态曲线':
            # 接通采样注释下面两行
            sw.current_value.append(round(5 * random.random(), 3))
            sw.current_value.pop(0)
            pass
        else:
            pass
        yy = sw.current_value[-(int(sw.current_set['data_depth']/100) * (self.val2 - self.val1)):]
        self.BigDiagram.update_diagram(yy)

    def draw_static(self):
        """

        :return:
        """
        yy = sw.current_value[-(int(sw.current_set['data_depth']/100) * (self.val2 - self.val1)):]
        self.BigDiagram.update_diagram(yy)

    def get_dataslider_valve(self, a, b):
        """

        :param a:
        :param b:
        :return:
        """
        self.val1 = a
        self.val2 = b
        if self.GB_Diagram.title() == '静态曲线':
            self.draw_static()
        # print(a, b)

    def resizeEvent(self, QResizeEvent):
        """
        重新实现resize
        :param QResizeEvent:
        :return:
        """
        # a, b = self.DS_DataSlider.get_valve()
        # print(a,b)
        # self.DS_DataSlider.set_valve(a, b, self.width())
        self.dynamic_diagram()

    def screen_shot(self):
        """
        save as a picture file
        :return:
        """
        file, ok = QtWidgets.QFileDialog.getSaveFileName(self, str('保存'), ' ', 'Image files (*.jpg, *.png)')
        if ok:
            self.BigDiagram.save_picture(file)

    def stop_timer_and_close(self):
        """

        :return:
        """
        # self.refresh_thread.deleteLater()
        self.reject()


class RefreshThread(QtCore.QThread):
    """
    IN
    """

    def __init__(self, _parent):
        super(RefreshThread, self).__init__()
        self.win = _parent

    def run(self):
        """
        刷新曲线图
        :return:
        """
        while True:
            time.sleep(0.01)
            if not self.win.fg_static:
                # self.win.dynamic_diagram()
                self.win.draw_dynamic()
            pass
