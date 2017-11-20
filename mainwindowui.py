#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import images.images_rc

class Ui_MainWindow(object):
    '''
    程序主界面
    '''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(300, 200, 1024, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setWindowTitle('可编程测试仪')
        MainWindow.setWindowIcon(QtGui.QIcon(":/qt.png"))  #设置程序窗口的图标
        # MainWindow.setMaximumSize(QtCore.QSize(1920, 1080)) #不设置最大值可以使用最大化按钮

        self.Init_MenuBar()
        MainWindow.setMenuBar(self.MenuBar)

        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setGeometry(QtCore.QRect(0, 30, 1010, 600))

        self.Init_InformationBox(self.mainWidget)
        self.Init_CurrentCurve(self.mainWidget)
        self.Init_ValveControl(self.mainWidget)


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
        self.GB_Information.setGeometry(QtCore.QRect(5, 0, 300, 200))
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
        self.GB_CurrentCurve.setGeometry(QtCore.QRect(315, 0, 695, 200))
        self.GB_CurrentCurve.setTitle('阀门状态')

        self.Layout_CurrentCurve = QtWidgets.QVBoxLayout(self.GB_CurrentCurve)

        self.Label_21 = QtWidgets.QLabel('电 流 值: 100mA')
        self.Label_22 = QtWidgets.QLabel('电 压 值: 5V')
        self.Label_23 = QtWidgets.QLabel('开阀到位: Yes')
        self.Label_24 = QtWidgets.QLabel('关阀到位: No')
        self.Layout_CurrentCurve.addWidget(self.Label_21)
        self.Layout_CurrentCurve.addWidget(self.Label_22)
        self.Layout_CurrentCurve.addWidget(self.Label_23)
        self.Layout_CurrentCurve.addWidget(self.Label_24)
        self.Layout_CurrentCurve.addStretch(0)

        self.BT_FullScreen = QtWidgets.QPushButton(self.GB_CurrentCurve)
        self.BT_FullScreen.setGeometry(645, 6, 50, 50)
        # self.BT_FullScreen.setText('全屏')
        style = '''QPushButton {background-image: url("./images/zoomout.png")}'''
        self.BT_FullScreen.setStyleSheet(style)

        wgt = QtWidgets.QWidget(self.GB_CurrentCurve)
        wgt.setGeometry(600, 100, 100, 100)
        self.BT_Dynamic = QtWidgets.QPushButton(wgt)
        # self.BT_Dynamic.setGeometry(645, 56, 50, 50)
        self.BT_Dynamic.setText('动态')
        self.BT_Static = QtWidgets.QPushButton(wgt)
        # self.BT_Static.setGeometry(645, 106, 50, 50)
        self.BT_Static.setText('静态')
        layout = QtWidgets.QVBoxLayout(wgt)
        layout.addWidget(self.BT_Dynamic)
        layout.addWidget(self.BT_Static)

    # 初始化阀门控制部分
    def Init_ValveControl(self, widget):
        self.GB_ValveControl = QtWidgets.QGroupBox(widget)
        self.GB_ValveControl.setGeometry(QtCore.QRect(5, 205, 1005, 300))
        self.GB_ValveControl.setTitle('阀门控制')

        self.Leftlist = QtWidgets.QListWidget(self.GB_ValveControl)
        self.Leftlist.setGeometry(10, 20, 100, 250)
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
        self.stack.setGeometry(120, 20, 750, 250)

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
        self.wgt = QtWidgets.QWidget(self.GB_ValveControl)
        self.wgt.setGeometry(900, 20, 100, 250)
        self.Layout_ControlButton = QtWidgets.QVBoxLayout(self.wgt)
        self.Layout_ControlButton.addWidget(self.BT_ValveOpen)
        self.Layout_ControlButton.addWidget(self.BT_ValveClose)
        self.Layout_ControlButton.addWidget(self.BT_ValveStop)
        self.Layout_ControlButton.addWidget(self.BT_M3)
        self.Layout_ControlButton.addWidget(self.BT_M4)

        # self.Layout_Stack = QtWidgets.QHBoxLayout(self.GB_ValveControl)
        # self.Layout_Stack.addWidget(self.Leftlist)
        # self.Layout_Stack.addWidget(self.stack)

    def stack1Ui(self, stack):
        self.wgt1 = QtWidgets.QWidget(stack)
        self.wgt1.setGeometry(0, 10, 600, 60)
        self.Layout_Stack = QtWidgets.QHBoxLayout(self.wgt1)
        self.Label_31 = QtWidgets.QLabel(stack)
        self.Label_31.setText('控制方式:')
        self.CB_SelectControl = QtWidgets.QComboBox(stack)
        self.CB_SelectControl.setMinimumHeight(40)
        self.CB_SelectControl.addItem('None')
        self.Label_32 = QtWidgets.QLabel(stack)
        self.Label_32.setText('电源:')
        self.CB_DCorAC = QtWidgets.QComboBox(stack)
        self.CB_DCorAC.setMinimumHeight(40)
        self.CB_DCorAC.addItem('DC')
        self.CB_DCorAC.addItem('AC')
        self.SB_Voltage = QtWidgets.QDoubleSpinBox(stack)
        self.SB_Voltage.setMinimumHeight(40)
        self.SB_Voltage.setMinimumWidth(80)
        self.Label_33 = QtWidgets.QLabel(stack)
        self.Label_33.setText('V')
        self.BT_Lock = QtWidgets.QPushButton(stack)
        self.BT_Lock.setMinimumHeight(40)
        self.BT_Lock.setText('锁定')
        self.Layout_Stack.addWidget(self.Label_31)
        self.Layout_Stack.addWidget(self.CB_SelectControl)
        self.Layout_Stack.addWidget(self.Label_32)
        self.Layout_Stack.addWidget(self.CB_DCorAC)
        self.Layout_Stack.addWidget(self.SB_Voltage)
        self.Layout_Stack.addWidget(self.Label_33)
        self.Layout_Stack.addWidget(self.BT_Lock)
        self.Layout_Stack.addStretch(0)

        self.wgt2 = QtWidgets.QWidget(stack)
        self.wgt2.setGeometry(0, 80, 600, 60)
        self.Layout_Stack2 = QtWidgets.QHBoxLayout(self.wgt2)
        self.CK_Auto = QtWidgets.QCheckBox('自动')
        self.Label_34 = QtWidgets.QLabel(stack)
        self.Label_34.setText('开阀:')
        self.SB_OpenTime = QtWidgets.QDoubleSpinBox(stack)
        self.SB_OpenTime.setMinimumHeight(40)
        self.SB_OpenTime.setMinimumWidth(60)
        self.Label_35 = QtWidgets.QLabel(stack)
        self.Label_35.setText('关阀:')
        self.SB_CloseTime = QtWidgets.QDoubleSpinBox(stack)
        self.SB_CloseTime.setMinimumHeight(40)
        self.SB_CloseTime.setMinimumWidth(60)
        self.BT_Begin = QtWidgets.QPushButton(stack)
        self.BT_Begin.setMinimumHeight(40)
        self.BT_Begin.setText('开始')
        self.BT_Stop = QtWidgets.QPushButton(stack)
        self.BT_Stop.setMinimumHeight(40)
        self.BT_Stop.setText('停止')
        self.Layout_Stack2.addWidget(self.CK_Auto)
        self.Layout_Stack2.addWidget(self.Label_34)
        self.Layout_Stack2.addWidget(self.SB_OpenTime)
        self.Layout_Stack2.addWidget(self.Label_35)
        self.Layout_Stack2.addWidget(self.SB_CloseTime)
        self.Layout_Stack2.addWidget(self.BT_Begin)
        self.Layout_Stack2.addWidget(self.BT_Stop)
        self.Layout_Stack2.addStretch(0)
        # 按钮初始不可用
        self.BT_Begin.setDisabled(1)
        self.BT_Stop.setDisabled(1)
        self.SB_OpenTime.setDisabled(1)
        self.SB_CloseTime.setDisabled(1)
        # 自动复选框信号连接按钮禁用函数
        self.CK_Auto.clicked.connect(self.AutoControlDisable)



    def stack2Ui(self, stack):

        self.wgt3 = QtWidgets.QWidget(stack)
        self.wgt3.setGeometry(0, 10, 600, 60)
        self.Layout_AdjustPageStack = QtWidgets.QHBoxLayout(self.wgt3)
        self.Label_41 = QtWidgets.QLabel(stack)
        self.Label_41.setText('调节阀输入：')
        self.SB_AdjustValveInput = QtWidgets.QDoubleSpinBox(stack)
        self.SB_AdjustValveInput.setMinimumHeight(40)
        self.SB_AdjustValveInput.setMinimumWidth(60)
        self.Label_42 = QtWidgets.QLabel(stack)
        self.Label_42.setText('mA')
        self.Label_43 = QtWidgets.QLabel(stack)
        self.Label_43.setText('步距:')
        self.CB_StepValve = QtWidgets.QComboBox(stack)
        self.CB_StepValve.setMinimumHeight(40)
        self.CB_StepValve.setMinimumWidth(50)
        self.CB_StepValve.addItem('1.0')
        self.CB_StepValve.addItem('0.1')
        self.CB_StepValve.addItem('10.0')

        self.Label_44 = QtWidgets.QLabel(stack)
        self.Label_44.setText('mA')
        self.Label_45 = QtWidgets.QLabel(stack)
        self.Label_45.setText('调节阀反馈信号：20mA')
        self.Layout_AdjustPageStack.addWidget(self.Label_41)
        self.Layout_AdjustPageStack.addWidget(self.SB_AdjustValveInput)
        self.Layout_AdjustPageStack.addWidget(self.Label_42)
        self.Layout_AdjustPageStack.addStretch(0)
        self.Layout_AdjustPageStack.addWidget(self.Label_43)
        self.Layout_AdjustPageStack.addWidget(self.CB_StepValve)
        self.Layout_AdjustPageStack.addWidget(self.Label_44)
        self.Layout_AdjustPageStack.addStretch(0)
        self.Layout_AdjustPageStack.addWidget(self.Label_45)
        self.Layout_AdjustPageStack.addStretch(0)

        self.Slider_AdjustValveControlSignal = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_AdjustValveControlSignal.setParent(stack)
        self.Slider_AdjustValveControlSignal.move(20, 100)
        self.Slider_AdjustValveControlSignal.resize(200, 20)

        self.Slider_AdjustValveControlSignal.setMinimum(0)
        self.Slider_AdjustValveControlSignal.setMaximum(20)
        self.Slider_AdjustValveControlSignal.setSingleStep(1)
        self.Slider_AdjustValveControlSignal.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider_AdjustValveControlSignal.setTickInterval(1)

        # 滑动条设置调节阀控制信号
        self.Slider_AdjustValveControlSignal.valueChanged.connect(self.AdjustValveControlSignalValveChange)


    def stack3Ui(self, stack):
        self.wgt4 = QtWidgets.QWidget(stack)
        self.wgt4.setGeometry(0, 10, 600, 200)
        self.Layout_BusPageStack = QtWidgets.QGridLayout(self.wgt4)
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


    def AutoControlDisable(self):
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

    def AdjustValveControlSignalValveChange(self):
        self.SB_AdjustValveInput.setValue(float(self.Slider_AdjustValveControlSignal.value()))











