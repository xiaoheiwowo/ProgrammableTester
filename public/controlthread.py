# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
阀门控制thread
"""
import time
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from .control import ElectricControl
from .datacache import HardwareData as hw
from .datacache import SoftwareData as sw
from .datacache import Flag_Of as flag


def debug_print(string=None):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        print("DEBUG: " + string)


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

    vol_cur_position = pyqtSignal(str, str, str, str)

    def __init__(self):
        super(ControlThread, self).__init__()
        print('Control Thread Run ...')

        # self.timer_update_win = QTimer(self)
        # self.timer_update_win.timeout.connect(self.read_position_signal)

        # 硬件控制
        self.elec = ElectricControl()

        # 初始化变量
        hw.extend_in = self.elec.read_digital()

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
            time.sleep(0.01)

            my_timer += 1
            # 定时器
            if my_timer == 50:
                flag.update_va_value = 1
                my_timer = 0

            # 控制方式锁定
            if flag.control_mode_lock:
                self.sample_current_once()
                # 显示检测位置及电压电流
                if flag.update_va_value:
                    self.read_position_signal()
                    flag.update_va_value = 0
            else:
                self.elec.init_relay_port()
            # 中断信号处理
            if flag.button_int:
                self.int_from_io()
                pass

            # BP5 停阀
            if flag.bp5_on:
                self.bp5_on()

            if flag.bp5_off:
                self.bp5_off()

            # 继电器自检程序
            if flag.relay_check:

                # 断开所有继电器
                self.elec.init_relay_port()
                self.elec.output_cut_x(0)
                self.elec.select_signal()

                for i in range(160):
                    # 继电器检测间隔时间
                    time.sleep(0.5)
                    # 检测继电器 i
                    self.relay_self_check(i)
                    if flag.relay_check == 0:
                        break
                flag.relay_check = 0
                self.elec.init_relay_port()
                self.elec.output_cut_x(1)
                pass

            # 采样校准
            # if flag.calibration_start:
            #     if open_cal:
            #         if not hw.calibration_page:
            #             for i in hw.calibration_relay_connect[hw.calibration_page]:
            #                 if i:
            #                     self.elec.connect_check_relay(i)
            #                     open_cal = 0
            #
            # else:
            #     open_cal = 1
            #     self.elec.select_power(0)
            #     self.elec.output_ac_power()
            #     self.elec.output_dc_power()
            #     self.elec.init_relay_port()

    # def time_control(self, switch):
    #     if switch and not self.timer_update_win.isActive():
    #         self.timer_update_win.start(1000)
    #         print(1)
    #     elif not switch and self.timer_update_win.isActive():
    #         self.timer_update_win.stop()
    #         print(2)
    #     else:
    #         print(3)
    #         pass

    def sample_current_once(self):
        """
        采样一次电流
        :return:
        """
        sw.current_value.pop(0)
        sw.current_value.append(self.read_current())
        pass

    def read_current(self):
        """

        :return:
        """
        if hw.control_mode['POWER'] == 1:
            return self.elec.read_i_dc() * 200
        elif hw.control_mode['POWER'] == 2:
            return self.elec.read_i_ac() * 200
        else:
            return 0
            pass

    def read_voltage(self):
        """

        :return:
        """
        # print(self.elec.read_u_dc())
        # print(self.elec.read_u_ac())
        if hw.control_mode['POWER'] == 1:
            return self.elec.read_u_dc() * 10
        elif hw.control_mode['POWER'] == 2:
            return self.elec.read_u_ac() * 100
        else:
            return 0
            pass

    def read_position_signal(self):
        """

        :return:
        """
        # hw.voltage_value_show = str(round(self.read_voltage(), 2))
        # hw.current_value_show = str(sw.current_value[-1])
        #
        # if self.elec.read_IO(self.elec.ON_SIGNAL):
        #     hw.open_signal = 'YES'
        # else:
        #     hw.open_signal = 'NO'
        # if self.elec.read_IO(self.elec.OFF_SIGNAL):
        #     hw.close_signal = 'YES'
        # else:
        #     hw.close_signal = 'NO'

        voltage_value_show = str(round(self.read_voltage(), 2))
        current_value_show = str(round(self.read_current(), 2))
        if self.elec.read_IO(self.elec.ON_SIGNAL):
            open_signal = 'YES'
        else:
            open_signal = 'NO'
        if self.elec.read_IO(self.elec.OFF_SIGNAL):
            close_signal = 'YES'
        else:
            close_signal = 'NO'
        self.vol_cur_position.emit(voltage_value_show, current_value_show, open_signal, close_signal)

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

    def adjust_voltage(self, vol_value):
        """
        直流电源： 输出0~36V
        交流电源： 输出0~300V
        :param vol_value:str 电压值
        :return:
        """
        if hw.control_mode['POWER'] == 1:
            self.elec.output_ac_power()
            self.elec.output_dc_power(float(vol_value) * 5 * hw.correct_dc / 36)
        elif hw.control_mode['POWER'] == 2:
            self.elec.output_dc_power()
            self.elec.output_ac_power(float(vol_value) * 5 * hw.correct_ac / 300)
        else:
            pass
        # 确定电压合格后接通电源
        time_a = time.time()
        while True:
            if time.time() - time_a > 3:
                break
            else:
                if self.voltage_ok():
                    self.connect_power()
                    break

    def cal_adjust_voltage(self, page, vol_value):
        """

        :param page:
        :param vol_value:
        :return:
        """
        print(page, vol_value)
        if page == 'aca' or 'acv':
            self.elec.output_dc_power()
            self.elec.output_ac_power(vol_value * 5 / 300)
        elif page == 'dcv' or 'dca':
            self.elec.output_ac_power()
            self.elec.output_dc_power(vol_value * 5 / 36)

        # 确定电压合格后接通电源
        self.cal_connect_power(page)

    def power_to_zero(self):
        """

        :return:
        """
        # 解锁后电源调为0
        self.elec.output_dc_power()
        self.elec.output_ac_power()

    def voltage_ok(self):
        """
        检测电压是否符合设定
        :return:
        """
        if hw.voltage:
            if abs(self.read_voltage() - hw.voltage) < 5:
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
            self.elec.select_power(hw.control_mode['POWER'])
        except:
            print('connect power error')
        pass

    def cal_connect_power(self, page):
        """

        :param page:
        :return:
        """
        try:
            if page == 'aca' or 'acv':
                self.elec.select_power(2)
            elif page == 'dcv' or 'dca':
                self.elec.select_power(1)
        except Exception:
            print('connect power error')

    def int_from_io(self):
        """
        中断
        :return:
        """
        extend_in_bak = hw.extend_in[:]
        hw.extend_in = self.elec.read_digital()
        # 检测输入口
        bt_num = None
        for i in [5, 6, 8, 10, 11, 12, 13, 14, 15]:
            if extend_in_bak[i] == 0 and hw.extend_in[i] == 1:
                debug_print('IO口电平变化: ' + str(i))
                bt_num = i
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

    # Control
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
                    self.elec.output_adjust_i(20)
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    self.elec.output_adjust_i(20)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    self.elec.output_adjust_v(5)
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    self.elec.output_adjust_v(5)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    self.elec.output_adjust_v(10)
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    self.elec.output_adjust_v(10)
            # 反作用
            elif hw.control_mode['EFFECT'] == 2:
                # 0~20mA
                if hw.control_mode['SIGNAL'] == 1:
                    self.elec.output_adjust_i()
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    self.elec.output_adjust_i(4)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    self.elec.output_adjust_v()
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    self.elec.output_adjust_v(1)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    self.elec.output_adjust_v()
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    self.elec.output_adjust_v(2)
                pass

        # 总线阀
        elif hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_on)
            print(self.elec.serial_receive())
            pass

        # BP5
        elif hw.control_mode['SPECIAL'] == 3:
            self.elec.init_relay_port()
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
                    self.elec.output_adjust_i(20)
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    self.elec.output_adjust_i(20)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    self.elec.output_adjust_v(5)
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    self.elec.output_adjust_v(5)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    self.elec.output_adjust_v(10)
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    self.elec.output_adjust_v(10)
            # 反作用
            elif hw.control_mode['EFFECT'] == 1:
                # 0~20mA
                if hw.control_mode['SIGNAL'] == 1:
                    self.elec.output_adjust_i()
                # 4~20mA
                elif hw.control_mode['SIGNAL'] == 2:
                    self.elec.output_adjust_i(4)
                # 0~5V
                elif hw.control_mode['SIGNAL'] == 3:
                    self.elec.output_adjust_v()
                # 1~5V
                elif hw.control_mode['SIGNAL'] == 4:
                    self.elec.output_adjust_v(1)
                # 0~10V
                elif hw.control_mode['SIGNAL'] == 5:
                    self.elec.output_adjust_v()
                # 2~10V
                elif hw.control_mode['SIGNAL'] == 6:
                    self.elec.output_adjust_v(2)
                pass

        # 总线阀
        elif hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_off)
            print(self.elec.serial_receive())
            pass

        # BP5
        elif hw.control_mode['SPECIAL'] == 3:
            self.elec.init_relay_port()
            for j in hw.control_mode['ON']:
                self.elec.connect_array_relay(j)
            flag.bp5_off = 1

        pass

    def stop_valve(self):
        """

        :return:
        """
        if hw.control_mode['SPECIAL'] == 2:
            self.elec.serial_send(sw.cmd_stop)
            print(self.elec.serial_receive())
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
            pass

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
            pass

    # 调节阀控制
    def adjust_control(self, value):
        """

        :param value:
        :return:
        """
        if hw.control_mode['SPECIAL'] == 1:
            for j in hw.control_mode['ON']:
                self.elec.connect_array_relay(j)

            if hw.control_mode['SIGNAL'] in [1, 2]:
                self.elec.output_adjust_i(value)
            if hw.control_mode['SIGNAL'] in [3, 4, 5, 6]:
                self.elec.output_adjust_v(value)

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
        self.elec.output_adjust_i()
        self.elec.output_adjust_i()

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

    def quit_calibration(self):
        """

        :return:
        """
        self.elec.select_power(0)
        self.elec.output_ac_power()
        self.elec.output_dc_power()
        self.elec.init_relay_port()

    def prepare_for_calibration(self, page):
        """

        :param page:
        :return:
        """
        for i in hw.calibration_relay_connect[page]:
            if i:
                self.elec.connect_check_relay(i)

    def cal_sample_once(self, page):
        """

        :param page:
        :return:
        """
        if page == 'aca':
            result = self.elec.read_i_ac()
            self.cal_sample_result_aca.emit(result)
        elif page == 'acv':
            result = self.elec.read_u_ac()
            self.cal_sample_result_acv.emit(result)
        elif page == 'dca':
            result = self.elec.read_i_dc()
            self.cal_sample_result_dca.emit(result)
        elif page == 'dcv':
            result = self.elec.read_u_dc()
            self.cal_sample_result_dcv.emit(result)
        else:
            debug_print('page error')
