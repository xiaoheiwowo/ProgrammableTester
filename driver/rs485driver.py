# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.1)

print('serial test start ...')
ser.write(bytes("\n Waiting for message...\n", 'utf-8'))
ser.write(b'0xff')

try:
    while True:
        msg = ser.readall()
        msgstr = msg.decode('utf-8')
        if msgstr:
            print(msgstr)
        ser.write(msg)
except KeyboardInterrupt:
    if ser != None:
        ser.close()