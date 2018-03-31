# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制
"""

# import sys
# sys.path.append("..")
# from public.datacache import HardwareData as hw
from driver.i2c import *
from driver.spi import *
from driver.rs485 import PiSerial
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


class ElectricControl(I2C_Driver, PiSerial):
    """
    control
    """

    # 常量
    HIGH = 1
    LOW = 0

    PORT_ACP = 0
    PORT_DCP = 1
    PORT_AT = 2
    PORT_VT = 3
    PORT_CUTX = 4

    B3_OPEN = 5
    B3_CLOSE = 6
    BT_OUT_CONTROL = 15
    BT_STOP = 14
    BT_CLOSE = 13
    ON_SIGNAL = 11
    OFF_SIGNAL = 10
    RELAY_TEST = 8

    def __init__(self):
        super(ElectricControl, self).__init__()

        # spi analog
        self.spi = SPI_Driver()
        self.spi.ads1256_cfg()

        # i2c digital
        self.cfg_extend_io()
        self.write_extend_output([0x00, 0x00])
        self.init_relay_port()

        # rs485.py
        # self.rs485 = PiSerial()
        self.serial_init()
        pass

    # Analog Output (5)
    def output_ac_power(self, vol=0):
        """

        :param vol: 电压值0~5v
        :return:
        """
        debug_print('调节直流电源 输出：' + str(vol) + 'V')
        if 0 <= vol <= 5:
            vol_2 = int(vol * 1023 / 5)
            high_bit = self.spi.DAC_A | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.spi.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_dc_power(self, vol=0):
        """

        :param vol:0~5v
        :return:
        """
        debug_print('调节直流电源 输出：' + str(vol) + 'V')
        if 0 <= vol <= 5:
            vol_2 = int(vol * 1023 / 5)
            high_bit = self.spi.DAC_B | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.spi.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_adjust_i(self, vol_i=0):
        """

        :param vol_i:0~20ma
        :return:
        """
        debug_print('调节阀控制信号 输出：' + str(vol_i) + 'mA')
        if 0 <= vol_i <= 20:
            vol_2 = int(vol_i * 1023 / 20)
            high_bit = self.spi.DAC_C | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.spi.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_adjust_v(self, vol=0):
        """

        :param vol:0~10v
        :return:
        """
        debug_print('调节阀控制信号 输出：' + str(vol) + 'V')
        if 0 <= vol <= 10:
            vol_2 = int(vol * 1023 / 10)
            high_bit = self.spi.DAC_D | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.spi.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_0(self):
        """
        all channel output 0
        :return:
        """

        self.output_ac_power()
        self.output_dc_power()
        self.output_adjust_i()
        self.output_adjust_v()

    # Analog Input (5)
    def read_i_dc(self):
        """

        :return:
        """
        debug_print('电流值：' + '100' + 'mA')
        self.spi.ads1256_one_shot(3)
        return self.spi.ReadADC()
        pass

    def read_u_dc(self):
        """

        :return:
        """
        debug_print('电压值：' + '5' + 'V')
        self.spi.ads1256_one_shot(4)
        return self.spi.ReadADC()
        pass

    def read_i_ac(self):
        """

        :return:
        """
        debug_print('电流值：' + '1' + 'mA')
        self.spi.ads1256_one_shot(1)
        return self.spi.ReadADC()
        pass

    def read_u_ac(self):
        """

        :return:
        """
        debug_print('电压值：' + '220' + 'V')
        self.spi.ads1256_one_shot(2)
        return self.spi.ReadADC()
        pass

    def read_feedback(self):
        """

        :return:
        """
        debug_print('反馈信号：' + '1' + 'mA')
        self.spi.ads1256_one_shot(0)
        # 电压信号
        vol = self.spi.ReadADC()
        # 转换为0~20mA
        cur = vol * 4
        return cur
        pass

    # IO
    def output_cut_x(self, relay_state):
        """

        :param relay_state: True 通电
        :return:
        """

        if relay_state:
            self.change_port_state(self.PORT_CUTX, self.HIGH)
        else:
            self.change_port_state(self.PORT_CUTX, self.LOW)

        debug_print('CUTX: ' + str(relay_state))
        pass

    def select_power(self, which):
        """

        :param which:int 1 DC, 2 AC, 0 NONE
        :return:
        """
        self.change_port_state(self.PORT_ACP, self.LOW)
        self.change_port_state(self.PORT_DCP, self.LOW)
        wp.delay(300)
        if which == 1:
            self.change_port_state(self.PORT_DCP, self.HIGH)
            debug_print('POWER: ' + 'DC')
            pass
        elif which == 2:
            self.change_port_state(self.PORT_ACP, self.HIGH)
            debug_print('POWER: ' + 'AC')
            pass
        else:
            debug_print('NO this power')

    def select_signal(self, which=0):
        """

        :param which:
        :return:
        """
        list_which = ['None', '20mA', '10V']
        self.change_port_state(self.PORT_AT, self.LOW)
        self.change_port_state(self.PORT_VT, self.LOW)
        wp.delay(300)
        if list_which[which] == '20mA':
            debug_print('SIGNAL: ' + '20mA')
            self.change_port_state(self.PORT_AT, self.HIGH)
            pass
        elif list_which[which] == '10V':
            debug_print('SIGNAL: ' + '10V')
            self.change_port_state(self.PORT_VT, self.HIGH)
            pass
        else:
            debug_print('NO SIGNAL')
        pass

    def read_digital(self):
        """
        读io口,
        :return:result, 如[0, 0, 1, 1, ..., 1, 0] 用hw.extend_io[0]表示端口P0
        """
        # hw.extend_in.clear()

        # 读扩展io口
        read_io = self.read_extend_input()

        list_io1 = list()
        list_io2 = list()
        for j in range(8):
            list_io1.append(int(bin(read_io[0])[2:].rjust(8, '0')[j]))
            list_io2.append(int(bin(read_io[1])[2:].rjust(8, '0')[j]))

        list_io1.reverse()
        list_io2.reverse()
        result = list_io1 + list_io2
        # for i in hw.extend_in:
        #     hw.extend_in[i] = int(hw.extend_in[i])
        return result
        pass

    def read_IO(self, _name):
        """

        :param _name:
        :return:
        """
        read = self.read_digital()
        return read[_name]

    @staticmethod
    def sampling_for_average(_data):
        """
        采样10次去掉1个最大值1个最小值求平均值
        :param _data:
        :return:
        """
        ad_list = _data
        ad_max = max(ad_list)
        ad_min = min(ad_list)

        ad_list.pop(ad_list.index(ad_max))
        ad_list.pop(ad_list.index(ad_min))

        ad_average = sum(ad_list) / len(ad_list)
        return ad_average


if __name__ == '__main__':
    control = ElectricControl()
    current = [0 for i in range(65535)]

    while True:
        try:
            current.pop(0)
            control.spi.ads1256_cfg()
            current.append(control.read_i_ac())
            print(current[-10:])
            time.sleep(1)
        except KeyboardInterrupt:
            break

    pass
