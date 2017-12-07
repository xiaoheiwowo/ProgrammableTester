#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.patheffects as patheffects
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import diagram, doubleslider
from public.globalvariable import GlobalVariable as gv
import random

class Ui_CurrentDiagram(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Ui_CurrentDiagram, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电流曲线')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.Init_DiagramArea()

        self.BT_Dynamic = QtWidgets.QPushButton('动态')
        self.BT_Dynamic.setFixedSize(50, 50)
        self.BT_Static = QtWidgets.QPushButton('静态')
        self.BT_Static.setFixedSize(50, 50)
        self.BT_ScreenShot = QtWidgets.QPushButton('截屏')
        self.BT_ScreenShot.setFixedSize(50,50)
        self.BT_ZoomIn = QtWidgets.QPushButton(self)
        self.BT_ZoomIn.setFixedSize(50, 50)
        self.BT_ZoomIn.setStyleSheet('''QPushButton {background-image: url("./images/zoomin.png")}''')

        self.refresh_time = QtCore.QTimer(self)
        self.refresh_time.timeout.connect(self.draw_static)
        self.refresh_time.start(100)
        # self.Label_d11 = QtWidgets.QLabel('BD3S')
        # self.Label_d12 = QtWidgets.QLabel('DC 5V')
        # self.Label_d13 = QtWidgets.QLabel('200mA')

        Layout_Other = QtWidgets.QVBoxLayout()

        # Layout_Other.addWidget(self.Label_d11)
        # Layout_Other.addWidget(self.Label_d12)
        # Layout_Other.addWidget(self.Label_d13)
        Layout_Other.addWidget(self.BT_ZoomIn)
        Layout_Other.addStretch(0)
        Layout_Other.addWidget(self.BT_ScreenShot)
        Layout_Other.addWidget(self.BT_Dynamic)
        Layout_Other.addWidget(self.BT_Static)

        Layout_Main = QtWidgets.QHBoxLayout()
        Layout_Main.addWidget(self.GB_Diagram)
        Layout_Main.addLayout(Layout_Other)
        self.setLayout(Layout_Main)

        # 变量
        self.val1 = 70
        self.val2 = 100
        # 信号
        self.BT_ZoomIn.clicked.connect(self.close)
        self.BT_Static.clicked.connect(self.static_diagram)
        self.BT_Dynamic.clicked.connect(self.dynamic_diagram)
        self.BT_ScreenShot.clicked.connect(self.BigDiagram.save_picture)

        self.DS_DataSlider.valve_changed.connect(self.get_dataslider_valve)

    def Init_DiagramArea(self):
        """
        初始化电流曲线区域
        :return:
        """
        self.GB_Diagram = QtWidgets.QGroupBox(self)
        self.GB_Diagram.setGeometry(10, 10, 900, 580)
        self.GB_Diagram.setTitle('动态曲线')

        self.BigDiagram = diagram.PlotWidget(self)

        self.DS_DataSlider = doubleslider.MDoubleSlider(self.GB_Diagram)
        self.DS_DataSlider.setMinimumHeight(50)
        self.DS_DataSlider.set_valve(70, 100, self.width())
        self.DS_DataSlider.set_handle_disabled(False, True)

        self.Layout_Diagram = QtWidgets.QVBoxLayout(self.GB_Diagram)
        self.Layout_Diagram.addWidget(self.BigDiagram)
        self.Layout_Diagram.addWidget(self.DS_DataSlider)


    def static_diagram(self):
        self.GB_Diagram.setTitle('静态曲线')
        self.DS_DataSlider.set_handle_disabled(False, False)
        self.mycid = self.BigDiagram.turn_on_cid()
        # self.refresh_time.stop()
        self.refresh_time.start(100)

    def dynamic_diagram(self):
        self.GB_Diagram.setTitle('动态曲线')
        try:
            self.BigDiagram.turn_off_cid(self.mycid)
        except:
            print('error')
        self.DS_DataSlider.set_valve(70, 100, self.width())
        self.DS_DataSlider.set_handle_disabled(False, True)

        self.refresh_time.start(100)

    def draw_static(self):
        if self.GB_Diagram.title() == '动态曲线':
            gv.current_valve.append(int(100 * random.random()))
            del gv.current_valve[0]
        else:
            pass
        yy = gv.current_valve[2 * self.val1 : 2 * self.val2]
        # self.val1
        # self.val2
        self.BigDiagram.update_diagram(yy*10)

    def get_dataslider_valve(self, a, b):
        self.val1 = a
        self.val2 = b
        # self.BigDiagram.update_diagram()
        print(a, b)

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

