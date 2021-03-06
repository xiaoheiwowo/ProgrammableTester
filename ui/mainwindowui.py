# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主界面UI类，实现交互功能
"""

import random
import time
import re
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import diagram
from public.datacache import SoftwareData as sw
from public.datacache import HardwareData as hw
from public.control import ElectricControl as vc
from public.datacache import Flag_Of as flag
from public.crc16ibm import *

fg_update_diagram = 1


class Ui_MainWin(QtWidgets.QMainWindow):
    """
    主界面UI类，实现交互功能
    """
    # 设置电压
    voltage_set = QtCore.pyqtSignal(float)
    # 调节阀输入信号
    adjust_input = QtCore.pyqtSignal(float)
    # 调节阀信号类型选择
    adjust_signal_select = QtCore.pyqtSignal()
    # 调节阀信号断开
    adjust_signal_cut_off = QtCore.pyqtSignal()
    # 解锁控制方式
    unlock = QtCore.pyqtSignal()
    # 总线阀选择，连接线路
    bus_valve_select = QtCore.pyqtSignal()
    # 总线阀断开接线
    bus_cut_off = QtCore.pyqtSignal()
    # 总线阀发送按钮点击
    send_clicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Ui_MainWin, self).__init__(parent, flags=QtCore.Qt.Window)

        self.setObjectName("MainWindow")
        self.resize(1024, 550)
        # self.move(0,0)
        self.setMinimumSize(QtCore.QSize(800, 300))
        self.setWindowTitle('可编程测试仪')
        self.setWindowIcon(QtGui.QIcon(":/logo.png"))
        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        # 主窗口widget
        self.mainWidget = QtWidgets.QWidget(self, flags=QtCore.Qt.Widget)
        self.setCentralWidget(self.mainWidget)

        # 菜单栏
        self.MenuBar = QtWidgets.QMenuBar()
        self.fault_number = self.MenuBar.addMenu('故障代码：0')
        self.SetMenu = self.MenuBar.addMenu('设置')
        # self.fault_number.setDisabled(True)
        self.Action_ControlSet = QtWidgets.QAction('控制方式设置', self)
        self.Action_PowerCalibration = QtWidgets.QAction('电源及采样校准', self)
        self.Action_RemoteControl = QtWidgets.QAction('网络及其他设置', self)
        self.Power_Set = QtWidgets.QAction('电源设置', self)
        self.Action_RelayCheck = QtWidgets.QAction('继电器自检', self)

        self.quit_button = QtWidgets.QAction('退出', self)
        self.quit_button.triggered.connect(self.close)

        self.init_menubar()
        self.setMenuBar(self.MenuBar)

        # 基本信息部分
        self.GB_Information = QtWidgets.QGroupBox(self.mainWidget)
        self.lb_host_name = QtWidgets.QLabel()
        self.lb_server_name = QtWidgets.QLabel()
        self.lb_connection_state = QtWidgets.QLabel()
        self.init_information_box()

        # 电流曲线部分
        self.GB_CurrentCurve = QtWidgets.QGroupBox(self.mainWidget)
        self.lb_current_value = QtWidgets.QLabel("电流值：")
        self.lb_voltage_value = QtWidgets.QLabel("电压值：")
        self.lb_open_completely = QtWidgets.QLabel("开到位：")
        self.lb_close_completely = QtWidgets.QLabel("关到位：")
        self.main_window_fig = diagram.PlotWidget(self)
        self.BT_FullScreen = QtWidgets.QPushButton()
        self.BT_Dynamic = QtWidgets.QPushButton()
        self.BT_Static = QtWidgets.QPushButton()

        self.init_current_curve()

        self.update_thread = UpdateThread(self)
        self.update_thread.start()

        # 阀门控制部分
        self.GB_ValveControl = QtWidgets.QGroupBox(self.mainWidget)
        self.left_list = QtWidgets.QListWidget(self.GB_ValveControl)
        self.stack_1 = QtWidgets.QWidget(flags=QtCore.Qt.Widget)
        self.stack_2 = QtWidgets.QWidget(flags=QtCore.Qt.Widget)
        self.stack_3 = QtWidgets.QWidget(flags=QtCore.Qt.Widget)
        self.stack = QtWidgets.QStackedWidget(self.GB_ValveControl)
        self.BT_ValveOpen = QtWidgets.QPushButton()
        self.BT_ValveClose = QtWidgets.QPushButton()
        self.BT_ValveStop = QtWidgets.QPushButton()
        self.BT_M3 = QtWidgets.QPushButton()
        self.BT_M4 = QtWidgets.QPushButton()

        # # stack1
        self.Layout_Basic = QtWidgets.QGridLayout(self.stack_1)
        self.lb_control_mode = QtWidgets.QLabel()
        self.CB_SelectControl = QtWidgets.QComboBox()
        self.lb_power_choose = QtWidgets.QLabel()
        self.SB_Voltage = QtWidgets.QDoubleSpinBox()
        self.lb_unit_v = QtWidgets.QLabel()
        self.BT_Lock = QtWidgets.QPushButton()
        self.CK_Auto = QtWidgets.QCheckBox('自动')
        self.lb_open_valve = QtWidgets.QLabel()
        self.SB_OpenTime = QtWidgets.QSpinBox()
        self.lb_close_valve = QtWidgets.QLabel()
        self.SB_CloseTime = QtWidgets.QSpinBox()
        self.BT_Begin = QtWidgets.QPushButton()
        self.BT_Stop = QtWidgets.QPushButton()

        # # stack2
        self.Layout_AdjustPage = QtWidgets.QGridLayout(self.stack_2)
        self.lb_adjust_input = QtWidgets.QLabel()
        self.SB_AdjustValveInput = QtWidgets.QDoubleSpinBox()
        self.lb_unit_ma = QtWidgets.QLabel()
        self.lb_step_length = QtWidgets.QLabel()
        self.CB_StepValve = QtWidgets.QComboBox()
        self.lb_unit_ma2 = QtWidgets.QLabel()
        self.lb_adjust_output = QtWidgets.QLabel()
        self.slider_adjust_input = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        # # stack3
        self.Layout_BusPageStack = QtWidgets.QGridLayout(self.stack_3)
        self.lb_set_date_out = QtWidgets.QLabel(self.stack_3)
        self.DE_SetDate = QtWidgets.QDateEdit()
        self.BT_WriteIn = QtWidgets.QPushButton(self.stack_3)
        self.BT_ClearR = QtWidgets.QPushButton(self.stack_3)
        self.lb_send_area = QtWidgets.QLabel(self.stack_3)
        self.lb_receive_area = QtWidgets.QLabel(self.stack_3)
        self.LE_Send = QtWidgets.QLineEdit()
        self.LE_Received = QtWidgets.QLineEdit()
        self.BT_Send = QtWidgets.QPushButton(self.stack_3)
        self.auto_test_timer = QtCore.QTimer(self)

        self.init_valve_control()
        self.load_data()

        # 主窗口布局
        layout_main = QtWidgets.QGridLayout(self.mainWidget)
        layout_main.addWidget(self.GB_Information, 0, 0, 2, 2)
        layout_main.addWidget(self.GB_CurrentCurve, 0, 2, 2, 4)
        layout_main.addWidget(self.GB_ValveControl, 2, 0, 3, 6)

        # 全屏显示
        # self.showFullScreen()

    #  初始化菜单栏
    def init_menubar(self):
        """

        :return:
        """
        # 控制方式设置
        self.SetMenu.addAction(self.Action_ControlSet)
        # 电源及采样校准
        self.SetMenu.addAction(self.Action_PowerCalibration)
        # 外控及其他设置
        self.SetMenu.addAction(self.Action_RemoteControl)
        # 电源设置
        self.SetMenu.addAction(self.Power_Set)
        # 继电器自检
        self.SetMenu.addAction(self.Action_RelayCheck)

        self.SetMenu.addAction(self.quit_button)

    def fault_prompt(self, num='0'):
        """
        故障提示
        :param num:
        :return:
        """
        self.fault_number.setTitle('故障代码:' + num)

    def init_information_box(self):
        """

        :return:
        """
        self.GB_Information.setMinimumWidth(250)
        self.GB_Information.setTitle('仪器状态')
        self.lb_host_name.setText('本机名：Program Tester 1')
        self.lb_server_name.setText('上位机名：Valve Tester 1')
        self.lb_connection_state.setText('连接状态：已连接')

        Layout_Information = QtWidgets.QVBoxLayout(self.GB_Information)
        Layout_Information.addWidget(self.lb_host_name)
        Layout_Information.addWidget(self.lb_server_name)
        Layout_Information.addWidget(self.lb_connection_state)
        # Layout_Information.addWidget(Label_13)
        # Layout_Information.addWidget(Label_14)
        Layout_Information.addStretch(1)

    def init_current_curve(self):
        """
        current
        :return:
        """
        self.GB_CurrentCurve.setTitle('电流曲线')
        self.lb_close_completely.setFixedWidth(150)

        Wgt_LB = QtWidgets.QWidget()
        Wgt_LB.setMaximumWidth(140)
        Layout_LB = QtWidgets.QVBoxLayout(Wgt_LB)
        Layout_LB.addWidget(self.lb_current_value)
        Layout_LB.addWidget(self.lb_voltage_value)
        Layout_LB.addWidget(self.lb_open_completely)
        Layout_LB.addWidget(self.lb_close_completely)
        Layout_LB.addStretch(1)

        self.main_window_fig.setMaximumHeight(180)
        self.main_window_fig.update_diagram(sw.current_value[-200:], myflag=0)

        self.BT_FullScreen.setFixedSize(50, 50)
        self.BT_FullScreen.setStyleSheet('''QPushButton {background-image: url("./images/zoomout.png")}''')
        self.BT_Dynamic.setText('动态')
        self.BT_Dynamic.setFixedSize(50, 50)
        self.BT_Static.setText('静态')
        self.BT_Static.setFixedSize(50, 50)
        # BUTTON 布局
        Layout_button = QtWidgets.QVBoxLayout()
        Layout_button.addWidget(self.BT_FullScreen, alignment=QtCore.Qt.AlignRight)
        Layout_button.addWidget(self.BT_Dynamic)
        Layout_button.addWidget(self.BT_Static)

        layout_current_curve = QtWidgets.QHBoxLayout(self.GB_CurrentCurve)
        layout_current_curve.addWidget(Wgt_LB)
        layout_current_curve.addWidget(self.main_window_fig)
        layout_current_curve.addLayout(Layout_button)

    def init_valve_control(self):
        """
        阀门控制
        :return:
        """
        self.GB_ValveControl.setTitle('阀门控制')
        self.left_list.setMaximumWidth(100)
        self.left_list.insertItem(0, '通用')
        self.left_list.insertItem(1, '调节阀+')
        self.left_list.insertItem(2, '总线阀+')
        self.left_list.setFont(QtGui.QFont('微软雅黑 Semilight', 12))

        self.stack1Ui()
        self.stack2Ui()
        self.stack3Ui()

        self.stack.addWidget(self.stack_1)
        self.stack.addWidget(self.stack_2)
        self.stack.addWidget(self.stack_3)

        self.BT_ValveOpen.setText('开阀')
        self.BT_ValveOpen.setMinimumHeight(40)
        self.BT_ValveClose.setText('关阀')
        self.BT_ValveClose.setMinimumHeight(40)
        self.BT_ValveStop.setText('停阀')
        self.BT_ValveStop.setMinimumHeight(40)
        self.BT_M3.setText('位置3')
        self.BT_M3.setMinimumHeight(40)
        self.BT_M4.setText('位置4')
        self.BT_M4.setMinimumHeight(40)
        self.valve_control_disabled(True)

        Layout_ControlButton = QtWidgets.QVBoxLayout()
        Layout_ControlButton.addWidget(self.BT_ValveOpen, alignment=QtCore.Qt.AlignCenter)
        Layout_ControlButton.addWidget(self.BT_ValveClose, alignment=QtCore.Qt.AlignCenter)
        Layout_ControlButton.addWidget(self.BT_ValveStop, alignment=QtCore.Qt.AlignCenter)
        Layout_ControlButton.addWidget(self.BT_M3, alignment=QtCore.Qt.AlignCenter)
        Layout_ControlButton.addWidget(self.BT_M4, alignment=QtCore.Qt.AlignCenter)

        Layout_Stack = QtWidgets.QHBoxLayout(self.GB_ValveControl)
        Layout_Stack.addWidget(self.left_list)
        Layout_Stack.addWidget(self.stack)
        wgt_ = QtWidgets.QWidget(self)
        wgt_.setFixedWidth(20)
        Layout_Stack.addWidget(wgt_)
        Layout_Stack.addLayout(Layout_ControlButton)

        # 左侧选项卡信号
        self.left_list.currentRowChanged.connect(self.display)

        self.CB_SelectControl.currentIndexChanged.connect(self.select_control_mode)
        self.BT_Dynamic.clicked.connect(self.press_dynamic)
        self.BT_Static.clicked.connect(self.press_static)

        self.SB_OpenTime.valueChanged.connect(self.get_open_time)
        self.SB_CloseTime.valueChanged.connect(self.get_close_time)
        self.BT_Begin.clicked.connect(self.begin_auto_test)
        self.BT_Stop.clicked.connect(self.stop_auto_test)

        # 自动复选框信号连接按钮禁用函数
        self.CK_Auto.clicked.connect(self.AutoTestDisable)
        self.BT_Lock.clicked.connect(self.JudgeLock)

        # 滑动条设置调节阀控制信号
        self.slider_adjust_input.valueChanged.connect(self.SB_AdjustValveInput.setValue)
        self.SB_AdjustValveInput.valueChanged.connect(self.slider_adjust_input.setValue)

        # 总线阀控制信号
        self.BT_Send.clicked.connect(self.press_send)
        self.BT_WriteIn.clicked.connect(self.press_write_in)
        self.BT_ClearR.clicked.connect(self.press_clear_use)

    # 标签页
    def stack1Ui(self):
        """

        :return:
        """
        self.lb_control_mode.setText('控制方式:')
        self.CB_SelectControl.setMinimumHeight(40)
        self.CB_SelectControl.addItem('None')
        self.lb_power_choose.setText('电压:')
        # self.CB_DCorAC.setMinimumHeight(40)
        # self.CB_DCorAC.addItem('DC')
        # self.CB_DCorAC.addItem('AC')
        self.SB_Voltage.setMinimumHeight(40)
        self.SB_Voltage.setMinimumWidth(80)
        self.SB_Voltage.setMaximum(300.00)
        self.lb_unit_v.setText('V')
        self.BT_Lock.setMinimumHeight(40)
        self.BT_Lock.setMinimumWidth(120)
        self.BT_Lock.setText('点击锁定')
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_outline_128px_1158661_easyicon.net.png'))
        self.BT_Stop.setFixedSize(120, 40)

        no_use_wgt = QtWidgets.QWidget(flags=QtCore.Qt.Widget)

        self.Layout_Basic.addWidget(self.lb_control_mode, 1, 0)
        self.Layout_Basic.addWidget(self.CB_SelectControl, 1, 1)
        self.Layout_Basic.addWidget(self.lb_power_choose, 1, 2)
        # self.Layout_Basic.addWidget(self.CB_DCorAC, 1, 3)
        self.Layout_Basic.addWidget(self.SB_Voltage, 1, 3)
        self.Layout_Basic.addWidget(self.lb_unit_v, 1, 4)
        self.Layout_Basic.addWidget(self.BT_Lock, 1, 5)
        self.Layout_Basic.addWidget(no_use_wgt, 1, 6, 1, 2)

        self.lb_open_valve.setText('        开阀:')
        self.SB_OpenTime.setMinimumHeight(40)
        self.SB_OpenTime.setMinimumWidth(60)
        self.lb_close_valve.setText('        关阀:')
        self.SB_CloseTime.setMinimumHeight(40)
        self.SB_CloseTime.setMinimumWidth(60)
        self.BT_Begin.setMinimumHeight(40)
        self.BT_Begin.setText('开始')
        self.BT_Stop.setMinimumHeight(40)
        self.BT_Stop.setMaximumWidth(90)
        self.BT_Stop.setText('停止')

        self.Layout_Basic.addWidget(self.CK_Auto)
        self.Layout_Basic.addWidget(self.lb_open_valve)
        self.Layout_Basic.addWidget(self.SB_OpenTime)
        self.Layout_Basic.addWidget(self.lb_close_valve)
        self.Layout_Basic.addWidget(self.SB_CloseTime)
        self.Layout_Basic.addWidget(self.BT_Begin)
        self.Layout_Basic.addWidget(self.BT_Stop)
        # self.Layout_Basic.setAlignment(QtCore.Qt.AlignRight)

        # 按钮初始不可用
        self.BT_Begin.setDisabled(1)
        self.BT_Stop.setDisabled(1)
        self.SB_OpenTime.setDisabled(1)
        self.SB_CloseTime.setDisabled(1)

    def stack2Ui(self):
        """

        :return:
        """

        self.lb_adjust_input.setText('调节阀输入：')
        self.SB_AdjustValveInput.setMinimumHeight(40)
        self.SB_AdjustValveInput.setMinimumWidth(60)
        self.SB_AdjustValveInput.setMaximum(20.00)
        self.lb_unit_ma.setText('mA')
        self.lb_step_length.setText('步距:')

        self.CB_StepValve.setMinimumHeight(40)
        self.CB_StepValve.setMinimumWidth(50)
        self.CB_StepValve.addItem('1.0')
        self.CB_StepValve.addItem('0.1')
        self.CB_StepValve.addItem('10.0')
        self.lb_unit_ma2.setText('mA')
        self.lb_adjust_output.setText('调节阀反馈信号：20mA')

        self.slider_adjust_input.move(20, 100)
        self.slider_adjust_input.resize(200, 20)
        self.slider_adjust_input.setMinimum(0)
        self.slider_adjust_input.setMaximum(20)
        self.slider_adjust_input.setSingleStep(1)
        self.slider_adjust_input.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_adjust_input.setTickInterval(1)

        self.Layout_AdjustPage.addWidget(self.lb_adjust_input, 0, 0)
        self.Layout_AdjustPage.addWidget(self.SB_AdjustValveInput, 0, 1)
        self.Layout_AdjustPage.addWidget(self.lb_unit_ma, 0, 2)
        self.Layout_AdjustPage.addWidget(self.slider_adjust_input, 0, 3, 1, 4)
        self.Layout_AdjustPage.addWidget(self.lb_step_length, 1, 0)
        self.Layout_AdjustPage.addWidget(self.CB_StepValve, 1, 1)
        self.Layout_AdjustPage.addWidget(self.lb_unit_ma2, 1, 2)
        self.Layout_AdjustPage.addWidget(self.lb_adjust_output, 1, 3)

    def stack3Ui(self):
        """

        :return:
        """

        self.lb_set_date_out.setMaximumWidth(100)
        self.lb_set_date_out.setText('设置出厂日期:')
        self.DE_SetDate.setCalendarPopup(True)
        self.DE_SetDate.setDate(QtCore.QDate.currentDate())
        self.DE_SetDate.setMaximumWidth(120)
        self.DE_SetDate.setMinimumHeight(40)
        self.BT_WriteIn.setMinimumHeight(40)
        self.BT_WriteIn.setMaximumWidth(60)
        self.BT_WriteIn.setText('写入')
        self.BT_ClearR.setMinimumHeight(40)
        self.BT_ClearR.setMaximumWidth(100)
        self.BT_ClearR.setText('清零使用次数')
        self.lb_send_area.setText('发送区:')
        self.LE_Send.setMinimumHeight(40)
        self.lb_receive_area.setText('接收区:')
        self.LE_Received.setMinimumHeight(40)
        self.BT_Send.setMinimumHeight(40)
        self.BT_Send.setMaximumWidth(60)
        self.BT_Send.setText('发送')

        self.Layout_BusPageStack.addWidget(self.lb_set_date_out, 1, 0)
        self.Layout_BusPageStack.addWidget(self.DE_SetDate, 1, 1)
        self.Layout_BusPageStack.addWidget(self.BT_WriteIn, 1, 2)
        self.Layout_BusPageStack.addWidget(self.BT_ClearR, 1, 3)
        self.Layout_BusPageStack.addWidget(self.lb_send_area, 2, 0)
        self.Layout_BusPageStack.addWidget(self.LE_Send, 2, 1, 1, 3)
        self.Layout_BusPageStack.addWidget(self.lb_receive_area, 3, 0)
        self.Layout_BusPageStack.addWidget(self.LE_Received, 3, 1, 1, 3)
        self.Layout_BusPageStack.addWidget(self.BT_Send, 2, 4)

    def display(self, i):
        """
        切换标签页
        :param i:
        :return:
        """
        self.stack.setCurrentIndex(i)

    def AutoTestDisable(self):
        """

        :return:
        """
        if self.CK_Auto.isChecked():
            self.BT_Begin.setDisabled(0)
            self.BT_Stop.setDisabled(0)
            self.SB_OpenTime.setDisabled(0)
            self.SB_CloseTime.setDisabled(0)
        else:
            self.BT_Begin.setDisabled(1)
            self.BT_Stop.setDisabled(1)
            self.SB_OpenTime.setDisabled(1)
            self.SB_CloseTime.setDisabled(1)

    def load_data(self):
        """

        :return:
        """
        pass
        # print('load data')
        # with open('pkl/controlmode.pkl', 'rb') as f:
        #     sw.control_mode = pickle.loads(f.read())
        #
        # lst = []
        # for i in range(len(sw.control_mode)):
        #     lst.append(sw.control_mode[i]['NAME'])
        # lst2 = list(set(lst))
        # for i in range(len(lst2)):
        #     self.CB_SelectControl.addItem(lst2[i])
        # for i in range(len(sw.control_mode)):
        # self.CB_SelectControl.addItem(sw.control_mode[i]['NAME'])

    def TimerStart(self):
        """

        :return:
        """
        self.QTimerLock.start(500)

    def JudgeLock(self):
        """
        判断是否锁定控制方式和电压
        :return:
        """
        if self.BT_M4.isEnabled():
            self.UnlockControl()
        else:
            self.LockControl()

    def LockControl(self):
        """

        :return:
        """
        if self.CB_SelectControl.currentText() != 'None' and self.SB_Voltage.text() != '0.00':
            self.BT_Lock.setIcon(QtGui.QIcon(':/lock_closed_outline_105.8691588785px_1158659_easyicon.net.png'))
            self.BT_Lock.setText('单击解锁')
            self.valve_control_disabled(False)
            hw.control_mode = sw.control_mode_selected
            hw.voltage = float(self.SB_Voltage.text())
            flag.control_mode_lock = 1

            # 发送信号
            self.voltage_set.emit(hw.voltage)
            print(hw.control_mode, hw.voltage)
        if hw.control_mode['SPECIAL'] == 1:
            self.adjust_page_update()
            # 选择调节阀门控制信号的信号
            self.adjust_signal_select.emit()

        if hw.control_mode['SPECIAL'] == 2:
            # 选择总线阀门控制方式时发送信号
            self.bus_valve_select.emit()

    def UnlockControl(self):
        """

        :return:
        """
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_outline_128px_1158661_easyicon.net.png'))
        self.BT_Lock.setText('单击锁定')
        self.valve_control_disabled(True)
        self.unlock.emit()
        flag.control_mode_lock = 0
        if hw.control_mode['SPECIAL'] == 1:
            self.adjust_signal_cut_off.emit()

        if hw.control_mode['SPECIAL'] == 2:
            self.bus_cut_off.emit()

    def valve_control_disabled(self, tof):
        """

        :param tof:
        :return:
        """
        self.BT_ValveOpen.setDisabled(tof)
        self.BT_ValveClose.setDisabled(tof)
        self.BT_ValveStop.setDisabled(tof)
        self.BT_M3.setDisabled(tof)
        self.BT_M4.setDisabled(tof)
        self.CK_Auto.setDisabled(tof)
        self.SB_AdjustValveInput.setDisabled(tof)
        self.slider_adjust_input.setDisabled(tof)
        self.BT_WriteIn.setDisabled(tof)
        self.BT_ClearR.setDisabled(tof)
        self.BT_Send.setDisabled(tof)
        self.CB_SelectControl.setDisabled(not tof)
        # self.CB_DCorAC.setDisabled(not tof)
        self.SB_Voltage.setDisabled(not tof)

    @staticmethod
    def select_control_mode(i):
        """
        选择一种控制方式
        :param i:
        :return:
        """
        if i:
            sw.control_mode_selected = sw.control_mode[i - 1]
        else:
            sw.control_mode_selected = sw.ControlForm.copy()
            pass
        # hw.control_mode = sw.control_mode[i - 1]

    # 电流曲线
    def draw_dynamic(self):
        """

        :return:
        """

        # yy = sw.current_value[-200:]
        # self.main_window_fig.update_diagram(yy, myflag=0)
        # self.main_window_fig.myTable.remove()

        # self.change_position_signal(hw.open_signal, hw.close_signal)
        # self.change_va_value(hw.current_value_show, hw.voltage_value_show)

        try:
            yy = sw.current_value[
                 -(int(sw.current_set['small_win_show_time'] * 1000 / sw.current_set['data_interval'])):]
        except:
            yy = sw.current_value[-1000:]
        self.main_window_fig.update_diagram(yy, myflag=0)

    @staticmethod
    def press_dynamic():
        """

        :return:
        """
        global fg_update_diagram
        fg_update_diagram = 1

    @staticmethod
    def press_static():
        """

        :return:
        """
        global fg_update_diagram
        fg_update_diagram = 0

    # 总线阀控制
    def press_send(self):
        """

        :return:
        """
        text = self.LE_Send.text()
        self.send_clicked.emit(text)
        pass

    def press_write_in(self):
        """

        :return:
        """
        date = self.DE_SetDate.date().getDate()
        byte_0 = hex(int(str(date[0])[:2]))[2:]
        byte_1 = hex(int(str(date[0])[2:]))[2:]
        byte_2 = hex(date[1])[2:].rjust(2, '0')
        byte_3 = hex(date[2])[2:].rjust(2, '0')

        cmd_date = '01 5B ' + byte_0 + ' ' + byte_1 + ' ' + byte_2 + ' ' + byte_3
        self.send_clicked.emit(crc(cmd_date.upper()))
        # print(date)

    def press_clear_use(self):
        """

        :return:
        """
        self.send_clicked.emit(sw.cmd_clear)
        pass

    def bus_return_show(self, msg):
        """

        :param msg:
        :return:
        """
        # 字符串分割
        result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", msg)
        if crc_check(result):
            self.LE_Received.setText(result.upper())
        else:
            self.LE_Received.setText('返回错误')

    # 自动测试
    def get_open_time(self):
        """
        获取自动测试开阀时间
        :return:
        """
        sw.open_time = self.SB_OpenTime.text()

    def get_close_time(self):
        """
        获取自动测试关阀时间
        :return:
        """
        sw.close_time = self.SB_CloseTime.text()

    def begin_auto_test(self):
        """
        开始自动测试
        :return:
        """
        self.BT_Begin.setDisabled(True)
        self.BT_Stop.setDisabled(False)
        # self.open_valve()

        if self.auto_test_timer.isActive():
            self.auto_test_timer.stop()
        try:
            self.auto_test_timer.timeout.disconnect(self.begin_auto_test)
        except:
            pass
        self.auto_test_timer.timeout.connect(self.auto_test)
        self.auto_test_timer.start(int(sw.open_time) * 1000)

        pass

    def stop_auto_test(self):
        """
        结束自动测试
        :return:
        """
        self.BT_Begin.setDisabled(False)
        self.BT_Stop.setDisabled(True)
        self.auto_test_timer.stop()

    def auto_test(self):
        """
        自动循环测试
        :return:
        """

        # self.close_valve()
        if self.auto_test_timer.isActive():
            self.auto_test_timer.stop()
        try:
            self.auto_test_timer.timeout.disconnect(self.auto_test)
        except:
            pass
        self.auto_test_timer.timeout.connect(self.begin_auto_test)
        self.auto_test_timer.start(int(sw.close_time) * 1000)

    # 窗口更新
    def window_update(self):
        """
        更新窗口电流电压以及到位信号
        :return:
        """

        # print(time.time())
        self.change_va_value(hw.current_value_show, hw.voltage_value_show)
        self.change_position_signal(hw.open_signal, hw.close_signal)

    def adjust_page_update(self):
        """

        :return:
        """
        if hw.control_mode['SIGNAL'] in [1, 2]:
            self.lb_unit_ma.setText('mA')
            self.lb_unit_ma2.setText('mA')
            self.SB_AdjustValveInput.setMaximum(20.00)
            self.slider_adjust_input.setRange(0, 20)
            self.SB_AdjustValveInput.setValue(0.00)
            self.slider_adjust_input.setValue(0)
        elif hw.control_mode['SIGNAL'] in [3, 4]:
            self.lb_unit_ma.setText('V')
            self.lb_unit_ma2.setText('V')
            self.SB_AdjustValveInput.setMaximum(5.00)
            self.slider_adjust_input.setRange(0, 5)
            self.SB_AdjustValveInput.setValue(0.00)
            self.slider_adjust_input.setValue(0)
        elif hw.control_mode['SIGNAL'] in [5, 6]:
            self.lb_unit_ma.setText('V')
            self.lb_unit_ma2.setText('V')
            self.SB_AdjustValveInput.setMaximum(10.00)
            self.slider_adjust_input.setRange(0, 10)
            self.SB_AdjustValveInput.setValue(0.00)
            self.slider_adjust_input.setValue(0)
        pass

    def change_host_name(self, name):
        """

        :param name:str
        :return:
        """
        self.lb_host_name.setText('本机名：' + name)

    def change_server_name(self, name):
        """

        :param name:str
        :return:
        """
        self.lb_server_name.setText('上位机名：' + name)

    def change_connection_state(self, state):
        """

        :param state:str
        :return:
        """
        self.lb_connection_state.setText('连接状态：' + state)

    def change_va_value(self, current, voltage):
        """

        :param current:str
        :param voltage:str
        :return:
        """
        self.lb_current_value.setText('电流值：' + current + 'mA')
        self.lb_voltage_value.setText('电压值：' + voltage + 'V')

    def change_position_signal(self, opened, closed):
        """

        :param opened: str  'Yes' or 'No'
        :param closed: str  'Yes' or 'No'
        :return:
        """
        if opened == 'YES':
            self.lb_open_completely.setText("<p>开到位：<font color=green>Yes</font></p>")
        else:
            self.lb_open_completely.setText("<p>开到位：<font color=red>No</font></p>")

        if closed == 'YES':
            self.lb_close_completely.setText("<p>关到位：<font color=green>Yes</font></p>")
        else:
            self.lb_close_completely.setText("<p>关到位：<font color=red>No</font></p>")

    def change_adjust_feedback(self, _cur):
        """

        :param _cur:
        :return:
        """
        self.lb_adjust_output.setText('反馈信号： ' + str(_cur))


class UpdateThread(QtCore.QThread):
    """
    更新界面数据和曲线
    """

    def __init__(self, _win):

        super(UpdateThread, self).__init__()
        self.win = _win

    def run(self):
        """

        :return:
        """

        # window_update_time = time.time()
        while flag.canvas_switch:
            time.sleep(1)

            if fg_update_diagram == 1:
                # sw.current_value.append(int(100 * random.random()))
                # del sw.current_value[0]
                if flag.control_mode_lock:
                    try:
                        yy = sw.current_value[
                             -(int(sw.current_set['small_win_show_time'] * 1000 / sw.current_set['data_interval'])):]
                    except:
                        yy = sw.current_value[-1000:]
                    self.win.main_window_fig.update_diagram(yy, myflag=0)
                    # self.win.window_update()
            # self.win.change_va_value(hw.current_value_show, hw.voltage_value_show)ram(yy, myflag=0)


class LongPressButton(QtWidgets.QPushButton):
    """
    长按按钮
    """

    def __init__(self, parent=None):
        super(LongPressButton, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.bt = QtWidgets.QPushButton(self)

        # signal
        self.bt.pressed.connect(self.tm_start)
        self.bt.released.connect(self.tm_stop)
        self.timer.timeout.connect(self.long_pressed)

    def setText(self, p_str):
        """

        :param p_str:
        :return:
        """
        self.bt.setText(p_str)

    def setIcon(self, icon):
        """

        :param icon:
        :return:
        """

        self.bt.setIcon(icon)

    def tm_start(self):
        """

        :return:
        """
        self.timer.start(800)

    def tm_stop(self):
        """

        :return:
        """
        self.timer.stop()

    def long_pressed(self):
        """

        :return:
        """
        pass
