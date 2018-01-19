# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""

import numpy as np
import pickle
import random
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import diagram

from public.datacache import SoftwareData as sw
from public.datacache import HardwareData as hw


class Ui_MainWindow(object):
    """
    程序主界面
    """
    def setupUi(self, main_window):
        """

        :param main_window:
        :return:
        """
        main_window.setObjectName("MainWindow")
        main_window.resize(1024, 550)
        main_window.setMinimumSize(QtCore.QSize(800, 300))
        main_window.setWindowTitle('可编程测试仪')
        main_window.setWindowIcon(QtGui.QIcon(":/qt.png"))

        # MainWindow.setMaximumSize(QtCore.QSize(1920, 1080)) #不设置最大值可以使用最大化按钮
        # 菜单栏
        self.Init_MenuBar()
        main_window.setMenuBar(self.MenuBar)
        # 主窗口widget
        self.mainWidget = QtWidgets.QWidget(self)
        main_window.setCentralWidget(self.mainWidget)

        self.Init_InformationBox(self.mainWidget)
        self.Init_CurrentCurve(self.mainWidget)
        self.Init_ValveControl(self.mainWidget)

        Layout_Main = QtWidgets.QGridLayout(self.mainWidget)
        Layout_Main.addWidget(self.GB_Information, 1, 0, 2, 2)
        Layout_Main.addWidget(self.GB_CurrentCurve, 1, 2, 2, 4)
        Layout_Main.addWidget(self.GB_ValveControl, 3, 0, 3, 6)

    #  初始化菜单栏
    def Init_MenuBar(self):
        """

        :return:
        """
        # 菜单栏
        self.MenuBar = QtWidgets.QMenuBar()
        self.SetMenu = self.MenuBar.addMenu('设置')
        # 控制方式设置
        self.Action_ControlSet = QtWidgets.QAction('控制方式设置', self)
        self.SetMenu.addAction(self.Action_ControlSet)
        # 电源及采样校准
        self.Action_PowerCalibration = QtWidgets.QAction('电源及采样校准', self)
        self.SetMenu.addAction(self.Action_PowerCalibration)
        # 外控设置
        self.Action_RemoteControl = QtWidgets.QAction('外控设置', self)
        self.SetMenu.addAction(self.Action_RemoteControl)
        # 其他设置
        self.Action_Others = QtWidgets.QAction('其他设置', self)
        self.SetMenu.addAction(self.Action_Others)
        # 继电器自检
        self.Action_RelayCheck = QtWidgets.QAction('继电器自检', self)
        self.SetMenu.addAction(self.Action_RelayCheck)

    def Init_InformationBox(self, widget):
        # 基本信息GroupBox
        self.GB_Information = QtWidgets.QGroupBox(widget)
        # self.GB_Information.setGeometry(QtCore.QRect(5, 0, 300, 200))
        self.GB_Information.setMinimumWidth(250)
        self.GB_Information.setTitle('仪器状态')

        self.Layout_Information = QtWidgets.QVBoxLayout(self.GB_Information)


        Label_11 = QtWidgets.QLabel('本机名:')
        Label_12 = QtWidgets.QLabel('主机名:')
        Label_13 = QtWidgets.QLabel('故障码:')
        Label_14 = QtWidgets.QLabel('其他:')
        self.Layout_Information.addWidget(Label_11)
        self.Layout_Information.addWidget(Label_12)
        self.Layout_Information.addWidget(Label_13)
        self.Layout_Information.addWidget(Label_14)
        self.Layout_Information.addStretch(0)

        pass
    # 初始化电流曲线部分
    def Init_CurrentCurve(self, widget):
        self.GB_CurrentCurve = QtWidgets.QGroupBox(widget)
        self.GB_CurrentCurve.setTitle('阀门状态')

        self.Label_21 = QtWidgets.QLabel('电 流 值: 100mA')
        self.Label_22 = QtWidgets.QLabel('电 压 值: 5V')
        self.Label_23 = QtWidgets.QLabel('开阀到位: Yes')
        self.Label_24 = QtWidgets.QLabel('关阀到位: No')

        Wgt_LB = QtWidgets.QWidget()
        Wgt_LB.setMaximumWidth(140)
        Layout_LB = QtWidgets.QVBoxLayout(Wgt_LB)
        Layout_LB.addWidget(self.Label_21)
        Layout_LB.addWidget(self.Label_22)
        Layout_LB.addWidget(self.Label_23)
        Layout_LB.addWidget(self.Label_24)
        Layout_LB.addStretch(0)

        self.BT_FullScreen = QtWidgets.QPushButton()
        self.BT_FullScreen.setFixedSize(50, 50)
        # self.BT_FullScreen.setText('全屏')
        self.BT_FullScreen.setStyleSheet('''QPushButton {background-image: url("./images/zoomout.png")}''')
        self.BT_Dynamic = QtWidgets.QPushButton()
        self.BT_Dynamic.setText('动态')
        self.BT_Dynamic.setFixedSize(50, 50)
        self.BT_Static = QtWidgets.QPushButton()
        self.BT_Static.setText('静态')
        self.BT_Static.setFixedSize(50, 50)

        Layout_button = QtWidgets.QVBoxLayout()
        Layout_button.addWidget(self.BT_FullScreen)
        Layout_button.addWidget(self.BT_Dynamic)
        Layout_button.addWidget(self.BT_Static)

        xx = np.arange(-10.0, 0, 0.05)
        yy = (np.cos(2*np.pi*xx)+1)*10
        self.SmallDiagram = diagram.PlotWidget(self)
        self.SmallDiagram.update_diagram(yy)
        self.SmallDiagram.myTable.remove()
        self.SmallDiagram.fig.subplots_adjust(0., 0., 1, 1)
        self.SmallDiagram.ax.xaxis.set_ticks_position('top')
        self.SmallDiagram.ax.yaxis.set_ticks_position('left')

        # self.DIAGRAM.figure.subplots_adjust(0.02, 0.25, 0.9, 0.96)
        self.SmallDiagram.ax.spines['top'].set_position(('data', 0))
        self.SmallDiagram.ax.spines['left'].set_position(('data', 0))

        Layout = QtWidgets.QHBoxLayout(self.GB_CurrentCurve)
        Layout.addWidget(Wgt_LB)
        Layout.addWidget(self.SmallDiagram)
        Layout.addLayout(Layout_button)

    # 初始化阀门控制部分
    def Init_ValveControl(self, widget):
        self.GB_ValveControl = QtWidgets.QGroupBox(widget)
        self.GB_ValveControl.setTitle('阀门控制')

        self.Leftlist = QtWidgets.QListWidget(self.GB_ValveControl)
        self.Leftlist.setMaximumWidth(100)
        self.Leftlist.insertItem(0, '通用')
        self.Leftlist.insertItem(1, '调节阀+')
        self.Leftlist.insertItem(2, '总线阀+')
        self.Leftlist.currentRowChanged.connect(self.display)

        self.stack_1 = QtWidgets.QWidget()
        self.stack_2 = QtWidgets.QWidget()
        self.stack_3 = QtWidgets.QWidget()

        self.stack1Ui(self.stack_1)
        self.stack2Ui(self.stack_2)
        self.stack3Ui(self.stack_3)

        self.stack = QtWidgets.QStackedWidget(self.GB_ValveControl)
        self.stack.addWidget(self.stack_1)
        self.stack.addWidget(self.stack_2)
        self.stack.addWidget(self.stack_3)

        self.BT_ValveOpen = QtWidgets.QPushButton()
        self.BT_ValveOpen.setText('开阀')
        self.BT_ValveOpen.setMinimumHeight(40)
        self.BT_ValveClose = QtWidgets.QPushButton()
        self.BT_ValveClose.setText('关阀')
        self.BT_ValveClose.setMinimumHeight(40)
        self.BT_ValveStop = QtWidgets.QPushButton()
        self.BT_ValveStop.setText('停阀')
        self.BT_ValveStop.setMinimumHeight(40)
        self.BT_M3 = QtWidgets.QPushButton()
        self.BT_M3.setText('位置3')
        self.BT_M3.setMinimumHeight(40)
        self.BT_M4 = QtWidgets.QPushButton()
        self.BT_M4.setText('位置4')
        self.BT_M4.setMinimumHeight(40)
        self.ValveControlButtonDisabled(True)

        Layout_ControlButton = QtWidgets.QVBoxLayout()
        Layout_ControlButton.addWidget(self.BT_ValveOpen)
        Layout_ControlButton.addWidget(self.BT_ValveClose)
        Layout_ControlButton.addWidget(self.BT_ValveStop)
        Layout_ControlButton.addWidget(self.BT_M3)
        Layout_ControlButton.addWidget(self.BT_M4)

        Layout_Stack = QtWidgets.QHBoxLayout(self.GB_ValveControl)
        Layout_Stack.addWidget(self.Leftlist)
        Layout_Stack.addWidget(self.stack)
        Layout_Stack.addLayout(Layout_ControlButton)

    def stack1Ui(self, stack):

        self.Layout_Basic = QtWidgets.QGridLayout(stack)
        self.Label_31 = QtWidgets.QLabel()
        self.Label_31.setText('        控制方式:')
        self.CB_SelectControl = QtWidgets.QComboBox()
        self.CB_SelectControl.setMinimumHeight(40)
        self.CB_SelectControl.addItem('None')
        self.Label_32 = QtWidgets.QLabel()
        self.Label_32.setText('        电源:')
        self.CB_DCorAC = QtWidgets.QComboBox()
        self.CB_DCorAC.setMinimumHeight(40)
        self.CB_DCorAC.addItem('DC')
        self.CB_DCorAC.addItem('AC')
        self.SB_Voltage = QtWidgets.QDoubleSpinBox()
        self.SB_Voltage.setMinimumHeight(40)
        self.SB_Voltage.setMinimumWidth(80)
        self.Label_33 = QtWidgets.QLabel()
        self.Label_33.setText('V')
        self.BT_Lock = QtWidgets.QPushButton()
        self.BT_Lock.setMinimumHeight(40)
        self.BT_Lock.setMinimumWidth(120)
        self.BT_Lock.setText('长按锁定')
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_outline_128px_1158661_easyicon.net.png'))
        self.QTimerLock = QtCore.QTimer(self)
        nousewgt = QtWidgets.QWidget()

        self.Layout_Basic.addWidget(self.Label_31, 1, 0)
        self.Layout_Basic.addWidget(self.CB_SelectControl, 1, 1)
        self.Layout_Basic.addWidget(self.Label_32, 1, 2)
        self.Layout_Basic.addWidget(self.CB_DCorAC, 1, 3)
        self.Layout_Basic.addWidget(self.SB_Voltage, 1, 4)
        self.Layout_Basic.addWidget(self.Label_33, 1, 5)
        self.Layout_Basic.addWidget(self.BT_Lock, 1, 6)
        self.Layout_Basic.addWidget(nousewgt, 1, 7, 1, 2)


        self.CK_Auto = QtWidgets.QCheckBox('自动')
        self.Label_34 = QtWidgets.QLabel()
        self.Label_34.setText('        开阀:')
        self.SB_OpenTime = QtWidgets.QDoubleSpinBox()
        self.SB_OpenTime.setMinimumHeight(40)
        self.SB_OpenTime.setMinimumWidth(60)
        self.Label_35 = QtWidgets.QLabel(stack)
        self.Label_35.setText('        关阀:')
        self.SB_CloseTime = QtWidgets.QDoubleSpinBox()
        self.SB_CloseTime.setMinimumHeight(40)
        self.SB_CloseTime.setMinimumWidth(60)
        self.BT_Begin = QtWidgets.QPushButton()
        self.BT_Begin.setMinimumHeight(40)
        self.BT_Begin.setText('开始')
        self.BT_Stop = QtWidgets.QPushButton()
        self.BT_Stop.setMinimumHeight(40)
        self.BT_Stop.setMaximumWidth(90)
        self.BT_Stop.setText('停止')

        self.Layout_Basic.addWidget(self.CK_Auto)
        self.Layout_Basic.addWidget(self.Label_34)
        self.Layout_Basic.addWidget(self.SB_OpenTime)
        self.Layout_Basic.addWidget(self.Label_35)
        self.Layout_Basic.addWidget(self.SB_CloseTime)
        self.Layout_Basic.addWidget(self.BT_Begin)
        self.Layout_Basic.addWidget(self.BT_Stop)
        # self.Layout_Basic.setAlignment(QtCore.Qt.AlignRight)

        # 按钮初始不可用
        self.BT_Begin.setDisabled(1)
        self.BT_Stop.setDisabled(1)
        self.SB_OpenTime.setDisabled(1)
        self.SB_CloseTime.setDisabled(1)
        # 自动复选框信号连接按钮禁用函数
        self.CK_Auto.clicked.connect(self.AutoTestDisable)
        self.BT_Lock.pressed.connect(self.TimerStart)
        self.BT_Lock.released.connect(self.QTimerLock.stop)
        self.QTimerLock.timeout.connect(self.LockControl)

    def stack2Ui(self, stack):

        Layout_AdjustPage = QtWidgets.QGridLayout(stack)
        self.Label_41 = QtWidgets.QLabel()
        self.Label_41.setText('调节阀输入：')
        self.SB_AdjustValveInput = QtWidgets.QDoubleSpinBox()
        self.SB_AdjustValveInput.setMinimumHeight(40)
        self.SB_AdjustValveInput.setMinimumWidth(60)
        self.Label_42 = QtWidgets.QLabel()
        self.Label_42.setText('mA')
        self.Label_43 = QtWidgets.QLabel()
        self.Label_43.setText('            步距:')
        self.CB_StepValve = QtWidgets.QComboBox()
        self.CB_StepValve.setMinimumHeight(40)
        self.CB_StepValve.setMinimumWidth(50)
        self.CB_StepValve.addItem('1.0')
        self.CB_StepValve.addItem('0.1')
        self.CB_StepValve.addItem('10.0')

        self.Label_44 = QtWidgets.QLabel()
        self.Label_44.setText('mA')
        self.Label_45 = QtWidgets.QLabel()
        self.Label_45.setText('调节阀反馈信号：20mA')
        Layout_AdjustPage.addWidget(self.Label_41, 1, 0)
        Layout_AdjustPage.addWidget(self.SB_AdjustValveInput, 1, 1)
        Layout_AdjustPage.addWidget(self.Label_42, 1, 2)
        Layout_AdjustPage.addWidget(self.Label_43, 1, 3)
        Layout_AdjustPage.addWidget(self.CB_StepValve, 1, 4)
        Layout_AdjustPage.addWidget(self.Label_44, 1, 5)
        Layout_AdjustPage.addWidget(self.Label_45, 1, 6)

        self.Slider_AdjustValveControlSignal = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_AdjustValveControlSignal.move(20, 100)
        self.Slider_AdjustValveControlSignal.resize(200, 20)
        self.Slider_AdjustValveControlSignal.setMinimum(0)
        self.Slider_AdjustValveControlSignal.setMaximum(20)
        self.Slider_AdjustValveControlSignal.setSingleStep(1)
        self.Slider_AdjustValveControlSignal.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider_AdjustValveControlSignal.setTickInterval(1)
        Layout_AdjustPage.addWidget(self.Slider_AdjustValveControlSignal, 2, 0, 1, 6)

        # 滑动条设置调节阀控制信号
        self.Slider_AdjustValveControlSignal.valueChanged.connect(self.AdjustValveControlSignalValveChange)

    def stack3Ui(self, stack):

        self.Layout_BusPageStack = QtWidgets.QGridLayout(stack)
        self.Label_51 = QtWidgets.QLabel(stack)
        self.Label_51.setMaximumWidth(100)
        self.Label_51.setText('设置出厂日期:')
        self.DE_SetDate = QtWidgets.QDateEdit()
        self.DE_SetDate.setCalendarPopup(True)
        self.DE_SetDate.setDate(QtCore.QDate.currentDate())
        self.DE_SetDate.setMaximumWidth(120)
        self.DE_SetDate.setMinimumHeight(40)
        self.BT_WriteIn = QtWidgets.QPushButton(stack)
        self.BT_WriteIn.setMinimumHeight(40)
        self.BT_WriteIn.setMaximumWidth(60)
        self.BT_WriteIn.setText('写入')
        self.BT_ClearR = QtWidgets.QPushButton(stack)
        self.BT_ClearR.setMinimumHeight(40)
        self.BT_ClearR.setMaximumWidth(100)
        self.BT_ClearR.setText('清零使用次数')
        self.Label_52 = QtWidgets.QLabel(stack)
        self.Label_52.setText('发送区:')
        self.LE_Send = QtWidgets.QLineEdit('输入')
        self.LE_Send.setMinimumHeight(40)
        self.Label_53 = QtWidgets.QLabel(stack)
        self.Label_53.setText('接收区:')
        self.LE_Received = QtWidgets.QLineEdit()
        self.LE_Received.setMinimumHeight(40)
        self.BT_Send = QtWidgets.QPushButton(stack)
        self.BT_Send.setMinimumHeight(40)
        self.BT_Send.setMaximumWidth(60)
        self.BT_Send.setText('发送')

        self.Layout_BusPageStack.addWidget(self.Label_51, 1, 0)
        self.Layout_BusPageStack.addWidget(self.DE_SetDate, 1, 1)
        self.Layout_BusPageStack.addWidget(self.BT_WriteIn, 1, 2)
        self.Layout_BusPageStack.addWidget(self.BT_ClearR, 1, 3)
        self.Layout_BusPageStack.addWidget(self.Label_52, 2, 0)
        self.Layout_BusPageStack.addWidget(self.LE_Send, 2, 1, 1, 3)
        self.Layout_BusPageStack.addWidget(self.Label_53, 3, 0)
        self.Layout_BusPageStack.addWidget(self.LE_Received, 3, 1, 1, 3)
        self.Layout_BusPageStack.addWidget(self.BT_Send, 2, 4)

    def display(self, i):
        self.stack.setCurrentIndex(i)

    def AutoTestDisable(self):
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

    def TimerStart(self):
        self.QTimerLock.start(1000)
        self.QTimerLock.timeout.connect(self.JudgeLock)

    def JudgeLock(self):
        self.QTimerLock.stop()
        if self.LockState:
            self.UnlockControl()
        else:
            self.LockControl()

    def LockControl(self):
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_closed_outline_105.8691588785px_1158659_easyicon.net.png'))
        self.BT_Lock.setText('长按解锁')
        self.ValveControlButtonDisabled(False)
        self.LockState = True

    def UnlockControl(self):
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_outline_128px_1158661_easyicon.net.png'))
        self.BT_Lock.setText('长按锁定')
        self.ValveControlButtonDisabled(True)
        self.LockState = False

    def ValveControlButtonDisabled(self, tof):
        self.BT_ValveOpen.setDisabled(tof)
        self.BT_ValveClose.setDisabled(tof)
        self.BT_ValveStop.setDisabled(tof)
        self.BT_M3.setDisabled(tof)
        self.BT_M4.setDisabled(tof)
        self.CK_Auto.setDisabled(tof)
        self.SB_AdjustValveInput.setDisabled(tof)
        self.Slider_AdjustValveControlSignal.setDisabled(tof)
        self.BT_WriteIn.setDisabled(tof)
        self.BT_ClearR.setDisabled(tof)
        self.BT_Send.setDisabled(tof)
        self.CB_SelectControl.setDisabled(not tof)
        self.CB_DCorAC.setDisabled(not tof)
        self.SB_Voltage.setDisabled(not tof)

    def AdjustValveControlSignalValveChange(self):
        self.SB_AdjustValveInput.setValue(float(self.Slider_AdjustValveControlSignal.value()))


