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
    server_url = "http://192.168.0.31:8181/kldpro/autodetect/setaddress"
    jsondata = {'name': 'TE1', 'ip': '192.168.0.34', 'port': 2332}
    postdata = {'jsondata': str(jsondata)}
    r = requests.post(url=server_url, data=postdata)
    return r.text


if __name__ == '__main__':
    print(register_in_server())
