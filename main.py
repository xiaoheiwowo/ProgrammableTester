#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 主窗口Ui类
import mainwindowui

# 控制方式窗口Ui类
import controlmodesetui

# 外控设置窗口Ui类
import remotecontrolsetui

# 电流曲线窗口Ui类
import currentdiagramui

# 电源及采样校准窗口Ui类
import powercalibrationui

# 继电器阵列自检Ui类
import relaycheckui

# 电源设置Ui类
import powersetui

# 绘图类
import diagram

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置字体 在树莓派上使用注释下行
    app.setFont(QFont('微软雅黑 Semilight', 9))

    win = PT_MainWindow()
    # win = PT_ControlModeSet()
    # win = PT_RemoteControlSet()
    # win = PT_CurrentDiagram()
    # win = PT_PowerCalibration()
    # win = PT_RelaySelfCheck()
    # win = PT_PowerSet()
    win.show()
    sys.exit(app.exec_())


