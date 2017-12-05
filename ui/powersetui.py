#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from ui import dialogbutton


class Ui_PowerSet(QtWidgets.QDialog):
    '''
    电源设置窗口，
    '''
    def __init__(self, parent = None):
        super(Ui_PowerSet, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电源设置')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.Init_PowerSet()

        # 保存、确定、取消按钮
        self.DB_DialogButton = dialogbutton.DialogButton(self)
        self.DB_DialogButton.setFixedSize(300, 50)
        self.DB_DialogButton.BT_Cancel1.clicked.connect(self.close)
        Layout_button = QtWidgets.QHBoxLayout()
        Layout_button.addStretch(1)
        Layout_button.addWidget(self.DB_DialogButton)

        Layout_Main = QtWidgets.QVBoxLayout(self)
        Layout_Main.addWidget(self.GB_PowerSet)
        Layout_Main.addLayout(Layout_button)


    # 初始化电源设置
    def Init_PowerSet(self):
        self.GB_PowerSet = QtWidgets.QGroupBox(self)
        self.GB_PowerSet.setGeometry(630, 10, 380, 500)
        self.GB_PowerSet.setTitle('电源设置')

        Label_g11 = QtWidgets.QLabel('DC调节精度Δ1：')
        Label_g12 = QtWidgets.QLabel('DC调节精度Δ2：')
        Label_g13 = QtWidgets.QLabel('AC调节精度Δ1：')
        Label_g14 = QtWidgets.QLabel('AC调节精度Δ2：')
        Label_g15 = QtWidgets.QLabel('安全极限误差Δ3：')
        Label_g16 = QtWidgets.QLabel('%')
        Label_g17 = QtWidgets.QLabel('%')
        Label_g18 = QtWidgets.QLabel('%')
        Label_g19 = QtWidgets.QLabel('%')
        Label_g21 = QtWidgets.QLabel('%')
        Label_g22 = QtWidgets.QLabel('')
        Label_g22.setPixmap(QtGui.QPixmap(':/dcac.png'))
        Label_g22.setScaledContents(True)
        # Label_g22.setFixedSize(300, 150)

        self.DCAdjustPrecision1 = QtWidgets.QSpinBox()
        self.DCAdjustPrecision1.setMinimumHeight(40)
        self.DCPermissibleErrors2 = QtWidgets.QSpinBox()
        self.DCPermissibleErrors2.setMinimumHeight(40)
        self.ACAdjustPrecision1 = QtWidgets.QSpinBox()
        self.ACAdjustPrecision1.setMinimumHeight(40)
        self.ACPermissibleErrors2 = QtWidgets.QSpinBox()
        self.ACPermissibleErrors2.setMinimumHeight(40)
        self.SafetyLimit = QtWidgets.QSpinBox()
        self.SafetyLimit.setMinimumHeight(40)
        TE_Instructions = QtWidgets.QTextEdit()
        TE_Instructions.setText('电源设置参数说明\n '
                                'Vx:电压设定值\n'
                                'Δ1:以Vx为中心的偏移相对值，调节时电压到达此区域视为达到要求\n'
                                'Δ2:以Vx为中心的偏移相对值，工作中当电压超出此区域开始调整\n'
                                'Δ3:电压误差超过Δ3断开电源，调整到Δ1范围内再接通。')
        TE_Instructions.setReadOnly(True)
        TE_Instructions.setFont(QtGui.QFont('微软雅黑 Semilight', 14))

        layout = QtWidgets.QGridLayout(self.GB_PowerSet)
        layout.addWidget(Label_g11, 1, 0)
        layout.addWidget(self.DCAdjustPrecision1,1 ,1)
        layout.addWidget(Label_g16,1 ,2)
        layout.addWidget(Label_g12)
        layout.addWidget(self.DCPermissibleErrors2)
        layout.addWidget(Label_g17)
        layout.addWidget(Label_g13)
        layout.addWidget(self.ACAdjustPrecision1)
        layout.addWidget(Label_g18)
        layout.addWidget(Label_g14)
        layout.addWidget(self.ACPermissibleErrors2)
        layout.addWidget(Label_g19)
        layout.addWidget(Label_g15)
        layout.addWidget(self.SafetyLimit)
        layout.addWidget(Label_g21)
        layout.addWidget(Label_g22, 1, 3, 5, 2)
        layout.addWidget(TE_Instructions, 6, 0, 1, 5)