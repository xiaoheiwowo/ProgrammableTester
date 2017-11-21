#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import dialogbutton

class Ui_RemoteControlSet(QtWidgets.QDialog):
    '''
    远程控制设置窗口，主要是网络连接
    '''
    def __init__(self, parent = None):
        super(Ui_RemoteControlSet, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 550)
        self.setWindowTitle('外控设置')
        self.setWindowIcon(QtGui.QIcon(":/entertainment_valve_72px_547701_easyicon.net.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.setFixedSize(300, 50)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(self.DB_DialogButton)

        self.Init_LocalNetSet()
        self.Init_ServerSelect()
        self.Init_ConnectionState()
        self.Init_BusValveAdvance()
        self.Init_CurrentDiagramSet()

        Layout_Net = QtWidgets.QVBoxLayout()
        Layout_Net.addWidget(self.GB_LocalNetSet)
        Layout_Net.addWidget(self.GB_ServerSelect)

        Layout_Current = QtWidgets.QVBoxLayout()
        Layout_Current.addWidget(self.GB_Test)
        Layout_Current.addWidget(self.GB_CurrentDiagramSet)

        Layout_GB = QtWidgets.QHBoxLayout()
        Layout_GB.addLayout(Layout_Net)
        Layout_GB.addLayout(Layout_Current)
        Layout_GB.addWidget(self.GB_BusValveAdvance)

        Layout_Main = QtWidgets.QVBoxLayout(self)
        Layout_Main.addLayout(Layout_GB)
        Layout_Main.addLayout(Layout_button)


    # 初始化网络本地设置
    def Init_LocalNetSet(self):
        '''
        本机网络相关设置
        :return:
        '''
        self.GB_LocalNetSet = QtWidgets.QGroupBox(self)
        self.GB_LocalNetSet.setGeometry(10, 10, 300, 250)
        self.GB_LocalNetSet.setTitle('本机')
        # 本机网络设置控件
        self.Layout_LocalNetSet = QtWidgets.QGridLayout(self.GB_LocalNetSet)
        self.Label_b11 = QtWidgets.QLabel('本机名:')
        self.LE_LocalName = QtWidgets.QLineEdit()
        self.RB_AutoGetIP = QtWidgets.QRadioButton('自动获得IP')
        self.RB_AutoGetIP.setChecked(True)
        self.RB_UseSettingBelow = QtWidgets.QRadioButton('使用下面的设置')
        self.Label_b12 = QtWidgets.QLabel('本机IP:')
        self.LE_LocalIP = QtWidgets.QLineEdit()
        self.Label_b13 = QtWidgets.QLabel('子网掩码:')
        self.LE_SubnetMask = QtWidgets.QLineEdit()
        self.Label_b14 = QtWidgets.QLabel('默认网关:')
        self.LE_DefaultGateway = QtWidgets.QLineEdit()
        self.Label_b15 = QtWidgets.QLabel('DNS:')
        self.LE_DefaultDNS = QtWidgets.QLineEdit()

        self.LE_DefaultDNS.setPlaceholderText('192.168.10.190')
        # 本机网络设置布局
        self.Layout_LocalNetSet.addWidget(self.Label_b11, 0 ,0)
        self.Layout_LocalNetSet.addWidget(self.LE_LocalName, 0, 1)
        self.Layout_LocalNetSet.addWidget(self.RB_AutoGetIP, 1, 0, 1, 2)
        self.Layout_LocalNetSet.addWidget(self.RB_UseSettingBelow, 2, 0, 1, 2)
        self.Layout_LocalNetSet.addWidget(self.Label_b12, 3, 0)
        self.Layout_LocalNetSet.addWidget(self.LE_LocalIP, 3, 1)
        self.Layout_LocalNetSet.addWidget(self.Label_b13, 4, 0)
        self.Layout_LocalNetSet.addWidget(self.LE_SubnetMask, 4, 1)
        self.Layout_LocalNetSet.addWidget(self.Label_b14, 5, 0)
        self.Layout_LocalNetSet.addWidget(self.LE_DefaultGateway, 5, 1)
        self.Layout_LocalNetSet.addWidget(self.Label_b15, 6, 0)
        self.Layout_LocalNetSet.addWidget(self.LE_DefaultDNS, 6, 1)

        self.IPSetDisable()
        # SIGNAL
        self.RB_AutoGetIP.clicked.connect(self.IPSetDisable)
        self.RB_UseSettingBelow.clicked.connect(self.IPSetEnable)
    # 初始化网络服务器设置
    def Init_ServerSelect(self):
        '''

        :return:
        '''
        self.GB_ServerSelect = QtWidgets.QGroupBox(self)
        self.GB_ServerSelect.setGeometry(10, 265, 300, 100)
        self.GB_ServerSelect.setTitle('上位机')

        self.Layout_ServerSelect = QtWidgets.QGridLayout(self.GB_ServerSelect)
        self.Label_b21 = QtWidgets.QLabel('计算机名:')
        self.CB_ServerName = QtWidgets.QComboBox()
        self.Label_b22 = QtWidgets.QLabel('计算机IP:')
        self.CB_ServerIP = QtWidgets.QComboBox()

        # 布局
        self.Layout_ServerSelect.addWidget(self.Label_b21, 0, 0)
        self.Layout_ServerSelect.addWidget(self.CB_ServerName, 0, 1, 1, 3)

        self.Layout_ServerSelect.addWidget(self.Label_b22, 1 ,0)
        self.Layout_ServerSelect.addWidget(self.CB_ServerIP, 1, 1, 1, 3)
    # 初始化连接测试
    def Init_ConnectionState(self):
        self.GB_Test = QtWidgets.QGroupBox(self)
        self.GB_Test.setTitle('测试')
        self.GB_Test.setMaximumHeight(150)
        layout = QtWidgets.QHBoxLayout(self.GB_Test)

        self.Label_c11 = QtWidgets.QLabel(self)
        # self.Label_c11.setGeometry(600, 350, 48, 48)
        self.Label_c11.setPixmap(QtGui.QPixmap(':/connect_no_48px_19637_easyicon.net.png'))
        self.BT_ConnectTest = QtWidgets.QPushButton(self)
        # self.BT_ConnectTest.setGeometry(680, 350, 80, 40)
        self.BT_ConnectTest.setText('测试')

        layout.addStretch(1)
        layout.addWidget(self.Label_c11)
        layout.addStretch(1)
        layout.addWidget(self.BT_ConnectTest)
        layout.addStretch(1)

        # signal
        self.BT_ConnectTest.pressed.connect(self.ConnectToServer)
        self.BT_ConnectTest.released.connect(self.ConnectFailed)
    # 初始化总线阀高级设置
    def Init_BusValveAdvance(self):
        self.GB_BusValveAdvance = QtWidgets.QGroupBox(self)
        self.GB_BusValveAdvance.setTitle('总线阀高级设置')
        self.GB_BusValveAdvance.setGeometry(320, 10, 300, 300) #695, 500)

        Label_e11 = QtWidgets.QLabel('开阀命令:')
        Label_e12 = QtWidgets.QLabel('关阀命令:')
        Label_e13 = QtWidgets.QLabel('停阀命令:')
        Label_e14 = QtWidgets.QLabel('位置3命令:')
        Label_e15 = QtWidgets.QLabel('位置4命令:')
        Label_e16 = QtWidgets.QLabel('数据位:')
        Label_e17 = QtWidgets.QLabel('校验位:')
        Label_e18 = QtWidgets.QLabel('停止位:')
        self.LE_OpenCommand = QtWidgets.QLineEdit()
        self.LE_CloseCommand = QtWidgets.QLineEdit()
        self.LE_StopCommand = QtWidgets.QLineEdit()
        self.LE_M3Command = QtWidgets.QLineEdit()
        self.LE_M4Command = QtWidgets.QLineEdit()
        self.CB_DataBits = QtWidgets.QComboBox()
        self.CB_CheckBits = QtWidgets.QComboBox()
        self.CB_StopBits = QtWidgets.QComboBox()
        # 布局
        layout = QtWidgets.QGridLayout(self.GB_BusValveAdvance)
        layout.addWidget(Label_e11,0,0)
        layout.addWidget(self.LE_OpenCommand,0,1)
        layout.addWidget(Label_e12)
        layout.addWidget(self.LE_CloseCommand)
        layout.addWidget(Label_e13)
        layout.addWidget(self.LE_StopCommand)
        layout.addWidget(Label_e14)
        layout.addWidget(self.LE_M3Command)
        layout.addWidget(Label_e15)
        layout.addWidget(self.LE_M4Command)
        layout.addWidget(Label_e16)
        layout.addWidget(self.CB_DataBits)
        layout.addWidget(Label_e17)
        layout.addWidget(self.CB_CheckBits)
        layout.addWidget(Label_e18)
        layout.addWidget(self.CB_StopBits)
    # 初始化电流曲线设置
    def Init_CurrentDiagramSet(self):
        self.GB_CurrentDiagramSet = QtWidgets.QGroupBox(self)
        self.GB_CurrentDiagramSet.setGeometry(320, 315, 300, 195)
        self.GB_CurrentDiagramSet.setTitle('电流曲线设置')

        Label_f11 = QtWidgets.QLabel('数据储存深度：')
        Label_f12 = QtWidgets.QLabel('pts')
        Label_f13 = QtWidgets.QLabel('数据保存间隔：')
        Label_f14 = QtWidgets.QLabel('ms')
        Label_f15 = QtWidgets.QLabel('可保存总时长：')
        Label_f16 = QtWidgets.QLabel('小窗口曲线显示时长：')
        Label_f17 = QtWidgets.QLabel('s')
        self.Label_TotalTime = QtWidgets.QLabel('196.605 s')
        self.Label_TotalTime.setMaximumHeight(15)

        self.LE_DataStorageDepth = QtWidgets.QLineEdit()
        self.SB_DateStorageInterval = QtWidgets.QSpinBox()
        self.SB_DisplayTime = QtWidgets.QSpinBox()

        layout = QtWidgets.QGridLayout(self.GB_CurrentDiagramSet)
        layout.addWidget(Label_f11, 1, 0)
        layout.addWidget(self.LE_DataStorageDepth, 1 ,1)
        layout.addWidget(Label_f12, 1, 2)
        layout.addWidget(Label_f13, 2, 0)
        layout.addWidget(self.SB_DateStorageInterval, 2, 1)
        layout.addWidget(Label_f14, 2, 2)
        layout.addWidget(Label_f15, 3, 0)
        layout.addWidget(self.Label_TotalTime, 3, 1)
        layout.addWidget(Label_f16, 4, 0)
        layout.addWidget(self.SB_DisplayTime, 4, 1)
        layout.addWidget(Label_f17, 4, 2)
    # 槽
    def IPSetEnable(self):
        self.LE_LocalIP.setDisabled(False)
        self.LE_SubnetMask.setDisabled(False)
        self.LE_DefaultGateway.setDisabled(False)
        self.LE_DefaultDNS.setDisabled(False)

    def IPSetDisable(self):
        self.LE_LocalIP.setDisabled(True)
        self.LE_SubnetMask.setDisabled(True)
        self.LE_DefaultGateway.setDisabled(True)
        self.LE_DefaultDNS.setDisabled(True)

    def ConnectToServer(self):
        self.Label_c11.setPixmap(QtGui.QPixmap(':/connect_creating_48px_15285_easyicon.net.png'))

    def ConnectFailed(self):
        self.Label_c11.setPixmap(QtGui.QPixmap(':/connect_no_48px_19637_easyicon.net.png'))