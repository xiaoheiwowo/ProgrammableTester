#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import dialogbutton

import remotecontrolsetui

class Ui_ControlModeSet(QtWidgets.QDialog):
    '''
    控制方式设置窗口，
    '''
    def __init__(self, parent = None):
        super(Ui_ControlModeSet, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 550)
        self.setWindowTitle('控制方式设置')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.Init_ControlModeList()
        self.Init_WiringDiagram()
        self.Init_Extend()

        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.setFixedSize(300, 50)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(self.DB_DialogButton)

        Layout_GroupBox = QtWidgets.QHBoxLayout()
        Layout_GroupBox.addWidget(self.TW_ControlModeList)
        Layout_GroupBox.addWidget(self.GB_WiringDiagram)
        Layout_GroupBox.addWidget(self.GB_Extend)
        Layout_GroupBox.addStretch(1)

        Layout_Main = QtWidgets.QVBoxLayout()
        Layout_Main.addLayout(Layout_GroupBox)
        Layout_Main.addLayout(Layout_button)
        self.setLayout(Layout_Main)
        # 变量
        self.PressedXNum = None
        self.PressedYNum = None

    def Init_ControlModeList(self):
        self.TW_ControlModeList = QtWidgets.QTableWidget(self)
        self.TW_ControlModeList.setFixedSize(200, 450)
        self.TW_ControlModeList.setRowCount(20)
        self.TW_ControlModeList.setColumnCount(2)
        self.TW_ControlModeList.setHorizontalHeaderLabels(['控制方式', '电压'])
        self.TW_ControlModeList.setColumnWidth(0, 89)
        self.TW_ControlModeList.setColumnWidth(1, 60)
        # self.TW_ControlModeList.setRowHeight(0, 30)

        for i in range(20):
            a = QtWidgets.QComboBox()
            a.addItem('DC')
            a.addItem('AC')
            # a.setStyleSheet('QComboBox{margin:3px};')
            self.TW_ControlModeList.setCellWidget(i, 1, a)

    def Init_WiringDiagram(self):

        self.GB_WiringDiagram = QtWidgets.QGroupBox(self)
        self.GB_WiringDiagram.setFixedSize(600, 450)
        self.GB_WiringDiagram.setTitle('接线图')

        TabWgt = QtWidgets.QTabWidget(self.GB_WiringDiagram)
        TabWgt.setGeometry(0, 20, 600, 430)

        self.Tab_ON = QtWidgets.QWidget(TabWgt)
        self.Tab_OFF = QtWidgets.QWidget(TabWgt)
        self.Tab_STOP = QtWidgets.QWidget(TabWgt)
        self.Tab_M3 = QtWidgets.QWidget(TabWgt)
        self.Tab_M4 = QtWidgets.QWidget(TabWgt)
        TabWgt.addTab(self.Tab_ON, 'ON')
        TabWgt.addTab(self.Tab_OFF, 'OFF')
        TabWgt.addTab(self.Tab_STOP, 'STOP')
        TabWgt.addTab(self.Tab_M3, 'M3')
        TabWgt.addTab(self.Tab_M4, 'M4')

    # ON标签页
        SA_ON = QtWidgets.QScrollArea(self.Tab_ON)
        SA_ON.setGeometry(2, 1, 590, 400)
        WgtON = QtWidgets.QWidget(SA_ON)
        WgtON.setMinimumSize(950, 400)
        SA_ON.setWidget(WgtON)

        self.BT_ONx = []
        self.BT_ONy = []
        # 生成X按钮
        for i in range(16):
            self.BT_ONx.append(QtWidgets.QPushButton(WgtON))
            self.BT_ONx[i].setText('X0' + (str(hex(i))[2]).upper())
            self.BT_ONx[i].setGeometry(55 * i + 60, 10, 50, 30)
            self.BT_ONx[i].setCheckable(True)
            self.BT_ONx[i].setFocusPolicy(QtCore.Qt.NoFocus)
        # 生成Y按钮
        for j in range(10):
            self.BT_ONy.append(QtWidgets.QPushButton(WgtON))
            self.BT_ONy[j].setText('Y0' + str(j))
            self.BT_ONy[j].setGeometry(5, 35 * j + 45, 50, 30)
            self.BT_ONy[j].setCheckable(True)
            self.BT_ONy[j].setFocusPolicy(QtCore.Qt.NoFocus)

        # self.DB_DialogButton.BT_OK1.isChecked()

        self.BT_ONx[0].clicked.connect(self.X00isPressed)
        self.BT_ONy[0].clicked.connect(self.Y00isPressed)
        # 画连线
        self.WgtDraw = QtWidgets.QWidget(WgtON)
        self.WgtDraw.setGeometry(55, 40, 550, 400)

        self.m = 55
        self.n = 35

        # self.Wiring = DrawWiring(self.WgtDraw, 30 + 0 * self.m, 20 + 0 * self.n)

    def X00isPressed(self):
        for i in range(16):
            if i != 0:
                self.BT_ONx[i].setChecked(False)
        for j in range(10):
            self.BT_ONy[j].setChecked(False)
        if self.BT_ONx[0].isChecked():
            self.PressedXNum = 0
        else:
            self.PressedXNum = None
            print('x0ispressed', self.PressedXNum)
            # self.Wiring = DrawWiring(self.WgtDraw, 30 + self.PressedXNum * self.m, 20 + 1 * self.n)
            # self.Wiring.show()

    def Y00isPressed(self):
        for i in range(10):
            if i != 0:
                self.BT_ONy[i].setChecked(False)
        for j in range(16):
            self.BT_ONx[j].setChecked(False)
        if self.BT_ONy[0].isChecked():
            self.PressedYNum = 0
            print('y0ispressed', self.PressedYNum)
            if self.PressedXNum == None:
                pass
            else:
                self.Wiring = DrawWiring(self.WgtDraw, 30 + self.PressedXNum * self.m, 20 + self.PressedYNum * self.n)
                self.Wiring.show()

                self.PressedXNum = None
                self.PressedYNum = None

    def Init_Extend(self):
        self.GB_Extend = QtWidgets.QGroupBox(self)
        self.GB_Extend.setFixedSize(200, 450)
        self.GB_Extend.setTitle('附加参数')
        # 调节阀部分
        self.Layout_Extend = QtWidgets.QVBoxLayout(self.GB_Extend)
        self.CK_isAdjustValve = QtWidgets.QCheckBox(self.GB_Extend)
        self.CK_isAdjustValve.setText('是调节阀')
        self.CK_isAdjustValve.setMinimumHeight(40)

        self.Layout_ControlMode2 = QtWidgets.QHBoxLayout()
        self.Label_a11 = QtWidgets.QLabel('控制方式:')
        self.CB_ControlMode2 = QtWidgets.QComboBox()
        self.CB_ControlMode2.addItem('0~20mA')
        self.CB_ControlMode2.setMinimumHeight(40)
        self.Layout_ControlMode2.addWidget(self.Label_a11)
        self.Layout_ControlMode2.addWidget(self.CB_ControlMode2)

        self.Layout_ActionMode = QtWidgets.QHBoxLayout()
        self.Label_a12 = QtWidgets.QLabel('作用方式:')
        self.CB_ActionMode = QtWidgets.QComboBox()
        self.CB_ActionMode.setMinimumHeight(40)
        self.CB_ActionMode.addItem('正作用')
        self.CB_ActionMode.addItem('反作用')
        self.Layout_ActionMode.addWidget(self.Label_a12)
        self.Layout_ActionMode.addWidget(self.CB_ActionMode)
        # 分隔线
        self.line1 = QtWidgets.QFrame()
        self.line1.resize(200, 10)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        # 总线阀部分
        self.Layout_isBusValve = QtWidgets.QHBoxLayout()
        self.CK_isBusValve = QtWidgets.QCheckBox(self.GB_Extend)
        self.CK_isBusValve.setText('是总线阀')
        self.BT_Advanced = QtWidgets.QPushButton('高级>>')
        self.BT_Advanced.setMinimumHeight(40)
        self.Layout_isBusValve.addWidget(self.CK_isBusValve)
        self.Layout_isBusValve.addWidget(self.BT_Advanced)

        self.Layout_BusProtocol = QtWidgets.QHBoxLayout()
        self.Label_a13 = QtWidgets.QLabel('总线协议:')
        self.CB_BusProtocol = QtWidgets.QComboBox()
        self.CB_BusProtocol.addItem('ModBus')
        self.CB_BusProtocol.setMinimumHeight(40)
        self.Layout_BusProtocol.addWidget(self.Label_a13)
        self.Layout_BusProtocol.addWidget(self.CB_BusProtocol)

        self.Layout_BaudRate = QtWidgets.QHBoxLayout()
        self.Label_a14 = QtWidgets.QLabel('波特率:')
        self.CB_BaudRate = QtWidgets.QComboBox()
        self.CB_BaudRate.addItem('9600')
        self.CB_BaudRate.setMinimumHeight(40)
        self.Layout_BaudRate.addWidget(self.Label_a14)
        self.Layout_BaudRate.addWidget(self.CB_BaudRate)
        # 分隔线
        self.line2 = QtWidgets.QFrame()
        self.line2.resize(200, 10)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        # BP5部分
        self.CK_isBP5 = QtWidgets.QCheckBox('由测试仪控制停阀')
        self.Label_a15 = QtWidgets.QLabel('本测试仪感知到位反馈信号后自动停阀(BP5)')
        # 使Label自动换行
        self.Label_a15.resize(150, 200)
        self.Label_a15.setWordWrap(True)
        self.Label_a15.setAlignment(QtCore.Qt.AlignTop)

        # 附加参数布局
        self.Layout_Extend.addWidget(self.CK_isAdjustValve)
        self.Layout_Extend.addLayout(self.Layout_ControlMode2)
        self.Layout_Extend.addLayout(self.Layout_ActionMode)
        self.Layout_Extend.addWidget(self.line1)
        self.Layout_Extend.addLayout(self.Layout_isBusValve)
        self.Layout_Extend.addLayout(self.Layout_BusProtocol)
        self.Layout_Extend.addLayout(self.Layout_BaudRate)
        self.Layout_Extend.addWidget(self.line2)
        self.Layout_Extend.addWidget(self.CK_isBP5)
        self.Layout_Extend.addWidget(self.Label_a15)
        # 信号
        self.BT_Advanced.clicked.connect(self.showRemoteControlForm)

    def showRemoteControlForm(self):
        self.remotecontrolset = PT_RemoteControlSet()
        self.remotecontrolset.show()

class PT_RemoteControlSet(remotecontrolsetui.Ui_RemoteControlSet):
    def __init__(self, parent=None):
        super(PT_RemoteControlSet, self).__init__(parent)

class DrawWiring(QtWidgets.QWidget):
    def __init__(self, Widget, x, y, parent=None):
        super(DrawWiring, self).__init__(parent)

        # self.Canvas = Widget
        self.x_wiring = x
        self.y_wiring = y
        self.setParent(Widget)

    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWiring(qp)
        qp.end()

    def drawWiring(self, qp):
        pen = QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.red)
        qp.drawLine(self.x_wiring, 0, self.x_wiring, self.y_wiring)
        qp.drawLine(0, self.y_wiring, self.x_wiring, self.y_wiring)
        qp.drawEllipse(self.x_wiring-3, self.y_wiring-3, 6, 6,)

    def clearAll(self):

        pass