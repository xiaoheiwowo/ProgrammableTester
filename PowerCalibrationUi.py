#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import DialogButton

class Ui_PowerCalibrationUi(QtWidgets.QDialog):
    '''
    电源及采样校准
    '''
    def __init__(self, parent=None):
        super(Ui_PowerCalibrationUi, self).__init__(parent)
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

        self.Tab_DCV = QtWidgets.QWidget(TabWgt)
        self.Tab_DCA = QtWidgets.QWidget(TabWgt)
        self.Tab_ACV = QtWidgets.QWidget(TabWgt)
        self.Tab_ACA = QtWidgets.QWidget(TabWgt)

        TabWgt.addTab(self.Tab_DCV, '直流电压')
        TabWgt.addTab(self.Tab_DCA, '直流电流')
        TabWgt.addTab(self.Tab_ACV, '交流电压')
        TabWgt.addTab(self.Tab_ACA, '交流电流')

        dfdf