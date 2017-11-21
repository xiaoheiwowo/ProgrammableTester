#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import dialogbutton

import diagram

import doubleslider
class Ui_CurrentDiagram(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Ui_CurrentDiagram, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 550)
        self.setWindowTitle('电流曲线')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 保存、确定、取消按钮
        # self.DB_DialogButton = DialogButton.DialogButton(self)
        # self.DB_DialogButton.move(700, 530)
        # self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

        self.Init_DiagramArea()

        wgt = QtWidgets.QWidget(self)
        wgt.setGeometry(920,10,90,580)
        layout = QtWidgets.QVBoxLayout(wgt)

        self.BT_Dynamic = QtWidgets.QPushButton('动态')
        self.BT_Static = QtWidgets.QPushButton('静态')

        layout.addWidget(self.BT_Dynamic)
        layout.addWidget(self.BT_Static)
        layout.addStretch(0)

    def Init_DiagramArea(self):
        GB_Diagram = QtWidgets.QGroupBox(self)
        GB_Diagram.setGeometry(10, 10, 900, 580)
        GB_Diagram.setTitle('电流曲线')

        wgt = QtWidgets.QWidget(self)
        wgt.setGeometry(50, 50, 900, 480)
        self.BigDiagram = diagram.BigPlotWidget(wgt)
        wgt2 = QtWidgets.QWidget(wgt)
        wgt2.setGeometry(0, 40, 100, 100)
        layout = QtWidgets.QVBoxLayout(wgt2)

        self.Label_d11 = QtWidgets.QLabel('BD3S')
        self.Label_d12 = QtWidgets.QLabel('DC 5V')
        self.Label_d13 = QtWidgets.QLabel('200mA')
        layout.addWidget(self.Label_d11)
        layout.addWidget(self.Label_d12)
        layout.addWidget(self.Label_d13)

        self.DS_DataSlider = doubleslider.MDoubleSlider(GB_Diagram)
        self.DS_DataSlider.setGeometry(50, 530, 800, 50)

        self.BT_ZoomIn = QtWidgets.QPushButton(GB_Diagram)
        self.BT_ZoomIn.setFixedSize(50, 50)
        style = '''QPushButton {background-image: url("./images/zoomin.png")}'''
        self.BT_ZoomIn.setStyleSheet(style)
        self.BT_ZoomIn.setGeometry(850, 5, 50, 50)

        # 信号
        self.BT_ZoomIn.clicked.connect(self.close)