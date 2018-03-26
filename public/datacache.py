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
    control_mode_selected = {}

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
    current_value = []

    # 静态电流曲线的列表
    static_current_value = []

    # double slider 最小滑块间距
    sliders_interval_min = 40

    # 服务器测试
    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
             20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
             40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
             60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
             80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

    # 电流曲线设置
    current_set = {'data_depth': 10000,
                   'data_interval': 10,
                   'data_time': 1000,
                   'small_win_show_time': 20}

    # 本机&上位机
    net_set = {'host_name': 'pc',
               'auto_ip': True,
               'host_ip': '192.168.10.33',
               'subnet_mask': '255.255.255.0',
               'default_gateway': '192.168.10.1',
               'dns': '192.168.10.222',
               'upper_name': 'upper',
               'upper_ip': '192.168.10.8',
               'server_ip': '192.168.0.112'}
    # 上位机ip
    upper_ip_list = ['192.168.10.101',
                     '192.168.10.102',
                     '192.168.10.103',
                     '192.168.10.104',
                     '192.168.10.105']
    # 上位机名称
    upper_name_list = ['Valve Test 1',
                       'Valve Test 2',
                       'Valve Test 3',
                       'Valve Test 4',
                       'Valve Test 5']

    # 开机默认设置
    control_set_bak = {'use_blank': True}

    # 电源采样校准数据
    data_list = {'acv': [[0, '0x0000', 0],
                         [100, '0x5555', 101],
                         [200, '0xAAAA', 202],
                         [300, '0xFFFF', 303]],

                 'aca': [[0, '0x0000', 0],
                         [100, '0x5555', 1],
                         [200, '0xAAAA', 2],
                         [300, '0xFFFF', 3]],

                 'dcv': [[0, '0x0000', 0],
                         [10, '0x5555', 11],
                         [20, '0xAAAA', 22],
                         [30, '0xFFFF', 33]],

                 'dca': [[0, '0x0000', 0],
                         [1, '0x5555', 1],
                         [2, '0xAAAA', 2],
                         [3, '0xFFFF', 3]]}

    data = {'control_set_bak': {'use_blank': True},
            'current_valve': current_value}

    # 自动测试设定的开阀时间和关阀时间
    open_time = 0
    close_time = 0


class HardwareData(object):
    """
    硬件数据缓存区
    """
    # i2c_data = []
    # spi_data = []
    # uart_data = []
    #
    # open_by_i2c = []
    # close_by_i2c = []
    # stop_by_i2c = []
    # m3_by_i2c = []
    # m4_by_i2c = []
    #
    # open_by_spi = []
    # close_by_spi = []
    # stop_by_spi = []
    # m3_by_spi = []
    # m4_by_spi = []
    # control_by_spi = []
    # return_from_valve = []
    #
    # open_by_uart = []
    # close_by_uart = []
    # stop_by_uart = []
    # m3_by_uart = []
    # m4_by_uart = []

    # 主界面上选择的控制方式和电压值
    control_mode = {'NAME': ' ',
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
    voltage = None

    # 总线阀的命令
    bus_cmd = '01 06 00 04 00 00 C8 0B'

    # 主界面上显示的电压值和电流值以及到位信号
    current_value_show = '  '
    voltage_value_show = '  '
    open_signal = 'YES'
    close_signal = 'NO'

    # 主界面上调节阀选项卡中显示的反馈信号
    adjust_valve_back = ''

    delay_array_state = ['0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000',
                         '0000000000000000']
    delay_test_state = ['0000000000000000'
                        '0000000000']

    extend_io_state = ['0000000000000000']

    # 扩展io口
    extend_in = []
    extend_out = [0x00, 0x00]

    # [SX00-SX09:[p0, p1] ]
    # 按照芯片排序 第一个列表中的两字节数据分别对应芯片SX00的P0和P1
    # register_port = [[0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00],
    #                  [0x00, 0x00]]

    # 按照继电器排序，第一个列表中的两字节对应继电器阵列第一行的继电器
    # delay_array = [[0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00],
    #                [0x00, 0x00]]

    pass
    # 自检继电器的
    ZJ00 = [0x00, 0x00]
    ZJ01 = [0x00, 0x00]

    # 电源调节修正参数
    correct_ac = 5 / 5.11
    correct_dc = 5 / 5.08


class DataForServer(object):
    """
    server data
    """

    # 电流数据
    current_value = []

    # 电压数据
    voltage_value = None

    # 电流数据指针sp
    sp = None


class Flag_Of(object):
    """
    标志位
    """

    # 继电器自检标志位
    relay_check = 0

    # 按键中断标志位
    button_int = 0

    # 控制方式和电压锁定标志位
    control_mode_lock = 0

    # 更新主界面电压电流值及到位信号标志位
    update_va_value = 0

    # 控制方式
    control_mode = []
