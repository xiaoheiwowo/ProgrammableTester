#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import DialogButton

class Ui_PowerCalibrationUi(QtWidgets.QDialog):
    '''
    电源及采样校准
    '''
    def __init__(self, parent=None):
        super(Ui_PowerCalibrationUi, self).__init__(parent)
        self.setGeometry(300, 200, 1024, 600)
        self.setWindowTitle('电源及采样校准')
        self.setWindowIcon(QtGui.QIcon(":/entertainment_valve_72px_547701_easyicon.net.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # 保存、确定、取消按钮
        self.DB_DialogButton = DialogButton.DialogButton(self)
        self.DB_DialogButton.move(700, 530)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)

        TabWgt = QtWidgets.QTabWidget(self)
        TabWgt.setGeometry(12, 10, 1000, 510)

        self.Tab_DCV = QtWidgets.QWidget(TabWgt)
        self.Tab_DCA = QtWidgets.QWidget(TabWgt)
        self.Tab_ACV = QtWidgets.QWidget(TabWgt)
        self.Tab_ACA = QtWidgets.QWidget(TabWgt)

        TabWgt.addTab(self.Tab_DCV, '直流电压')
        TabWgt.addTab(self.Tab_DCA, '直流电流')
        TabWgt.addTab(self.Tab_ACV, '交流电压')
        TabWgt.addTab(self.Tab_ACA, '交流电流')

        self.Init_TabDCV()
        self.Init_TabDCA()
        self.Init_TabACV()
        self.Init_TabACA()

    def Init_TabDCV(self):
        GB_ListDCV = QtWidgets.QGroupBox(self.Tab_DCV)
        GB_ListDCV.setGeometry(10, 10, 300, 450)
        GB_ListDCV.setTitle('基准表')

        self.TW_ListDCV = QtWidgets.QTableWidget(GB_ListDCV)
        self.TW_ListDCV.setGeometry(10, 30, 280, 400)
        self.TW_ListDCV.setRowCount(20)
        self.TW_ListDCV.setColumnCount(3)
        self.TW_ListDCV.setHorizontalHeaderLabels(['Vi(V)', '采样Vo', 'Vn(V)'])
        self.TW_ListDCV.setColumnWidth(0, 70)
        self.TW_ListDCV.setColumnWidth(1, 70)
        self.TW_ListDCV.setColumnWidth(2, 70)

        self.Label_dcv = QtWidgets.QLabel(self.Tab_DCV)
        self.Label_dcv.setGeometry(350, 20, 300, 440)
        self.Label_dcv.setText('ddd')
        self.Label_dcv.setPixmap(QtGui.QPixmap(':/dcv.png'))
        self.Label_dcv.setScaledContents(True)

        self.TE_OperationStepsDCV = QtWidgets.QTextEdit(self.Tab_DCV)
        self.TE_OperationStepsDCV.setGeometry(680, 20, 300, 440)
        self.TE_OperationStepsDCV.setText('操作步骤:\n'
                                          '1、按照左图连接电压表。\n'
                                          '2、向Vi中输入一个电压值(0~36V)。\n'
                                          '3、待电压表读数稳定后将电压表示数填入Vn。\n'
                                          '4、重复上述步骤添加多组数据。')
        self.TE_OperationStepsDCV.setFont(QtGui.QFont('微软雅黑 Semilight', 16))
        self.TE_OperationStepsDCV.setReadOnly(True)
        self.TE_OperationStepsDCV.setFocusPolicy(QtCore.Qt.NoFocus)

    def Init_TabDCA(self):
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
        GB_ListACV = QtWidgets.QGroupBox(self.Tab_ACV)
        GB_ListACV.setGeometry(10, 10, 300, 450)
        GB_ListACV.setTitle('基准表')

        self.TW_ListACV = QtWidgets.QTableWidget(GB_ListACV)
        self.TW_ListACV.setGeometry(10, 30, 280, 400)
        self.TW_ListACV.setRowCount(20)
        self.TW_ListACV.setColumnCount(3)
        self.TW_ListACV.setHorizontalHeaderLabels(['Vi(V)', '采样Vo', 'Vn(V)'])
        self.TW_ListACV.setColumnWidth(0, 70)
        self.TW_ListACV.setColumnWidth(1, 70)
        self.TW_ListACV.setColumnWidth(2, 70)

        self.Label_acv = QtWidgets.QLabel(self.Tab_ACV)
        self.Label_acv.setGeometry(350, 20, 300, 440)
        self.Label_acv.setText('ddd')
        self.Label_acv.setPixmap(QtGui.QPixmap(':/acv.png'))
        self.Label_acv.setScaledContents(True)

        self.TE_OperationStepsACV = QtWidgets.QTextEdit(self.Tab_ACV)
        self.TE_OperationStepsACV.setGeometry(680, 20, 300, 440)
        self.TE_OperationStepsACV.setText('操作步骤(注意高压):\n'
                                          '1、按照左图连接电压表。\n'
                                          '2、向Vi中输入一个电压值(0~300V)。\n'
                                          '3、待电压表读数稳定后将电压表示数填入Vn。\n'
                                          '4、重复上述步骤添加多组数据。')
        self.TE_OperationStepsACV.setFont(QtGui.QFont('微软雅黑 Semilight', 16))
        self.TE_OperationStepsACV.setReadOnly(True)
        self.TE_OperationStepsACV.setFocusPolicy(QtCore.Qt.NoFocus)
        pass

    def Init_TabACA(self):
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
        pass




