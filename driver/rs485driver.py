# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.1)

print('serial test start ...')
ser.write(bytes("\n Waiting for message...\n", 'utf-8'))
try:
    while True:
        msg = ser.readall()
        print(msg)
        # print(type(msg))
        ser.write(msg)
except KeyboardInterrupt:
    if ser != None:
        ser.close()