#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import random

import dialogbutton

class Ui_RelaySelfCheck(QtWidgets.QDialog):
    '''
    电源及采样校准
    '''
    def __init__(self, parent=None):
        super(Ui_RelaySelfCheck, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 600)
        self.setWindowTitle('电源及采样校准')
        self.setWindowIcon(QtGui.QIcon(":/entertainment_valve_72px_547701_easyicon.net.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.move(700, 530)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

        self.DB_DialogButton.BT_Save1.setText('开始')
        self.DB_DialogButton.BT_OK1.setText('停止')
        self.DB_DialogButton.BT_Cancel1.setText('返回')

        self.DB_DialogButton.BT_Save1.clicked.connect(self.CheckBegin)
        self.DB_DialogButton.BT_OK1.clicked.connect(self.CheckStop)

        TabWgt = QtWidgets.QTabWidget(self)
        TabWgt.setGeometry(12, 10, 1000, 510)

        self.Tab_PowerON = QtWidgets.QWidget(TabWgt)
        self.Tab_PowerOFF = QtWidgets.QWidget(TabWgt)

        TabWgt.addTab(self.Tab_PowerON, '线圈通电')
        TabWgt.addTab(self.Tab_PowerOFF, '线圈断电')

        self.Label_Fault = QtWidgets.QLabel(TabWgt)
        self.Label_Fault.setText('故障:')
        self.Label_Fault.setGeometry(900, -5, 50, 30)

        self.Label_Mark = QtWidgets.QLabel(TabWgt)
        self.Label_Mark.setPixmap(QtGui.QPixmap(':/trouble_update_24px_2350_easyicon.net.png'))
        self.Label_Mark.setGeometry(950, -5, 50, 30)


        self.StopMark = 0
        self.Init_TabON()
        self.Init_TabOFF()

    def Init_TabON(self):

        self.arry=[]
        for x in range(16):
            for y in range(10):
                self.arry.append(QtWidgets.QLabel(self.Tab_PowerON))
                self.arry[x*10+y].setText('J0' + str((str(hex(x))[2]).upper()) + '0' + str(y))
                self.arry[x*10+y].setGeometry(55*(x+1), 40*(y+0.5), 50, 25)
                self.arry[x*10+y].setAlignment(QtCore.Qt.AlignCenter)
                # self.arry[x*10+y].setFont(QtGui.QFont('', 10))
                self.arry[x*10+y].setStyleSheet('background-color:gray')

    def Init_TabOFF(self):
        self.arryB=[]
        for x in range(16):
            for y in range(10):
                self.arryB.append(QtWidgets.QLabel(self.Tab_PowerOFF))
                self.arryB[x*10+y].setText('J0' + str((str(hex(x))[2]).upper()) + '0' + str(y))
                self.arryB[x*10+y].setGeometry(55*(x+1), 40*(y+0.5), 50, 25)
                self.arryB[x*10+y].setAlignment(QtCore.Qt.AlignCenter)
                # self.arryB[x*10+y].setFont(QtGui.QFont('', 10))
                self.arryB[x*10+y].setStyleSheet('background-color:gray')

    def CheckBegin(self):
        for i in range(160):
            if random.random() > 0.95:
                self.arry[i].setStyleSheet('background-color:red')
                self.arryB[i].setStyleSheet('background-color:red')

            else:
                self.arry[i].setStyleSheet('background-color:green')
                self.arryB[i].setStyleSheet('background-color:green')

            if self.StopMark == 1:
                self.StopMark = 0
                break

    def CheckStop(self):
        self.StopMark = 1