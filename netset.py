# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
introduction
"""
import os
import socket
from socket import gethostbyname, gethostname

host = gethostbyname(gethostname())
# 命令行模式
os.system('arp -a > net_temp.txt')
with open('net_temp.txt') as fp:
    for line in fp:
        line = line.split()[:2]

socket.gethostbyaddr()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('192.168.10.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
