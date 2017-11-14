#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 主窗口Ui类
import MainWindowUi

# 控制方式窗口Ui类




class Form(QMainWindow, MainWindowUi.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Form()
    win.show()
    sys.exit(app.exec_())


