# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更改树莓派的eth0网卡设置
功能：1 使用静态ip， 2 使用DHCP， 3 设置IP 等
实现方式：直接更改/etc/dhcpcd.conf文件
注意：更改后需要重启树莓派更新设置
"""

import re
import os

ip_cfg_file = 'dhcpcd.conf'

re_ip = r'^static\sip_address'
re_router = r'^static\srouters'
re_dns = r'^static\sdomain_name_servers'

re_eth0 = r'^#interface\seth0'
re_eth0_1 = r'^interface\seth0'
re_static = r'^#static\sip_address'


def set_dhcp_ip():
    """
    网络设置为自动获取IP
    :return:
    """
    with open(ip_cfg_file) as f:
        # 文件读取到列表
        temp = f.readlines()
        for j in range(len(temp)):
            # 匹配 interface eth0
            match = re.match(re_eth0_1, temp[j])
            if match:
                # 匹配 static ip_address
                match2 = re.match(re_ip, temp[j + 1])
                if match2:
                    # 注释掉相应行
                    for k in range(5):
                        temp[j + k] = '#' + temp[j + k]
                    break

    with open(ip_cfg_file, 'w') as f:
        for j in temp:
            f.write(j)


def set_static_ip():
    """
    网络设置为使用静态IP
    :return:
    """
    with open(ip_cfg_file) as f:
        temp = f.readlines()
        for j in range(len(temp)):
            match = re.match(re_eth0, temp[j])
            if match:
                match2 = re.match(re_static, temp[j + 1])
                if match2:
                    for k in range(5):
                        temp[j + k] = temp[j + k][1:]
                    break

    with open(ip_cfg_file, 'w') as f:
        for j in temp:
            f.write(j)


def net_config(ip, router, dns):
    """
    设置静态IP
    :param ip:  str) ip address
    :param router: str
    :param dns: str
    :return:
    """
    if not isinstance(ip, str):
        return 0
    temp = list()
    with open(ip_cfg_file, 'r') as f:
        temp = f.readlines()
        for j in range(len(temp)):
            match_ip = re.match(re_ip, temp[j])
            if match_ip:
                temp[j] = 'static ip_address=' + ip + '/24\n'
                temp[j + 2] = 'static routers=' + router + '\n'
                temp[j + 3] = 'static domain_name_servers=' + dns + ' 8.8.8.8 fd51:42f8:caae:d92e::1\n'
                break
    with open(ip_cfg_file, 'w') as f:
        for j in temp:
            f.write(j)
    pass


if __name__ == '__main__':
    # net_config('192.168.11.194', '192.168.11.1', '192.168.0.222')
    # set_dhcp_ip()
    while True:
        print('1 dhcp'
              '2 static')
        a = input('please choose ...')
        if a == '1':
            set_dhcp_ip()
        if a == '2':
            set_static_ip()
