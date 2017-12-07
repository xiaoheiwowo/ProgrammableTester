#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# 绘图类
# import diagram
# socketserver
from socketserver import TCPServer
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 控制方式窗口Ui类
from ui import controlmodesetui
# 电流曲线窗口Ui类
from ui import currentdiagramui
# 电源及采样校准窗口Ui类
from ui import powercalibrationui
# 电源设置Ui类
from ui import powersetui
# 继电器阵列自检Ui类
from ui import relaycheckui
# 外控设置窗口Ui类
from ui import remotecontrolsetui
# 主窗口Ui类
from ui import mainwindowui

from ui import currentwindowui

import tcpsocket
# import qdarkstyle


class PT_MainWindow(QMainWindow, mainwindowui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PT_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Action_ControlSet.triggered.connect(self.showControlSetForm)
        self.Action_RemoteControl.triggered.connect(self.showRemoteControlForm)
        self.Action_Others.triggered.connect(self.showPowerSetForm)
        self.Action_PowerCalibration.triggered.connect(self.showPowerCalibrationForm)
        self.Action_RelayCheck.triggered.connect(self.showRelayCheckForm)

        self.BT_FullScreen.clicked.connect(self.showCurrentDiagramForm)

    def showControlSetForm(self):
        self.controlset = PT_ControlModeSet()
        self.controlset.show()

    def showRemoteControlForm(self):
        self.remotecontrol = PT_RemoteControlSet()
        self.remotecontrol.show()

    def showCurrentDiagramForm(self):
        self.currentdiagram = PT_CurrentDiagram()
        self.currentdiagram.show()

    def showPowerCalibrationForm(self):
        self.powercalibration = PT_PowerCalibration()
        self.powercalibration.show()

    def showRelayCheckForm(self):
        self.relaycheck = PT_RelaySelfCheck()
        self.relaycheck.show()

    def showPowerSetForm(self):
        self.powerset = PT_PowerSet()
        self.powerset.show()


class PT_ControlModeSet(controlmodesetui.Ui_ControlModeSet):
    def __init__(self, parent=None):
        super(PT_ControlModeSet, self).__init__(parent)


class PT_RemoteControlSet(remotecontrolsetui.Ui_RemoteControlSet):
    def __init__(self, parent=None):
        super(PT_RemoteControlSet, self).__init__(parent)


class PT_CurrentDiagram(currentdiagramui.Ui_CurrentDiagram):
    def __init__(self, parent=None):
        super(PT_CurrentDiagram, self).__init__(parent)


class PT_PowerCalibration(powercalibrationui.Ui_PowerCalibration):
    def __init__(self, parent=None):
        super(PT_PowerCalibration, self).__init__(parent)


class PT_RelaySelfCheck(relaycheckui.Ui_RelaySelfCheck):
    def __init__(self, parent=None):
        super(PT_RelaySelfCheck, self).__init__(parent)


class PT_PowerSet(powersetui.Ui_PowerSet):
    def __init__(self, parent=None):
        super(PT_PowerSet, self).__init__(parent)


class PT_CurrentWindow(currentwindowui.Ui_CurrentWindow):
    def __init__(self, parent=None):
        super(PT_CurrentWindow, self).__init__(parent)


class tcpThread(QThread):
    def __init__(self):
        super(tcpThread, self).__init__()
        print('new thread init')

    def run(self):
        serv = TCPServer(('localhost', 21567), tcpsocket.TcpHandler)
        serv.serve_forever()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置字体 在树莓派上使用注释下行
    # app.setFont(QFont('微软雅黑 Semilight', 9))
    # 启动server线程
    # thread = tcpThread()
    # thread.start()

    win = PT_MainWindow()
    # win = PT_ControlModeSet()
    # win = PT_RemoteControlSet()
    # win = PT_CurrentDiagram()
    # win = PT_CurrentWindow()
    # win = PT_PowerCalibration()
    # win = PT_RelaySelfCheck()
    # win = PT_PowerSet()
    # 全局黑色主题
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win.show()
    sys.exit(app.exec_())
