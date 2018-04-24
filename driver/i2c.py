# !/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
introduction
"""
import time
import os

try:
    import smbus2 as i2c2
except ImportError:
    pass
try:
    import smbus as i2c2
except ImportError:
    pass

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
try:
    from public.datacache import Flag_Of as flag
except:
    pass


# class flag(object):
#     button_int = 0


# wiringpi 的中断注册函数使用有问题 改用RPI.GPIO
# 中断引脚
int_pin = 36

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
config_port0 = 0b11100000
config_port1 = 0b11111101

input_port = [5, 6, 7, 8, 10, 11, 12, 13, 14, 15]
output_port = [0, 1, 2, 3, 4, 9]

config_all_output = 0x00


def debug_print(string):
    """
    debug
    :param string:
    :return:
    """
    # print('DEBUG [ ' + string + ' ]')
    pass


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
        # 中断注册
        # self.init_gpio_int()

    def __i2c_write_byte_data(self, i2c_addr, register, value):
        """

        :param i2c_addr:
        :param register:
        :param value:
        :return:
        """
        try:
            self.i2c_bus.write_byte_data(i2c_addr, register, value)
        except OSError:
            debug_print('Remote I/O error')

    def __i2c_read_byte_data(self, i2c_addr, register):
        """

        :param i2c_addr:
        :param register:
        :return:
        """
        try:
            return self.i2c_bus.read_byte_data(i2c_addr, register)
        except OSError:
            debug_print('Remote I/O error')
            return 0

    def __read_pca9548(self):
        """

        :return:
        """
        try:
            _data = self.i2c_bus.read_byte(addr_pca9548)
            return _data
        except IOError:
            pass

    def __write_pca9548(self, dat):
        """

        :param dat:
        :return:
        """
        try:
            self.i2c_bus.write_byte(addr_pca9548, dat)
        except IOError:
            pass

    def reset_pca9548(self):
        """
        reset后不接通i2c通道
        :return:
        """
        self.__i2c_write_byte_data(addr_pca9548, 0x00, 0x00)

    def select_i2c_channel(self, channel=0):
        """
        选择i2c通道。0为扩展io口， 1和2为继电器阵列以及自检继电器控制io口
        :param channel:
        :return:
        """
        if channel == 0:
            self.__write_pca9548(0b00000001)
        elif channel == 1:
            self.__write_pca9548(0b00000010)
        elif channel == 2:
            self.__write_pca9548(0b00000100)
        else:
            debug_print('Channel' + str(channel) + ' Not Found')

    def cfg_extend_io(self):
        """
        初始化扩展IO口，将io口配置为输入或者输出
        :return:
        """

        self.select_i2c_channel()
        self.__i2c_write_byte_data(addr_pca9535, cmd_config_p0, config_port0)
        self.__i2c_write_byte_data(addr_pca9535, cmd_config_p1, config_port1)

    def read_extend_input(self):
        """
        read extend io input
        :return: a list [port0, port1]
        """
        self.select_i2c_channel()
        data = list()
        data.append(self.__i2c_read_byte_data(addr_pca9535, cmd_input_p0))
        data.append(self.__i2c_read_byte_data(addr_pca9535, cmd_input_p1))
        return data

    def read_extend_output(self):
        """
        read extend io output port
        :return: return a list:[port0, port1]
        """
        self.select_i2c_channel()
        data = list()
        data.append(self.__i2c_read_byte_data(addr_pca9535, cmd_output_p0))
        data.append(self.__i2c_read_byte_data(addr_pca9535, cmd_output_p1))
        return data

    def write_extend_output(self, data):
        """
        set extend io output port
        :param data:list [0x00, 0x00]
        :return:
        """
        self.select_i2c_channel()
        self.__i2c_write_byte_data(addr_pca9535, cmd_output_p0, data[0])
        self.__i2c_write_byte_data(addr_pca9535, cmd_output_p1, data[1])

    def change_port_state(self, port_num, port_state):
        """
        change one port state
        :param port_num:io口序号，0~15
        :param port_state:1高电平，0低电平
        :return:
        """

        if port_num in output_port:
            port = self.read_extend_output()
            if port_state == 1:
                if port_num < 8:
                    port[0] |= 1 << port_num
                else:
                    port[1] |= 1 << port_num - 8

            elif port_state == 0:
                if port_num < 8:
                    port[0] &= ~(1 << port_num)
                else:
                    port[1] &= ~(1 << port_num - 8)
            else:
                pass
            self.write_extend_output(port)
        else:
            debug_print('This port can not output.')
            pass

    def init_relay_port(self):
        """
        初始化继电器阵列
        PCA9535输出高电平时继电器线圈通电
        :return:
        """
        try:
            self.select_i2c_channel(1)
            for i in range(5):
                self.__i2c_write_byte_data(0x21 + i, cmd_config_p0, config_all_output)
                self.__i2c_write_byte_data(0x21 + i, cmd_config_p1, config_all_output)
                self.__i2c_write_byte_data(0x21 + i, cmd_output_p0, 0x00)
                self.__i2c_write_byte_data(0x21 + i, cmd_output_p1, 0x00)
            self.select_i2c_channel(2)
            for i in range(7):
                self.__i2c_write_byte_data(0x21 + i, cmd_config_p0, config_all_output)
                self.__i2c_write_byte_data(0x21 + i, cmd_config_p1, config_all_output)
                self.__i2c_write_byte_data(0x21 + i, cmd_output_p0, 0x00)
                self.__i2c_write_byte_data(0x21 + i, cmd_output_p1, 0x00)
            pass
            time.sleep(0.05)
        except:
            debug_print('Init Delay Error!')

    def read_relay_state(self):
        """

        :return:
        """
        all_chip_port = list()
        for j in range(10):
            self.select_i2c_channel(j % 2 + 1)
            one_chip_port = list()
            one_chip_port.append(self.__i2c_read_byte_data(0x21 + j // 2, cmd_output_p0))
            one_chip_port.append(self.__i2c_read_byte_data(0x21 + j // 2, cmd_output_p1))
            all_chip_port.append(one_chip_port)
        return all_chip_port

    def connect_array_relay(self, relay_number):
        """
        连接一个继电器
        程序中用0~159作为继电器阵列中的继电器序号
        :param relay_number: int 序号
        :return:
        """
        if 0 <= relay_number < 160:
            # 行
            row = relay_number % 10

            # 列
            column = relay_number // 10

            # 芯片地址
            address = row // 2 + 0x21

            # 芯片端口
            port = row % 2

            # 输出寄存器
            register = port + 2

            # i2c通道
            if column <= 7:
                i2c_channel = 1
                offset = column
            else:
                i2c_channel = 2
                offset = column - 8

            self.select_i2c_channel(i2c_channel)
            output = self.__i2c_read_byte_data(address, register)

            debug_print('Read: ' + str(output))

            output |= 1 << offset
            self.__i2c_write_byte_data(address, register, output)

            debug_print('Write: ' + str(output))
            debug_print('Delay ' + str(relay_number) + ' Connected!\n')
        else:
            debug_print('Delay Number Error!\n')

    def disconnect_array_relay(self, relay_number):
        """
        断开一个继电器
        程序中用0~159作为继电器阵列中的继电器序号
        :param relay_number: int 序号
        :return:
        """
        if 0 <= relay_number < 160:
            # 行
            row = relay_number % 10

            # 列
            column = relay_number // 10

            # 芯片地址
            address = row // 2 + 0x21

            # 芯片端口
            port = row % 2

            # 芯片寄存器
            register = port + 2

            # i2c通道
            if column <= 7:
                i2c_channel = 1
                offset = column
            else:
                i2c_channel = 2
                offset = column - 8

            self.select_i2c_channel(i2c_channel)
            output = self.__i2c_read_byte_data(address, register)

            debug_print('Read: ' + str(output))

            output &= ~(1 << offset)
            self.__i2c_write_byte_data(address, register, output)

            debug_print('Write: ' + str(output))
            debug_print('Delay ' + str(relay_number) + ' Disconnected!\n')
        else:
            debug_print('Delay Number Error!\n')

    def __check_relay_connect(self, relay_number):
        """
        connect a check relay
                relay     number
                ST1 ----  0
                ST2 ----  1
                ...
                ST16 ---  15

                SP1 ----  16
                SP2 ----  17
                ...
                SP10 ---  25
        :param relay_number:int 0~25
        :return:
        """
        if 0 <= relay_number < 26:
            self.select_i2c_channel(2)
            if relay_number < 8:
                address = 0x26
                output = self.__i2c_read_byte_data(address, cmd_output_p1)
                output |= 1 << 7 - relay_number
                self.__i2c_write_byte_data(address, cmd_output_p1, output)

            elif 8 <= relay_number < 16:
                address = 0x26
                output = self.__i2c_read_byte_data(address, cmd_output_p0)
                output |= 1 << 15 - relay_number
                self.__i2c_write_byte_data(address, cmd_output_p0, output)

            elif 16 <= relay_number < 24:
                address = 0x27
                output = self.__i2c_read_byte_data(address, cmd_output_p0)
                output |= 1 << relay_number - 16
                self.__i2c_write_byte_data(address, cmd_output_p0, output)

            elif 24 <= relay_number < 26:
                address = 0x27
                output = self.__i2c_read_byte_data(address, cmd_output_p1)
                output |= 1 << relay_number - 24
                self.__i2c_write_byte_data(address, cmd_output_p1, output)
            else:
                pass
        else:
            debug_print('Delay Number Error!\n')
            pass

    def __check_relay_disconnect(self, relay_number):
        """
        dis connect a check relay
        :param relay_number:
        :return:
        """
        if 0 <= relay_number < 26:
            self.select_i2c_channel(2)
            if relay_number < 8:
                address = 0x26
                output = self.__i2c_read_byte_data(address, cmd_output_p1)
                output &= ~(1 << 7 - relay_number)
                self.__i2c_write_byte_data(address, cmd_output_p1, output)

            elif 8 <= relay_number < 16:
                address = 0x26
                output = self.__i2c_read_byte_data(address, cmd_output_p0)
                output &= ~(1 << 15 - relay_number)
                self.__i2c_write_byte_data(address, cmd_output_p0, output)

            elif 16 <= relay_number < 24:
                address = 0x27
                output = self.__i2c_read_byte_data(address, cmd_output_p0)
                output &= ~(1 << relay_number - 16)
                self.__i2c_write_byte_data(address, cmd_output_p0, output)

            elif 24 <= relay_number < 26:
                address = 0x27
                output = self.__i2c_read_byte_data(address, cmd_output_p1)
                output &= ~(1 << relay_number - 24)
                self.__i2c_write_byte_data(address, cmd_output_p1, output)
            else:
                pass
        else:
            debug_print('Delay Number Error!\n')
            pass
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

        self.__check_relay_connect(column)
        self.__check_relay_connect(row + 16)

    def disconnect_check_relay(self, index):
        """
        断开2个自检继电器
        :param index:1~159
        :return:
        """
        debug_print('TEST: ' + str(index) + '0')

        # 行
        row = index % 10
        # 列
        column = index // 10

        self.__check_relay_disconnect(column)
        self.__check_relay_disconnect(row + 15)

    def close_i2c(self):
        """

        :return:
        """
        self.i2c_bus.close()

    def init_gpio_int(self):
        """

        :return:
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int_pin, GPIO.IN)
        # 中断注册
        GPIO.add_event_detect(int_pin, GPIO.FALLING, callback=self.int_from_pca9535, bouncetime=20)

    @staticmethod
    def int_from_pca9535(pin_number):
        """

        :param pin_number:
        :return:
        """
        debug_print(str(pin_number) + 'Int from pca9535-1.')
        flag.button_int = 1

    def test_connect(self, num):
        self.__check_relay_connect(num)

    def test_disconnect(self, num):
        self.__check_relay_disconnect(num)

