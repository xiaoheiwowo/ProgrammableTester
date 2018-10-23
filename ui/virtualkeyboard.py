# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成在软件中的虚拟键盘
功能：当点击可输入的控件时自动弹出键盘窗口，点击按键可更改控件中的内容
按键：数字按键，字母按键，（Shift？），删除，回车，-，
"""
import random
import sys
import pickle
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class VirtualKeyboard(QWidget):
    def __init__(self, where_to_input):
        super(VirtualKeyboard, self).__init__()
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        keyboard_layout = QVBoxLayout(self)
        self.where_to_input = where_to_input
        # self.setGeometry(0, 100, 100, 190)
        self.move(0, 0)
        self.number_button = []
        number_layout = QHBoxLayout(self)
        for i in range(10):
            self.number_button.append(QPushButton(str(i)))
            self.number_button[i].setFixedSize(30, 30)
            number_layout.addWidget(self.number_button[i])

        self.number_button[0].clicked.connect(lambda: self.key_press('0'))
        self.number_button[1].clicked.connect(lambda: self.key_press('1'))
        self.number_button[2].clicked.connect(lambda: self.key_press('2'))
        self.number_button[3].clicked.connect(lambda: self.key_press('3'))
        self.number_button[4].clicked.connect(lambda: self.key_press('4'))
        self.number_button[5].clicked.connect(lambda: self.key_press('5'))
        self.number_button[6].clicked.connect(lambda: self.key_press('6'))
        self.number_button[7].clicked.connect(lambda: self.key_press('7'))
        self.number_button[8].clicked.connect(lambda: self.key_press('8'))
        self.number_button[9].clicked.connect(lambda: self.key_press('9'))

        letter_layout_top = QHBoxLayout(self)
        letter_list_top = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        self.letter_button_top = []
        for i in range(len(letter_list_top)):
            self.letter_button_top.append(QPushButton(letter_list_top[i]))
            self.letter_button_top[i].setFixedSize(30, 30)
            letter_layout_top.addWidget(self.letter_button_top[i])

        self.letter_button_top[0].clicked.connect(lambda: self.key_press('Q'))
        self.letter_button_top[1].clicked.connect(lambda: self.key_press('W'))
        self.letter_button_top[2].clicked.connect(lambda: self.key_press('E'))
        self.letter_button_top[3].clicked.connect(lambda: self.key_press('R'))
        self.letter_button_top[4].clicked.connect(lambda: self.key_press('T'))
        self.letter_button_top[5].clicked.connect(lambda: self.key_press('Y'))
        self.letter_button_top[6].clicked.connect(lambda: self.key_press('U'))
        self.letter_button_top[7].clicked.connect(lambda: self.key_press('I'))
        self.letter_button_top[8].clicked.connect(lambda: self.key_press('O'))
        self.letter_button_top[9].clicked.connect(lambda: self.key_press('P'))

        letter_layout_mid = QHBoxLayout(self)
        letter_list_mid = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ent']
        self.letter_button_mid = []
        for i in range(len(letter_list_mid)):
            self.letter_button_mid.append(QPushButton(letter_list_mid[i]))
            self.letter_button_mid[i].setFixedSize(30, 30)
            letter_layout_mid.addWidget(self.letter_button_mid[i])

        self.letter_button_mid[0].clicked.connect(lambda: self.key_press('A'))
        self.letter_button_mid[1].clicked.connect(lambda: self.key_press('S'))
        self.letter_button_mid[2].clicked.connect(lambda: self.key_press('D'))
        self.letter_button_mid[3].clicked.connect(lambda: self.key_press('F'))
        self.letter_button_mid[4].clicked.connect(lambda: self.key_press('G'))
        self.letter_button_mid[5].clicked.connect(lambda: self.key_press('H'))
        self.letter_button_mid[6].clicked.connect(lambda: self.key_press('J'))
        self.letter_button_mid[7].clicked.connect(lambda: self.key_press('K'))
        self.letter_button_mid[8].clicked.connect(lambda: self.key_press('L'))
        self.letter_button_mid[9].clicked.connect(lambda: self.key_press('Enter'))

        letter_layout_btm = QHBoxLayout(self)
        letter_list_btm = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '-', 'Del']
        self.letter_button_btm = []
        for i in range(len(letter_list_btm)):
            self.letter_button_btm.append(QPushButton(letter_list_btm[i]))
            self.letter_button_btm[i].setFixedSize(30, 30)
            letter_layout_btm.addWidget(self.letter_button_btm[i])

        self.letter_button_btm[0].clicked.connect(lambda: self.key_press('Z'))
        self.letter_button_btm[1].clicked.connect(lambda: self.key_press('X'))
        self.letter_button_btm[2].clicked.connect(lambda: self.key_press('C'))
        self.letter_button_btm[3].clicked.connect(lambda: self.key_press('V'))
        self.letter_button_btm[4].clicked.connect(lambda: self.key_press('B'))
        self.letter_button_btm[5].clicked.connect(lambda: self.key_press('N'))
        self.letter_button_btm[6].clicked.connect(lambda: self.key_press('M'))
        self.letter_button_btm[7].clicked.connect(lambda: self.key_press('.'))
        self.letter_button_btm[8].clicked.connect(lambda: self.key_press('-'))
        self.letter_button_btm[9].clicked.connect(lambda: self.key_press('Del'))

        keyboard_layout.addLayout(number_layout)
        keyboard_layout.addLayout(letter_layout_top)
        keyboard_layout.addLayout(letter_layout_mid)
        keyboard_layout.addLayout(letter_layout_btm)

    def key_press(self, key_):
        # print(key_)
        # self.input_content.emit(key_)
        if key_.lower() == 'del':
            print('delete')
            self.where_to_input.setText(self.where_to_input.text()[:-1])
        elif key_.lower() == 'enter':
            self.deleteLater()
        else:
            self.where_to_input.setText(self.where_to_input.text() + key_)

    # def closeEvent(self, QCloseEvent):
    #     self.setFocusPolicy(Qt.StrongFocus)


class TestMain(QWidget):

    def __init__(self):
        super(TestMain, self).__init__()
        layout = QVBoxLayout(self)

        self.input_ = MyLineEdit()
        self.input_2 = QLineEdit(self)
        layout.addWidget(self.input_)
        layout.addWidget(self.input_2)

        self.input_.clicked.connect(lambda: self.ppp(self.input_))


    def ppp(self, who):

        self.input_keyboard = VirtualKeyboard(who)
        self.input_keyboard.show()


class MyLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self):
        super(MyLineEdit, self).__init__()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
        super(MyLineEdit, self).mousePressEvent(QMouseEvent)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = TestMain()
    win.show()
    sys.exit(app.exec_())
