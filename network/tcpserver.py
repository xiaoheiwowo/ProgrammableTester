# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试仪作为服务器等待客户端请求并作出相应的回复
暂未实现自动连续向客户端发送数据
"""
import sys
import time
import random
import pickle
import threading
from socketserver import BaseRequestHandler, TCPServer

sys.path.append('..')

from public.datacache import SoftwareData as sw
from public.datacache import HardwareData as hw
from public.datacache import DataForServer as ds

host = 'localhost'
port = 21567


class TcpHandler(BaseRequestHandler):
    """
    服务器消息处理
    """

    def handle(self):
        """

        :return:
        """

        print('Get connection from: ', self.client_address)
        while True:
            msg = self.request.recv(1024)
            if not msg:
                break
            # self.request.send(b'GET\n')
            debug_print(str(msg))
            msgstr = msg.decode('utf-8')
            # 读取最新数据
            if msgstr[:2] == '00':
                debug_print('RDATA')
                self.ReadData(msgstr)
                pass
            # 读取历史数据
            elif msgstr[:2] == '01':
                debug_print('RHDATA')
                self.ReadHistoryData(msgstr)
                pass
            # 连续读取最新数据
            elif msgstr[:2] == '02':
                debug_print('RDATAC')
                self.read_data_continue(msgstr)
                pass
            # 停止连续读取最新数据
            elif msgstr[:2] == '03':
                debug_print('SRDATAC')
                self.stop_read_data_continue(msgstr)
                pass
            # 停止向测试数据数组写入数据
            elif msgstr[:2] == '04':
                debug_print('ARRAYF')
                self.array_fixed(msgstr)
                pass
            # 开始向测试数据数组写入数据
            elif msgstr[:2] == '05':
                debug_print('ARRAYR')
                self.array_recovery(msgstr)
                pass
            # 读取状态字节
            elif msgstr[:2] == '06':
                debug_print('RSTATE')
                self.ReadState(msgstr)
                pass
            # 清空数据
            elif msgstr[:2] == '07':
                debug_print('CLEAN')
                self.CleanData(msgstr)
                pass
            # 读取控制方式
            elif msgstr[:2] == '08':
                debug_print('READC')
                self.ReadControlMode(msgstr)
                pass
            # 设置控制方式
            elif msgstr[:2] == '09':
                debug_print('SETC')
                self.SetControlMode(msgstr)
                pass
            # 设置电压
            elif msgstr[:2] == '0A':
                debug_print('SETU')
                self.SetVoltage(msgstr)
                pass
            # 读取变量sp
            elif msgstr[:2] == '0B':
                debug_print('RSP')
                self.ReadSP(msgstr)
                pass
            # 控制阀门
            elif msgstr[:2] == '0C':
                debug_print('CONTROL')
                self.ControlValve(msgstr)
                pass
            # 输入错误
            else:
                debug_print('错误命令')
                self.request.send(b'CMD ERROR')
                pass

    def ReadData(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        if msgstr[2:4] == '00':
            # 读电流
            self.request.send(bytes('500mA', 'utf-8'))
            debug_print('500mA')
            pass
        elif msgstr[2:4] == '01':
            # 读电压
            self.request.send(bytes('12V', 'utf-8'))
            debug_print('12v')
            pass
        elif msgstr[2:4] == '02':
            cur = ds.current_value[-1]
            vol = ds.voltage_value
            self.request.send(bytes(str(cur)+' '+str(vol), 'utf-8'))
            debug_print('500mA 12v')
            # 读电流和电压
            pass
        else:
            debug_print('CMD ERROR')
            self.request.send(bytes('CMD ERROR', 'utf-8'))

    def ReadHistoryData(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        try:
            start = msgstr[2:6]
            length = msgstr[6:10]
            data = ds.current_value[int(start):int(start) + int(length)]
            self.request.send(bytes(str(data), 'utf-8'))
        except:
            self.request.send(b'error 01')
        pass

    def read_data_continue(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def stop_read_data_continue(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def array_fixed(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def array_recovery(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def ReadState(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes('state ' + msgstr, 'utf-8'))
        pass

    def CleanData(self, msgstr):
        """

        :param msgstr:
        :return:
        """

        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def ReadControlMode(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        control = ds.control_mode
        self.request.send(bytes(str(control), 'utf-8'))
        pass

    def SetControlMode(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def SetVoltage(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass

    def ReadSP(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes('5555', 'utf-8'))
        pass

    def ControlValve(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.send(bytes(msgstr, 'utf-8'))
        pass


class TcpThread(threading.Thread):
    """
    TCP线程，在此线程内接收请求并处理
    """

    def __init__(self):
        super(TcpThread, self).__init__()
        print('TCP Thread Run ...')

    def run(self):
        """

        :return:
        """
        remote_control_server = TCPServer((host, port), TcpHandler)
        remote_control_server.serve_forever()


def debug_print(string):
    """
    debug
    :param string:
    :return:
    """

    # print('DEBUG [ ' + string + ' ]')
    pass


def data_init():
    """
    数据初始化
    :return:
    """
    # 电流值采样列表初始化为0
    ds.current_value = list()
    for j in range(sw.current_set['data_depth']):
        ds.current_value.append(0)

    ds.voltage_value = 0
    ds.sp = 0


def read_file():
    """

    :return:
    """
    with open('../pkl/controlmode.pkl', 'rb') as f:
        ds.control_mode = pickle.loads(f.read())


if __name__ == '__main__':
    data_init()
    read_file()
    # 启动tcp server线程
    tcp_thread = TcpThread()
    tcp_thread.start()
    while True:
        time.sleep(1)
        ds.current_value.pop(0)
        ds.current_value.append(round(random.random() * 100))
        ds.voltage_value = round(random.random()*10)
        pass
