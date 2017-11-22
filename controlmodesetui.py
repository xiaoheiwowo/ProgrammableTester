#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import dialogbutton

import remotecontrolsetui

# 常量
m = 55
n = 35

class Ui_ControlModeSet(QtWidgets.QDialog):
    '''
    控制方式设置窗口，
    '''
    def __init__(self, parent = None):
        super(Ui_ControlModeSet, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
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
        # self.DB_DialogButton.BT_Save1.setFocusPolicy(QtCore.Qt.StrongFocus)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(self.DB_DialogButton)

        Layout_GroupBox = QtWidgets.QHBoxLayout()
        Layout_GroupBox.addWidget(self.TW_ControlModeList)
        Layout_GroupBox.addWidget(self.TabWgt)
        Layout_GroupBox.addWidget(self.GB_Extend)

        Layout_Main = QtWidgets.QVBoxLayout()
        Layout_Main.addLayout(Layout_GroupBox)
        Layout_Main.addLayout(Layout_button)
        self.setLayout(Layout_Main)


    def Init_ControlModeList(self):
        self.TW_ControlModeList = QtWidgets.QTableWidget(self)
        self.TW_ControlModeList.setFixedWidth(200)
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

        # self.GB_WiringDiagram = QtWidgets.QGroupBox(self)
        # self.GB_WiringDiagram.setTitle('接线图')

        self.TabWgt = QtWidgets.QTabWidget(self)
        self.Tab_ON = QtWidgets.QWidget(self.TabWgt)
        self.Tab_OFF = QtWidgets.QWidget(self.TabWgt)
        self.Tab_STOP = QtWidgets.QWidget(self.TabWgt)
        self.Tab_M3 = QtWidgets.QWidget(self.TabWgt)
        self.Tab_M4 = QtWidgets.QWidget(self.TabWgt)
        self.TabWgt.addTab(self.Tab_ON, 'ON')
        self.TabWgt.addTab(self.Tab_OFF, 'OFF')
        self.TabWgt.addTab(self.Tab_STOP, 'STOP')
        self.TabWgt.addTab(self.Tab_M3, 'M3')
        self.TabWgt.addTab(self.Tab_M4, 'M4')

        # Layout_Tab = QtWidgets.QHBoxLayout(self.GB_WiringDiagram)
        # Layout_Tab.addWidget(self.TabWgt)

    # 标签页
        self.TON = ControlModeWiring(self.Tab_ON)
        self.TOFF = ControlModeWiring(self.Tab_OFF)
        self.TSTOP = ControlModeWiring(self.Tab_STOP)
        self.TM3 = ControlModeWiring(self.Tab_M3)
        self.TM4 = ControlModeWiring(self.Tab_M4)

    def Init_Extend(self):
        self.GB_Extend = QtWidgets.QGroupBox(self)
        self.GB_Extend.setMinimumWidth(200)
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

        self.CB_ControlMode2.setDisabled(True)
        self.CB_ActionMode.setDisabled(True)
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
        self.BT_Advanced.setFocusPolicy(QtCore.Qt.NoFocus)
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

        self.BT_Advanced.setDisabled(True)
        self.CB_BaudRate.setDisabled(True)
        self.CB_BusProtocol.setDisabled(True)
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
        self.CK_isAdjustValve.clicked.connect(self.setAdjustValve)
        self.CK_isBusValve.clicked.connect(self.setBusValve)
        self.CK_isBP5.clicked.connect(self.setBP5)

    def showRemoteControlForm(self):
        self.remotecontrolset = PT_RemoteControlSet()
        self.remotecontrolset.show()

    def setAdjustValve(self):
        if self.CK_isAdjustValve.isChecked():
            self.CB_ControlMode2.setDisabled(False)
            self.CB_ActionMode.setDisabled(False)

            self.CK_isBusValve.setChecked(False)
            self.CK_isBP5.setChecked(False)
            self.setBusValve()
        else:
            self.CB_ControlMode2.setDisabled(True)
            self.CB_ActionMode.setDisabled(True)

    def setBusValve(self):
        if self.CK_isBusValve.isChecked():
            self.BT_Advanced.setDisabled(False)
            self.CB_BusProtocol.setDisabled(False)
            self.CB_BaudRate.setDisabled(False)

            self.CK_isAdjustValve.setChecked(False)
            self.setAdjustValve()
            self.CK_isBP5.setChecked(False)
        else:
            self.BT_Advanced.setDisabled(True)
            self.CB_BusProtocol.setDisabled(True)
            self.CB_BaudRate.setDisabled(True)

    def setBP5(self):
        if self.CK_isBP5.isChecked():
            self.CK_isAdjustValve.setChecked(False)
            self.CK_isBusValve.setChecked(False)
            self.setAdjustValve()
            self.setBusValve()
        pass

class PT_RemoteControlSet(remotecontrolsetui.Ui_RemoteControlSet):
    def __init__(self, parent=None):
        super(PT_RemoteControlSet, self).__init__(parent)

class DrawWiring(QtWidgets.QWidget):
    def __init__(self, Widget, x, y, parent=None):
        super(DrawWiring, self).__init__(parent)
        self.resize(1000, 500)
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

class ControlModeWiring(QtWidgets.QWidget):
    def __init__(self, wgt, parent = None):
        super(ControlModeWiring, self).__init__(parent)

        self.SA = QtWidgets.QScrollArea(wgt)
        Layout_tab = QtWidgets.QHBoxLayout(wgt)
        Layout_tab.addWidget(self.SA)
        Layout_tab.setContentsMargins(2, 2, 2, 2)
        Wgt = QtWidgets.QWidget(self.SA)
        Wgt.resize(950, 400)
        self.SA.setWidget(Wgt)
        self.WgtDraw = QtWidgets.QWidget(Wgt)
        self.WgtDraw.setGeometry(55, 40, 950, 400)
        self.drawWiring()

        # 变量
        self.PressedXNum = None
        self.PressedYNum = None
        self.XMark = False
        self.YMark = False
        self.wiringShow = []
        for i in range(160):
            self.wiringShow.append(False)

        self.BT_x = []
        self.BT_y = []
        # 生成X按钮
        for i in range(16):
            self.BT_x.append(QtWidgets.QPushButton(Wgt))
            self.BT_x[i].setText('X0' + (str(hex(i))[2]).upper())
            self.BT_x[i].setGeometry(55 * i + 60, 10, 50, 30)
            self.BT_x[i].setCheckable(True)
            self.BT_x[i].setFocusPolicy(QtCore.Qt.NoFocus)

        # 生成Y按钮
        for j in range(10):
            self.BT_y.append(QtWidgets.QPushButton(Wgt))
            self.BT_y[j].setText('Y0' + str(j))
            self.BT_y[j].setGeometry(5, 35 * j + 45, 50, 30)
            self.BT_y[j].setCheckable(True)
            self.BT_y[j].setFocusPolicy(QtCore.Qt.NoFocus)

        # 信号
        self.BT_x[0].clicked.connect(lambda: self.XisPressed(0))
        self.BT_x[1].clicked.connect(lambda: self.XisPressed(1))
        self.BT_x[2].clicked.connect(lambda: self.XisPressed(2))
        self.BT_x[3].clicked.connect(lambda: self.XisPressed(3))
        self.BT_x[4].clicked.connect(lambda: self.XisPressed(4))
        self.BT_x[5].clicked.connect(lambda: self.XisPressed(5))
        self.BT_x[6].clicked.connect(lambda: self.XisPressed(6))
        self.BT_x[7].clicked.connect(lambda: self.XisPressed(7))
        self.BT_x[8].clicked.connect(lambda: self.XisPressed(8))
        self.BT_x[9].clicked.connect(lambda: self.XisPressed(9))
        self.BT_x[10].clicked.connect(lambda: self.XisPressed(10))
        self.BT_x[11].clicked.connect(lambda: self.XisPressed(11))
        self.BT_x[12].clicked.connect(lambda: self.XisPressed(12))
        self.BT_x[13].clicked.connect(lambda: self.XisPressed(13))
        self.BT_x[14].clicked.connect(lambda: self.XisPressed(14))
        self.BT_x[15].clicked.connect(lambda: self.XisPressed(15))

        self.BT_y[0].clicked.connect(lambda: self.YisPressed(0))
        self.BT_y[1].clicked.connect(lambda: self.YisPressed(1))
        self.BT_y[2].clicked.connect(lambda: self.YisPressed(2))
        self.BT_y[3].clicked.connect(lambda: self.YisPressed(3))
        self.BT_y[4].clicked.connect(lambda: self.YisPressed(4))
        self.BT_y[5].clicked.connect(lambda: self.YisPressed(5))
        self.BT_y[6].clicked.connect(lambda: self.YisPressed(6))
        self.BT_y[7].clicked.connect(lambda: self.YisPressed(7))
        self.BT_y[8].clicked.connect(lambda: self.YisPressed(8))
        self.BT_y[9].clicked.connect(lambda: self.YisPressed(9))

        # 使用QSignalMapper
        # self.BT_x[0].clicked.connect(self.XMapper.map)
        # self.BT_y[0].clicked.connect(self.YMapper.map)
        # self.XMapper = QtCore.QSignalMapper()
        # self.YMapper = QtCore.QSignalMapper()
        # self.XMapper.setMapping(self.BT_x[1], self.BT_x[1].text())
        # self.XMapper.mapped(str).connect(self.XisPressed(str))

    def XisPressed(self, int):
        print('X', int)
        self.PressedXNum = int
        self.XMark = True
        for i in range(16):
            if i != int:
                self.BT_x[i].setChecked(False)
        # if self.YMark:
        #     if not self.wiringShow[self.PressedXNum * 10 + self.PressedYNum]:
        #         self.wiring[self.PressedXNum * 10 + self.PressedYNum].show()
        #         self.wiringShowMark[self.PressedXNum * 10 + self.PressedYNum] = True
        #     else:
        #         self.wiring[self.PressedXNum * 10 + self.PressedYNum].hide()
        #         self.wiringShow[self.PressedXNum * 10 + self.PressedYNum] = False
        #
        #     self.XMark = False
        #     self.YMark = False
        #     self.BT_x[self.PressedXNum].setChecked(False)
        #     self.BT_y[self.PressedYNum].setChecked(False)
        #     self.PressedXNum = None
        #     self.PressedYNum = None

    def YisPressed(self, int):
        print('Y', int)
        self.YMark = True
        self.PressedYNum = int
        for i in range(10):
            if i != int:
                self.BT_y[i].setChecked(False)

        if self.XMark:
            if self.wiringShow[self.PressedXNum * 10 + self.PressedYNum]:
                self.wiring[self.PressedXNum * 10 + self.PressedYNum].hide()
                self.wiringShow[self.PressedXNum * 10 + self.PressedYNum] = False
            else:
                self.wiring[self.PressedXNum * 10 + self.PressedYNum].show()
                self.wiringShow[self.PressedXNum * 10 + self.PressedYNum] = True
            self.BT_x[self.PressedXNum].setChecked(False)
            self.BT_y[self.PressedYNum].setChecked(False)
            self.PressedXNum = None
            self.PressedYNum = None
            self.XMark = False
            self.YMark = False

    def drawWiring(self):
        self.wiring = []
        for i in range(16):
            for j in range(10):
                self.wiring.append(DrawWiring(self.WgtDraw, 30 + i * m, 20 + j * n))
                # self.wiring[i * 10 + j].show()
                self.wiring[i * 10 + j].hide()