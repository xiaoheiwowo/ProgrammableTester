# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向服务器发送http请求， 包含本机ip，端口，地址。
"""
import requests


def register_in_server():
    """

    :return:
    """
    server_url = "http://192.168.0.32:8080/kldpro/autodetect/setaddress"
    json_data = {'name': 'TE1', 'ip': '192.168.0.32', 'port': 9955}
    post_data = {'jsondata': str(json_data)}
    r = requests.post(url=server_url, data=post_data)
    return r.text


if __name__ == '__main__':
    print(register_in_server())
