# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
import sys
import pickle
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

from public.datacache import SoftwareData as sw

import tcpsocket
# import qdarkstyle


class PT_MainWindow(QMainWindow, mainwindowui.Ui_MainWindow):
    """
    introduction
    useless
    """
    def __init__(self, parent=None):
        super(PT_MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.control_set = PT_ControlModeSet()
        self.remote_control = PT_RemoteControlSet()
        self.current_diagram = PT_CurrentDiagram()
        self.power_calibration = PT_PowerCalibration()
        self.relay_check = PT_RelaySelfCheck()
        self.power_set = PT_PowerSet()

        # SIGNAL
        self.Action_ControlSet.triggered.connect(self.show_control_set_form)
        self.Action_RemoteControl.triggered.connect(self.show_remote_control_form)
        self.Action_Others.triggered.connect(self.show_power_set_form)
        self.Action_PowerCalibration.triggered.connect(self.show_power_calibration_form)
        self.Action_RelayCheck.triggered.connect(self.show_relay_check_form)

        self.BT_FullScreen.clicked.connect(self.show_current_diagram_form)

    def show_control_set_form(self):
        """

        :return:
        """
        self.control_set.show()

    def show_remote_control_form(self):
        """

        :return:
        """
        self.remote_control.show()

    def show_current_diagram_form(self):
        """

        :return:
        """

        self.current_diagram.show()

    def show_power_calibration_form(self):
        """

        :return:
        """

        self.power_calibration.show()

    def show_relay_check_form(self):
        """

        :return:
        """

        self.relay_check.show()

    def show_power_set_form(self):
        """

        :return:
        """

        self.power_set.show()


class PT_ControlModeSet(controlmodesetui.Ui_ControlModeSet):
    """
    introduction
    """

    def __init__(self, parent=None):
        super(PT_ControlModeSet, self).__init__(parent)


class PT_RemoteControlSet(remotecontrolsetui.Ui_RemoteControlSet):
    """
    introduction
    """
    def __init__(self, parent=None):
        super(PT_RemoteControlSet, self).__init__(parent)


class PT_CurrentDiagram(currentdiagramui.Ui_CurrentDiagram):
    """
    introduction
    """
    def __init__(self, parent=None):
        super(PT_CurrentDiagram, self).__init__(parent)


class PT_PowerCalibration(powercalibrationui.Ui_PowerCalibration):
    """
    introduction
    """
    def __init__(self, parent=None):
        super(PT_PowerCalibration, self).__init__(parent)


class PT_RelaySelfCheck(relaycheckui.Ui_RelaySelfCheck):
    """
    introduction
    """
    def __init__(self, parent=None):
        super(PT_RelaySelfCheck, self).__init__(parent)


class PT_PowerSet(powersetui.Ui_PowerSet):
    """
    introduction
    """
    def __init__(self, parent=None):
        super(PT_PowerSet, self).__init__(parent)


class PT_MainWin(mainwindowui.Ui_MainWin):
    """
    introduction
    """
    def __init__(self, parent=None):
        super(PT_MainWin, self).__init__(parent)

        self.load_control_mode()

        self.current_diagram = PT_CurrentDiagram()
        self.control_set = PT_ControlModeSet()
        self.power_set = PT_PowerSet()
        self.remote_control = PT_RemoteControlSet()
        self.power_calibration = PT_PowerCalibration()
        self.relay_check = PT_RelaySelfCheck()
        # SIGNAL
        self.Action_ControlSet.triggered.connect(self.show_control_set_form)
        self.Action_RemoteControl.triggered.connect(self.show_remote_control_form)
        self.Action_Others.triggered.connect(self.show_power_set_form)
        self.Action_PowerCalibration.triggered.connect(self.show_power_calibration_form)
        self.Action_RelayCheck.triggered.connect(self.show_relay_check_form)

        self.BT_FullScreen.clicked.connect(self.show_current_diagram_form)
        self.control_set.confirm.connect(self.update_main_win)

    def show_control_set_form(self):
        """

        :return:
        """
        self.control_set.show()

    def show_remote_control_form(self):
        """

        :return:
        """
        self.remote_control.show()

    def show_current_diagram_form(self):
        """

        :return:
        """
        self.current_diagram.show()

    def show_power_calibration_form(self):
        """

        :return:
        """
        self.power_calibration.show()

    def show_relay_check_form(self):
        """

        :return:
        """
        self.relay_check.show()

    def show_power_set_form(self):
        """

        :return:
        """
        self.power_set.show()

    def load_control_mode(self):
        """

        :return:
        """
        print('load control mode')
        with open('pkl/controlmode.pkl', 'rb') as f:
            sw.control_mode = pickle.loads(f.read())

        lst = []
        for i in range(len(sw.control_mode)):
            lst.append(sw.control_mode[i]['NAME'])
        self.CB_SelectControl.clear()
        self.CB_SelectControl.addItem('None')
        lst2 = list(set(lst))
        for i in range(len(lst2)):
            self.CB_SelectControl.addItem(lst2[i])

    def update_main_win(self):
        """

        :return:
        """
        print('update')
        self.load_control_mode()
        # self.delete_dialog()
        pass

    def delete_dialog(self):
        try:
            self.current_diagram.deleteLater()
        except:
            pass



class TcpThread(QThread):
    """
    TCP线程，在此线程内接收请求并处理
    """
    def __init__(self):
        super(TcpThread, self).__init__()
        print('new thread init')

    def run(self):
        """

        :return:
        """
        remote_control_server = TCPServer(('localhost', 21567), tcpsocket.TcpHandler)
        remote_control_server.serve_forever()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置字体 在树莓派上使用注释下行
    app.setFont(QFont('微软雅黑 Semilight', 9))
    # 启动server线程
    # thread = TcpThread()
    # thread.start()

    # win = PT_MainWindow()
    # win = PT_ControlModeSet()
    # win = PT_RemoteControlSet()
    # win = PT_CurrentDiagram()
    # win = PT_PowerCalibration()
    # win = PT_RelaySelfCheck()
    # win = PT_PowerSet()
    win = PT_MainWin()
    # 全局黑色主题
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win.show()
    sys.exit(app.exec_())
