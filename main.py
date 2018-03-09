# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
# import random
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
from public.datacache import HardwareData as hw
from public.control import Digital, Analog

import tcpsocket

import time


# import qdarkstyle


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

    # MY SIGNAL
    # open_valve = pyqtSignal()
    # close_valve = pyqtSignal()
    # stop_valve = pyqtSignal()
    # m3_valve = pyqtSignal()
    # m4_valve = pyqtSignal()

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

        # 启动tcp server线程
        self.tcp_thread = TcpThread()
        self.tcp_thread.start()

        # 启动控制线程
        self.control_thread = ControlThread()
        self.control_thread.start()

        self.BT_ValveOpen.clicked.connect(self.control_thread.digital.open_valve)
        self.BT_ValveClose.clicked.connect(self.control_thread.digital.close_valve)
        self.BT_ValveStop.clicked.connect(self.control_thread.digital.stop_valve)
        self.BT_M3.clicked.connect(self.control_thread.digital.m3_valve)
        self.BT_M4.clicked.connect(self.control_thread.digital.m4_valve)

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
        self.CB_SelectControl.clear()
        self.CB_SelectControl.addItem('None')
        lst = ['', 'DC', 'AC']
        for i in range(len(sw.control_mode)):
            self.CB_SelectControl.addItem(lst[sw.control_mode[i]['POWER']] + ' ' + sw.control_mode[i]['NAME'])

    def update_main_win(self):
        """

        :return:
        """
        print('update')
        self.load_control_mode()
        # self.delete_dialog()
        pass

    def delete_dialog(self):
        """

        :return:
        """
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
        print('TCP Thread Run ...')

    def run(self):
        """

        :return:
        """
        remote_control_server = TCPServer(('localhost', 21567), tcpsocket.TcpHandler)
        remote_control_server.serve_forever()


class ControlThread(QThread):
    """
    控制线程
    """

    def __init__(self):
        super(ControlThread, self).__init__()
        print('Control Thread Run ...')
        self.calibration_timer = QTimer(self)
        self.calibration_timer.timeout.connect(self.read_io)

        # # 硬件
        self.digital = Digital()
        self.analog = Analog()

        self.calibration_timer.start(1000)

    def run(self):
        """

        :return:
        """
        # hw.current_value.clear()
        sw.current_value = [0 for j in range(65535)]
        print('1')
        while True:
            self.read_hard()
            print(time.time())
            time.sleep(0.01)
            # if sw.begin_ad == 1:
            #     time.sleep(0.01)
            #     self.read_hard()
            # else:
            #     sw.current_value = [0 for j in range(65535)]
            #     pass

    def read_hard(self):
        """

        :return:
        """
        sw.current_value.pop(0)
        sw.current_value.append(self.read_current())
        hw.current_value_show = str(sw.current_value[-1])
        # time1 = time.time()
        # print('read ad ' + str(time1))
        pass

    def read_current(self):
        """

        :return:
        """
        if hw.voltage == 'DC':
            return self.analog.read_i_dc()
        elif hw.voltage == 'AC':
            return self.analog.read_i_ac()
        else:
            return self.analog.read_i_ac()
            pass

    def read_voltage(self):
        """

        :return:
        """
        if hw.voltage == 'DC':
            return self.analog.read_u_dc()
        elif hw.voltage == 'AC':
            return self.analog.read_u_ac()
        else:
            return self.analog.read_u_ac()
            pass

    def read_io(self):
        """

        :return:
        """
        self.digital.read_digital()
        hw.voltage_value_show = str(self.read_voltage())
        self.read_current()
        if self.digital.read_on_signal() == 1:
            hw.open_signal = 'YES'
        else:
            hw.open_signal = 'NO'
        if self.digital.read_off_signal() == 1:
            hw.close_signal = 'YES'
        else:
            hw.close_signal = 'NO'


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 设置字体 在树莓派上使用注释下行
    app.setFont(QFont('微软雅黑 Semilight', 9))

    win = PT_MainWin()
    # win = PT_ControlModeSet()
    # win = PT_RemoteControlSet()
    # win = PT_CurrentDiagram()
    # win = PT_PowerCalibration()
    # win = PT_RelaySelfCheck()
    # win = PT_PowerSet()

    # 全局黑色主题
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win.show()
    sys.exit(app.exec_())
