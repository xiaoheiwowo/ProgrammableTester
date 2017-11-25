#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import diagram
import matplotlib.animation as animation
import numpy as np
import random
import matplotlib.patheffects as patheffects
import doubleslider
class Ui_CurrentDiagram(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Ui_CurrentDiagram, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电流曲线')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 保存、确定、取消按钮
        # self.DB_DialogButton = DialogButton.DialogButton(self)
        # self.DB_DialogButton.move(700, 530)
        # self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

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

        self.BT_ZoomIn.clicked.connect(self.close)
        self.BT_Static.clicked.connect(self.onstart)
    def Init_DiagramArea(self):
        self.GB_Diagram = QtWidgets.QGroupBox(self)
        self.GB_Diagram.setGeometry(10, 10, 900, 580)
        self.GB_Diagram.setTitle('电流曲线')

        xx = np.arange(-10.0, 0, 0.05)
        yy = (np.cos(2*np.pi*xx)+1)*10
        self.BigDiagram = diagram.PlotWidget(self, xx, yy)


        self.DS_DataSlider = doubleslider.MDoubleSlider(self.GB_Diagram)
        self.DS_DataSlider.setMinimumHeight(50)
        # self.DS_DataSlider.setGeometry(50, 530, 800, 50)

        Layout_Diagram = QtWidgets.QVBoxLayout(self.GB_Diagram)
        Layout_Diagram.addWidget(self.BigDiagram)
        Layout_Diagram.addWidget(self.DS_DataSlider)

        # 信号

    def update_line(self, _):
        Y = 10 * np.random.rand(10)
        X = range(-10, 0)
        # self.BigDiagram.myFigure1.clear(self)
        return self.BigDiagram.myFigure1.plot(X, Y, linewidth=1.5, color='r', label='Current', ls='-', marker='o',
                            mec='r', mfc='r', ms=6,
                            path_effects=[patheffects.SimpleLineShadow(), patheffects.Normal()])

    def onstart(self):
        # self.BigDiagram = diagram.PlotWidget(self,xx=range(-20,0),yy=np.random.rand(20))
        # self.BigDiagram.__init__(self, xx=range(-20,0),yy=np.random.rand(20))
        # self.ani = animation.FuncAnimation(self.BigDiagram.figure, self.update_line, blit=True, interval=25)
        print('d')
        pass
