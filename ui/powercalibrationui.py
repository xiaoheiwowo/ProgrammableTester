# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
import random
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import dialogbutton
from public.datacache import SoftwareData as sw


class Ui_PowerCalibration(QtWidgets.QDialog):
    """
    电源及采样校准
    """

    def __init__(self, parent=None):
        super(Ui_PowerCalibration, self).__init__(parent)
        self.resize(1024, 520)
        self.move(0, 0)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电源及采样校准')
        self.setWindowIcon(QtGui.QIcon(":/logo.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.setFixedSize(300, 50)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(self.DB_DialogButton)

        self.TabWgt = QtWidgets.QTabWidget(self)
        Layout_Main = QtWidgets.QVBoxLayout()
        Layout_Main.addWidget(self.TabWgt)
        Layout_Main.addLayout(Layout_button)
        self.setLayout(Layout_Main)

        self.Tab_DCV = QtWidgets.QWidget(self.TabWgt)
        self.Tab_DCA = QtWidgets.QWidget(self.TabWgt)
        self.Tab_ACV = QtWidgets.QWidget(self.TabWgt)
        self.Tab_ACA = QtWidgets.QWidget(self.TabWgt)

        self.TabWgt.addTab(self.Tab_DCV, '直流电压')
        self.TabWgt.addTab(self.Tab_DCA, '直流电流')
        self.TabWgt.addTab(self.Tab_ACV, '交流电压')
        self.TabWgt.addTab(self.Tab_ACA, '交流电流')
        # 设置打开时默认标签页
        self.TabWgt.setCurrentIndex(0)
        self.load_data_from_pkl()

        self.tab_aca = Tab_Widgets(widget=self.Tab_ACA, page='aca')
        self.tab_acv = Tab_Widgets(widget=self.Tab_ACV, page='acv')
        self.tab_dca = Tab_Widgets(widget=self.Tab_DCA, page='dca')
        self.tab_dcv = Tab_Widgets(widget=self.Tab_DCV, page='dcv')

        # signal
        self.DB_DialogButton.BT_Save1.clicked.connect(self.save_data)
        self.DB_DialogButton.BT_OK1.clicked.connect(self.ok_and_exit)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

    @staticmethod
    def load_data_from_pkl():
        """

        :return:
        """
        with open('pkl/calibration.pkl', 'rb') as f:
            sw.data_list = pickle.loads(f.read())

        pass

    @staticmethod
    def save_data():
        """
        保存所有数据
        :return:
        """
        with open('pkl/calibration.pkl', 'wb') as f:
            f.write(pickle.dumps(sw.data_list))
        pass

    def ok_and_exit(self):
        """

        :return:
        """
        self.save_data()
        self.close()
        pass


class Tab_Widgets(QtWidgets.QWidget):
    """
    标签页内容
    """
    png_wiring = {'acv': ':/acv.png',
                  'aca': ':/aca.png',
                  'dcv': ':/dcv.png',
                  'dca': ':/dca.png'}

    # 采样校准操作说明
    text_operation = {'dcv': '操作步骤:\n'
                             '1、按照上图连接电压表。\n'
                             '2、向Vi中输入一个电压值(0~36V)。\n'
                             '3、待电压表读数稳定后将电压表示数填入Vn。\n'
                             '4、重复上述步骤添加多组数据。',
                      'dca': '操作步骤:\n'
                             '1、按照上图连接电流表。\n'
                             '2、调节适当的电压值(0~5V)。\n'
                             '3、待电流表读数稳定后将电流表示数填入In。\n'
                             '4、重复上述步骤添加多组数据。',
                      'acv': '操作步骤(注意高压):\n'
                             '1、按照上图连接电压表。\n'
                             '2、向Vi中输入一个电压值(0~300V)。\n'
                             '3、待电压表读数稳定后将电压表示数填入Vn。\n'
                             '4、重复上述步骤添加多组数据。',
                      'aca': '操作步骤:\n'
                             '1、按照上图连接电流表。\n'
                             '2、调节适当的电压值(0~10V)。\n'
                             '3、待电流表读数稳定后将电流表示数填入In。\n'
                             '4、重复上述步骤添加多组数据。'}

    def __init__(self, widget, page, parent=None):
        """
        初始化
        :param widget: 父widget
        :param page: 标签页页码
        :param parent:
        """
        super(Tab_Widgets, self).__init__(parent)
        self.widget = widget
        self.page = page
        self.png = Tab_Widgets.png_wiring[page]
        self.text = Tab_Widgets.text_operation[page]
        self.tw_list = QtWidgets.QTableWidget(self.widget)
        # 设置不可编辑
        self.tw_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.bt_new = QtWidgets.QPushButton()
        self.bt_delete = QtWidgets.QPushButton()
        self.label_png = QtWidgets.QLabel()
        self.label_operation = QtWidgets.QLabel()
        self.list_checkbox = []
        self.init_widget()
        self.load_data()

        self.dia_new = Dia_Add_Line(self, voltage_limit=305, page=page)

        # signal
        self.bt_new.clicked.connect(self.list_append_line)
        self.bt_delete.clicked.connect(self.list_delete_line)
        self.dia_new.get_valve.connect(self.update_list)
        self.tw_list.itemClicked.connect(self.list_select_line)

    def init_widget(self):
        """
        控件设置
        :return:
        """
        self.tw_list.setFixedWidth(265)
        self.tw_list.setRowCount(len(sw.data_list[self.page]))
        self.tw_list.setColumnCount(4)
        self.tw_list.setHorizontalHeaderLabels([' ', '电压(V)', '采样Io', 'In(mA)'])
        self.tw_list.setColumnWidth(0, 30)
        self.tw_list.setColumnWidth(1, 60)
        self.tw_list.setColumnWidth(2, 70)
        self.tw_list.setColumnWidth(3, 60)
        self.tw_list.horizontalHeader().setSectionResizeMode(2)
        self.tw_list.verticalHeader().setVisible(False)
        self.tw_list.setSelectionBehavior(1)

        for i in range(len(sw.data_list[self.page])):
            self.list_checkbox.append(QtWidgets.QCheckBox())
            self.list_checkbox[i].setDisabled(True)
            self.list_checkbox[i].setStyleSheet('QCheckBox{margin:6px}')
            self.tw_list.setCellWidget(i, 0, self.list_checkbox[i])

        self.bt_new.setText('添加')
        self.bt_new.setFixedSize(80, 40)
        self.bt_delete.setText('删除')
        self.bt_delete.setFixedSize(80, 40)
        layout_bt = QtWidgets.QHBoxLayout()
        layout_bt.addStretch(1)
        layout_bt.addWidget(self.bt_new)
        layout_bt.addStretch(1)
        layout_bt.addWidget(self.bt_delete)
        layout_bt.addStretch(1)

        layout_list = QtWidgets.QVBoxLayout()
        layout_list.addWidget(self.tw_list)
        layout_list.addLayout(layout_bt)

        self.label_png.setPixmap(QtGui.QPixmap(self.png))
        self.label_png.setScaledContents(True)
        self.label_png.setFixedSize(600, 300)

        self.label_operation.setText(self.text)
        self.label_operation.setFont(QtGui.QFont('微软雅黑 Semilight', 10))
        layout_label = QtWidgets.QVBoxLayout()
        layout_label.addWidget(self.label_png)
        layout_label.addWidget(self.label_operation)

        layout = QtWidgets.QHBoxLayout(self.widget)
        layout.addLayout(layout_list)
        layout.addStretch(1)
        layout.addLayout(layout_label)
        layout.addStretch(1)

    def load_data(self):
        """

        :return:
        """
        for i in range(len(sw.data_list[self.page])):
            item1 = QtWidgets.QTableWidgetItem(str(sw.data_list[self.page][i][0]))
            item2 = QtWidgets.QTableWidgetItem(sw.data_list[self.page][i][1])
            item3 = QtWidgets.QTableWidgetItem(str(sw.data_list[self.page][i][2]))
            self.tw_list.setItem(i, 1, item1)
            self.tw_list.setItem(i, 2, item2)
            self.tw_list.setItem(i, 3, item3)

    def list_append_line(self):
        """

        :return:
        """
        self.dia_new.le_samp.clear()
        self.dia_new.sb_vol.clear()
        self.dia_new.le_real.clear()
        self.dia_new.show()

    def list_select_line(self, item):
        """

        :param item:
        :return:
        """
        for i in self.list_checkbox:
            i.setChecked(False)
        self.list_checkbox[item.row()].setChecked(True)
        pass

    def list_delete_line(self):
        """

        :return:
        """

        for i in range(len(sw.data_list[self.page])):
            if self.list_checkbox[i].isChecked():
                sw.data_list[self.page].pop(i)
        self.update_list()
        pass

    def update_list(self):
        """

        :return:
        """
        print('x')
        self.list_checkbox = []
        self.init_widget()
        self.load_data()


class Dia_Add_Line(QtWidgets.QDialog):
    """
    对话窗，添加一行校准参数
    """

    get_valve = QtCore.pyqtSignal()  # [int, str, int])

    def __init__(self, parent=None, voltage_limit=None, page=None):
        super(Dia_Add_Line, self).__init__(parent)
        # self.setFixedSize(500, 300)
        self.setWindowTitle('添加校准点')
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.page = page
        label_vol = QtWidgets.QLabel()
        label_vol.setFixedSize(50, 40)

        self.sb_vol = QtWidgets.QSpinBox()
        self.sb_vol.setFixedSize(100, 40)
        self.sb_vol.setRange(0, voltage_limit)
        bt_adjust = QtWidgets.QPushButton()
        bt_adjust.setFixedSize(100, 40)
        bt_adjust.setText('调节电压')

        label_samp = QtWidgets.QLabel()

        self.le_samp = QtWidgets.QLineEdit()
        self.le_samp.setFixedSize(100, 40)
        self.le_samp.setReadOnly(True)
        bt_samp = QtWidgets.QPushButton()
        bt_samp.setFixedSize(100, 40)
        bt_samp.setText('采样')

        label_real = QtWidgets.QLabel()

        self.le_real = QtWidgets.QLineEdit()
        self.le_real.setFixedSize(100, 40)
        bt_save = QtWidgets.QPushButton()
        bt_save.setFixedSize(100, 40)
        bt_save.setText('确定')
        if page == 'acv' or page == 'dcv':
            label_vol.setText('V:')
            label_samp.setText('Vo:')
            label_real.setText('Vn:')
        else:
            label_vol.setText('V:')
            label_samp.setText('Io:')
            label_real.setText('In:')
        # 验证器 0~400 两位小数
        vali_real = QtGui.QRegExpValidator(self)
        reg_real = QtCore.QRegExp('^([1-3]\d\d|[1-9]\d|[1-9])(\.\d{1,2})?$')
        vali_real.setRegExp(reg_real)

        # vali_real2 = QtGui.QDoubleValidator(self)
        # vali_real2.setRange(0.00, 305.00, decimals=2)
        # vali_real2.setTop(400.00)

        self.le_real.setValidator(vali_real)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(label_vol, 0, 0)
        layout.addWidget(self.sb_vol, 0, 1)
        layout.addWidget(bt_adjust, 0, 2)
        layout.addWidget(label_samp, 1, 0)
        layout.addWidget(self.le_samp, 1, 1)
        layout.addWidget(bt_samp, 1, 2)
        layout.addWidget(label_real, 2, 0)
        layout.addWidget(self.le_real, 2, 1)
        layout.addWidget(bt_save, 2, 2)

        # signal
        bt_save.clicked.connect(self.save_valve)
        bt_samp.clicked.connect(self.get_sampling)

    def save_valve(self):
        """

        :return:
        """
        try:
            list1 = [int(self.sb_vol.text()), self.le_samp.text(), int(self.le_real.text())]
            a = True
        except ValueError:
            print('ValueError')
            a = False
        if a:
            sw.data_list[self.page].append(list1)
            self.get_valve.emit()
            print(list1)
        self.close()

    def get_sampling(self):
        """

        :return:
        """
        self.le_samp.setText(hex(int(65535 * random.random())))
        print(hex(int(65535 * random.random())))
