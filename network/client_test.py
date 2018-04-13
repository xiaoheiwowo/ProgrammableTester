# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
import socket
import time


# 命令字节
cmd_rdata = '00'
cmd_rhdata = '01'
cmd_rdatac = '02'
cmd_srdatac = '03'
cmd_arrayf = '04'
cmd_arrayr = '05'
cmd_rstate = '06'
cmd_clean = '07'
cmd_readc = '08'
cmd_setc = '09'
cmd_setu = '0A'
cmd_rsp = '0B'
cmd_control = '0C'

# 功能字节
fun_read_i = '00'
fun_read_u = '01'
fun_read_both = '02'

fun_dc = '00'
fun_ac = '01'

fun_open = '00'
fun_close = '01'
fun_stop = '02'

# 本地主机名
host = 'localhost'
# 设置端口
port = 21567
# 缓存大小
buf = 10000


class ClientTest(QtWidgets.QWidget):
    """
    测试客户端
    """

    def __init__(self):
        super(ClientTest, self).__init__()
        self.setWindowTitle('测试客户端')
        self.resize(500, 800)
        # self.setFixedWidth(500)

        # 建立socket
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect((host, port))

        layout_bt = QtWidgets.QVBoxLayout(self)

        list_bt = list()
        for i in range(13):
            list_bt.append(QtWidgets.QPushButton(self))
            list_bt[i].setText('Button ' + str(i))
            list_bt[i].setFixedHeight(40)
            layout_bt.addWidget(list_bt[i])

        self.lb_return = QtWidgets.QLabel(self)
        self.lb_return.setText('返回数据：')
        self.lb_return.setAlignment(QtCore.Qt.AlignTop)
        self.lb_return.setWordWrap(True)

        layout_bt.addWidget(self.lb_return)
        self.bt = QtWidgets.QPushButton()
        # self.bt.setFixedHeight()
        # self.bt.setText('333333')
        # self.bt.setGeometry(100, 100, 100, 100)

        list_bt[0].setText('读取最新数据')
        list_bt[1].setText('读取历史数据')
        list_bt[2].setText('连续读取最新数据')
        list_bt[3].setText('停止连续读取最新数据')
        list_bt[4].setText('停止向测试数据数组写入数据')
        list_bt[5].setText('开始向测试数据数组写入数据')
        list_bt[6].setText('读取状态字节')
        list_bt[7].setText('清空数据')
        list_bt[8].setText('读取控制方式')
        list_bt[9].setText('设置控制方式')
        list_bt[10].setText('设置电压')
        list_bt[11].setText('读取变量sp')
        list_bt[12].setText('控制阀门运动或停止')

        list_bt[0].clicked.connect(self.press_bt0)
        list_bt[1].clicked.connect(self.press_bt1)
        list_bt[2].clicked.connect(self.press_bt2)
        list_bt[3].clicked.connect(self.press_bt3)
        list_bt[4].clicked.connect(self.press_bt4)
        list_bt[5].clicked.connect(self.press_bt5)
        list_bt[6].clicked.connect(self.press_bt6)
        list_bt[7].clicked.connect(self.press_bt7)
        list_bt[8].clicked.connect(self.press_bt8)
        list_bt[9].clicked.connect(self.press_bt9)
        list_bt[10].clicked.connect(self.press_bta)
        list_bt[11].clicked.connect(self.press_btb)
        list_bt[12].clicked.connect(self.press_btc)

    @staticmethod
    def client_send(_data):
        """

        :param _data:
        :return:
        """

        # 建立socket
        client_socket = socket.socket()

        # 连接服务，指定主机和端口
        client_socket.connect((host, port))

        # 发送数据
        client_socket.send(bytes(_data, 'utf-8'))

        time.sleep(1)
        # 接收小于 1024 字节的数据
        msg = client_socket.recv(buf)

        # 关闭socket
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()

        return msg.decode('utf-8')
        # print(msg.decode('utf-8'))

    def return_data(self, massage):
        """

        :param massage:
        :return:
        """
        self.lb_return.setText('返回数据： ' + str(massage))

    def press_bt0(self):
        """
        读取最新数据
        :return:
        """
        msg = self.client_send(cmd_rdata + fun_read_both)
        self.return_data(msg)
        pass

    def press_bt1(self):
        msg = self.client_send(cmd_rhdata + '00000100')
        self.return_data(msg)

    def press_bt2(self):
        msg = self.client_send(cmd_rdatac + '02')
        self.return_data(msg)

    def press_bt3(self):
        msg = self.client_send(cmd_srdatac)
        self.return_data(msg)

    def press_bt4(self):
        msg = self.client_send(cmd_arrayf)
        self.return_data(msg)

    def press_bt5(self):
        msg = self.client_send(cmd_arrayr)
        self.return_data(msg)

    def press_bt6(self):
        msg = self.client_send(cmd_rstate)
        self.return_data(msg)

    def press_bt7(self):
        msg = self.client_send(cmd_clean)
        self.return_data(msg)

    def press_bt8(self):
        msg = self.client_send(cmd_readc)
        self.return_data(msg)

    def press_bt9(self):
        msg = self.client_send(cmd_setc)
        self.return_data(msg)

    def press_bta(self):
        msg = self.client_send(cmd_setu)
        self.return_data(msg)

    def press_btb(self):
        msg = self.client_send(cmd_rsp)
        self.return_data(msg)

    def press_btc(self):
        msg = self.client_send(cmd_control + fun_open)
        self.return_data(msg)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ClientTest()
    win.show()
    sys.exit(app.exec_())
    pass
