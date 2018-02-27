# !/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
introduction
"""

from public.datacache import HardwareData as hw

# import smbus2 as i2c2
try:
    import smbus2 as i2c2
except ImportError:
    pass
try:
    import smbus as i2c2
except ImportError:
    pass

addr_pca9548 = 0x70
addr_pca9535 = 0x21

# command byte
cmd_input_p0 = 0x00
cmd_input_p1 = 0x01
cmd_output_p0 = 0x02
cmd_output_p1 = 0x03
cmd_inversion_p0 = 0x04
cmd_inversion_p1 = 0x05
cmd_config_p0 = 0x06
cmd_config_p1 = 0x07

# 1:input 0:output
config_port0 = 0b01100000
config_port1 = 0b11111101

config_all_output = 0x00


class PCF8574(object):
    """
    :keyword
    """

    def __init__(self):
        self.i2c_bus = i2c2.SMBus(1)
        self.addr = 0x24
        pass

    def read_chip(self):
        """

        :return:
        """
        data = self.i2c_bus.read_byte(self.addr)
        return data
        pass

    def write_chip(self, dat):
        """

        :param dat:
        :return:
        """
        self.i2c_bus.write_byte(self.addr, dat)
        pass


class I2C_Driver(object):
    """
    I2C驱动
    PCA9548：
        地址：0x70
        寄存器：0b00000000 每一位控制一路i2c通断

    """

    def __init__(self):
        self.i2c_bus = i2c2.SMBus(1)

    def read_pca9548(self):
        """

        :return:
        """
        data = self.i2c_bus.read_byte(addr_pca9548)
        return data

    def write_pca9548(self, dat):
        """

        :param dat:
        :return:
        """
        self.i2c_bus.write_byte(addr_pca9548, dat)

    def select_i2c_channel(self, channel=0):
        """
        选择i2c通道。0为扩展io口， 1和2为继电器阵列以及自检继电器控制io口
        :param channel:
        :return:
        """
        if channel == 0:
            self.write_pca9548(0b00000001)
        elif channel == 1:
            self.write_pca9548(0b00000010)
        elif channel == 2:
            self.write_pca9548(0b00000100)
        else:
            print('Channel' + str(channel) + ' Not Found')

    def init_extend_io(self):
        """
        初始化扩展IO口，将io口配置为输入或者输出
        :return:
        """

        self.select_i2c_channel()
        self.i2c_bus.write_byte_data(addr_pca9535, cmd_config_p0, config_port0)
        self.i2c_bus.write_byte_data(addr_pca9535, cmd_config_p1, config_port1)

    def read_extend_io(self):
        """

        :return:
        """
        self.select_i2c_channel()
        data = list()
        data.append(self.i2c_bus.read_byte_data(addr_pca9535, cmd_input_p0))
        data.append(self.i2c_bus.read_byte_data(addr_pca9535, cmd_input_p1))
        return data

    def write_extend_io(self, data):
        """

        :param data:
        :return:
        """
        self.select_i2c_channel()
        self.i2c_bus.write_byte_data(addr_pca9535, cmd_output_p0, data[0])
        self.i2c_bus.write_byte_data(addr_pca9535, cmd_output_p1, data[1])

    def init_delay(self):
        """
        初始化继电器阵列
        PCA9535输出高电平时继电器线圈通电
        :return:
        """
        self.select_i2c_channel(1)
        for i in range(5):
            self.i2c_bus.write_byte_data(0x21 + i, cmd_config_p0, config_all_output)
            self.i2c_bus.write_byte_data(0x21 + i, cmd_config_p1, config_all_output)
            self.i2c_bus.write_byte_data(0x21 + i, cmd_output_p0, 0x00)
            self.i2c_bus.write_byte_data(0x21 + i, cmd_output_p1, 0x00)
        self.select_i2c_channel(2)
        for i in range(7):
            self.i2c_bus.write_byte_data(0x21 + i, cmd_config_p0, config_all_output)
            self.i2c_bus.write_byte_data(0x21 + i, cmd_config_p1, config_all_output)
            self.i2c_bus.write_byte_data(0x21 + i, cmd_output_p0, 0x00)
            self.i2c_bus.write_byte_data(0x21 + i, cmd_output_p1, 0x00)
        pass

    def set_delay_array(self):
        """

        :return:
        """

        for i in range(10):
            self.select_i2c_channel(i % 2 + 1)
            self.i2c_bus.write_byte_data(0x21 + i // 2, cmd_output_p0, hw.register_port[i][0])
            self.i2c_bus.write_byte_data(0x21 + i // 2, cmd_output_p1, hw.register_port[i][1])

    def set_delay_test(self):
        """
        设置自检继电器
        :return:
        """

        self.select_i2c_channel(1)
        self.i2c_bus.write_byte_data(0x25, cmd_output_p0, hw.ZJ00[0])
        self.i2c_bus.write_byte_data(0x25, cmd_output_p1, hw.ZJ00[1])
        self.i2c_bus.write_byte_data(0x26, cmd_output_p0, hw.ZJ01[0])
        self.i2c_bus.write_byte_data(0x26, cmd_output_p1, hw.ZJ01[1])

        pass

    def read_delay_state(self):
        """

        :return:
        """
        all_chip_port = list()
        for i in range(10):
            self.select_i2c_channel(i % 2 + 1)
            one_chip_port = list()
            one_chip_port.append(self.i2c_bus.read_byte_data(0x21 + i // 2, cmd_output_p0))
            one_chip_port.append(self.i2c_bus.read_byte_data(0x21 + i // 2, cmd_output_p1))
            all_chip_port.append(one_chip_port)
        return all_chip_port

    def close_i2c(self):
        """

        :return:
        """
        self.i2c_bus.close()

    def read_port(self, num):
        """

        :param num:
        :return:
        """
        pass

    def write_port(self, num, state):
        """
        设置扩展io口输出。
        :param num:io口序号，0~15
        :param state:1高电平，0低电平
        :return:
        """
        port = self.read_extend_io()
        if state == 1:
            if num < 8:
                port[0] |= 1 << num
            else:
                port[1] |= 1 << num - 8

        elif state == 0:
            if num < 8:
                port[0] &= ~(1 << num)
            else:
                port[1] &= ~(1 << num - 8)
        else:
            pass

        self.write_extend_io(port)


class I2C_DRIVER(object):
    """
    introduction
    """

    @staticmethod
    def init_i2c():
        """

        :return:
        """
        pass

    @staticmethod
    def init_pca9535():
        """

        :return:
        """
        pass


if __name__ == "__main__":
    pcf8 = PCF8574()
    pcf8.read_chip()
    pcf8.write_chip(0x22)
    pcf8.read_chip()
