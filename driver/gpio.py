# !/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
introduction
"""


from driver import wiringpi as wp

#
INPUT = 0
OUTPUT = 1

LOW = 0
HIGH = 1

# 物理引脚
INT_PIN = 36


def init_gpio():
    """
    初始化gpio口
    :return:
    """
    # Set up the wiringpi object to use physical pin numbers
    wp.wiringPiSetupPhys()

    #
    wp.pinMode(INT_PIN, INPUT)
    # wp.digitalWrite(CS_PIN, HIGH)

    # 中断注册
    print('INT: ')
    print(wp.wiringPiISR(INT_PIN, wp.INT_EDGE_FALLING, int_from_pca9535))


def int_from_pca9535():
    """
    中断处理函数
    :return:
    """

    pass


def reset_pca9548():
    """
    RESET
    :return:
    """
    pass
