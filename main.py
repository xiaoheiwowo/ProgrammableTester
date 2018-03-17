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
import random

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
from driver.i2c import int_from_pca9535, init_gpio_int


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
        self.Power_Set.triggered.connect(self.show_power_set_form)
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
        self.BT_ValveOpen.clicked.connect(self.control_thread.digital.open_valve)
        self.BT_ValveClose.clicked.connect(self.control_thread.digital.close_valve)
        self.BT_ValveStop.clicked.connect(self.control_thread.digital.stop_valve)
        self.BT_M3.clicked.connect(self.control_thread.digital.m3_valve)
        self.BT_M4.clicked.connect(self.control_thread.digital.m4_valve)

        # 自检开始按钮
        self.control_thread.relay_check_signal.connect(self.relay_check.get_check_result)

        # 设置电压信号槽
        self.voltage_set.connect(self.control_thread.adjust_voltage)

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
        # print('update')
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

    # 继电器自检信号
    relay_check_signal = pyqtSignal(int, int, int)

    def __init__(self):
        super(ControlThread, self).__init__()
        print('Control Thread Run ...')

        # 硬件控制
        self.digital = Digital()
        self.analog = Analog()

    def run(self):
        """

        :return:
        """
        my_timer = 0
        self.digital.read_digital()
        # 中断注册
        try:
            init_gpio_int()
            pass
        except:
            print('中断注册失败！')
        while True:
            time.sleep(0.01)

            my_timer += 1
            # 定时器
            if my_timer == 100:
                flag.update_va_value = 1
                my_timer = 0

            # 控制方式锁定
            if flag.control_mode_lock:
                self.current_sample_once()

                # 显示检测位置及电压电流
                if flag.update_va_value:
                    self.read_position_signal()
                    flag.update_va_value = 0

            # 解锁后电源调为0
            else:
                self.analog.output_dcp()
                self.analog.output_acp()

            # 确定电压合格后接通电源
            if self.voltage_ok():
                self.connect_power()

            # 中断信号处理
            if flag.button_int:
                self.int_from_io()
                pass

            # 继电器自检程序
            if flag.relay_check:

                # 断开所有继电器
                self.digital.i2c.init_relay()

                for i in range(160):
                    time.sleep(0.5)
                    # 检测继电器 i
                    self.relay_self_check(i)
                    if flag.relay_check == 0:
                        self.digital.i2c.init_relay()
                        self.digital.output_cut_x(1)
                        break

                flag.relay_check = 0
                pass

    def current_sample_once(self):
        """
        更新一次电流测试数据
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
        if hw.control_mode['POWER'] == 1:
            return self.analog.read_i_dc() * 200
        elif hw.control_mode['POWER'] == 2:
            return self.analog.read_i_ac() * 200
        else:
            return 0
            pass

    def read_voltage(self):
        """

        :return:
        """
        if hw.control_mode['POWER'] == 1:
            return self.analog.read_u_dc() * 10
        elif hw.control_mode['POWER'] == 2:
            return self.analog.read_u_ac() * 100
        else:
            return 0
            pass

    def read_position_signal(self):
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

    def relay_self_check(self, index):
        """
        继电器自检
        :param index: 继电器序号
        :return:
        """
        self.digital.connect_check_relay(index)

        # 继电器响应延时
        time.sleep(0.1)
        self.digital.read_digital()
        # print(self.digital.read_digital())
        if self.digital.read_test() == 0:
            off_ok = 1
        else:
            off_ok = 0

        self.digital.connect_relay(index)

        time.sleep(0.1)
        self.digital.read_digital()
        # print(self.digital.read_digital())
        if self.digital.read_test() == 1:
            on_ok = 1
        else:
            on_ok = 0

        # 发送信号
        """
        index: 继电器序号
        on_ok: 接通继电器正常
        off_ok: 断开继电器正常
        """
        self.relay_check_signal.emit(index, on_ok, off_ok)

        # 断开继电器
        self.digital.disconnect_check_relay(index)
        self.digital.disconnect_relay(index)
        pass

    def adjust_voltage(self, vol_value):
        """
        直流电源： 输出0~36V
        交流电源： 输出0~300V
        :param vol_value:str 电压值
        :return:
        """
        if hw.control_mode['POWER'] == 1:
            self.analog.output_acp()
            self.analog.output_dcp(int(vol_value) * 5 * hw.correct_dc / 36)
        elif hw.control_mode['POWER'] == 2:
            self.analog.output_dcp()
            self.analog.output_acp(int(vol_value) * 5 * hw.correct_ac / 300)
        else:
            pass

    def voltage_ok(self):
        """
        检测电压是否符合设定
        :return:
        """
        if abs(self.read_voltage() - hw.voltage) < 2:
            return 1
        else:
            return 0

    def connect_power(self):
        """
        接通电源
        :return:
        """
        self.digital.select_power(hw.control_mode['POWER'])
        pass

    def int_from_io(self):
        """
        中断
        :return:
        """
        extend_in_bak = hw.extend_in[:]
        self.digital.read_digital()
        # 检测输入口
        for i in [5, 6, 7, 8, 10, 11, 12, 13, 14, 15]:
            if extend_in_bak[i] == 0 and hw.extend_in[i] == 1:
                print('IO口电平变化: ' + str(i))
                break
        flag.button_int = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 设置字体 在树莓派上使用注释下行
    # app.setFont(QFont('微软雅黑 Semilight', 9))

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
