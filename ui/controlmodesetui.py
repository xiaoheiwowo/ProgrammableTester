# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle

from PyQt5 import QtCore, QtGui, QtWidgets

from public.datacache import SoftwareData as sw

from ui import remotecontrolsetui, dialogbutton

import images.images_rc


def debug_print(*string):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        # print("DEBUG: " + string)


class Ui_ControlModeSet(QtWidgets.QDialog):
    """
    控制方式设置窗口，
    """
    confirm = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Ui_ControlModeSet, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('控制方式设置')
        self.setWindowIcon(QtGui.QIcon(":/logo.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.readfile()
        self.Init_ControlModeList()
        self.Init_WiringDiagram()
        self.Init_Extend()

        self.load_control_list()

        # 保存、确定、取消按钮
        self.bt_save = QtWidgets.QPushButton()
        self.bt_cancel = QtWidgets.QPushButton()
        self.bt_save.setText('保存')
        self.bt_cancel.setText('退出')
        self.bt_save.clicked.connect(self.save_control_mode)
        self.bt_cancel.clicked.connect(self.reject)
        wgt = QtWidgets.QWidget()
        wgt.setFixedSize(100, 50)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(wgt)
        Layout_button.addWidget(self.bt_save)
        Layout_button.addWidget(self.bt_cancel)

        Layout_GroupBox = QtWidgets.QHBoxLayout()
        Layout_GroupBox.addLayout(self.Layout_ControlList)
        Layout_GroupBox.addWidget(self.TabWgt)
        Layout_GroupBox.addWidget(self.GB_Extend)

        Layout_Main = QtWidgets.QVBoxLayout()
        Layout_Main.addLayout(Layout_GroupBox)
        Layout_Main.addLayout(Layout_button)
        self.setLayout(Layout_Main)

    def Init_ControlModeList(self):
        """

        :return:
        """
        self.TW_ControlModeList = QtWidgets.QTableWidget(self)
        self.TW_ControlModeList.setFixedWidth(200)
        self.TW_ControlModeList.setRowCount(len(sw.control_mode) + 1)
        self.TW_ControlModeList.setColumnCount(3)
        self.TW_ControlModeList.setHorizontalHeaderLabels(['', '控制方式', '电压'])
        self.TW_ControlModeList.setColumnWidth(0, 30)
        self.TW_ControlModeList.setColumnWidth(1, 70)
        self.TW_ControlModeList.setColumnWidth(2, 60)
        # self.TW_ControlModeList.horizontalHeader().setDisabled(True)
        self.TW_ControlModeList.horizontalHeader().setSectionResizeMode(2)
        self.TW_ControlModeList.verticalHeader().setVisible(False)
        self.TW_ControlModeList.setSelectionBehavior(1)

        self.update_control_list()

        self.BT_NewControl = QtWidgets.QPushButton('新建')
        self.BT_DelateControl = QtWidgets.QPushButton('删除')
        Layout_New = QtWidgets.QHBoxLayout()
        Layout_New.addWidget(self.BT_NewControl)
        Layout_New.addWidget(self.BT_DelateControl)

        self.Layout_ControlList = QtWidgets.QVBoxLayout()
        self.Layout_ControlList.addWidget(self.TW_ControlModeList)
        self.Layout_ControlList.addLayout(Layout_New)

        self.BT_NewControl.clicked.connect(self.new_control_mode)
        self.BT_DelateControl.clicked.connect(self.delate_control_mode)
        self.TW_ControlModeList.itemClicked.connect(self.load_wiring_ex)

    def Init_WiringDiagram(self):
        """

        :return:
        """

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

        self.TabWgt.tabBarClicked.connect(self.change_page)

    def Init_Extend(self):
        """

        :return:
        """
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
        self.CB_ControlMode2.addItem('None')
        self.CB_ControlMode2.addItem('0~20mA')
        self.CB_ControlMode2.addItem('4~20mA')
        self.CB_ControlMode2.addItem('0~5V')
        self.CB_ControlMode2.addItem('1~5V')
        self.CB_ControlMode2.addItem('0~10V')
        self.CB_ControlMode2.addItem('2~10V')
        self.CB_ControlMode2.setMinimumHeight(40)
        self.Layout_ControlMode2.addWidget(self.Label_a11)
        self.Layout_ControlMode2.addWidget(self.CB_ControlMode2)

        self.Layout_ActionMode = QtWidgets.QHBoxLayout()
        self.Label_a12 = QtWidgets.QLabel('作用方式:')
        self.CB_ActionMode = QtWidgets.QComboBox()
        self.CB_ActionMode.setMinimumHeight(40)
        self.CB_ActionMode.addItem('None')
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
        self.CB_BusProtocol.addItem('None')
        self.CB_BusProtocol.addItem('RS485')
        self.CB_BusProtocol.addItem('ModBus')
        self.CB_BusProtocol.addItem('Other')
        self.CB_BusProtocol.setMinimumHeight(40)
        self.Layout_BusProtocol.addWidget(self.Label_a13)
        self.Layout_BusProtocol.addWidget(self.CB_BusProtocol)

        self.Layout_BaudRate = QtWidgets.QHBoxLayout()
        self.Label_a14 = QtWidgets.QLabel('波特率:')
        self.CB_BaudRate = QtWidgets.QComboBox()
        self.CB_BaudRate.addItem('None')
        self.CB_BaudRate.addItem('1200')
        self.CB_BaudRate.addItem('2400')
        self.CB_BaudRate.addItem('4800')
        self.CB_BaudRate.addItem('9600')
        self.CB_BaudRate.addItem('19200')
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
        # self.BT_Advanced.clicked.connect(self.showRemoteControlForm)
        self.CK_isAdjustValve.clicked.connect(self.setAdjustValve)
        self.CK_isBusValve.clicked.connect(self.setBusValve)
        self.CK_isBP5.clicked.connect(self.setBP5)

    def readfile(self):
        """

        :return:
        """
        a = [{'NAME': 'BD3', 'POWER': 2, 'ON': [0, 1, 12], 'OFF': [0, 12], 'STOP': [], 'M3': [], 'M4': [],
              'SPECIAL': 0, 'SIGNAL': 0, 'EFFECT': 0, 'PROTOCOL': 0, 'BAUDRATE': 0},
             {'NAME': 'BD3S', 'POWER': 1, 'ON': [20, 21, 32, 43, 54, 65], 'OFF': [20, 32, 43, 54, 65], 'STOP': [],
              'M3': [], 'M4': [], 'SPECIAL': 0, 'SIGNAL': 0, 'EFFECT': 0, 'PROTOCOL': 0, 'BAUDRATE': 0},
             {'NAME': 'B3', 'POWER': 1, 'ON': [0, 11], 'OFF': [0, 12], 'STOP': [], 'M3': [], 'M4': [],
              'SPECIAL': 0, 'SIGNAL': 0, 'EFFECT': 0, 'PROTOCOL': 0, 'BAUDRATE': 0},
             {'NAME': '0~20mA', 'POWER': 1, 'ON': [20, 32, 81, 73, 92], 'OFF': [], 'STOP': [], 'M3': [],
              'M4': [], 'SPECIAL': 1, 'SIGNAL': 1, 'EFFECT': 1, 'PROTOCOL': 0, 'BAUDRATE': 0},
             {'NAME': 'RS485', 'POWER': 1, 'ON': [20, 31, 102, 113], 'OFF': [], 'STOP': [], 'M3': [], 'M4': [],
              'SPECIAL': 2, 'SIGNAL': 0, 'EFFECT': 0, 'PROTOCOL': 1, 'BAUDRATE': 4},
             {'NAME': 'BP5', 'POWER': 1, 'ON': [23, 34, 40, 51, 62], 'OFF': [24, 33, 40, 51, 62], 'STOP': [],
              'M3': [], 'M4': [], 'SPECIAL': 3, 'SIGNAL': 0, 'EFFECT': 0, 'PROTOCOL': 0, 'BAUDRATE': 0}
             ]
        '''
        键值说明：
        ID：int 序号
        NAME: str 控制方式名称 
        POWER: int 电源类型 0:None 1:DC 2:AC
        ON: list 继电器接通列表
        OFF: list 继电器接通列表
        STOP: list 继电器接通列表
        M3: list 继电器接通列表
        M4: list 继电器接通列表
        SPECIAL: int 0: 普通  1: 调节阀  2: 总线阀  3: BP5
        SIGNAL: 调节阀控制信号6种 0 None, 1 0~20mA, 2 4~20mA, 3 0~5V, 4 1~5V, 5 0~10V, 6 2~10V
        EFFECT: 作用方式，0: None  1: 正作用  2: 反作用
        PROTOCOL: 总线协议 0：None 1: RS485  2: ModBus
        BAUDRATE: 波特率  1200~19200
        ...
        '''
        # with open('pkl/controlmode.pkl', 'wb') as f:
        #     f.write(pickle.dumps(a))

        with open('pkl/controlmode.pkl', 'rb') as f:
            sw.control_mode = pickle.loads(f.read())

    def load_control_list(self):
        """

        :return:
        """
        for i in range(len(sw.control_mode)):
            item0 = QtWidgets.QTableWidgetItem(sw.control_mode[i]['NAME'])
            self.TW_ControlModeList.setItem(i, 1, item0)
            self.CB_VList[i].setCurrentIndex(sw.control_mode[i]['POWER'])

    def load_wiring_ex(self, item):
        """

        :param item:
        :return:
        """
        sw.select_line = item.row()
        for m in range(160):
            self.TON.wiring[m].hide()
            self.TOFF.wiring[m].hide()
            self.TSTOP.wiring[m].hide()
            self.TM3.wiring[m].hide()
            self.TM4.wiring[m].hide()

        for n in range(len(sw.control_mode)):
            self.CK_VList[n].setChecked(False)

        self.CK_VList[item.row()].setChecked(True)
        data = sw.control_mode[item.row()]
        for j in data['ON']:
            self.TON.one_wiring_show(j)
        for j in data['OFF']:
            self.TOFF.one_wiring_show(j)
        for j in data['STOP']:
            self.TSTOP.one_wiring_show(j)
        for j in data['M3']:
            self.TM3.one_wiring_show(j)
        for j in data['M4']:
            self.TM4.one_wiring_show(j)
        if data['SPECIAL'] == 0:
            self.CK_isAdjustValve.setChecked(False)
            self.CK_isBusValve.setChecked(False)
            self.CK_isBP5.setChecked(False)
            self.setAdjustValve()
            self.setBusValve()
        elif data['SPECIAL'] == 1:
            self.CK_isAdjustValve.setChecked(True)
            self.setAdjustValve()
            self.CB_ControlMode2.setCurrentIndex(data['SIGNAL'])
            self.CB_ActionMode.setCurrentIndex(data['EFFECT'])
        elif data['SPECIAL'] == 2:
            self.CK_isBusValve.setChecked(True)
            self.setBusValve()
            self.CB_BusProtocol.setCurrentIndex(data['PROTOCOL'])
            self.CB_BaudRate.setCurrentIndex(data['BAUDRATE'])
        elif data['SPECIAL'] == 3:
            self.CK_isBP5.setChecked(True)
            self.setBP5()
        else:
            pass

    def change_page(self, page=0):
        """

        :param page:
        :return:
        """
        # print(page)
        pass

    def update_control_list(self):
        """

        :return:
        """
        # rowcount = len(gv.control_mode) - 1
        self.TW_ControlModeList.setRowCount(0)
        self.TW_ControlModeList.setRowCount(len(sw.control_mode) + 1)
        self.CB_VList = []
        self.CK_VList = []
        for i in range(len(sw.control_mode)):
            self.CK_VList.append(QtWidgets.QCheckBox())
            self.CK_VList[i].setDisabled(True)
            self.CK_VList[i].setStyleSheet('QCheckBox{margin:6px}')
            self.TW_ControlModeList.setCellWidget(i, 0, self.CK_VList[i])

            self.CB_VList.append(QtWidgets.QComboBox())
            self.CB_VList[i].addItem('None')
            self.CB_VList[i].addItem('DC')
            self.CB_VList[i].addItem('AC')
            self.CB_VList[i].setStyleSheet('QComboBox{margin:3px}')
            self.TW_ControlModeList.setCellWidget(i, 2, self.CB_VList[i])

    def new_control_mode(self):
        """

        :return:
        """
        text, ok = QtWidgets.QInputDialog.getText(self, '新建控制方式', '输入控制方式名称：')
        if ok:
            # 赋值语句不改变引用，不会创建新的对象，此处需调用copy函数生成一个新的对象，否则会导致第二次改动上一次的dict
            newcontrol = sw.ControlForm.copy()
            newcontrol['NAME'] = str(text)
            sw.control_mode.append(newcontrol)
        self.update_control_list()
        self.load_control_list()

    def delate_control_mode(self):
        """

        :return:
        """
        if sw.select_line:
            del sw.control_mode[sw.select_line]
            del self.CB_VList
            del self.CK_VList
        self.update_control_list()
        self.load_control_list()
        debug_print('delate')

    def save_control_mode(self):
        """

        :return:
        """
        if sw.select_line:
            wiringON = []
            wiringOFF = []
            wiringSTOP = []
            wiringM3 = []
            wiringM4 = []
            for i in range(160):
                if self.TON.wiringShow[i]:
                    wiringON.append(i)
                if self.TOFF.wiringShow[i]:
                    wiringOFF.append(i)
                if self.TSTOP.wiringShow[i]:
                    wiringSTOP.append(i)
                if self.TM3.wiringShow[i]:
                    wiringM3.append(i)
                if self.TM4.wiringShow[i]:
                    wiringM4.append(i)
            sw.control_mode[sw.select_line]['ON'] = wiringON.copy()
            sw.control_mode[sw.select_line]['OFF'] = wiringOFF.copy()
            sw.control_mode[sw.select_line]['STOP'] = wiringSTOP.copy()
            sw.control_mode[sw.select_line]['M3'] = wiringM3.copy()
            sw.control_mode[sw.select_line]['M4'] = wiringM4.copy()
            sw.control_mode[sw.select_line]['POWER'] = self.CB_VList[sw.select_line].currentIndex()
            sw.control_mode[sw.select_line]['NAME'] = self.TW_ControlModeList.item(sw.select_line, 1).text()
            if self.CK_isAdjustValve.isChecked():
                sw.control_mode[sw.select_line]['SPECIAL'] = 1
                sw.control_mode[sw.select_line]['SIGNAL'] = self.CB_ControlMode2.currentIndex()
                sw.control_mode[sw.select_line]['EFFECT'] = self.CB_ActionMode.currentIndex()
                sw.control_mode[sw.select_line]['PROTOCOL'] = None
                sw.control_mode[sw.select_line]['BAUDRATE'] = None
            elif self.CK_isBusValve.isChecked():
                sw.control_mode[sw.select_line]['SPECIAL'] = 2
                sw.control_mode[sw.select_line]['PROTOCOL'] = self.CB_BusProtocol.currentIndex()
                sw.control_mode[sw.select_line]['BAUDRATE'] = self.CB_BaudRate.currentIndex()
                sw.control_mode[sw.select_line]['SIGNAL'] = None
                sw.control_mode[sw.select_line]['EFFECT'] = None
            elif self.CK_isBP5.isChecked():
                sw.control_mode[sw.select_line]['SPECIAL'] = 3
            else:
                sw.control_mode[sw.select_line]['SPECIAL'] = 0

            with open('pkl/controlmode.pkl', 'wb') as f:
                f.write(pickle.dumps(sw.control_mode))

            self.confirm.emit()
            debug_print('save')

    def save_and_close(self):
        """

        :return:
        """
        debug_print('save and close')
        # self.save_control_mode()
        self.close()

    # def showRemoteControlForm(self):
    #     """
    #
    #     :return:
    #     """
    #     self.remotecontrolset = PT_RemoteControlSet()
    #     self.remotecontrolset.show()

    def setAdjustValve(self):
        """

        :return:
        """
        if self.CK_isAdjustValve.isChecked():
            self.CB_ControlMode2.setDisabled(False)
            self.CB_ActionMode.setDisabled(False)

            self.CK_isBusValve.setChecked(False)
            self.CK_isBP5.setChecked(False)
            self.setBusValve()
        else:
            self.CB_ControlMode2.setCurrentIndex(0)
            self.CB_ControlMode2.setDisabled(True)
            self.CB_ActionMode.setCurrentIndex(0)
            self.CB_ActionMode.setDisabled(True)

    def setBusValve(self):
        """

        :return:
        """
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
            self.CB_BusProtocol.setCurrentIndex(0)
            self.CB_BaudRate.setDisabled(True)
            self.CB_BaudRate.setCurrentIndex(0)

    def setBP5(self):
        """

        :return:
        """
        if self.CK_isBP5.isChecked():
            self.CK_isAdjustValve.setChecked(False)
            self.CK_isBusValve.setChecked(False)
            self.setAdjustValve()
            self.setBusValve()
        pass


# class PT_RemoteControlSet(remotecontrolsetui.Ui_RemoteControlSet):
#     def __init__(self, parent=None):
#         super(PT_RemoteControlSet, self).__init__(parent)


class DrawWiring(QtWidgets.QWidget):
    """
    绘制连线
    """

    def __init__(self, widget, x, y, parent=None):
        super(DrawWiring, self).__init__(parent)
        self.resize(1000, 500)
        # self.Canvas = Widget
        self.x_wiring = x
        self.y_wiring = y
        self.setParent(widget)

    def paintEvent(self, QPaintEvent):
        """

        :param QPaintEvent:
        :return:
        """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWiring(qp)
        qp.end()

    def drawWiring(self, qp):
        """

        :param qp:
        :return:
        """
        pen = QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.red)
        qp.drawLine(self.x_wiring, 0, self.x_wiring, self.y_wiring)
        qp.drawLine(0, self.y_wiring, self.x_wiring, self.y_wiring)
        qp.drawEllipse(self.x_wiring - 3, self.y_wiring - 3, 6, 6, )


class DrawBackground(QtWidgets.QWidget):
    """
    绘制背景
    """

    def __init__(self, widget, parent=None):
        super(DrawBackground, self).__init__(parent)
        self.resize(1000, 500)
        self.setParent(widget)

    def paintEvent(self, QPaintEvent):
        """

        :param QPaintEvent:
        :return:
        """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWiring(qp)
        qp.end()

    @staticmethod
    def drawWiring(qp):
        """

        :param qp:
        :return:
        """
        pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        # qp.setBrush(QtCore.Qt.blue)
        for i in range(11):
            qp.drawLine(3, 3 + i * 35, 883, 3 + i * 35)
        for i in range(17):
            qp.drawLine(3 + i * 55, 3, 3 + i * 55, 353)


class ControlModeWiring(QtWidgets.QWidget):
    """
    连线
    """

    def __init__(self, wgt, parent=None):
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
        self.drawback = DrawBackground(self.WgtDraw)

        self.wiring = []
        self.draw_wiring()

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
        self.BT_x[0].clicked.connect(lambda: self.x_is_pressed(0))
        self.BT_x[1].clicked.connect(lambda: self.x_is_pressed(1))
        self.BT_x[2].clicked.connect(lambda: self.x_is_pressed(2))
        self.BT_x[3].clicked.connect(lambda: self.x_is_pressed(3))
        self.BT_x[4].clicked.connect(lambda: self.x_is_pressed(4))
        self.BT_x[5].clicked.connect(lambda: self.x_is_pressed(5))
        self.BT_x[6].clicked.connect(lambda: self.x_is_pressed(6))
        self.BT_x[7].clicked.connect(lambda: self.x_is_pressed(7))
        self.BT_x[8].clicked.connect(lambda: self.x_is_pressed(8))
        self.BT_x[9].clicked.connect(lambda: self.x_is_pressed(9))
        self.BT_x[10].clicked.connect(lambda: self.x_is_pressed(10))
        self.BT_x[11].clicked.connect(lambda: self.x_is_pressed(11))
        self.BT_x[12].clicked.connect(lambda: self.x_is_pressed(12))
        self.BT_x[13].clicked.connect(lambda: self.x_is_pressed(13))
        self.BT_x[14].clicked.connect(lambda: self.x_is_pressed(14))
        self.BT_x[15].clicked.connect(lambda: self.x_is_pressed(15))

        self.BT_y[0].clicked.connect(lambda: self.y_is_pressed(0))
        self.BT_y[1].clicked.connect(lambda: self.y_is_pressed(1))
        self.BT_y[2].clicked.connect(lambda: self.y_is_pressed(2))
        self.BT_y[3].clicked.connect(lambda: self.y_is_pressed(3))
        self.BT_y[4].clicked.connect(lambda: self.y_is_pressed(4))
        self.BT_y[5].clicked.connect(lambda: self.y_is_pressed(5))
        self.BT_y[6].clicked.connect(lambda: self.y_is_pressed(6))
        self.BT_y[7].clicked.connect(lambda: self.y_is_pressed(7))
        self.BT_y[8].clicked.connect(lambda: self.y_is_pressed(8))
        self.BT_y[9].clicked.connect(lambda: self.y_is_pressed(9))

        # 使用QSignalMapper
        # self.BT_x[0].clicked.connect(self.XMapper.map)
        # self.BT_y[0].clicked.connect(self.YMapper.map)
        # self.XMapper = QtCore.QSignalMapper()
        # self.YMapper = QtCore.QSignalMapper()
        # self.XMapper.setMapping(self.BT_x[1], self.BT_x[1].text())
        # self.XMapper.mapped(str).connect(self.XisPressed(str))

    def x_is_pressed(self, a):
        """

        :param a:
        :return:
        """
        debug_print('X', a)
        self.PressedXNum = a
        self.XMark = True
        for i in range(16):
            if i != a:
                self.BT_x[i].setChecked(False)

        if self.YMark:
            num = self.PressedXNum * 10 + self.PressedYNum
            if self.wiringShow[num]:
                self.wiring[num].hide()
                self.wiringShow[num] = False
            else:
                if not self.wiring_lock(num):
                    self.waringbox()
                else:
                    self.wiring[num].show()
                    self.wiringShow[num] = True
            self.BT_x[self.PressedXNum].setChecked(False)
            self.BT_y[self.PressedYNum].setChecked(False)
            self.PressedXNum = None
            self.PressedYNum = None
            self.XMark = False
            self.YMark = False

    def y_is_pressed(self, a):
        """

        :param a:
        :return:
        """
        debug_print('Y', a)
        self.YMark = True
        self.PressedYNum = a
        for i in range(10):
            if i != a:
                self.BT_y[i].setChecked(False)
        if self.XMark:
            _num = self.PressedXNum * 10 + self.PressedYNum
            if self.wiringShow[_num]:
                self.wiring[_num].hide()
                self.wiringShow[_num] = False
            else:
                if not self.wiring_lock(_num):
                    self.waring_box()
                else:
                    self.wiring[_num].show()
                    self.wiringShow[_num] = True
            self.BT_x[self.PressedXNum].setChecked(False)
            self.BT_y[self.PressedYNum].setChecked(False)
            self.PressedXNum = None
            self.PressedYNum = None
            self.XMark = False
            self.YMark = False

    def one_wiring_show(self, num):
        """

        :param num:
        :return:
        """
        self.wiring[num].show()
        self.wiringShow[num] = True

    def one_wiring_hide(self, num):
        """

        :param num:
        :return:
        """
        self.wiring[num].hide()
        self.wiringShow[num] = False

    def draw_wiring(self):
        """

        :return:
        """
        # self.wiring = []
        for i in range(16):
            for j in range(10):
                self.wiring.append(DrawWiring(self.WgtDraw, 30 + i * 55, 20 + j * 35))
                # self.wiring[i * 10 + j].show()
                self.wiring[i * 10 + j].hide()

    def waring_box(self):
        """
        消息弹窗
        :return:
        """
        _ = QtWidgets.QMessageBox.warning(self, 'Warning', '连线冲突                       ',
                                          QtWidgets.QMessageBox.Ok)

    def wiring_lock(self, wi):
        """
        检测连线是否冲突
        :param wi: wiring
        :return: bool
        """

        li = []
        for i in range(160):
            if self.wiringShow[i]:
                li.append(i)
                li.append(i - 10)
                li.append(i - 20)
        if int(str(wi)[-1]) in li:
            return False
        else:
            return True


class KeyBoardUi(QtWidgets.QMessageBox):
    """
    虚拟键盘
    """

    def __init__(self):
        super(KeyBoardUi, self).__init__()
