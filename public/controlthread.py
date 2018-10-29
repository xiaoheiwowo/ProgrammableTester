# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制thread

未完成：
    BP5 断电刹车
    使用校准表
"""
import time
import random
import os
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from .control import ElectricControl
# from driver.spi import *
from .raspiad import *
from .datacache import HardwareData as hw
from .datacache import SoftwareData as sw
from .datacache import Flag_Of as flag
# from public.addaprocess import AD_DA_2


def debug_print(string=None):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        # print("DEBUG: " + string)


class ControlThread(QThread):
    """
    控制线程
    """

    # 继电器自检信号
    relay_check_signal = pyqtSignal(int, int, int)
    # 总线命令收到信号
    bus_cmd_get = pyqtSignal(str)
    # 实体按钮信号
    bt_on_clicked = pyqtSignal()
    bt_off_clicked = pyqtSignal()
    bt_stop_clicked = pyqtSignal()
    # 阀门bp5信号
    # is_bp5 = pyqtSignal(int)

    # 校准采样结果
    cal_sample_result_aca = pyqtSignal(float)
    cal_sample_result_acv = pyqtSignal(float)
    cal_sample_result_dca = pyqtSignal(float)
    cal_sample_result_dcv = pyqtSignal(float)

    # 更新界面电流电压值及到位信号
    valve_vol_cur = pyqtSignal(str, str)
    valve_pos_signal = pyqtSignal(str, str)

    # 调节阀反馈信号
    adjust_feedback = pyqtSignal(float)

    def __init__(self):
        super(ControlThread, self).__init__()

        # 硬件控制
        self.elec = ElectricControl()

        # ADDA
        self.raspi = RaspiAD()
        self.raspi.spi.hard_reset()
        self.raspi.send_sample_data.connect(self.rcv_ad_data)
        # self.start_pi_ad()
        time.sleep(1)
        self.raspi.start()

        # 调节电压定时
        self.wait_for_vol = VoltageOk()
        self.wait_for_vol.voltage_ok_signal.connect(self.connect_power)

        # 初始化变量
        hw.extend_in = self.elec.read_digital()
        print('Control Thread Run ...')
        # 中断注册
        try:
            self.elec.init_gpio_int()
            pass
        except:
            print('中断注册失败！')

    def run(self):
        """

        :return:
        """

        # my_timer = QTimer()
        # my_timer.timeout.connect(self.read_position_signal)
        # my_timer.start(1000)
        my_timer = 0
        self.elec.output_cut_x(1)
        while True:
            time.sleep(0.1)

            my_timer += 1
            # 定时器
            if my_timer == 10:
                flag.update_va_value = 1
                my_timer = 0

            # 控制方式锁定
            if flag.control_mode_lock:
                # 显示检测位置
                if flag.update_va_value:
                    self.read_position_signal()
                    flag.update_va_value = 0
            else:
                self.elec.init_relay_port()
            # 中断信号处理
            if flag.button_int:
                self.int_from_io()
                pass

            # 继电器自检程序
            if flag.relay_check:

                # 断开所有继电器
                self.elec.init_relay_port()
                self.elec.output_cut_x(0)
                self.elec.select_signal()

                for j in range(160):
                    # 继电器检测间隔时间
                    time.sleep(0.5)
                    # 检测继电器 i
                    self.relay_self_check(j)
                    if flag.relay_check == 0:
                        break
                flag.relay_check = 0
                self.elec.init_relay_port()
                self.elec.output_cut_x(1)
                pass

    @staticmethod
    def sample_current_once():
        """
        采样一次电流
        :return:
        """
        print(time.time())
        sw.current_value.pop(0)
        # self.ad_da.spi_driver.ads1256_one_shot(3)
        # result = round(self.ad_da.spi_driver.ReadADC(), 3)
        # self.ad_da.current_ad_channel = 3
        result = round(random.random() * 100, 2)
        sw.current_value.append(result)
        pass

    def read_position_signal(self):
        """

        :return:
        """
        if self.elec.read_IO(self.elec.ON_SIGNAL):
            open_signal = 'YES'
        else:
            open_signal = 'NO'
        if self.elec.read_IO(self.elec.OFF_SIGNAL):
            close_signal = 'YES'
        else:
            close_signal = 'NO'
        # self.valve_vol_cur.emit(current_value_show, voltage_value_show)
        self.valve_pos_signal.emit(open_signal, close_signal)

    def adjust_voltage(self, vol_value):
        """
        直流电源： 输出0~36V
        交流电源： 输出0~300V
        :param vol_value:str 电压值
        :return:
        """
        if hw.control_mode['POWER'] == 1:
            self.write_da_channel(1, 0)
            self.write_da_channel(0, float(vol_value * 5 / 36))
        elif hw.control_mode['POWER'] == 2:
            self.write_da_channel(0, 0)
            self.write_da_channel(1, float(vol_value * 5 / 300))

        # 确定电压合格后接通电源
        self.wait_for_vol.start()
        # time_a = time.time()
        # while True:
        #     if time.time() - time_a > 8:
        #         print('超时')
        #         break
        #     else:
        #         if self.voltage_ok():
        #             self.connect_power()
        #             break

    def power_to_zero(self):
        """

        :return:
        """
        # 解锁后电源调为0
        self.write_da_channel(0, 0)
        self.write_da_channel(1, 0)

    def connect_power(self):
        """
        接通电源
        :return:
        """
        try:
            self.elec.select_power(hw.control_mode['POWER'])
        except:
            print('connect power error')
        pass

    def relay_self_check(self, index):
        """
        继电器自检
        :param index: 继电器序号
        :return:
        """
        self.elec.connect_check_relay(index)

        # 继电器响应延时
        time.sleep(0.1)
        if self.elec.read_IO(self.elec.RELAY_TEST) == 0:
            off_ok = 1
        else:
            off_ok = 0

        self.elec.connect_array_relay(index)

        time.sleep(0.1)
        if self.elec.read_IO(self.elec.RELAY_TEST) == 1:
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
        self.elec.disconnect_array_relay(index)
        self.elec.disconnect_check_relay(index)
        pass

    # IO中断
    def int_from_io(self):
        """
        中断
        :return:
        """
        extend_in_bak = hw.extend_in[:]
        hw.extend_in = self.elec.read_digital()
        # 检测输入口
        bt_num = None
        for j in [5, 6, 8, 10, 11, 12, 13, 14, 15]:
            if extend_in_bak[j] == 0 and hw.extend_in[j] == 1:
                debug_print('IO口电平变化: ' + str(j))
                bt_num = j
                break
        else:
            # print('null')
            pass

        self.button_clicked(bt_num)
        flag.button_int = 0

    def button_clicked(self, bt_num):
        """

        :param bt_num:
        :return:
        """
        if flag.control_mode_lock:
            if bt_num == self.elec.BT_OPEN:
                self.open_valve()
                self.bt_on_clicked.emit()
            elif bt_num == self.elec.BT_CLOSE:
                self.close_valve()
                self.bt_off_clicked.emit()
            elif bt_num == self.elec.BT_STOP:
                self.stop_valve()
                self.bt_stop_clicked.emit()
            elif bt_num == self.elec.BT_OUT_CONTROL:
                print('外控')

            elif bt_num == self.elec.ON_SIGNAL:
                self.valve_pos_signal.emit('YES', 'NO')
                if hw.control_mode['SPECIAL'] == 3:
                    if flag.bp5_on == 1:
                        self.stop_valve()
                        flag.bp5_on = 0
                    pass
            elif bt_num == self.elec.OFF_SIGNAL:
                self.valve_pos_signal.emit('NO', 'YES')
                if hw.control_mode['SPECIAL'] == 3:
                    if flag.bp5_off == 1:
                        self.stop_valve()
                        flag.bp5_off = 0
            else:
                pass

    def bp5_on(self):
        """

        :return:
        """
        if self.elec.read_IO(self.elec.ON_SIGNAL):
            self.stop_valve()

            flag.bp5_on = 0

    def bp5_off(self):
        """

        :return:
        """
        if self.elec.read_IO(self.elec.OFF_SIGNAL):
            self.stop_valve()

            flag.bp5_off = 0

    # 基本控制
    def open_valve(self):
        """

        :return:
        """
        # 普通阀门
        if hw.control_mode['SPECIAL'] == 0:
            self.elec.init_relay_port()
            for j in hw.control_mode['ON']:
                self.elec.connect_array_relay(j)
            debug_print('open valve ' + str(hw.control_mode['ON']))

        # 调节阀
        elif hw.control_mode['SPECIAL'] == 1:
            self.elec.init_relay_port()
            for j in hw.control_mode['ON']:
                self.elec.connect_array_relay(j)
            # 正作用
            if hw.control_mode['EFFECT'] == 1:
                # 0~20mA
                if hw.control_mode['SIGNAL'] == 1:
                    self.write_da_channel(2, 20)
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    self.write_da_channel(2, 20)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    self.write_da_channel(3, 5)
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    self.write_da_channel(3, 5)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    self.write_da_channel(3, 10)
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    self.write_da_channel(3, 10)
            # 反作用
            elif hw.control_mode['EFFECT'] == 2:
                # 0~20mA
                if hw.control_mode['SIGNAL'] == 1:
                    self.write_da_channel(2, 0)
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    self.write_da_channel(2, 4)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    self.write_da_channel(3, 0)
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    self.write_da_channel(3, 1)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    self.write_da_channel(3, 0)
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    self.write_da_channel(3, 2)
                pass

        # 总线阀
        elif hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_on)
            print(self.elec.serial_receive())
            pass

        # BP5
        elif hw.control_mode['SPECIAL'] == 3:
            if not self.elec.read_IO(self.elec.ON_SIGNAL):
                self.elec.init_relay_port()
                # time.sleep(0.2)
                for j in hw.control_mode['ON']:
                    self.elec.connect_array_relay(j)
                flag.bp5_on = 1
                pass
        pass

    def close_valve(self):
        """

        :return:
        """
        # 普通阀门
        if hw.control_mode['SPECIAL'] == 0:
            debug_print('close valve ' + str(hw.control_mode['OFF']))
            self.elec.init_relay_port()
            for j in hw.control_mode['OFF']:
                self.elec.connect_array_relay(j)
        # 调节阀
        elif hw.control_mode['SPECIAL'] == 1:
            for j in hw.control_mode['ON']:
                self.elec.connect_array_relay(j)
            # 正作用
            if hw.control_mode['EFFECT'] == 2:
                # 0~20mA
                if hw.control_mode['SIGNAL'] == 1:
                    self.write_da_channel(2, 20)
                    # self.elec.output_adjust_i(20)
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    # self.elec.output_adjust_i(20)
                    self.write_da_channel(2, 20)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    # self.elec.output_adjust_v(5)
                    self.write_da_channel(3, 5)
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    # self.elec.output_adjust_v(5)
                    self.write_da_channel(3, 5)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    # self.elec.output_adjust_v(10)
                    self.write_da_channel(3, 10)
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    # self.elec.output_adjust_v(10)
                    self.write_da_channel(3, 10)
            # 反作用
            elif hw.control_mode['EFFECT'] == 1:
                # 0~20mA
                if hw.control_mode['SIGNAL'] == 1:
                    # self.elec.output_adjust_i()
                    self.write_da_channel(2, 0)
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    # self.elec.output_adjust_i(4)
                    self.write_da_channel(2, 4)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    # self.elec.output_adjust_v()
                    self.write_da_channel(3, 0)
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    # self.elec.output_adjust_v(1)
                    self.write_da_channel(3, 1)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    # self.elec.output_adjust_v()
                    self.write_da_channel(3, 0)
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    # self.elec.output_adjust_v(2)
                    self.write_da_channel(3, 2)
                pass

        # 总线阀
        elif hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_off)
            print(self.elec.serial_receive())
            pass

        # BP5
        elif hw.control_mode['SPECIAL'] == 3:
            if not self.elec.read_IO(self.elec.OFF_SIGNAL):
                self.elec.init_relay_port()
                # time.sleep(0.2)
                for j in hw.control_mode['OFF']:
                    self.elec.connect_array_relay(j)
                flag.bp5_off = 1

        pass

    def stop_valve(self):
        """

        :return:
        """
        # BUS
        if hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_stop)
            debug_print(self.elec.serial_receive())

        # BP5
        elif hw.control_mode['SPECIAL'] == 3:
            self.elec.init_relay_port()
            # time.sleep(0.2)

            # for j in hw.control_mode['OFF']:
            #     self.elec.connect_check_relay(j)
        else:
            debug_print('stop valve ' + str(hw.control_mode['STOP']))
            self.elec.init_relay_port()
        pass

    def m3_valve(self):
        """

        :return:
        """
        if hw.control_mode['SPECIAL'] == 0:
            debug_print('m3 ' + str(hw.control_mode['M3']))
            group = hw.control_mode['M3']
            self.elec.init_relay_port()
            for j in group:
                self.elec.connect_array_relay(j)
        # 总线阀
        elif hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_m3)
            debug_print(self.elec.serial_receive())

    def m4_valve(self):
        """

        :return:
        """
        if hw.control_mode['SPECIAL'] == 0:
            debug_print('m4 ' + str(hw.control_mode['M4']))
            group = hw.control_mode['M4']
            self.elec.init_relay_port()
            for j in group:
                self.elec.connect_array_relay(j)
        elif hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_m4)
            debug_print(self.elec.serial_receive())

    # 调节阀控制
    def adjust_control(self, control_value):
        """

        :param control_value:
        :return:
        """
        if hw.control_mode['SPECIAL'] == 1:
            for j in hw.control_mode['ON']:
                self.elec.connect_array_relay(j)

            if hw.control_mode['SIGNAL'] in [1, 2]:
                # self.elec.output_adjust_i(control_value)
                self.write_da_channel(2, control_value)
            if hw.control_mode['SIGNAL'] in [3, 4, 5, 6]:
                # self.elec.output_adjust_v(control_value)
                self.write_da_channel(3, control_value)

    def adjust_signal_connect(self):
        """

        :return:
        """
        if hw.control_mode['SIGNAL'] in [1, 2]:
            self.elec.select_signal(1)
        if hw.control_mode['SIGNAL'] in [3, 4, 5, 6]:
            self.elec.select_signal(2)

    def adjust_signal_disconnect(self):
        """

        :return:
        """
        self.elec.select_signal()
        # self.elec.output_adjust_i()
        # self.elec.output_adjust_i()
        self.write_da_channel(2, 0)
        self.write_da_channel(3, 0)

    def read_adjust_feedback(self):
        """

        :return:
        """
        if hw.control_mode['SPECIAL'] == 1:
            self.adjust_feedback.emit(self.get_ad_data(0) * 4)
            pass

    # 总线阀控制
    def bus_connect(self):
        """

        :return:
        """
        for j in hw.control_mode['ON']:
            self.elec.connect_array_relay(j)

    def bus_disconnect(self):
        """

        :return:
        """
        self.elec.init_relay_port()

    def rs485_send_data(self, msg):
        """
        当发送按钮按下，发送一组命令并收到返回消息
        :param msg:str
        :return:
        """
        self.elec.serial_send(msg)
        time.sleep(0.5)
        self.bus_cmd_get.emit(self.elec.serial_receive())

    # 采样控制
    def cal_adjust_voltage(self, page, vol_value):
        """

        :param page:
        :param vol_value:
        :return:
        """
        # print(page, vol_value)
        if page in ['aca', 'acv']:
            self.write_da_channel(0, 0)
            self.write_da_channel(1, float(vol_value) * 5 / 300)
            # hw.da_value[0] = 0
            # hw.da_value[1] = float(vol_value) * 5 / 300
        elif page in ['dcv', 'dca']:
            self.write_da_channel(1, 0)
            self.write_da_channel(0, float(vol_value) * 5 / 36)
            # hw.da_value[1] = 0
            # hw.da_value[0] = float(vol_value) * 5 / 36

        # 确定电压合格后接通电源
        self.cal_connect_power(page)
        # time_a = time.time()
        # while True:
        #     if time.time() - time_a > 5:
        #         print('超时')
        #         break
        #     else:
        #         if self.voltage_ok():
        #             self.cal_connect_power(page)
        #             break

    def cal_connect_power(self, page):
        """

        :param page:
        :return:
        """
        try:
            if page in ['aca', 'acv']:
                self.elec.select_power(2)
            elif page in ['dcv', 'dca']:
                self.elec.select_power(1)
        except Exception:
            print('connect power error')

    def quit_calibration(self):
        """

        :return:
        """
        self.elec.select_power(0)
        self.elec.init_relay_port()
        self.write_da_channel(0, 0)
        self.write_da_channel(1, 0)

    def prepare_for_calibration(self, page):
        """

        :param page:
        :return:
        """
        for j in hw.calibration_relay_connect[page]:
            if j:
                self.elec.connect_check_relay(j)

    def cal_sample_once(self, page):
        """

        :param page:
        :return:
        """
        if page == 'aca':
            result = self.cal_get_ad_data(1)
            self.cal_sample_result_aca.emit(result)
        elif page == 'acv':
            result = self.cal_get_ad_data(2)
            self.cal_sample_result_acv.emit(result)
        elif page == 'dca':
            result = self.cal_get_ad_data(3)
            self.cal_sample_result_dca.emit(result)
        elif page == 'dcv':
            result = self.cal_get_ad_data(4)
            self.cal_sample_result_dcv.emit(result)
        else:
            debug_print('page error')

    @staticmethod
    def cal_get_ad_data(_ch):
        """

        :param _ch:
        :return:
        """
        return hw.ad_value[_ch]

    def get_ad_data(self, _ch):
        """

        :param _ch:
        :return:0~5
        """
        if _ch == 0:
            return round(hw.ad_value[_ch] * 5 / 0xfff, 1)
        elif _ch == 1:
            return self.calibrate_sample(hw.calibrate_list_aca, hw.ad_value[_ch]) * 200
        elif _ch == 2:
            return self.calibrate_sample(hw.calibrate_list_acv, hw.ad_value[_ch]) * 100
        elif _ch == 3:
            return self.calibrate_sample(hw.calibrate_list_dca, hw.ad_value[_ch]) * 200
        elif _ch == 4:
            return self.calibrate_sample(hw.calibrate_list_dcv, hw.ad_value[_ch]) * 10
        else:
            return 0

    # AD/DA
    def rcv_ad_data(self, _data):
        """
        接收处理采样数据
        :param _data:
        :return:
        """

        mm = _data.strip('[]').split(',')
        nn = list(map(int, mm))
        # print(nn)
        hw.ad_value = [i for i in nn[-5:]]
        # print(hw.ad_value)

        # 直流
        if hw.control_mode['POWER'] == 1:
            for i in range(len(mm)):
                if i % 8 == 6:
                    sw.current_value.pop(0)
                    sw.current_value.append(round(self.calibrate_sample(hw.calibrate_list_dca, int(mm[i])) * 200, 1))
            hw.voltage_value_show = str(round(self.get_ad_data(4), 1))
            hw.current_value_show = str(sw.current_value[-1])
        # 交流
        elif hw.control_mode['POWER'] == 2:
            for i in range(len(mm)):
                if i % 8 == 4:
                    sw.current_value.pop(0)
                    sw.current_value.append(round(float(mm[i]) / 0xfff * 1000, 1))
            # hw.voltage_value_show = str(round(float(mm[-3]) / 0xfff * 500, 1))
            hw.voltage_value_show = str(round(self.get_ad_data(2), 1))
            hw.current_value_show = str(sw.current_value[-1])
        # print(hw.voltage_value_show, hw.current_value_show)
        self.valve_vol_cur.emit(hw.current_value_show, hw.voltage_value_show)

    def write_da_channel(self, _ch, _value):
        """

        :param _ch:
        :param _value:
        :return:
        """
        # print(_ch, _value)

        if _ch == 0:
            self.raspi.da_out[0]['flag'] = 1
            self.raspi.da_out[0]['value'] = int(self.calibrate_power(hw.calibrate_list_dcp, _value) * 0x3ff / 5)
        elif _ch == 1:
            self.raspi.da_out[1]['flag'] = 1
            self.raspi.da_out[1]['value'] = int(self.calibrate_power(hw.calibrate_list_acp, _value) * 0x3ff / 5)
        elif _ch == 2:
            self.raspi.da_out[2]['flag'] = 1
            self.raspi.da_out[2]['value'] = int(self.calibrate_power(hw.calibrate_list_ti, _value) * 0x3ff / 20)
        elif _ch == 3:
            self.raspi.da_out[3]['flag'] = 1
            self.raspi.da_out[3]['value'] = int(self.calibrate_power(hw.calibrate_list_tv, _value) * 0x3ff / 10)
        pass

    @staticmethod
    def calibrate_power(cal_list, vol):
        """

        :param cal_list:
        :param vol:
        :return:
        """
        # print(vol)
        for j in range(len(cal_list)):
            if cal_list[j] > vol:
                y_1, y_2 = j - 1, j
                x_1, x_2 = cal_list[j - 1], cal_list[j]
                x = vol
                y = (y_2 - y_1) * (x - x_1) / (x_2 - x_1) + y_1
                # print(y)
                return y

    @staticmethod
    def calibrate_sample(cal_dic, value):
        if len(cal_dic['samp']) < 2:
            return round(value * 5 / 4095, 3)
        else:
            for i in range(len(cal_dic['samp'])):
                if cal_dic['samp'][i] > value:
                    y_1, y_2 = cal_dic['standard'][i-1], cal_dic['standard'][i]
                    x_1, x_2 = cal_dic['samp'][i-1], cal_dic['samp'][i]
                    x = value
                    y = (y_2 - y_1) * (x - x_1) / (x_2 - x_1) + y_1
                    return round(y, 3)


class VoltageOk(QThread):
    """
    按钮
    """
    voltage_ok_signal = pyqtSignal()

    def __init__(self):
        super(VoltageOk, self).__init__()

    def run(self):
        start = time.time()
        while True:
            time.sleep(0.5)
            if time.time() - start > 8:
                print('调节电压超时')
                break
            else:
                if self.voltage_ok():
                    self.voltage_ok_signal.emit()
                    break
        pass

    def voltage_ok(self):
        """
        检测电压是否符合设定
        :return:
        """
        if hw.voltage:
            print(hw.da_value, hw.voltage)
            if hw.control_mode['POWER'] == 1:
                if abs(self.read_voltage() - hw.voltage) < 2:
                    return 1
                else:
                    return 0
            if hw.control_mode['POWER'] == 2:
                if abs(self.read_voltage() - hw.voltage) < 8:
                    return 1
                else:
                    return 0
        else:
            return 0

    def read_voltage(self):
        """

        :return:
        """
        if hw.control_mode['POWER'] == 1:
            return self.calibrate_sample(hw.calibrate_list_dcv, hw.ad_value[4]) * 10
        elif hw.control_mode['POWER'] == 2:
            return self.calibrate_sample(hw.calibrate_list_acv, hw.ad_value[2]) * 100
        else:
            return 0
            pass

    @staticmethod
    def calibrate_sample(cal_dic, value):
        if len(cal_dic['samp']) < 2:
            return round(value * 5 / 4095, 3)
        else:
            for i in range(len(cal_dic['samp'])):
                if cal_dic['samp'][i] > value:
                    y_1, y_2 = cal_dic['standard'][i-1], cal_dic['standard'][i]
                    x_1, x_2 = cal_dic['samp'][i-1], cal_dic['samp'][i]
                    x = value
                    y = (y_2 - y_1) * (x - x_1) / (x_2 - x_1) + y_1
                    return round(y, 3)

