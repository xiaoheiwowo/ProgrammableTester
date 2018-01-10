# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局静态类
"""


class SoftwareData(object):
    """
    软件数据缓存区
    """
    # 当前选择行
    select_line = None
    # 控制方式数据模版
    ControlForm = {'NAME': ' ',
                   'POWER': 0,
                   'ON': [],
                   'OFF': [],
                   'STOP': [],
                   'M3': [],
                   'M4': [],
                   'SPECIAL': 0,
                   'SIGNAL': 0,
                   'EFFECT': 0,
                   'PROTOCOL': 0,
                   'BAUDRATE': 0}

    # 控制方式数据
    control_mode = []

    # 总线阀
    cmd_on = '01 06 00 04 00 00 C8 0B'
    cmd_off = '01 06 00 04 00 64 C9 E0'
    cmd_stop = '01 06 00 04 00 BA 49 B8'
    cmd_m3 = '01 06 00 04 00 1E 48 03'
    cmd_m4 = '01 06 00 04 00 B3 89 BE'
    data_bits = 3
    check_bits = 1
    stop_bits = 1

    bus_control = ['01 06 00 04 00 00 C8 0B',
                   '01 06 00 04 00 64 C9 E0',
                   '01 06 00 04 00 BA 49 B8',
                   '01 06 00 04 00 1E 48 03',
                   '01 06 00 04 00 B3 89 BE',
                   3,
                   0,
                   0]

    bus_control_bak = ['01 06 00 04 00 00 C8 0B',
                       '01 06 00 04 00 64 C9 E0',
                       '01 06 00 04 00 BA 49 B8',
                       '01 06 00 04 00 1E 48 03',
                       '01 06 00 04 00 B3 89 BE',
                       3,
                       0,
                       0]

    # 电流数据
    current_valve = [75, 59, 10, 34, 6, 0, 1, 6, 49, 74, 17, 47, 89, 24, 41, 27, 6, 37, 61, 64,
                     88, 63, 4, 90, 95, 28, 24, 2, 21, 41, 53, 74, 40, 51, 10, 95, 23, 74, 58,
                     1, 28, 82, 65, 56, 42, 96, 65, 9, 61, 49, 14, 69, 33, 5, 88, 40, 15, 87,
                     28, 25, 36, 49, 80, 19, 35, 4, 2, 96, 63, 18, 94, 93, 72, 2, 16, 98, 34,
                     15, 72, 27, 97, 31, 62, 2, 95, 74, 87, 67, 9, 43, 86, 44, 87, 16, 87, 77,
                     4, 70, 40, 56, 26, 36, 31, 14, 22, 88, 13, 53, 96, 60, 63, 99, 93, 81, 49,
                     29, 25, 91, 0, 99, 88, 32, 95, 24, 57, 43, 71, 32, 51, 94, 80, 28, 15, 10,
                     94, 81, 91, 81, 98, 39, 40, 19, 50, 40, 76, 62, 71, 33, 61, 99, 0, 49, 52,
                     31, 97, 43, 74, 71, 65, 50, 45, 36, 21, 86, 96, 4, 73, 32, 13, 11, 80, 49,
                     91, 44, 31, 27, 56, 96, 84, 24, 17, 34, 4, 91, 46, 61, 34, 31, 94, 78, 53,
                     91, 63, 57, 90, 59, 95, 88, 28, 4]

    static_current_valve = []

    # doubleslider 最小滑块间距
    sliders_interval_min = 40

    # 服务器测试
    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
             20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
             40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
             60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
             80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

    # 电流曲线设置
    current_set = {'data_depth': 100,
                   'data_interval': 10,
                   'data_time': 100.555,
                   'small_win_show_time': 20}

    # 本机&上位机
    net_set = {'host_name': 'pc',
               'auto_ip': True,
               'host_ip': '192.168.10.33',
               'subnet_mask': '255.255.255.0',
               'default_gateway': '192.168.10.1',
               'dns': '192.168.10.222',
               'upper_name': 'upper',
               'upper_ip': '192.168.10.8'}

    upper_ip_list = ['192.168.10.101',
                     '192.168.10.102',
                     '192.168.10.103',
                     '192.168.10.104',
                     '192.168.10.105']

    upper_name_list = ['Valve Test 1',
                       'Valve Test 2',
                       'Valve Test 3',
                       'Valve Test 4',
                       'Valve Test 5']

    # 开机默认设置
    control_set_bak = {'use_blank': True}

    # 电源采样校准数据
    data_list = {'acv': [[0,   '0x0000', 0],
                         [100, '0x5555', 101],
                         [200, '0xAAAA', 202],
                         [300, '0xFFFF', 303]],

                 'aca': [[0,   '0x0000', 0],
                         [100, '0x5555', 1],
                         [200, '0xAAAA', 2],
                         [300, '0xFFFF', 3]],

                 'dcv': [[0,  '0x0000', 0],
                         [10, '0x5555', 11],
                         [20, '0xAAAA', 22],
                         [30, '0xFFFF', 33]],

                 'dca': [[0, '0x0000', 0],
                         [1, '0x5555', 1],
                         [2, '0xAAAA', 2],
                         [3, '0xFFFF', 3]]}

    data = {'control_set_bak': {'use_blank': True},
            'current_valve': current_valve}


class HardwareData(object):
    """
    硬件数据缓存区
    """
    i2c_data = []
    spi_data = []
    uart_data = []

    control_mode = ['none', 0]
    voltage = 'none'

    open_by_i2c = []
    close_by_i2c = []
    stop_by_i2c = []
    m3_by_i2c = []
    m4_by_i2c = []

    open_by_spi = []
    close_by_spi = []
    stop_by_spi = []
    m3_by_spi = []
    m4_by_spi = []
    control_by_spi = []
    return_from_valve = []

    open_by_uart = []
    close_by_uart = []
    stop_by_uart = []
    m3_by_uart = []
    m4_by_uart = []