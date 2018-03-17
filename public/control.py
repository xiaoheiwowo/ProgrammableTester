# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制
"""

import sys

sys.path.append("..")
from public.datacache import HardwareData as hw
from driver.i2c import *
from driver.spi import *

try:
    import wiringpi as wp
except ImportError:
    # from driver import wiringpi as wp
    pass


def debug_print(string=None):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        # print("DEBUG: " + string)


# 常量
HIGH = 1
LOW = 0

PORT_ACP = 0
PORT_DCP = 1
PORT_AT = 2
PORT_VT = 3
PORT_CUTX = 4


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
        """

        :return:
        """
        debug_print('close valve ' + str(hw.control_mode['OFF']))

        pass

    @staticmethod
    def stop_valve():
        """

        :return:
        """
        debug_print('stop valve ' + str(hw.control_mode['STOP']))

        pass

    @staticmethod
    def m3_valve():
        """

        :return:
        """
        debug_print('m3 ' + str(hw.control_mode['M3']))

        pass

    @staticmethod
    def m4_valve():
        """

        :return:
        """
        debug_print('m4 ' + str(hw.control_mode['M4']))

        pass

    @staticmethod
    def bus_control(cmd=''):
        """

        :param cmd:
        :return:
        """
        debug_print('发送: ' + cmd)
        debug_print('接收：' + cmd * 2)
        pass

    @staticmethod
    def adjust_control(signal):
        """

        :param signal:
        :return:
        """
        debug_print('调节阀输入信号: ' + str(signal))
        pass


class Analog(object):
    """
    采样
    """

    def __init__(self):
        self.spi_ = SPI_Driver()
        self.spi_.spi_init()
        self.spi_.ads1256_cfg()

        pass

    def output_dcp(self, u=0):
        """

        :param u:
        :return:
        """
        debug_print('调节直流电源 输出：' + str(u) + 'V')
        self.spi_.output_dc_power(u)
        pass

    def output_acp(self, u=0):
        """

        :param u:
        :return:
        """
        debug_print('调节交流电源 输出：' + str(u) + 'V')
        self.spi_.output_ac_power(u)
        pass

    def output_20ma(self, i_=0):
        """

        :param i_:
        :return:
        """
        debug_print('调节阀控制信号 输出：' + str(i_) + 'mA')
        self.spi_.output_adjust_i(i_)
        pass

    def output_10v(self, u=0):
        """

        :param u:
        :return:
        """
        debug_print('调节阀控制信号 输出：' + str(u) + 'V')
        self.spi_.output_adjust_v(u)
        pass

    def sampling_for_average(self, index):
        """
        采样10次去掉1个最大值1个最小值求平均值
        :param index:
        :return:
        """
        ad_list = list()
        for i in range(10):
            ad_list.append(self.spi_.read_channel(index))

        ad_max = max(ad_list)
        ad_min = min(ad_list)

        ad_list.pop(ad_list.index(ad_max))
        ad_list.pop(ad_list.index(ad_min))

        ad_average = sum(ad_list) / len(ad_list)
        return ad_average

    def read_i_dc(self):
        """

        :return:
        """
        debug_print('电流值：' + '100' + 'mA')
        self.spi_.ads1256_one_shot(3)
        return self.spi_.ReadADC()
        pass

    def read_u_dc(self):
        """

        :return:
        """
        debug_print('电压值：' + '5' + 'V')
        self.spi_.ads1256_one_shot(4)
        return self.spi_.ReadADC()
        pass

    def read_i_ac(self):
        """

        :return:
        """
        debug_print('电流值：' + '1' + 'mA')
        self.spi_.ads1256_one_shot(1)
        return self.spi_.ReadADC()
        pass

    def read_u_ac(self):
        """

        :return:
        """
        debug_print('电压值：' + '220' + 'V')
        self.spi_.ads1256_one_shot(2)
        return self.spi_.ReadADC()
        pass

    def read_feedback(self):
        """

        :return:
        """
        debug_print('反馈信号：' + '1' + 'mA')
        self.spi_.ads1256_one_shot(0)
        # 电压信号
        vol = self.spi_.ReadADC()
        # 转换为0~20mA
        cur = vol * 4
        return cur
        pass

    @staticmethod
    def adjust_control(signal):
        """

        :param signal:
        :return:
        """
        debug_print('调节阀输入信号: ' + str(signal))
        pass


class Digital(object):
    """
    数字信号控制
    """

    # 不能同时连接交流和直流电源
    # 不能同时连接电流和电压信号控制调节阀

    def __init__(self):
        self.i2c = I2C_Driver()
        self.i2c.init_extend_io()
        self.i2c.init_relay()
        pass

    def read_int(self):
        """

        :return:
        """
        pass

    def output_reset(self):
        """
        reset pca9548
        :return:
        """
        # reset_pca9548()
        debug_print('RESET PCA9548')
        self.i2c.reset_pca9548()
        pass

    def connect_relay(self, index):
        """

        :param index:
        :return:
        """
        debug_print('CONNECT: ' + str(index) + '1')
        self.i2c.connect_array_relay(index)
        pass

    def disconnect_relay(self, index):
        """

        :param index:
        :return:
        """
        debug_print('DISCONNECT: ' + str(index) + '0')
        self.i2c.disconnect_array_relay(index)
        pass

    def connect_check_relay(self, index):
        """
        连接2个自检继电器
        :param index:
        :return:
        """
        debug_print('TEST: ' + str(index) + '1')
        # 行
        row = index % 10
        # 列
        column = index // 10

        self.i2c.connect_check_relay(column)
        self.i2c.connect_check_relay(row + 16)

    def disconnect_check_relay(self, index):
        """
        断开2个自检继电器
        :param index:1~159
        :return:
        """
        debug_print('TEST: ' + str(index) + '1')

        # 行
        row = index % 10
        # 列
        column = index // 10

        self.i2c.disconnect_check_relay(column)
        self.i2c.disconnect_check_relay(row + 15)

    def output_cut_x(self, relay_state):
        """

        :param relay_state: True 通电
        :return:
        """

        if relay_state:
            self.i2c.change_port_state(PORT_CUTX, HIGH)
        else:
            self.i2c.change_port_state(PORT_CUTX, LOW)

        debug_print('CUTX: ' + str(relay_state))
        pass

    def select_power(self, which):
        """

        :param which:int 1 DC, 2 AC, 0 NONE
        :return:
        """
        self.i2c.change_port_state(PORT_ACP, LOW)
        self.i2c.change_port_state(PORT_DCP, LOW)
        wp.delay(300)
        if which == 1:
            self.i2c.change_port_state(PORT_DCP, HIGH)
            debug_print('POWER: ' + 'DC')
            pass
        elif which == 2:
            self.i2c.change_port_state(PORT_ACP, HIGH)
            debug_print('POWER: ' + 'AC')
            pass
        else:
            debug_print('NO this power')

    def select_signal(self, which):
        """

        :param which:
        :return:
        """
        self.i2c.change_port_state(PORT_AT, LOW)
        self.i2c.change_port_state(PORT_VT, LOW)
        wp.delay(300)
        if which == '20mA':
            debug_print('SIGNAL: ' + '20mA')
            self.i2c.change_port_state(PORT_AT, HIGH)
            pass
        elif which == '10V':
            debug_print('SIGNAL: ' + '10V')
            self.i2c.change_port_state(PORT_VT, HIGH)
            pass
        else:
            debug_print('NO SIGNAL')
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
        for j in range(8):
            list_io1.append(int(bin(read_io[0])[2:].rjust(8, '0')[j]))
            list_io2.append(int(bin(read_io[1])[2:].rjust(8, '0')[j]))

        list_io1.reverse()
        list_io2.reverse()
        hw.extend_in = list_io1 + list_io2
        # for i in hw.extend_in:
        #     hw.extend_in[i] = int(hw.extend_in[i])
        return hw.extend_in
        pass

    @staticmethod
    def read_b3_open():
        """

        :return:
        """
        return hw.extend_in[5]
        pass

    @staticmethod
    def read_b3_close():
        """

        :return:
        """

        return hw.extend_in[6]
        pass

    @staticmethod
    def read_btn_outcontrol():
        """

        :return:
        """
        return hw.extend_in[15]
        pass

    @staticmethod
    def read_btn_stop():
        """

        :return:
        """
        return hw.extend_in[14]
        pass

    @staticmethod
    def read_btn_close():
        """

        :return:
        """
        return hw.extend_in[13]
        pass

    @staticmethod
    def read_btn_open():
        """

        :return:
        """
        return hw.extend_in[12]
        pass

    @staticmethod
    def read_on_signal():
        """

        :return:
        """
        return hw.extend_in[11]
        pass

    @staticmethod
    def read_off_signal():
        """

        :return:
        """
        return hw.extend_in[10]
        pass

    @staticmethod
    def set_signal_com():
        """

        :return:
        """
        pass

    @staticmethod
    def read_test():
        """

        :return:
        """
        return hw.extend_in[8]
        pass

    @staticmethod
    def num_to_array(relay_number):
        """
        程序中用0~159作为继电器阵列中的继电器序号，此函数将单个序号转入hw.delay_array。
        :param relay_number:
        :return:
        """

        # 行
        row = int(str(relay_number)[-1])
        # 列
        column = int(str(relay_number)[:-2])

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
        for j in [0, 2, 4, 6, 8]:
            tem[j][1], tem[j + 1][0] = tem[j + 1][0], tem[j][1]
        hw.register_port = tem[:]
        pass

    def open_valve(self):
        """

        :return:
        """
        debug_print('open valve ' + str(hw.control_mode['ON']))
        group = hw.control_mode['ON']
        self.i2c.init_relay()
        for j in group:
            self.connect_relay(j)
        pass

    def close_valve(self):
        """

        :return:
        """
        debug_print('close valve ' + str(hw.control_mode['OFF']))
        group = hw.control_mode['OFF']
        self.i2c.init_relay()
        for j in group:
            self.connect_relay(j)
        pass

    def stop_valve(self):
        """

        :return:
        """
        debug_print('stop valve ' + str(hw.control_mode['STOP']))
        group = hw.control_mode['STOP']
        self.i2c.init_relay()
        for j in group:
            self.connect_relay(j)
        pass

    def m3_valve(self):
        """

        :return:
        """
        debug_print('m3 ' + str(hw.control_mode['M3']))
        group = hw.control_mode['M3']
        self.i2c.init_relay()
        for j in group:
            self.connect_relay(j)
        pass

    def m4_valve(self):
        """

        :return:
        """
        debug_print('m4 ' + str(hw.control_mode['M4']))
        group = hw.control_mode['M4']
        self.i2c.init_relay()
        for j in group:
            self.connect_relay(j)
        pass


if __name__ == '__main__':
    digital = Digital()
    analog = Analog()
    current = [0 for i in range(65535)]

    while True:
        try:
            current.pop(0)
            analog.spi_.ads1256_cfg()
            current.append(analog.read_i_ac())
            print(current[-10:])
            time.sleep(1)
        except KeyboardInterrupt:
            break

    pass
