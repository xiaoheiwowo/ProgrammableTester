# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
在新进程中运行adda程序。通过queue与主进程通讯
"""
import random
import time
from multiprocessing import Process, Queue

from driver.spi import SPI_Driver
from PyQt5.QtCore import QThread, pyqtSignal
from public.datacache import HardwareData as hw
from public.datacache import Flag_Of as flag
from threading import Thread, Lock


class AD_DA_2(QThread):
    # 通道开关
    read_channel = [0, 0, 0, 0, 0]
    write_channel = [0, 0, 0, 0]

    # 当前ad通道
    current_ad_channel = 5

    cmd_list = [['FK', 0],
                ['ACA', 0],
                ['ACV', 0],
                ['DCA', 0],
                ['DCV', 0],
                ['ACP', 0],
                ['DCP', 0],
                ['TI', 0],
                ['TV', 0]]

    def __init__(self):
        super(AD_DA_2, self).__init__()
        self.cmd_queue = Queue()
        self.data_queue = Queue()

        print('ADDA Thread Run ...')
        self.process = ADDA_Process(self.cmd_queue, self.data_queue)
        self.process.start()

        # 防止父线程和子线程同时使用queue发生冲突
        # self.lock_for_queue = Lock()

    def run(self):
        """

        :return:
        """
        # self.cmd_queue.put(['ACP', 0])
        # self.cmd_queue.put(['DCP', 0])
        # self.cmd_queue.put(['TI', 0])
        # self.cmd_queue.put(['TV', 0])

        while True:
            time.sleep(1)
            if not self.cmd_queue.empty():
                self.cmd_into_queue(['ACI', 0])
            if not self.data_queue.empty():
                a = self.data_queue.get()
                print(a)

    def close_process(self):
        """

        :return:
        """
        self.process.terminate()

    def cmd_into_queue(self, cmd):
        """

        :return:
        """
        if isinstance(cmd, list):
            # with self.lock_for_queue:
            self.cmd_queue.put(cmd)
        else:
            print('error')

    def read_ad(self, _ch):
        """

        :return:
        """
        # with self.lock_for_queue:
        # self.cmd_queue.put(self.cmd_list[_ch])
        #
        # time_mark = time.time()
        # while True:
        #     if time.time() - time_mark > 0.5:
        #         print('采样超时')
        #         break
        #     if not self.data_queue.empty():
        #         result = self.data_queue.get()
        #         if isinstance(result, list):
        #             return result[-1]
        #         elif isinstance(result, float):
        #             return result
        #         break
        pass

    def write_da(self, _ch, _value):
        """

        :param _ch:
        :param _value:
        :return:
        """
        # list_cmd = ['DCP', 'ACP', 'TI', 'TV']
        # cmd = [str(list_cmd[_ch]), _value]
        # self.cmd_into_queue(cmd)
        pass

    @staticmethod
    def calibrate_power(cal_list, vol):
        """

        :param cal_list:
        :param vol:
        :return:
        """
        # print(vol)
        for j in range(len(cal_list)):
            if cal_list[j] > vol:
                y_1, y_2 = j - 1, j
                x_1, x_2 = cal_list[j - 1], cal_list[j]
                x = vol
                y = (y_2 - y_1) * (x - x_1) / (x_2 - x_1) + y_1
                # print(y)
                return y


class ADDA_Process(Process):
    """
    ADDA_Process
    """

    def __init__(self, q_cmd, q_data):
        super(ADDA_Process, self).__init__()
        self.q_cmd = q_cmd
        self.q_data = q_data

    def run(self):
        """
        使用两个队列queue与主进程数据交换，cmd_queue是主进程发送命令的队列，data_queue是子进程将采样数据返回给主进程的队列
        :param q_cmd:
        :param q_data:
        :return:
        """

        print('ADDA Process Run ...')
        spi_driver = SPI_Driver()
        spi_driver.ads1256_cfg()

        q_cmd = self.q_cmd
        q_data = self.q_data

        dt_aci = list()
        dt_dci = list()
        dt_acv = 0
        dt_dcv = 0
        feedback = 0

        for j in range(100):
            dt_aci.append(0)
            dt_dci.append(0)

        while True:
            # time.sleep(0.005)
            print(time.time())
            spi_driver.ads1256_one_shot(0)
            feedback = round(spi_driver.ReadADC(), 3)

            # spi_driver.ads1256_one_shot(1)
            # dt_aci.append(round(spi_driver.ReadADC(), 3))
            # dt_aci.pop(0)
            #
            # spi_driver.ads1256_one_shot(2)
            # dt_acv = round(spi_driver.ReadADC(), 3)
            #
            # spi_driver.ads1256_one_shot(3)
            # dt_dci.append(round(spi_driver.ReadADC(), 3))
            # dt_dci.pop(0)
            #
            # spi_driver.ads1256_one_shot(4)
            # dt_dcv = round(spi_driver.ReadADC(), 3)

            if not q_cmd.empty():

                cmd = q_cmd.get()

                if cmd[0] == 'ACI':
                    q_data.put(dt_dci)
                elif cmd[0] == 'ACV':
                    q_data.put(dt_acv)
                elif cmd[0] == 'DCI':
                    q_data.put(dt_dci)
                elif cmd[0] == 'DCV':
                    q_data.put(dt_dcv)
                elif cmd[0] == 'FK':
                    q_data.put(feedback)
                elif cmd[0] == 'ACP':
                    spi_driver.output_ac_power(cmd[1])
                elif cmd[0] == 'DCP':
                    spi_driver.output_ac_power(cmd[1])
                elif cmd[0] == 'TI':
                    spi_driver.output_ac_power(cmd[1])
                elif cmd[0] == 'TV':
                    spi_driver.output_ac_power(cmd[1])
                else:
                    pass



class AD_DA(QThread):
    """
    ad da
    """

    # 通道开关
    read_channel = [0, 0, 0, 0, 0]
    write_channel = [0, 0, 0, 0]

    # 当前ad通道
    current_ad_channel = 5

    def __init__(self):
        super(AD_DA, self).__init__()
        self.spi_driver = SPI_Driver()
        print('ADDA Thread Run ...')

    def run(self):
        """

        :return:
        """

        self.spi_driver.ads1256_cfg()

        while True:
            time.sleep(0.1)
            if flag.control_mode_lock or flag.calibration_start:
                # AD
                for j in range(5):
                    if self.read_channel[j]:
                        # print(time.time())

                        if self.current_ad_channel != j:
                            self.spi_driver.ads1256_one_shot(j)
                            self.current_ad_channel = j
                        hw.ad_value[j] = self.spi_driver.ReadADC()

                        # print(time.time())
                        # print('AD' + str(j) + ': ' + str(hw.ad_value[j]))
                        # time.sleep(0.005)
                        self.read_channel[j] = 0

                for j in range(4):
                    if self.write_channel[j]:
                        self.__write_da(j)
                        self.write_channel[j] = 0

                # for j in range(5):
                #     self.ad_and_da.ads1256_one_shot(j)
                #     hw.ad_value[j] = self.ad_and_da.ReadADC()
                #     # print('AD' + str(j) + ': ' + str(hw.ad_value[j]))
                #     # time.sleep(0.005)

                # DA
                # print(hw.da_value)
                # self.spi_driver.output_dc_power(hw.da_value[0])
                # self.spi_driver.output_ac_power(hw.da_value[1])
            if not (flag.control_mode_lock or flag.calibration_start):
                time.sleep(1)
                self.spi_driver.output_dc_power(0)
                self.spi_driver.output_ac_power(0)
                self.spi_driver.output_adjust_v(0)
                self.spi_driver.output_adjust_i(0)

    def __write_da(self, _ch=4):
        """

        :param _ch:
        :return:
        """
        if _ch == 0:
            if hw.da_value[_ch] == 0:
                self.spi_driver.output_dc_power(0)
            else:
                self.spi_driver.output_dc_power(self.calibrate_power(hw.calibrate_list_dcp, hw.da_value[_ch]))
        elif _ch == 1:
            if hw.da_value[_ch] == 0:
                self.spi_driver.output_ac_power(0)
            else:
                self.spi_driver.output_ac_power(self.calibrate_power(hw.calibrate_list_acp, hw.da_value[_ch]))
        elif _ch == 2:
            vol = hw.da_value[_ch] / 4
            j = 0
            for j in range(6):
                if vol <= hw.calibrate_list_ti[j][1]:
                    break

            x_1, y_1 = float(hw.calibrate_list_ti[j][1]), float(hw.calibrate_list_ti[j][0])
            x_2, y_2 = float(hw.calibrate_list_ti[j - 1][1]), float(hw.calibrate_list_ti[j - 1][0])
            x = float(vol)

            y = (y_2 - y_1) * (x - x_1) / (x_2 - x_1) + y_1
            self.spi_driver.output_adjust_i(round(y, 3) * 4)
        elif _ch == 3:
            self.spi_driver.output_adjust_v(hw.da_value[_ch])

        else:
            pass

    @staticmethod
    def calibrate_power(cal_list, vol):
        """

        :param cal_list:
        :param vol:
        :return:
        """
        # print(vol)
        for j in range(len(cal_list)):
            if cal_list[j] > vol:
                y_1, y_2 = j - 1, j
                x_1, x_2 = cal_list[j - 1], cal_list[j]
                x = vol
                y = (y_2 - y_1) * (x - x_1) / (x_2 - x_1) + y_1
                # print(y)
                return y

    def ad_da_loop(self):
        """

        :return:
        """
        pass

    def switch_channel(self, _ch):
        """

        :param _ch:
        :return:
        """
        pass
