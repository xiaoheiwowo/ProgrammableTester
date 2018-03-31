# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time


class PiSerial(object):
    """
    in
    """
    def serial_init(self):
        """

        :return:
        """
        self.ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.1)
        self.ser.write(bytes("\n Waiting for message...\n", 'utf-8'))

    def serial_send(self, msg_str):
        """

        :return:
        """
        try:
            msg_b = bytes.fromhex(msg_str)
            self.ser.write(msg_b)
        except ValueError:
            print('命令错误')

    def serial_receive(self):
        """

        :return:
        """

        return bytes.hex(self.ser.readall())

    def serial_close(self):
        """

        :return:
        """
        self.ser.close()


if __name__ == '__main__':
    print('serial test start ...')
    my_ser = PiSerial()
    while True:
        time.sleep(0.1)
        try:
            # cmd = input('IN\n')
            msg = my_ser.serial_receive()
            print(str(msg.decode()))
            my_ser.serial_send(msg)
        except KeyboardInterrupt:
            break

    my_ser.serial_close()