if __name__ == "__main__":
    i2c = I2C_Driver()
    i2c.cfg_extend_io()
    i2c.init_relay_port()

    # 中断
    # init_gpio_int()

    try:
        i2c.write_extend_output([0xff, 0xff])
        while True:
            print('1 EXTEND IO TEST')
            print('2 RELAY ARRAY TEST')
            print('3 READ IO TEST')
            print('4 INT TEST')
            print('5 CHECK RELAY TEST')
            choice = input('Please Choose...\n')
            if choice == '1':
                while True:
                    try:
                        print('You choose EXTEND IO TEST.\n')
                        try:
                            num = int(input('choose port 0 ~ 15:\n'))
                            state = int(input('0 or 1?\n'))
                            print('set port ' + str(num) + ' as ' + str(state))
                            i2c.change_port_state(num, state)
                            print(i2c.read_extend_output())

                        except ValueError:
                            print('Input Error!\n')
                    except KeyboardInterrupt:
                        os.system('clear')
                        break
            elif choice == '2':
                while True:
                    try:
                        print('You choose RELAY ARRAY TEST.\n')
                        control = input('1:connect, 2:disconnect\n')
                        number = input('delay number: \n')
                        if control == '1':
                            i2c.connect_array_relay(int(number))
                        elif control == '2':
                            i2c.disconnect_array_relay(int(number))
                        else:
                            print('Input Error!\n')
                        pass
                    except KeyboardInterrupt:
                        os.system('clear')
                        break

            elif choice == '3':
                while True:
                    try:
                        print('You choose READ IO TEST.\n')
                        a = input('Press Enter to read io.')
                        print(i2c.read_extend_input())
                    except KeyboardInterrupt:
                        os.system('clear')
                        break

            elif choice == '4':
                print('You choose INT TEST.\n')
                while True:
                    try:
                        i2c.read_extend_input()
                        # i2c.i2c_bus.read_byte_data(addr_pca9535, cmd_input_p1)
                        if flag.button_int == 1:
                            print('read port:')
                            print(i2c.read_extend_input())
                            flag.button_int = 0
                        else:
                            pass
                    except KeyboardInterrupt:
                        # os.system('clear')
                        break
            elif choice == '5':
                print('You choose CHECK RELAY TEST.\n')
                while True:
                    try:
                        control = input('1:connect, 2:disconnect\n')
                        number = input('delay number: \n')
                        if control == '1':
                            i2c.test_connect(int(number))
                        elif control == '2':
                            i2c.test_disconnect(int(number))
                        else:
                            print('Input Error!\n')
                            pass
                    except KeyboardInterrupt:
                        os.system('clear')
                        break
            else:
                pass

    except KeyboardInterrupt:
        i2c.write_extend_output([0x00, 0x00])
        i2c.close_i2c()
        os.system('clear')
        debug_print('[i2c close]')
