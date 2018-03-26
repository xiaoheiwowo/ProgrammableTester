# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制thread
"""
import time
from PyQt5.QtCore import QThread, pyqtSignal

from .control import Digital, Analog
from .datacache import HardwareData as hw
from .datacache import SoftwareData as sw
from .datacache import Flag_Of as flag

from driver.i2c import init_gpio_int


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
                self.digital.output_cut_x(0)
                self.digital.select_signal(None)

                for i in range(160):
                    # 继电器检测间隔时间
                    time.sleep(0.5)
                    # 检测继电器 i
                    self.relay_self_check(i)
                    if flag.relay_check == 0:
                        self.digital.i2c.init_relay()
                        self.digital.output_cut_x(1)
                        break

                flag.relay_check = 0
                self.digital.output_cut_x(1)
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
        if hw.voltage:
            if abs(self.read_voltage() - hw.voltage) < 2:
                return 1
            else:
                return 0
        else:
            return 0

    def connect_power(self):
        """
        接通电源
        :return:
        """
        try:
            self.digital.select_power(hw.control_mode['POWER'])
        except:
            print('connect power error')
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

    def adjust_input(self, _input):
        self.analog.output_20ma(_input)
        pass