class Ui_MainWin(QtWidgets.QMainWindow):
    """
    IN
    """
    lock_state = True

    def __init__(self, parent=None):
        super(Ui_MainWin, self).__init__(parent, flags=QtCore.Qt.Window)

        self.setObjectName("MainWindow")
        self.resize(1024, 550)
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
        self.Action_RemoteControl = QtWidgets.QAction('外控设置', self)
        self.Action_Others = QtWidgets.QAction('其他设置', self)
        self.Action_RelayCheck = QtWidgets.QAction('继电器自检', self)

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
        self.lb_current_valve = QtWidgets.QLabel('电流值: 100mA')
        self.lb_voltage_valve = QtWidgets.QLabel('电压值: 5V')
        self.lb_open_completely = QtWidgets.QLabel('开到位: Yes')
        self.lb_close_completely = QtWidgets.QLabel('关到位: No')
        self.main_window_fig = diagram.PlotWidget(self)
        self.BT_FullScreen = QtWidgets.QPushButton()
        self.BT_Dynamic = QtWidgets.QPushButton()
        self.BT_Static = QtWidgets.QPushButton()
        self.refresh_timer = QtCore.QTimer(self)

        self.init_current_curve()

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
        # self.CB_DCorAC = QtWidgets.QComboBox()
        self.SB_Voltage = QtWidgets.QDoubleSpinBox()
        self.lb_unit_v = QtWidgets.QLabel()
        self.BT_Lock = QtWidgets.QPushButton()
        self.QTimerLock = QtCore.QTimer(self)
        self.CK_Auto = QtWidgets.QCheckBox('自动')
        self.lb_open_valve = QtWidgets.QLabel()
        self.SB_OpenTime = QtWidgets.QDoubleSpinBox()
        self.lb_close_valve = QtWidgets.QLabel()
        self.SB_CloseTime = QtWidgets.QDoubleSpinBox()
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

        self.init_valve_control()
        self.load_data()

        # 主窗口布局
        layout_main = QtWidgets.QGridLayout(self.mainWidget)
        layout_main.addWidget(self.GB_Information, 0, 0, 2, 2)
        layout_main.addWidget(self.GB_CurrentCurve, 0, 2, 2, 4)
        layout_main.addWidget(self.GB_ValveControl, 2, 0, 3, 6)

    #  初始化菜单栏
    def init_menubar(self):
        """

        :return:
        """
        # 控制方式设置
        self.SetMenu.addAction(self.Action_ControlSet)
        # 电源及采样校准
        self.SetMenu.addAction(self.Action_PowerCalibration)
        # 外控设置
        self.SetMenu.addAction(self.Action_RemoteControl)
        # 其他设置
        self.SetMenu.addAction(self.Action_Others)
        # 继电器自检
        self.SetMenu.addAction(self.Action_RelayCheck)

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

        Wgt_LB = QtWidgets.QWidget()
        Wgt_LB.setMaximumWidth(140)
        Layout_LB = QtWidgets.QVBoxLayout(Wgt_LB)
        Layout_LB.addWidget(self.lb_current_valve)
        Layout_LB.addWidget(self.lb_voltage_valve)
        Layout_LB.addWidget(self.lb_open_completely)
        Layout_LB.addWidget(self.lb_close_completely)
        Layout_LB.addStretch(1)

        self.main_window_fig.setMaximumHeight(180)
        # xx = np.arange(-10.0, 0, 0.05)
        # yy = (np.cos(2*np.pi*xx)+1)*10
        self.main_window_fig.update_diagram(sw.current_valve, myflag=0)

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
        Layout_Stack.addLayout(Layout_ControlButton)

        # signal
        self.left_list.currentRowChanged.connect(self.display)
        self.CB_SelectControl.currentIndexChanged.connect(self.select_control_mode)
        # self.CB_SelectControl.activated.connect(self.load_data)
        # self.CB_DCorAC.currentIndexChanged.connect(self.select_power)
        self.SB_Voltage.valueChanged.connect(self.set_voltage)
        self.refresh_timer.timeout.connect(self.draw_dynamic)
        self.BT_Dynamic.clicked.connect(self.press_dynamic)
        self.BT_Static.clicked.connect(self.press_static)

        # 自动复选框信号连接按钮禁用函数
        self.CK_Auto.clicked.connect(self.AutoTestDisable)
        self.BT_Lock.pressed.connect(self.TimerStart)
        self.BT_Lock.released.connect(self.QTimerLock.stop)
        # self.QTimerLock.timeout.connect(self.LockControl)

        # 滑动条设置调节阀控制信号
        self.slider_adjust_input.valueChanged.connect(self.adjust_input_change)
        self.QTimerLock.timeout.connect(self.JudgeLock)

    def stack1Ui(self):
        """

        :return:
        """
        self.lb_control_mode.setText('      控制方式:')
        self.CB_SelectControl.setMinimumHeight(40)
        self.CB_SelectControl.addItem('None')
        self.lb_power_choose.setText('        电压:')
        # self.CB_DCorAC.setMinimumHeight(40)
        # self.CB_DCorAC.addItem('DC')
        # self.CB_DCorAC.addItem('AC')
        self.SB_Voltage.setMinimumHeight(40)
        self.SB_Voltage.setMinimumWidth(80)
        self.lb_unit_v.setText('V')
        self.BT_Lock.setMinimumHeight(40)
        self.BT_Lock.setMinimumWidth(120)
        self.BT_Lock.setText('长按锁定')
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
        self.lb_unit_ma.setText('mA')
        self.lb_step_length.setText('            步距:')

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

        self.Layout_AdjustPage.addWidget(self.lb_adjust_input, 1, 0)
        self.Layout_AdjustPage.addWidget(self.SB_AdjustValveInput, 1, 1)
        self.Layout_AdjustPage.addWidget(self.lb_unit_ma, 1, 2)
        self.Layout_AdjustPage.addWidget(self.lb_step_length, 1, 3)
        self.Layout_AdjustPage.addWidget(self.CB_StepValve, 1, 4)
        self.Layout_AdjustPage.addWidget(self.lb_unit_ma2, 1, 5)
        self.Layout_AdjustPage.addWidget(self.lb_adjust_output, 1, 6)
        self.Layout_AdjustPage.addWidget(self.slider_adjust_input, 2, 0, 1, 6)

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
        self.QTimerLock.start(1000)

    def JudgeLock(self):
        """

        :return:
        """
        self.QTimerLock.stop()
        if self.lock_state:
            self.UnlockControl()
        else:
            self.LockControl()

    def LockControl(self):
        """

        :return:
        """
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_closed_outline_105.8691588785px_1158659_easyicon.net.png'))
        self.BT_Lock.setText('长按解锁')
        self.valve_control_disabled(False)
        self.lock_state = True

        print(hw.control_mode, hw.voltage)

    def UnlockControl(self):
        """

        :return:
        """
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_outline_128px_1158661_easyicon.net.png'))
        self.BT_Lock.setText('长按锁定')
        self.valve_control_disabled(True)
        self.lock_state = False

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

    def adjust_input_change(self):
        """

        :return:
        """
        self.SB_AdjustValveInput.setValue(float(self.slider_adjust_input.value()))

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

    def change_va_valve(self, current, voltage):
        """

        :param current:str
        :param voltage:str
        :return:
        """
        self.lb_current_valve.setText('电流值：' + current)
        self.lb_voltage_valve.setText('电压值：' + voltage)

    def change_position_signal(self, opened, closed):
        """

        :param opened: str  'Yes' or 'No'
        :param closed: str  'Yes' or 'No'
        :return:
        """
        self.lb_open_completely.setText('开阀到位：' + opened)
        self.lb_close_completely.setText('关阀到位：' + closed)

    def select_control_mode(self, i):
        """

        :param i:
        :return:
        """
        # print(self.CB_SelectControl.currentText(), i)
        hw.control_mode[0] = self.CB_SelectControl.currentText()
        hw.control_mode[1] = i
        # print(hw.control_mode)

    def set_voltage(self):
        """

        :return:
        """
        hw.voltage = self.SB_Voltage.text()

    def draw_dynamic(self):

        sw.current_valve.append(int(100 * random.random()))
        del sw.current_valve[0]
        yy = sw.current_valve
        self.main_window_fig.update_diagram(yy, myflag=0)
        # self.main_window_fig.myTable.remove()


    def press_dynamic(self):
        if not self.refresh_timer.isActive():
            self.refresh_timer.start(300)

    def press_static(self):
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()

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

