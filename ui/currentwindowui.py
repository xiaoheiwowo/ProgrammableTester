#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.patheffects as patheffects
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import diagram, doubleslider


class Ui_CurrentWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_CurrentWindow, self).__init__(parent)
        self.resize(1024, 550)
        self.setMinimumSize(600, 300)
        self.setWindowTitle('电流曲线')
        self.setWindowIcon(QtGui.QIcon(":/qt.png"))
        # 设置窗口模态
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        layout_main = QtWidgets.QHBoxLayout()
        self.TAB_Current = QtWidgets.QTabWidget()
        self.TAB_Current.addTab(self.tab1, '静态')
        self.TAB_Current.addTab(self.tab2, '动态')
        self.TAB_Current.setTabPosition(3)
        layout_main.addWidget(self.TAB_Current)
        self.setLayout(layout_main)

        self.tab1ui()
        self.tab2ui()

    def tab1ui(self):
        pass

    def tab2ui(self):
        pass