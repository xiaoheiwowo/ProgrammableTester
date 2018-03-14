# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
# import random
import os
import sys
import pickle
import time
import tcpsocket

from socketserver import TCPServer
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 控制方式窗口Ui类
from ui.controlmodesetui import Ui_ControlModeSet
# 电流曲线窗口Ui类
from ui.currentdiagramui import Ui_CurrentDiagram
# 电源及采样校准窗口Ui类
from ui.powercalibrationui import Ui_PowerCalibration
# 电源设置Ui类
from ui.powersetui import Ui_PowerSet
# 继电器阵列自检Ui类
from ui.relaycheckui import Ui_RelaySelfCheck
# 外控设置窗口Ui类
from ui.remotecontrolsetui import Ui_RemoteControlSet
# 主窗口Ui类
from ui import mainwindowui

from public.datacache import SoftwareData as sw
from public.datacache import HardwareData as hw
from public.datacache import Flag_Of as flag
from public.control import Digital, Analog

# import qdarkstyle


class PT_MainWin(mainwindowui.Ui_MainWin):
    """
    introduction
    """

    def __init__(self, parent=None):
        super(PT_MainWin, self).__init__(parent)

        self.load_control_mode()

        self.current_diagram = Ui_CurrentDiagram()
        self.control_set = Ui_ControlModeSet()
        self.power_set = Ui_PowerSet()
        self.remote_control = Ui_RemoteControlSet()
        self.power_calibration = Ui_PowerCalibration()
        self.relay_check = Ui_RelaySelfCheck()

        # SIGNAL 菜单
        self.Action_ControlSet.triggered.connect(self.show_control_set_form)
        self.Action_RemoteControl.triggered.connect(self.show_remote_control_form)
        self.Action_Others.triggered.connect(self.show_power_set_form)
        self.Action_PowerCalibration.triggered.connect(self.show_power_calibration_form)
        self.Action_RelayCheck.triggered.connect(self.show_relay_check_form)

        self.BT_FullScreen.clicked.connect(self.show_current_diagram_form)
        self.control_set.confirm.connect(self.update_main_win)



        # 启动tcp server线程
        # self.tcp_thread = TcpThread()
        # self.tcp_thread.start()

        # 电流值采样列表初始化为0
        sw.current_value = []
        for j in range(sw.current_set['data_depth']):
            sw.current_value.append(0)

        # 配置 hostname
        # try:
        #     os.systme('sudo hostname' + str(sw.net_set['host_name']))
        # except:pass

        # 启动控制线程, windows下运行需要注释下面部分
        self.control_thread = ControlThread()
        self.control_thread.start()
        # self.BT_ValveOpen.clicked.connect(self.control_thread.digital.open_valve)
        # self.BT_ValveClose.clicked.connect(self.control_thread.digital.close_valve)
        # self.BT_ValveStop.clicked.connect(self.control_thread.digital.stop_valve)
        # self.BT_M3.clicked.connect(self.control_thread.digital.m3_valve)
        # self.BT_M4.clicked.connect(self.control_thread.digital.m4_valve)

        # 自检开始按钮
        # self.relay_check.DB_DialogButton.BT_OK1.clicked.connect(self.control_thread.digital.check_)
        self.control_thread.relay_check_signal.connect(self.relay_check.get_value)

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
        # print('load control mode')
        with open('pkl/controlmode.pkl', 'rb') as f:
            sw.control_mode = pickle.loads(f.read())
        self.CB_SelectControl.clear()
        self.CB_SelectControl.addItem('None')
        lst = ['', 'DC', 'AC']
        for i in range(len(sw.control_mode)):
            self.CB_SelectControl.addItem(lst[sw.control_mode[i]['POWER']] + ' ' + sw.control_mode[i]['NAME'])

    def update_main_win(self):
        """
        退出控制方式设置窗口更新住界面下的控制方式列表
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

    def relay_self_check(self):
        """
        继电器阵列自检
        :return:
        """
        pass

    def relay_self_check_stop(self):
        """
        停止自检
        :return:
        """
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

    relay_check_signal = pyqtSignal(int, int, int)

    def __init__(self):
        super(ControlThread, self).__init__()
        print('Control Thread Run ...')

        self.calibration_timer = QTimer(self)
        self.calibration_timer.timeout.connect(self.read_io)

        # 硬件
        # self.digital = Digital()
        # self.analog = Analog()

        # self.calibration_timer.start(1000)

    def run(self):
        """

        :return:
        """
        while True:
            time.sleep(0.01)
            # self.read_hard()

            # 继电器自检程序
            if flag.relay_check:
                for i in range(160):
                    time.sleep(0.5)

                    # 检测继电器i
                    self.relay_check_signal.emit(1, 0, 1)
                    if flag.relay_check == 0:
                        break

                flag.relay_check = 0
                pass

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
    # win = Ui_ControlModeSet()
    # win = Ui_RemoteControlSet()
    # win = Ui_CurrentDiagram()
    # win = Ui_PowerCalibration()
    # win = Ui_RelaySelfCheck()
    # win = Ui_PowerSet()

    # 黑色主题
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    win.show()
    sys.exit(app.exec_())
