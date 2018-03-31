# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRC16IBM - A001 - MODBUS
"""
from PyCRC.CRC16 import CRC16


def crc(input_date):
    """

    :param input_date:
    :return:
    """
    crc_tool = CRC16(modbus_flag=True)
    try:
        data_b = bytes.fromhex(input_date)
    except (ValueError, TypeError):
        print('参数错误')
    except Exception:
        print(' ')
    else:
        crc_code = crc_tool.calculate(data_b)
        crc_high = hex(crc_code >> 8)[2:]
        crc_low = hex(crc_code & 0x00ff)[2:]
        result = input_date + ' ' + crc_low + ' ' + crc_high
        return result.upper()


def crc_check(return_data):
    """

    :param return_data:
    :return:
    """
    try:
        _ = bytes.fromhex(return_data)
    except (TypeError, ValueError):
        print('参数错误')
        return False

    if crc(return_data[:-6].upper()) == return_data.upper():
        return True
    else:
        return False


if __name__ == '__main__':

    # cmd = '01 06 01 00'
    ret = '01 5B 14 12 03 1F 80 CA'
    # print(crc(cmd))
    print(crc_check(ret))
