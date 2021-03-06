# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial.tools.list_ports
import serial
import time


class WinSerial(object):
    """
    in
    """
    def __init__(self):
        self.ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.2)
        self.ser.write(bytes("\n Waiting for message...\n", 'utf-8'))

    def serial_send(self, msg_str):
        """

        :return:
        """

        self.ser.write(msg_str)

    def serial_receive(self):
        """

        :return:
        """
        return self.ser.readall()

    def serial_close(self):
        """

        :return:
        """
        self.ser.close()


if __name__ == '__main__':
    print('serial test start ...')
    my_ser = WinSerial()
    while True:
        time.sleep(0.1)
        try:
            # cmd = input('IN\n')
            msg = my_ser.serial_receive()
            if msg:
                print(bytes.hex(msg))
            my_ser.serial_send(msg)
        except KeyboardInterrupt:
            break

    my_ser.serial_close()
