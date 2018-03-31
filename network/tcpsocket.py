# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试仪作为服务器等待客户端请求并作出相应的回复
暂未实现自动连续向客户端发送数据
"""

from socketserver import BaseRequestHandler, TCPServer

from public.datacache import SoftwareData as sw


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
            print(msg)
            msgstr = msg.decode('utf-8')
            # 读取最新数据
            if msgstr[:2] == '00':
                print('RDATA', msgstr)
                self.ReadData(msgstr)
                pass
            # 读取历史数据
            elif msgstr[:2] == '01':
                print('RHDATA')
                self.ReadHistoryData(msgstr)
                pass
            # 连续读取最新数据
            elif msgstr[:2] == '02':
                print('RDATAC')
                self.read_data_continue(msgstr)
                pass
            # 停止连续读取最新数据
            elif msgstr[:2] == '03':
                print('SRDATAC')
                self.stop_read_data_continue(msgstr)
                pass
            # 停止向测试数据数组写入数据
            elif msgstr[:2] == '04':
                print('ARRAYF')
                self.array_fixed(msgstr)
                pass
            # 开始向测试数据数组写入数据
            elif msgstr[:2] == '05':
                print('ARRAYR')
                self.array_recovery(msgstr)
                pass
            # 读取状态字节
            elif msgstr[:2] == '06':
                print('RSTATE')
                self.ReadState(msgstr)
                pass
            # 清空数据
            elif msgstr[:2] == '07':
                print('CLEAN')
                self.CleanData(msgstr)
                pass
            # 读取控制方式
            elif msgstr[:2] == '08':
                print('READC')
                self.ReadControlMode(msgstr)
                pass
            # 设置控制方式
            elif msgstr[:2] == '09':
                print('SETC')
                self.SetControlMode(msgstr)
                pass
            # 设置电压
            elif msgstr[:2] == '0A':
                print('SETU')
                self.SetVoltage(msgstr)
                pass
            # 读取变量sp
            elif msgstr[:2] == '0B':
                print('RSP')
                self.ReadSP(msgstr)
                pass
            # 控制阀门
            elif msgstr[:2] == '0C':
                print('CONTROL')
                self.ControlValve(msgstr)
                pass
            # 输入错误
            else:
                print('错误命令')
                self.request.serial_send(b'error command')
                pass

    def ReadData(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        if msgstr[2:4] == '00':
            # 读电流
            self.request.serial_send(bytes('500mA', 'utf-8'))
            print('500mA')
            pass
        elif msgstr[2:4] == '01':
            # 读电压
            self.request.serial_send(bytes('12V', 'utf-8'))
            print('12v')
            pass
        elif msgstr[2:4] == '02':
            self.request.serial_send(bytes('500mA 12V', 'utf-8'))
            print('500mA 12v')
            # 读电流和电压
            pass
        else:
            print('error')
            self.request.serial_send(bytes('error', 'utf-8'))

    def ReadHistoryData(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        try:
            start = msgstr[2:6]
            lengh = msgstr[6:10]
            data = sw.current_value[int(start):int(start) + int(lengh)]
            self.request.serial_send(bytes(str(data), 'utf-8'))
        except:
            self.request.serial_send(b'error 01')
        pass

    def read_data_continue(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def stop_read_data_continue(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def array_fixed(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def array_recovery(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def ReadState(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes('state ' + msgstr, 'utf-8'))
        pass

    def CleanData(self, msgstr):
        """

        :param msgstr:
        :return:
        """

        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def ReadControlMode(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes('BD3S', 'utf-8'))
        pass

    def SetControlMode(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def SetVoltage(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass

    def ReadSP(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes('5555', 'utf-8'))
        pass

    def ControlValve(self, msgstr):
        """

        :param msgstr:
        :return:
        """
        self.request.serial_send(bytes(msgstr, 'utf-8'))
        pass
