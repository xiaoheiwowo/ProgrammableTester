#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from PyQt5 import QtCore, QtGui, QtWidgets

from ui import dialogbutton


from public.datacache import Flag_Of as flag


class Ui_RelaySelfCheck(QtWidgets.QDialog):
    """
    电源及采样校准
    """

    def __init__(self, parent=None):
        super(Ui_RelaySelfCheck, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电源及采样校准')
        self.setWindowIcon(QtGui.QIcon(":/logo.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.setFixedSize(300, 50)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(self.DB_DialogButton)

        self.DB_DialogButton.BT_Save1.setText('开始')
        self.DB_DialogButton.BT_OK1.setText('停止')
        self.DB_DialogButton.BT_Cancel1.setText('返回')
        # 信号
        self.DB_DialogButton.BT_Save1.clicked.connect(self.CheckBegin)
        self.DB_DialogButton.BT_OK1.clicked.connect(self.CheckStop)

        TabWgt = QtWidgets.QTabWidget(self)
        # TabWgt.setFixedSize(1000, 450)

        self.Tab_PowerON = QtWidgets.QWidget(TabWgt)
        self.Tab_PowerOFF = QtWidgets.QWidget(TabWgt)

        TabWgt.addTab(self.Tab_PowerON, '线圈通电')
        TabWgt.addTab(self.Tab_PowerOFF, '线圈断电')

        Layout_Main = QtWidgets.QVBoxLayout()
        Layout_Main.addWidget(TabWgt)
        Layout_Main.addLayout(Layout_button)
        self.setLayout(Layout_Main)

        # 故障指示
        # self.Label_Fault = QtWidgets.QLabel(TabWgt)
        # self.Label_Fault.setText('故障:')
        # self.Label_Fault.setGeometry(900, -5, 50, 30)

        # self.Label_Mark = QtWidgets.QLabel(TabWgt)
        # self.Label_Mark.setPixmap(QtGui.QPixmap(':/trouble_update_24px_2350_easyicon.net.png'))
        # self.Label_Mark.setGeometry(950, -5, 50, 30)

        self.StopMark = 0
        self.array_on = []
        self.array_off = []
        self.Init_TabON()
        self.Init_TabOFF()

        global flag_relay_check
        flag_relay_check = 1

    def Init_TabON(self):
        """
        生成TabOFF标签页按钮
        :return:
        """

        for x in range(16):
            for y in range(10):
                self.array_on.append(QtWidgets.QLabel(self.Tab_PowerON))
                self.array_on[x * 10 + y].setText('J0' + str((str(hex(x))[2]).upper()) + '0' + str(y))
                self.array_on[x * 10 + y].setGeometry(55 * (x + 1), 40 * (y + 0.5), 50, 25)
                self.array_on[x * 10 + y].setAlignment(QtCore.Qt.AlignCenter)
                self.array_on[x * 10 + y].setStyleSheet('background-color:gray')

    def Init_TabOFF(self):
        """
        生成TabOFF标签页按钮
        :return:
        """

        for x in range(16):
            for y in range(10):
                self.array_off.append(QtWidgets.QLabel(self.Tab_PowerOFF))
                self.array_off[x * 10 + y].setText('J0' + str((str(hex(x))[2]).upper()) + '0' + str(y))
                self.array_off[x * 10 + y].setGeometry(55 * (x + 1), 40 * (y + 0.5), 50, 25)
                self.array_off[x * 10 + y].setAlignment(QtCore.Qt.AlignCenter)
                self.array_off[x * 10 + y].setStyleSheet('background-color:gray')

    def CheckBegin(self):
        """

        :return:
        """
        for i in range(160):
            if random.random() > 0.95:
                self.array_on[i].setStyleSheet('background-color:red')
                self.array_off[i].setStyleSheet('background-color:red')

            else:
                self.array_on[i].setStyleSheet('background-color:green')
                self.array_off[i].setStyleSheet('background-color:green')

            if self.StopMark == 1:
                self.StopMark = 0
                break
        flag.relay_check = 1

    def CheckStop(self):
        """

        :return:
        """
        self.StopMark = 1
        flag.relay_check = 0

    @staticmethod
    def get_value(_index, _on, _off):
        """
        获取值槽函数
        :return:
        """
        print(_index, _on, _off)


class CheckThread(QtCore.QThread):
    """
    自检继电器线程
    """

    def __init__(self, _win):
        super(CheckThread, self).__init__()
        self.win = _win

    def run(self):
        """
        运行函数
        :return:
        """
        while True:
            time.sleep(0.5)
            pass
