#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
# 保存、确定、取消按钮

class DialogButton(QtWidgets.QWidget):
    '''
    窗口下方的按钮：保存，确定，取消
    '''
    def __init__(self, parent = None):
        super(DialogButton, self).__init__(parent)

        self.BT_Save1 = QtWidgets.QPushButton('保存')
        self.BT_OK1 = QtWidgets.QPushButton('确定')
        self.BT_Cancel1 = QtWidgets.QPushButton('取消')
        self.wgt = QtWidgets.QWidget(self)
        self.wgt.resize(300, 50)
        self.layout = QtWidgets.QHBoxLayout(self.wgt)
        self.layout.addWidget(self.BT_Save1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.BT_OK1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.BT_Cancel1)


