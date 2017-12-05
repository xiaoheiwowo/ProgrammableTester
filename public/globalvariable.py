

class GlobalVariable(object):
    """
    全局变量
    """
    # 当前选择行
    select_line = None
    # 控制方式数据模版
    ControlForm = {'NAME': ' ', 'POWER': 0, 'ON': [], 'OFF': [], 'STOP': [], 'M3': [], 'M4': [],
                   'SPECIAL': 0, 'SIGNAL': 0, 'EFFECT': 0, 'PROTOCOL': 0, 'BAUDRATE': 0}

    # 控制方式数据
    control_mode = []

    # 总线阀
    cmd_on = '01 06 00 04 00 00 C8 0B'
    cmd_off = '01 06 00 04 00 64 C9 E0'
    cmd_stop = '01 06 00 04 00 BA 49 B8'
    cmd_m3 = '01 06 00 04 00 1E 48 03'
    cmd_m4 = '01 06 00 04 00 B3 89 BE'
    data_bits = 8
    check_bits = None
    stop_bits = 1

    bus_control_bak = ['01 06 00 04 00 00 C8 0B',
                       '01 06 00 04 00 64 C9 E0',
                       '01 06 00 04 00 BA 49 B8',
                       '01 06 00 04 00 1E 48 03',
                       '01 06 00 04 00 B3 89 BE',
                       8, None, 1]

