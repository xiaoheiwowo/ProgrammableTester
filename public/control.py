# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制
"""
from public.datacache import HardwareData as hw
from public.function import *
# from driver.gpio import *
from driver.i2c import *


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
        self.i2c = I2C_Driver()
        pass

    def read_int(self):
        pass

    @staticmethod
    def output_reset():
        """
        reset pca9548
        :return:
        """
        # reset_pca9548()
        debug_print('RESET PCA9548')
        pass

    def connect_relay(self, index):
        debug_print('CONNECT: ' + str(index) + '1')
        pass

    def disconnect_relay(self, index):
        debug_print('DISCONNECT: ' + str(index) + '0')
        pass

    def output_cutx(self, state):
        """

        :param state: True 通电
        :return:
        """

        if state:
            hw.extend_out[0] |= 1 << 4
        else:
            hw.extend_out[0] &= ~(1 << 4)

        debug_print('CUTX')
        pass

    def output_vt(self, state):
        """

        :param state:
        :return:
        """
        if state:
            hw.extend_out[0] |= 1 << 3
        else:
            hw.extend_out[0] &= ~(1 << 3)
        pass

    def output_at(self, state):
        """

        :param state:
        :return:
        """
        if state:
            hw.extend_out[0] |= 1 << 2
        else:
            hw.extend_out[0] &= ~(1 << 2)
        pass

    def output_acp(self, state):
        """

        :param state:
        :return:
        """
        if state:
            hw.extend_out[0] |= 1 << 0
        else:
            hw.extend_out[0] &= ~(1 << 0)
        pass

    def output_dcp(self, state):
        """

        :param state:
        :return:
        """
        if state:
            hw.extend_out[0] |= 1 << 1
        else:
            hw.extend_out[0] &= ~(1 << 1)
        pass

    def select_power(self, which):
        if which == 'DC':
            self.output_acp(False)
            self.output_dcp(True)
            debug_print('POWER: ' + 'DC')
            pass
        elif which == 'AC':
            self.output_dcp(False)
            self.output_acp(True)
            debug_print('POWER: ' + 'AC')
            pass
        else:
            debug_print('NO POWER')

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
        return hw.extend_in[5]
        pass

    def read_b3_close(self):
        return hw.extend_in[6]
        pass

    def read_btn_outcontrol(self):
        return hw.extend_in[15]
        pass

    def read_btn_stop(self):
        return hw.extend_in[14]
        pass

    def read_btn_close(self):
        return hw.extend_in[13]
        pass

    def read_btn_open(self):
        return hw.extend_in[12]
        pass

    def read_on_signal(self):
        return hw.extend_in[11]
        pass

    def read_off_signal(self):
        return hw.extend_in[10]
        pass

    def set_signal_com(self):
        pass

    def read_test(self):
        return hw.extend_in[8]
        pass

    def read_digital(self):
        """
        读io口,结果写入hw.extend_out,如[0, 0, 1, 1, ..., 1, 0] 用hw.extend_io[0]表示端口P0
        :return:
        """
        hw.extend_in.clear()

        # 读扩展io口
        read_io = self.i2c.read_extend_io()

        list_io1 = list()
        list_io2 = list()
        for i in range(8):
            list_io1.append(bin(read_io[0])[2:].rjust(8, '0')[i])
            list_io2.append(bin(read_io[1])[2:].rjust(8, '0')[i])

        list_io1.reverse()
        list_io2.reverse()
        hw.extend_in = list_io1 + list_io2
        pass

    @staticmethod
    def num_to_array(num):
        """
        程序中用0~159作为继电器阵列中的继电器序号，此函数将单个序号转入hw.delay_array。
        :param num:
        :return:
        """

        # 行
        row = int(str(num)[-1])
        # 列
        column = int(str(num)[:-2])

        if column <= 7:
            hw.delay_array[row][0] |= 1 << 7 - column
        else:
            hw.delay_array[row][1] |= 1 << 14 - column

    @staticmethod
    def array_to_register():
        """
        此函数将hw.delay_array转为hw.register_port。
        :return:
        """
        tem = hw.delay_array[:]
        for i in [0, 2, 4, 6, 8]:
            tem[i][1], tem[i + 1][0] = tem[i + 1][0], tem[i][1]
        hw.register_port = tem[:]
        pass


if __name__ == '__main__':
    test = Digital()
    pass
