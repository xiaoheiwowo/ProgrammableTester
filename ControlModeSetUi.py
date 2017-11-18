#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import DialogButton

import RemoteControlSetUi

class Ui_ControlModeSet(QtWidgets.QDialog):
    '''
    控制方式设置窗口，
    '''
    def __init__(self, parent = None):
        super(Ui_ControlModeSet, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 600)
        self.setWindowTitle('控制方式设置')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)



        self.Init_ControlModeList()
        self.Init_WiringDiagram()
        self.Init_Extend()

        # 保存、确定、取消按钮
        self.DB_DialogButton = DialogButton.DialogButton(self)
        self.DB_DialogButton.move(700, 530)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

    def Init_ControlModeList(self):
        self.TW_ControlModeList = QtWidgets.QTableWidget(self)
        self.TW_ControlModeList.setGeometry(0, 10, 200, 500)
        self.TW_ControlModeList.setRowCount(20)
        self.TW_ControlModeList.setColumnCount(2)
        self.TW_ControlModeList.setHorizontalHeaderLabels(['控制方式', '电压'])
        self.TW_ControlModeList.setColumnWidth(0, 89)
        self.TW_ControlModeList.setColumnWidth(1, 60)
        # self.TW_ControlModeList.setRowHeight(0, 30)

        for i in range(20):
            a = QtWidgets.QComboBox()
            a.addItem('DC')
            a.addItem('AC')
            # a.setStyleSheet('QComboBox{margin:3px};')
            self.TW_ControlModeList.setCellWidget(i, 1, a)

    def Init_WiringDiagram(self):

        self.GB_WiringDiagram = QtWidgets.QGroupBox(self)
        self.GB_WiringDiagram.setGeometry(210, 10, 600, 500)
        self.GB_WiringDiagram.setTitle('接线图')

    def Init_Extend(self):
        self.GB_Extend = QtWidgets.QGroupBox(self)
        self.GB_Extend.setGeometry(820, 10, 200, 500)
        self.GB_Extend.setTitle('附加参数')
        # 调节阀部分
        self.Layout_Extend = QtWidgets.QVBoxLayout(self.GB_Extend)
        self.CK_isAdjustValve = QtWidgets.QCheckBox(self.GB_Extend)
        self.CK_isAdjustValve.setText('是调节阀')
        self.CK_isAdjustValve.setMinimumHeight(40)

        self.Layout_ControlMode2 = QtWidgets.QHBoxLayout()
        self.Label_a11 = QtWidgets.QLabel('控制方式:')
        self.CB_ControlMode2 = QtWidgets.QComboBox()
        self.CB_ControlMode2.addItem('0~20mA')
        self.CB_ControlMode2.setMinimumHeight(40)
        self.Layout_ControlMode2.addWidget(self.Label_a11)
        self.Layout_ControlMode2.addWidget(self.CB_ControlMode2)

        self.Layout_ActionMode = QtWidgets.QHBoxLayout()
        self.Label_a12 = QtWidgets.QLabel('作用方式:')
        self.CB_ActionMode = QtWidgets.QComboBox()
        self.CB_ActionMode.setMinimumHeight(40)
        self.CB_ActionMode.addItem('正作用')
        self.CB_ActionMode.addItem('反作用')
        self.Layout_ActionMode.addWidget(self.Label_a12)
        self.Layout_ActionMode.addWidget(self.CB_ActionMode)
        # 分隔线
        self.line1 = QtWidgets.QFrame()
        self.line1.resize(200, 10)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        # 总线阀部分
        self.Layout_isBusValve = QtWidgets.QHBoxLayout()
        self.CK_isBusValve = QtWidgets.QCheckBox(self.GB_Extend)
        self.CK_isBusValve.setText('是总线阀')
        self.BT_Advanced = QtWidgets.QPushButton('高级>>')
        self.BT_Advanced.setMinimumHeight(40)
        self.Layout_isBusValve.addWidget(self.CK_isBusValve)
        self.Layout_isBusValve.addWidget(self.BT_Advanced)

        self.Layout_BusProtocol = QtWidgets.QHBoxLayout()
        self.Label_a13 = QtWidgets.QLabel('总线协议:')
        self.CB_BusProtocol = QtWidgets.QComboBox()
        self.CB_BusProtocol.addItem('ModBus')
        self.CB_BusProtocol.setMinimumHeight(40)
        self.Layout_BusProtocol.addWidget(self.Label_a13)
        self.Layout_BusProtocol.addWidget(self.CB_BusProtocol)

        self.Layout_BaudRate = QtWidgets.QHBoxLayout()
        self.Label_a14 = QtWidgets.QLabel('波特率:')
        self.CB_BaudRate = QtWidgets.QComboBox()
        self.CB_BaudRate.addItem('9600')
        self.CB_BaudRate.setMinimumHeight(40)
        self.Layout_BaudRate.addWidget(self.Label_a14)
        self.Layout_BaudRate.addWidget(self.CB_BaudRate)
        # 分隔线
        self.line2 = QtWidgets.QFrame()
        self.line2.resize(200, 10)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        # BP5部分
        self.CK_isBP5 = QtWidgets.QCheckBox('由测试仪控制停阀')
        self.Label_a15 = QtWidgets.QLabel('本测试仪感知到位反馈信号后自动停阀(BP5)')
        # 使Label自动换行
        self.Label_a15.resize(150, 200)
        self.Label_a15.setWordWrap(True)
        self.Label_a15.setAlignment(QtCore.Qt.AlignTop)

        # 附加参数布局
        self.Layout_Extend.addWidget(self.CK_isAdjustValve)
        self.Layout_Extend.addLayout(self.Layout_ControlMode2)
        self.Layout_Extend.addLayout(self.Layout_ActionMode)
        self.Layout_Extend.addWidget(self.line1)
        self.Layout_Extend.addLayout(self.Layout_isBusValve)
        self.Layout_Extend.addLayout(self.Layout_BusProtocol)
        self.Layout_Extend.addLayout(self.Layout_BaudRate)
        self.Layout_Extend.addWidget(self.line2)
        self.Layout_Extend.addWidget(self.CK_isBP5)
        self.Layout_Extend.addWidget(self.Label_a15)
        # 信号
        self.BT_Advanced.clicked.connect(self.showRemoteControlForm)

    def showRemoteControlForm(self):
        self.remotecontrolset = PT_RemoteControlSet()
        self.remotecontrolset.show()

class PT_RemoteControlSet(RemoteControlSetUi.Ui_RemoteControlSet):
    def __init__(self, parent=None):
        super(PT_RemoteControlSet, self).__init__(parent)

