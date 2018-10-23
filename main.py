# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
# import random
import sys
import pickle
import time

from socketserver import TCPServer
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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
from public.controlthread import ControlThread

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

        self.control_set.BT_Advanced.clicked.connect(self.show_remote_control_form)

        # 启动tcp server线程
        # self.tcp_thread = TcpThread()
        # self.tcp_thread.start()

        try:
            # 启动控制线程
            self.control_thread = ControlThread()
            self.control_thread.start()

            # 开关停按钮
            self.BT_ValveOpen.clicked.connect(self.control_thread.open_valve)
            self.BT_ValveClose.clicked.connect(self.control_thread.close_valve)
            self.BT_ValveStop.clicked.connect(self.control_thread.stop_valve)
            self.BT_M3.clicked.connect(self.control_thread.m3_valve)
            self.BT_M4.clicked.connect(self.control_thread.m4_valve)

            # 自检开始按钮
            self.control_thread.relay_check_signal.connect(self.relay_check.get_check_result)
            # 设置电压信号槽
            self.voltage_set.connect(self.control_thread.adjust_voltage)
            # 调节阀控制信号
            self.SB_AdjustValveInput.valueChanged.connect(self.control_thread.adjust_control)
            # 调节阀反馈信号
            self.control_thread.adjust_feedback.connect(self.change_adjust_feedback)
            # 解锁后电源调为0
            self.unlock.connect(self.control_thread.power_to_zero)
            # 选择调节阀信号
            self.adjust_signal_select.connect(self.control_thread.adjust_signal_connect)
            # 调节阀信号断开
            self.adjust_signal_cut_off.connect(self.control_thread.adjust_signal_disconnect)
            # 总线阀连接
            self.bus_valve_select.connect(self.control_thread.bus_connect)
            # 总线阀断开
            self.bus_cut_off.connect(self.control_thread.bus_disconnect)
            # 总线命令发送
            self.send_clicked.connect(self.control_thread.rs485_send_data)
            # 总线命令接受
            self.control_thread.bus_cmd_get.connect(self.bus_return_show)

            # 准备添加校准数据
            self.power_calibration.tab_aca.add_cal_data.connect(self.control_thread.prepare_for_calibration)
            self.power_calibration.tab_acv.add_cal_data.connect(self.control_thread.prepare_for_calibration)
            self.power_calibration.tab_dca.add_cal_data.connect(self.control_thread.prepare_for_calibration)
            self.power_calibration.tab_dcv.add_cal_data.connect(self.control_thread.prepare_for_calibration)
            # 采样校准调节电压
            self.power_calibration.tab_aca.dia_new.cal_adjust_vol.connect(self.control_thread.cal_adjust_voltage)
            self.power_calibration.tab_acv.dia_new.cal_adjust_vol.connect(self.control_thread.cal_adjust_voltage)
            self.power_calibration.tab_dca.dia_new.cal_adjust_vol.connect(self.control_thread.cal_adjust_voltage)
            self.power_calibration.tab_dcv.dia_new.cal_adjust_vol.connect(self.control_thread.cal_adjust_voltage)
            # 采样一次
            self.power_calibration.tab_aca.dia_new.cal_sample.connect(self.control_thread.cal_sample_once)
            self.power_calibration.tab_acv.dia_new.cal_sample.connect(self.control_thread.cal_sample_once)
            self.power_calibration.tab_dca.dia_new.cal_sample.connect(self.control_thread.cal_sample_once)
            self.power_calibration.tab_dcv.dia_new.cal_sample.connect(self.control_thread.cal_sample_once)
            # 采样数据返回给界面
            self.control_thread.cal_sample_result_aca.connect(self.power_calibration.tab_aca.dia_new.get_sampling)
            self.control_thread.cal_sample_result_acv.connect(self.power_calibration.tab_acv.dia_new.get_sampling)
            self.control_thread.cal_sample_result_dca.connect(self.power_calibration.tab_dca.dia_new.get_sampling)
            self.control_thread.cal_sample_result_dcv.connect(self.power_calibration.tab_dcv.dia_new.get_sampling)
            # 添加一组校准数据完成
            self.power_calibration.tab_aca.dia_new.add_data_finish.connect(self.control_thread.quit_calibration)
            self.power_calibration.tab_acv.dia_new.add_data_finish.connect(self.control_thread.quit_calibration)
            self.power_calibration.tab_dca.dia_new.add_data_finish.connect(self.control_thread.quit_calibration)
            self.power_calibration.tab_dcv.dia_new.add_data_finish.connect(self.control_thread.quit_calibration)

            # 更新电流电压值，到位信号显示
            self.control_thread.valve_vol_cur.connect(self.change_va_value)
            self.control_thread.valve_pos_signal.connect(self.change_position_signal)

        except:
            print("It can't work in windows.")

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
        flag.calibration_start = 1
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

    def closeEvent(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        try:
            self.control_thread.elec.write_extend_output([0x00, 0x00])
            self.control_thread.elec.init_relay_port()
            # self.control_thread.elec.output_0()
            # self.control_thread.ad_da.close_process()
        except:
            pass

        self.close()


def data_init():
    """
    数据初始化
    :return:
    """
    # 电流值采样列表初始化为0
    sw.current_value = list()
    for j in range(sw.current_set['data_depth']):
        sw.current_value.append(0)


if __name__ == '__main__':
    data_init()
    app = QApplication(sys.argv)
    win = PT_MainWin()
    # win = Ui_ControlModeSet()
    # win = Ui_RemoteControlSet()
    # win = Ui_CurrentDiagram()
    # win = Ui_PowerCalibration()
    # win = Ui_RelaySelfCheck()
    # win = Ui_PowerSet()

    # 黑色主题
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # 设置字体 在树莓派上使用注释下行
    # app.setFont(QFont('微软雅黑 Semilight', 9))
    win.show()
    sys.exit(app.exec_())
