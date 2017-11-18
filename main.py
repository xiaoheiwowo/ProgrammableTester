#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 主窗口Ui类
import MainWindowUi

# 控制方式窗口Ui类
import ControlModeSetUi

# 外控设置窗口Ui类
import RemoteControlSetUi

# 电流曲线窗口Ui类
import CurrentDiagramUi

# 电源及采样校准窗口Ui类
import PowerCalibrationUi

# 绘图类
import Diagram

class PT_MainWindow(QMainWindow, MainWindowUi.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PT_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Action_ControlSet.triggered.connect(self.showControlSetForm)
        self.Action_RemoteControl.triggered.connect(self.showRemoteControlForm)
        self.Action_Others.triggered.connect(self.showRemoteControlForm)

        self.BT_FullScreen.clicked.connect(self.showCurrentDiagramForm)

        # 电流曲线
        wgt = QWidget(self)
        wgt.setGeometry(450, 50, 450, 160)
        DIAGRAM = Diagram.PlotWidget(wgt)

    def showControlSetForm(self):
        self.controlset = PT_ControlModeSet()
        self.controlset.show()


    def showRemoteControlForm(self):
        self.remotecontrol = PT_RemoteControlSet()
        self.remotecontrol.show()


    def showCurrentDiagramForm(self):
        self.currentdiagram = PT_CurrentDiagram()
        self.currentdiagram.show()

class PT_ControlModeSet(ControlModeSetUi.Ui_ControlModeSet):
    def __init__(self, parent=None):
        super(PT_ControlModeSet, self).__init__(parent)

class PT_RemoteControlSet(RemoteControlSetUi.Ui_RemoteControlSet):
    def __init__(self, parent=None):
        super(PT_RemoteControlSet, self).__init__(parent)

class PT_CurrentDiagram(CurrentDiagramUi.Ui_CurrentDiagram):
    def __init__(self, parent=None):
        super(PT_CurrentDiagram, self).__init__(parent)

class PT_PowerCalibration(PowerCalibrationUi.Ui_PowerCalibrationUi):
    def __init__(self, parent=None):
        super(PT_PowerCalibration, self).__init__(parent)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setFont(QFont('微软雅黑 Semilight'))

    # win = PT_MainWindow()
    # win = PT_ControlModeSet()
    # win = PT_RemoteControlSet()
    # win = PT_CurrentDiagram()
    win = PT_PowerCalibration()
    win.show()
    sys.exit(app.exec_())


