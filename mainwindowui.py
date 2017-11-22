#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import images.images_rc

import diagram

class Ui_MainWindow(object):
    '''
    程序主界面
    '''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 550)
        MainWindow.setMinimumSize(QtCore.QSize(600, 300))
        MainWindow.setWindowTitle('可编程测试仪')
        MainWindow.setWindowIcon(QtGui.QIcon(":/qt.png"))

        # MainWindow.setMaximumSize(QtCore.QSize(1920, 1080)) #不设置最大值可以使用最大化按钮
        # 菜单栏
        self.Init_MenuBar()
        MainWindow.setMenuBar(self.MenuBar)
        # 主窗口widget
        self.mainWidget = QtWidgets.QWidget(self)
        MainWindow.setCentralWidget(self.mainWidget)

        self.Init_InformationBox(self.mainWidget)
        self.Init_CurrentCurve(self.mainWidget)
        self.Init_ValveControl(self.mainWidget)

        Layout_Main = QtWidgets.QGridLayout(self.mainWidget)
        Layout_Main.addWidget(self.GB_Information, 1, 0, 2, 2)
        Layout_Main.addWidget(self.GB_CurrentCurve, 1, 2, 2, 4)
        Layout_Main.addWidget(self.GB_ValveControl, 3, 0, 3, 6)

    #  初始化菜单栏
    def Init_MenuBar(self):
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

        self.Wgt_MainWinCurrent = QtWidgets.QWidget(self.GB_CurrentCurve)
        DIAGRAM = diagram.PlotWidget(self.Wgt_MainWinCurrent)


        Layout = QtWidgets.QHBoxLayout(self.GB_CurrentCurve)
        Layout.addWidget(Wgt_LB)
        Layout.addWidget(self.Wgt_MainWinCurrent)
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
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_128px_1175616_easyicon.net.png'))
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
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_128px_1175615_easyicon.net.png'))
        self.BT_Lock.setText('长按解锁')
        self.ValveControlButtonDisabled(False)
        self.LockState = True

    def UnlockControl(self):
        self.BT_Lock.setIcon(QtGui.QIcon(':/lock_open_128px_1175616_easyicon.net.png'))
        self.BT_Lock.setText('长按锁定')
        self.ValveControlButtonDisabled(True)
        self.LockState = False

    def ValveControlButtonDisabled(self, bool):
        self.BT_ValveOpen.setDisabled(bool)
        self.BT_ValveClose.setDisabled(bool)
        self.BT_ValveStop.setDisabled(bool)
        self.BT_M3.setDisabled(bool)
        self.BT_M4.setDisabled(bool)
        self.CK_Auto.setDisabled(bool)
        self.SB_AdjustValveInput.setDisabled(bool)
        self.Slider_AdjustValveControlSignal.setDisabled(bool)
        self.BT_WriteIn.setDisabled(bool)
        self.BT_ClearR.setDisabled(bool)
        self.BT_Send.setDisabled(bool)
        self.CB_SelectControl.setDisabled(not bool)
        self.CB_DCorAC.setDisabled(not bool)
        self.SB_Voltage.setDisabled(not bool)

    def AdjustValveControlSignalValveChange(self):
        self.SB_AdjustValveInput.setValue(float(self.Slider_AdjustValveControlSignal.value()))











