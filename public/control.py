# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制
"""
from public.datacache import HardwareData as hw
from public.function import *


class ValveControl(object):
    """
    control
    """

    def __init__(self):
        pass

    @staticmethod
    def open_valve():
        """

        :return:
        """
        debug_print('open valve ' + str(hw.control_mode['ON']))
        pass

    @staticmethod
    def close_valve():
        debug_print('close valve ' + str(hw.control_mode['OFF']))

        pass

    @staticmethod
    def stop_valve():
        debug_print('stop valve ' + str(hw.control_mode['STOP']))

        pass

    @staticmethod
    def m3_valve():
        debug_print('m3 ' + str(hw.control_mode['M3']))

        pass

    @staticmethod
    def m4_valve():
        debug_print('m4 ' + str(hw.control_mode['M4']))

        pass

    @staticmethod
    def bus_control(cmd=''):
        debug_print('发送: ' + cmd)
        debug_print('接收：' + cmd * 2)
        pass

    @staticmethod
    def adjust_control(signal):
        debug_print('调节阀输入信号: ' + str(signal))
        pass


class Analog(object):
    """
    采样
    """

    def __init__(self):
        pass

    def output_dcp(self, u=0):
        debug_print('调节直流电源 输出：' + str(u) + 'V')
        pass

    def output_acp(self, u=0):
        debug_print('调节交流电源 输出：' + str(u) + 'V')
        pass

    def output_20ma(self, i=0):
        debug_print('调节阀控制信号 输出：' + str(i) + 'mA')
        pass

    def output_10v(self, u=0):
        debug_print('调节阀控制信号 输出：' + str(u) + 'V')
        pass

    def read_i_dc(self):
        debug_print('电流值：' + '100' + 'mA')
        pass

    def read_u_dc(self):
        debug_print('电压值：' + '5' + 'V')
        pass

    def read_i_ac(self):
        debug_print('电流值：' + '1' + 'mA')
        pass

    def read_u_ac(self):
        debug_print('电压值：' + '220' + 'V')
        pass

    def read_feedback(self):
        debug_print('反馈信号：' + '1' + 'mA')
        pass


class Digital(object):
    """
    IO
    """
    # 不能同时连接交流和直流电源
    # 不能同时连接电流和电压信号控制调节阀
    POWER_SELECT = ''
    ADJUST_SIGNAL = ''

    def __init__(self):
        pass

    def read_int(self):
        pass

    def output_reset(self):
        debug_print('RESET PCA9548')
        pass

    def connect_relay(self, index):
        debug_print('CONNECT: ' + str(index) + '1')
        pass

    def disconnect_relay(self, index):
        debug_print('DISCONNECT: ' + str(index) + '0')
        pass

    def output_cutx(self):
        debug_print('CUTX')
        pass

    def output_dap(self, use=0):
        pass

    def output_dcp(self, use=0):
        pass

    def select_power(self, which):
        if which == 'DC':
            debug_print('POWER: ' + 'DC')
            pass
        elif which == 'AC':
            debug_print('POWER: ' + 'AC')
            pass
        else:
            debug_print('NO POWER')

    def output_20ma(self):
        pass

    def output_10v(self):
        pass

    def select_signal(self, which):
        if which == '20mA':
            debug_print('SIGNAL: ' + '20mA')
            pass
        elif which == '10V':
            debug_print('SIGNAL: ' + '10V')
            pass
        else:
            debug_print('NO SIGNAL')
        pass

    def read_b3_open(self):
        pass

    def read_b3_close(self):
        pass

    def read_btn_outcontrol(self):
        pass

    def read_btn_stop(self):
        pass

    def read_btn_close(self):
        pass

    def read_btn_open(self):
        pass

    def read_on_signal(self):
        pass

    def read_off_signal(self):
        pass

    def set_signal_com(self):
        pass

    def read_test(self):
        pass

    def read_digital(self):
        """
        读io口
        :return:
        """
        pass
