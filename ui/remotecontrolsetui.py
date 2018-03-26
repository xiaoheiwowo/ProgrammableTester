# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import dialogbutton
# 全局变量静态类
from public.datacache import SoftwareData as sw

import pickle
import json


class Ui_RemoteControlSet(QtWidgets.QDialog):
    """
    远程控制设置窗口，主要是网络连接
    """

    def __init__(self, parent=None):
        super(Ui_RemoteControlSet, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('网络及其他设置')
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

        self.Init_LocalNetSet()
        # self.Init_ServerSelect()
        # self.Init_ConnectionState()
        self.Init_BusValveAdvance()
        self.Init_CurrentDiagramSet()

        Layout_Net = QtWidgets.QVBoxLayout()
        Layout_Net.addWidget(self.GB_LocalNetSet)
        # Layout_Net.addWidget(self.GB_ServerSelect)

        Layout_Current = QtWidgets.QVBoxLayout()
        # Layout_Current.addWidget(self.GB_Test)
        Layout_Current.addWidget(self.GB_CurrentDiagramSet)

        Layout_GB = QtWidgets.QHBoxLayout()
        Layout_GB.addLayout(Layout_Net)
        Layout_GB.addLayout(Layout_Current)
        Layout_GB.addWidget(self.GB_BusValveAdvance)

        Layout_Main = QtWidgets.QVBoxLayout(self)
        Layout_Main.addLayout(Layout_GB)
        Layout_Main.addLayout(Layout_button)

        self.load_all()
        # signal
        self.DB_DialogButton.BT_Save1.clicked.connect(self.save_all)
        self.DB_DialogButton.BT_OK1.clicked.connect(self.save_and_exit)

    def Init_LocalNetSet(self):
        """
        初始化网络本地设置
        :return:
        """
        self.GB_LocalNetSet = QtWidgets.QGroupBox(self)
        # self.GB_LocalNetSet.setGeometry(10, 10, 300, 250)
        self.GB_LocalNetSet.setTitle('网络设置（重启生效）')
        # 本机网络设置控件
        self.Layout_LocalNetSet = QtWidgets.QGridLayout(self.GB_LocalNetSet)

        self.lb_server_ip = QtWidgets.QLabel('服务器IP：')
        self.LE_server_ip = QtWidgets.QLineEdit()

        self.Label_b11 = QtWidgets.QLabel('本机名称:')
        self.LE_LocalName = QtWidgets.QLineEdit()
        vali_hostname = QtGui.QRegExpValidator(self)
        reg = QtCore.QRegExp('[a-zA-Z0-9\\s]+$')
        vali_hostname.setRegExp(reg)
        self.LE_LocalName.setValidator(vali_hostname)
        self.RB_AutoGetIP = QtWidgets.QRadioButton('自动获得IP')
        self.RB_AutoGetIP.setChecked(True)
        self.RB_UseSettingBelow = QtWidgets.QRadioButton('使用下面的设置')
        vali_ip = QtGui.QRegExpValidator(self)
        regip = QtCore.QRegExp('^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)$')
        vali_ip.setRegExp(regip)
        self.Label_b12 = QtWidgets.QLabel('本机IP:')
        self.LE_LocalIP = QtWidgets.QLineEdit()
        self.LE_LocalIP.setValidator(vali_ip)

        # 子网掩码使用默认255.255.255.0
        # self.Label_b13 = QtWidgets.QLabel('子网掩码:')
        # self.LE_SubnetMask = QtWidgets.QLineEdit()
        # self.LE_SubnetMask.setValidator(vali_ip)

        self.Label_b14 = QtWidgets.QLabel('默认网关:')
        self.LE_DefaultGateway = QtWidgets.QLineEdit()
        self.LE_DefaultGateway.setValidator(vali_ip)
        self.Label_b15 = QtWidgets.QLabel('DNS:')
        self.LE_DefaultDNS = QtWidgets.QLineEdit()
        self.LE_DefaultDNS.setValidator(vali_ip)

        self.LE_DefaultDNS.setPlaceholderText('192.168.10.190')
        # 网络设置布局
        self.Layout_LocalNetSet.addWidget(self.lb_server_ip, 0, 0, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.LE_server_ip, 0, 1, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.Label_b11, 1, 0, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.LE_LocalName, 1, 1, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.RB_AutoGetIP, 2, 0, 1, 2)
        self.Layout_LocalNetSet.addWidget(self.RB_UseSettingBelow, 3, 0, 1, 2)
        self.Layout_LocalNetSet.addWidget(self.Label_b12, 4, 0, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.LE_LocalIP, 4, 1, 1, 2)
        # self.Layout_LocalNetSet.addWidget(self.Label_b13, 4, 0)
        # self.Layout_LocalNetSet.addWidget(self.LE_SubnetMask, 4, 1)
        self.Layout_LocalNetSet.addWidget(self.Label_b14, 5, 0, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.LE_DefaultGateway, 5, 1, 1, 2)
        self.Layout_LocalNetSet.addWidget(self.Label_b15, 6, 0, 1, 1)
        self.Layout_LocalNetSet.addWidget(self.LE_DefaultDNS, 6, 1, 1, 2)

        self.IPSetDisable()
        # SIGNAL
        self.RB_AutoGetIP.clicked.connect(self.IPSetDisable)
        self.RB_UseSettingBelow.clicked.connect(self.IPSetEnable)

    # 不显示
    def Init_ServerSelect(self):
        """
        初始化网络服务器设置
        :return:
        """
        self.GB_ServerSelect = QtWidgets.QGroupBox(self)
        self.GB_ServerSelect.setGeometry(10, 265, 300, 100)
        self.GB_ServerSelect.setTitle('服务器地址')

        self.Layout_ServerSelect = QtWidgets.QGridLayout(self.GB_ServerSelect)
        # self.Label_b21 = QtWidgets.QLabel('计算机名:')
        # self.CB_ServerName = QtWidgets.QComboBox()
        # for i in sw.upper_name_list:
        #     self.CB_ServerName.addItem(i)

        self.Label_b22 = QtWidgets.QLabel('计算机IP:')
        self.LE_server_ip = QtWidgets.QLineEdit()
        # self.CB_ServerIP = QtWidgets.QComboBox()
        # for i in sw.upper_ip_list:
        #     self.CB_ServerIP.addItem(i)

        # 布局
        # self.Layout_ServerSelect.addWidget(self.Label_b21, 0, 0)
        # self.Layout_ServerSelect.addWidget(self.CB_ServerName, 0, 1, 1, 3)

        self.Layout_ServerSelect.addWidget(self.Label_b22, 1, 0)
        self.Layout_ServerSelect.addWidget(self.LE_server_ip, 1, 1, 1, 3)
        # SIGNAL
        # self.CB_ServerIP.currentIndexChanged.connect(self.CB_ServerName.setCurrentIndex)
        # self.CB_ServerName.currentIndexChanged.connect(self.CB_ServerIP.setCurrentIndex)

    # 不显示
    def Init_ConnectionState(self):
        """
        初始化连接测试
        :return:
        """
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

    def Init_BusValveAdvance(self):
        """
        初始化总线阀高级设置
        :return:
        """
        self.GB_BusValveAdvance = QtWidgets.QGroupBox(self)
        self.GB_BusValveAdvance.setTitle('总线阀高级设置')
        # self.GB_BusValveAdvance.setGeometry(320, 10, 300, 300) #695, 500)

        vali_cmd = QtGui.QRegExpValidator(self)
        reg_cmd = QtCore.QRegExp('[0-9A-Z]{2}\\s[0-9A-Z]{2}\\s[0-9A-Z]{2}\\s[0-9A-Z]{2}\\s[0-9A-Z]{2}\\s[0-9A-Z]{2}\\'
                                 's[0-9A-Z]{2}\\s[0-9A-Z]{2}$')
        vali_cmd.setRegExp(reg_cmd)
        Label_e11 = QtWidgets.QLabel('开阀命令:')
        Label_e12 = QtWidgets.QLabel('关阀命令:')
        Label_e13 = QtWidgets.QLabel('停阀命令:')
        Label_e14 = QtWidgets.QLabel('位置3命令:')
        Label_e15 = QtWidgets.QLabel('位置4命令:')
        Label_e16 = QtWidgets.QLabel('数据位:')
        Label_e17 = QtWidgets.QLabel('校验位:')
        Label_e18 = QtWidgets.QLabel('停止位:')
        self.LE_OpenCommand = QtWidgets.QLineEdit()
        self.LE_OpenCommand.setValidator(vali_cmd)
        self.LE_CloseCommand = QtWidgets.QLineEdit()
        self.LE_CloseCommand.setValidator(vali_cmd)
        self.LE_StopCommand = QtWidgets.QLineEdit()
        self.LE_StopCommand.setValidator(vali_cmd)
        self.LE_M3Command = QtWidgets.QLineEdit()
        self.LE_M3Command.setValidator(vali_cmd)
        self.LE_M4Command = QtWidgets.QLineEdit()
        self.LE_M4Command.setValidator(vali_cmd)
        self.CB_DataBits = QtWidgets.QComboBox()
        self.CB_DataBits.addItem('5')
        self.CB_DataBits.addItem('6')
        self.CB_DataBits.addItem('7')
        self.CB_DataBits.addItem('8')
        self.CB_CheckBits = QtWidgets.QComboBox()
        self.CB_CheckBits.addItem('None')
        self.CB_CheckBits.addItem('Even')
        self.CB_CheckBits.addItem('Odd')
        self.CB_CheckBits.addItem('Mark')
        self.CB_CheckBits.addItem('Space')
        self.CB_StopBits = QtWidgets.QComboBox()
        self.CB_StopBits.addItem('1')
        self.CB_StopBits.addItem('1.5')
        self.CB_StopBits.addItem('2')
        # 布局
        layout = QtWidgets.QGridLayout(self.GB_BusValveAdvance)
        layout.addWidget(Label_e11, 0, 0)
        layout.addWidget(self.LE_OpenCommand, 0, 1)
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

    def Init_CurrentDiagramSet(self):
        """
        初始化电流曲线设置
        :return:
        """
        self.GB_CurrentDiagramSet = QtWidgets.QGroupBox(self)
        # self.GB_CurrentDiagramSet.setGeometry(320, 315, 300, 195)
        self.GB_CurrentDiagramSet.setTitle('电流曲线设置')

        Label_f11 = QtWidgets.QLabel('数据储存深度：')
        Label_f12 = QtWidgets.QLabel('pts')
        Label_f13 = QtWidgets.QLabel('数据保存间隔：')
        Label_f14 = QtWidgets.QLabel('ms')
        Label_f15 = QtWidgets.QLabel('可保存总时长：')
        Label_f16 = QtWidgets.QLabel('默认显示时长：')
        Label_f17 = QtWidgets.QLabel('s')
        self.Label_TotalTime = QtWidgets.QLabel('196.605 s')
        self.Label_TotalTime.setMaximumHeight(15)

        self.LE_DataStorageDepth = QtWidgets.QLineEdit()
        # 整形验证器
        vali_int = QtGui.QIntValidator(self)
        vali_int.setRange(0, 65535)
        self.LE_DataStorageDepth.setValidator(vali_int)
        self.SB_DateStorageInterval = QtWidgets.QSpinBox()
        self.SB_DateStorageInterval.setRange(0, 100)
        self.SB_DisplayTime = QtWidgets.QSpinBox()
        self.SB_DisplayTime.setRange(0, 60)

        layout = QtWidgets.QGridLayout(self.GB_CurrentDiagramSet)
        layout.addWidget(Label_f11, 1, 0)
        layout.addWidget(self.LE_DataStorageDepth, 1, 1)
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
        """

        :return:
        """
        self.LE_LocalIP.setDisabled(False)
        # self.LE_SubnetMask.setDisabled(False)
        self.LE_DefaultGateway.setDisabled(False)
        self.LE_DefaultDNS.setDisabled(False)

    def IPSetDisable(self):
        """

        :return:
        """

        self.LE_LocalIP.setDisabled(True)
        # self.LE_SubnetMask.setDisabled(True)
        self.LE_DefaultGateway.setDisabled(True)
        self.LE_DefaultDNS.setDisabled(True)

    def ConnectToServer(self):
        """

        :return:
        """
        self.Label_c11.setPixmap(QtGui.QPixmap(':/connect_creating_48px_15285_easyicon.net.png'))

    def ConnectFailed(self):
        """

        :return:
        """
        self.Label_c11.setPixmap(QtGui.QPixmap(':/connect_no_48px_19637_easyicon.net.png'))

    def save_all(self):
        """
        保存设置
        :return:
        """
        sw.net_set['server_ip'] = self.LE_server_ip.text()
        sw.net_set['host_name'] = self.LE_LocalName.text()
        sw.net_set['host_ip'] = self.LE_LocalIP.text()
        # sw.net_set['subnet_mask'] = self.LE_SubnetMask.text()
        sw.net_set['default_gateway'] = self.LE_DefaultGateway.text()
        sw.net_set['dns'] = self.LE_DefaultDNS.text()

        sw.current_set['data_depth'] = int(self.LE_DataStorageDepth.text())
        sw.current_set['data_interval'] = self.SB_DateStorageInterval.value()
        sw.current_set['data_time'] = sw.current_set['data_depth'] * sw.current_set['data_interval'] / 1000
        self.Label_TotalTime.setText(str(sw.current_set['data_time']) + ' s')
        sw.current_set['small_win_show_time'] = self.SB_DisplayTime.value()

        sw.bus_control[0] = self.LE_OpenCommand.text()
        sw.bus_control[1] = self.LE_CloseCommand.text()
        sw.bus_control[2] = self.LE_StopCommand.text()
        sw.bus_control[3] = self.LE_M3Command.text()
        sw.bus_control[4] = self.LE_M4Command.text()
        sw.bus_control[5] = self.CB_DataBits.currentIndex()
        sw.bus_control[6] = self.CB_CheckBits.currentIndex()
        sw.bus_control[7] = self.CB_StopBits.currentIndex()

        if self.RB_AutoGetIP.isChecked():
            sw.net_set['auto_ip'] = True
        else:
            sw.net_set['auto_ip'] = False

        with open('pkl/currentset.pkl', 'wb') as f1:
            f1.write(pickle.dumps(sw.current_set))
        with open('pkl/netset.pkl', 'wb') as f2:
            f2.write(pickle.dumps(sw.net_set))
        with open('pkl/buscontrol.pkl', 'wb') as f3:
            f3.write(pickle.dumps(sw.bus_control))
        # Json
        # with open('json/data.json', 'w') as f:
        # json.dump(gv.data, f, ensure_ascii=False, indent=10)

    def load_all(self):
        """

        :return:
        """
        with open('pkl/currentset.pkl', 'rb') as f1:
            sw.current_set = pickle.loads(f1.read())
        with open('pkl/netset.pkl', 'rb') as f2:
            sw.net_set = pickle.loads(f2.read())
        with open('pkl/buscontrol.pkl', 'rb') as f3:
            sw.bus_control = pickle.loads(f3.read())

        self.LE_server_ip.setText(sw.net_set['server_ip'])
        self.LE_LocalName.setText(sw.net_set['host_name'])
        self.LE_LocalIP.setText(sw.net_set['host_ip'])
        # self.LE_SubnetMask.setText(sw.net_set['subnet_mask'])
        self.LE_DefaultGateway.setText(sw.net_set['default_gateway'])
        self.LE_DefaultDNS.setText(sw.net_set['dns'])

        self.LE_DataStorageDepth.setText(str(sw.current_set['data_depth']))
        self.SB_DateStorageInterval.setValue(sw.current_set['data_interval'])
        self.Label_TotalTime.setText(str(sw.current_set['data_time']) + ' s')
        self.SB_DisplayTime.setValue(sw.current_set['small_win_show_time'])

        self.LE_OpenCommand.setText(sw.bus_control[0])
        self.LE_CloseCommand.setText(sw.bus_control[1])
        self.LE_StopCommand.setText(sw.bus_control[2])
        self.LE_M3Command.setText(sw.bus_control[3])
        self.LE_M4Command.setText(sw.bus_control[4])
        self.CB_DataBits.setCurrentIndex(sw.bus_control[5])
        self.CB_CheckBits.setCurrentIndex(sw.bus_control[6])
        self.CB_StopBits.setCurrentIndex(sw.bus_control[7])

        if sw.net_set['auto_ip']:
            self.RB_AutoGetIP.setChecked(True)
            self.IPSetDisable()
            self.RB_UseSettingBelow.setChecked(False)
        else:
            self.RB_AutoGetIP.setChecked(False)
            self.IPSetEnable()
            self.RB_UseSettingBelow.setChecked(True)

        # 修改系统文件
        pass

    def save_and_exit(self):
        """
        保存退出
        :return:
        """

        self.save_all()
        self.close()
