# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插值计算
"""

data_test = [[0, 0.001, 0],
             [300, 3.000, 303]]


def calculate(input_data, refer_data):
    """

    :param input_data: float 采样值
    :param refer_data: list 校准数据表
    :return:
    """
    i = 0
    for i in range(len(refer_data)):
        if input_data <= refer_data[i][1]:
            break

    x_1, y_1 = float(refer_data[i][1]), float(refer_data[i][2])
    x_2, y_2 = float(refer_data[i - 1][1]), float(refer_data[i - 1][2])
    x = float(input_data)

    y = (y_2 - y_1)*(x - x_1) / (x_2 - x_1) + y_1

    if y < 0:
        return 0
    else:
        return round(y, 3)
    pass


if __name__ == '__main__':
    print(calculate(2, data_test))
