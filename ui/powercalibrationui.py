# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from ui import dialogbutton

from public.globalvariable import GlobalVariable as gv

import pickle
import json


class Ui_PowerCalibration(QtWidgets.QDialog):
    """
    电源及采样校准
    """
    def __init__(self, parent=None):
        super(Ui_PowerCalibration, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电源及采样校准')
        self.setWindowIcon(QtGui.QIcon(":/entertainment_valve_72px_547701_easyicon.net.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.setFixedSize(300, 50)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)
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
        self.TabWgt.setCurrentIndex(2)
        # ACV
        self.tw_list_acv = QtWidgets.QTableWidget(self.Tab_ACV)
        self.label_png_acv = QtWidgets.QLabel(self.Tab_ACV)
        self.label_operation_steps_acv = QtWidgets.QLabel(self.Tab_ACV)
        self.bt_adjust_acv = QtWidgets.QPushButton(self.Tab_ACV)
        self.bt_calibrate_acv = QtWidgets.QPushButton(self.Tab_ACV)
        self.list_checkbox_acv = []

        self.Init_TabDCV()
        self.Init_TabDCA()
        self.Init_TabACV()
        self.Init_TabACA()

    def Init_TabDCV(self):
        """

        :return:
        """
        GB_ListDCV = QtWidgets.QGroupBox(self.Tab_DCV)
        # GB_ListDCV.setGeometry(10, 10, 300, 450)
        GB_ListDCV.setTitle('基准表')

        self.TW_ListDCV = QtWidgets.QTableWidget()
        self.TW_ListDCV.setFixedWidth(270)
        self.TW_ListDCV.setRowCount(20)
        self.TW_ListDCV.setColumnCount(3)
        self.TW_ListDCV.setHorizontalHeaderLabels(['Vi(V)', '采样Vo', 'Vn(V)'])
        self.TW_ListDCV.setColumnWidth(0, 70)
        self.TW_ListDCV.setColumnWidth(1, 70)
        self.TW_ListDCV.setColumnWidth(2, 70)

        Layout_GBList = QtWidgets.QHBoxLayout(GB_ListDCV)
        Layout_GBList.addWidget(self.TW_ListDCV)

        self.Label_dcv = QtWidgets.QLabel(self.Tab_DCV)
        self.Label_dcv.setFixedSize(300, 400)
        self.Label_dcv.setText('ddd')
        self.Label_dcv.setPixmap(QtGui.QPixmap(':/dcv.png'))
        self.Label_dcv.setScaledContents(True)

        self.operation_steps_dcv = QtWidgets.QLabel(self.Tab_DCV)
        # self.TE_OperationStepsDCV.setGeometry(680, 20, 300, 440)
        self.operation_steps_dcv.setText('操作步骤:\n'
                                          '1、按照左图连接电压表。\n'
                                          '2、向Vi中输入一个电压值(0~36V)。\n'
                                          '3、待电压表读数稳定后将电压表示数填入Vn。\n'
                                          '4、重复上述步骤添加多组数据。')
        self.operation_steps_dcv.setFont(QtGui.QFont('微软雅黑 Semilight', 10))
        # self.operation_steps_dcv.setReadOnly(True)
        # self.operation_steps_dcv.setFocusPolicy(QtCore.Qt.NoFocus)

        Layout_DCV = QtWidgets.QHBoxLayout(self.Tab_DCV)
        Layout_DCV.addWidget(GB_ListDCV)
        Layout_DCV.addWidget(self.Label_dcv)
        Layout_DCV.addWidget(self.operation_steps_dcv)

    def Init_TabDCA(self):
        """

        :return:
        """
        GB_ListDCA = QtWidgets.QGroupBox(self.Tab_DCA)
        GB_ListDCA.setGeometry(10, 10, 230, 450)
        GB_ListDCA.setTitle('基准表')

        Label_vinput = QtWidgets.QLabel('电压(V):')
        self.SB_VInput = QtWidgets.QDoubleSpinBox()
        self.SB_VInput.setMinimumWidth(100)
        self.SB_VInput.setMinimumHeight(40)
        self.SB_VInput.setMinimum(0)
        self.SB_VInput.setMaximum(5.00)

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(Label_vinput)
        layout2.addWidget(self.SB_VInput)

        self.TW_ListDCA = QtWidgets.QTableWidget()
        self.TW_ListDCA.setGeometry(10, 30, 280, 400)
        self.TW_ListDCA.setRowCount(20)
        self.TW_ListDCA.setColumnCount(2)
        self.TW_ListDCA.setHorizontalHeaderLabels(['采样Io', 'In(mA)'])
        self.TW_ListDCA.setColumnWidth(0, 75)
        self.TW_ListDCA.setColumnWidth(1, 75)

        layout = QtWidgets.QVBoxLayout(GB_ListDCA)
        layout.addLayout(layout2)
        layout.addWidget(self.TW_ListDCA)

        self.Label_dca = QtWidgets.QLabel(self.Tab_DCA)
        self.Label_dca.setGeometry(250, 20, 300, 440)
        self.Label_dca.setText('ddd')
        self.Label_dca.setPixmap(QtGui.QPixmap(':/dca.png'))
        self.Label_dca.setScaledContents(True)

        self.TE_OperationStepsDCA = QtWidgets.QTextEdit(self.Tab_DCA)
        self.TE_OperationStepsDCA.setGeometry(570, 20, 400, 440)
        self.TE_OperationStepsDCA.setText('操作步骤:\n'
                                          '1、按照左图连接电流表。\n'
                                          '2、调节适当的电压值(0~5V)。\n'
                                          '3、待电流表读数稳定后将电流表示数填入In。\n'
                                          '4、重复上述步骤添加多组数据。')
        self.TE_OperationStepsDCA.setFont(QtGui.QFont('微软雅黑 Semilight', 16))
        self.TE_OperationStepsDCA.setReadOnly(True)
        self.TE_OperationStepsDCA.setFocusPolicy(QtCore.Qt.NoFocus)
        pass

    def Init_TabACV(self):
        """
        初始化交流电压校准tab
        :return:
        """
        # GB_ListACV = QtWidgets.QGroupBox(self.Tab_ACV)
        # GB_ListACV.setGeometry(10, 10, 300, 450)
        # GB_ListACV.setTitle('基准表')

        self.tw_list_acv.setMinimumWidth(265)
        self.tw_list_acv.setRowCount(20)
        self.tw_list_acv.setColumnCount(4)
        self.tw_list_acv.setHorizontalHeaderLabels([' ', 'Vi(V)', '采样Vo', 'Vn(V)'])
        self.tw_list_acv.setColumnWidth(0, 30)
        self.tw_list_acv.setColumnWidth(1, 60)
        self.tw_list_acv.setColumnWidth(2, 60)
        self.tw_list_acv.setColumnWidth(3, 60)
        self.tw_list_acv.horizontalHeader().setSectionResizeMode(2)
        # self.TW_ListACV.verticalHeader().setVisible(False)
        self.tw_list_acv.setSelectionBehavior(1)
        for i in range(20):
            item0 = QtWidgets.QTableWidgetItem(str(i * 16))
            self.tw_list_acv.setItem(i, 1, item0)

        self.bt_adjust_acv.setText('调节电压')
        self.bt_adjust_acv.setFixedSize(80, 40)
        self.bt_calibrate_acv.setText('采样')
        self.bt_calibrate_acv.setFixedSize(80, 40)

        for i in range(20):
            self.list_checkbox_acv.append(QtWidgets.QRadioButton())
            # self.list_checkbox_acv[i].setDisabled(True)
            self.list_checkbox_acv[i].setStyleSheet('QRadioButton{margin:6px}')
            self.tw_list_acv.setCellWidget(i, 0, self.list_checkbox_acv[i])

        self.label_png_acv.setPixmap(QtGui.QPixmap(':/acv.png'))
        self.label_png_acv.setScaledContents(True)
        self.label_png_acv.setFixedSize(600, 300)

        self.label_operation_steps_acv.setText('                    操作步骤(注意高压):\n'
                                          '                    1、按照上图连接电压表。\n'
                                          '                    2、向Vi中输入一个电压值(0~300V)。\n'
                                          '                    3、待电压表读数稳定后将电压表示数填入Vn。\n'
                                          '                    4、重复上述步骤添加多组数据。')
        self.label_operation_steps_acv.setFont(QtGui.QFont('微软雅黑 Semilight', 10))

        layout_bt = QtWidgets.QHBoxLayout()
        layout_bt.addStretch(1)
        layout_bt.addWidget(self.bt_adjust_acv)
        layout_bt.addStretch(1)
        layout_bt.addWidget(self.bt_calibrate_acv)
        layout_bt.addStretch(1)

        layout_list_and_bt = QtWidgets.QVBoxLayout()
        layout_list_and_bt.addWidget(self.tw_list_acv)
        layout_list_and_bt.addLayout(layout_bt)

        layout_png_and_label = QtWidgets.QVBoxLayout()
        layout_png_and_label.addWidget(self.label_png_acv)
        layout_png_and_label.addWidget(self.label_operation_steps_acv)
        layout_acv = QtWidgets.QHBoxLayout(self.Tab_ACV)
        layout_acv.addLayout(layout_list_and_bt)
        layout_acv.addStretch(1)
        layout_acv.addLayout(layout_png_and_label)
        layout_acv.addStretch(1)

        # SIGNAL
        self.tw_list_acv.itemClicked.connect(self.acv_select)
        self.bt_adjust_acv.clicked.connect(self.adjust_voltage)

    def acv_select(self, item):
        """

        :param item:
        :return:
        """
        for i in self.list_checkbox_acv:
            i.setChecked(False)
        self.list_checkbox_acv[item.row()].setChecked(True)
        # print('xx')

    def Init_TabACA(self):
        """

        :return:
        """

        GB_ListACA = QtWidgets.QGroupBox(self.Tab_ACA)
        GB_ListACA.setGeometry(10, 10, 230, 450)
        GB_ListACA.setTitle('基准表')

        Label_vinput = QtWidgets.QLabel('电压(V):')
        self.SB_ACVInput = QtWidgets.QDoubleSpinBox()
        self.SB_ACVInput.setMinimumWidth(100)
        self.SB_ACVInput.setMinimumHeight(40)
        self.SB_ACVInput.setMinimum(0)
        self.SB_ACVInput.setMaximum(10.00)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(Label_vinput)
        layout2.addWidget(self.SB_ACVInput)

        self.TW_ListACA = QtWidgets.QTableWidget()
        self.TW_ListACA.setGeometry(10, 30, 280, 400)
        self.TW_ListACA.setRowCount(20)
        self.TW_ListACA.setColumnCount(2)
        self.TW_ListACA.setHorizontalHeaderLabels(['采样Io', 'In(mA)'])
        self.TW_ListACA.setColumnWidth(0, 75)
        self.TW_ListACA.setColumnWidth(1, 75)

        layout = QtWidgets.QVBoxLayout(GB_ListACA)
        layout.addLayout(layout2)
        layout.addWidget(self.TW_ListACA)

        Label_aca = QtWidgets.QLabel(self.Tab_ACA)
        Label_aca.setGeometry(250, 20, 300, 440)
        Label_aca.setText('ddd')
        Label_aca.setPixmap(QtGui.QPixmap(':/aca.png'))
        Label_aca.setScaledContents(True)

        self.TE_OperationStepsACA = QtWidgets.QTextEdit(self.Tab_ACA)
        self.TE_OperationStepsACA.setGeometry(570, 20, 400, 440)
        self.TE_OperationStepsACA.setText('操作步骤:\n'
                                          '1、按照左图连接电流表。\n'
                                          '2、调节适当的电压值(0~10V)。\n'
                                          '3、待电流表读数稳定后将电流表示数填入In。\n'
                                          '4、重复上述步骤添加多组数据。')
        self.TE_OperationStepsACA.setFont(QtGui.QFont('微软雅黑 Semilight', 16))
        self.TE_OperationStepsACA.setReadOnly(True)
        self.TE_OperationStepsACA.setFocusPolicy(QtCore.Qt.NoFocus)

    def load_data(self):
        """
        载入所有数据
        :return:
        """
        pass

    def save_data(self):
        """
        保存所有数据
        :return:
        """
        pass

    def adjust_voltage(self):
        """

        :return:
        """
        print(self.TabWgt.currentIndex())
        for i in range(20):
            if self.list_checkbox_acv[i].isChecked():
                select_row = i
        try:
            print(select_row)
            # 调节电压
        except:
            print('err')

