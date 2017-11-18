#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import DialogButton

class Ui_RelaySelfCheckUi(QtWidgets.QDialog):
    '''
    电源及采样校准
    '''
    def __init__(self, parent=None):
        super(Ui_RelaySelfCheckUi, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 600)
        self.setWindowTitle('电源及采样校准')
        self.setWindowIcon(QtGui.QIcon(":/entertainment_valve_72px_547701_easyicon.net.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # 保存、确定、取消按钮
        self.DB_DialogButton = DialogButton.DialogButton(self)
        self.DB_DialogButton.move(700, 530)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

        TabWgt = QtWidgets.QTabWidget(self)
        TabWgt.setGeometry(12, 10, 1000, 510)

        self.Tab_PowerON = QtWidgets.QWidget(TabWgt)
        self.Tab_PowerOFF = QtWidgets.QWidget(TabWgt)

        TabWgt.addTab(self.Tab_PowerON, '线圈通电')
        TabWgt.addTab(self.Tab_PowerOFF, '线圈断电')

        self.Init_TabON()
        self.Init_TabOFF()

    def Init_TabON(self):
        pass

    def Init_TabOFF(self):
        pass