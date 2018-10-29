import time
from PyQt5.QtCore import QThread, pyqtSignal
import sys
sys.path.append('..')
from driver.spi2 import *


class RaspiAD(QThread):
    """
    树莓派数据采集卡控制程序
    """
    buf_size = 0
    ad_ch_num = 0
    send_sample_data = pyqtSignal(str)

    def __init__(self):
        super(RaspiAD, self).__init__()
        self.spi = SPIDriver()
        self.da_out = [{'flag': 0, 'value': 0},
                       {'flag': 0, 'value': 0},
                       {'flag': 0, 'value': 0},
                       {'flag': 0, 'value': 0}]

    def run(self):
        self.config_sample(99, 8)
        while not self.isInterruptionRequested():
        # while 1:
            time.sleep(0.1)
            # print(time.time())
            if self.spi.read_int_pin():
                self.spi.chip_select_pic()
                cmd = (7 << 8) + 255
                self.spi.SendWord(cmd)
                # while self.spi.read_int_pin() == 1:
                #     pass
                self.spi.delay_us(1000)
                result = []
                # self.spi.SendWord(0xaaaa)
                for i in range((self.buf_size + 1) * self.ad_ch_num):
                    # self.spi.delay_us(3)
                    ret = self.spi.SendWord(0xaaaa)
                    result.append(ret)
                    if ret == 0xaaaa:
                        print(ret)
                        # result.append(ret)
                    # else:
                    #     result.append(ret)
                self.send_sample_data.emit(str(result))
                # print(str(result))
                self.spi.chip_release_pic()
                time.sleep(0.2)

            for i in range(4):
                if self.da_out[i]['flag'] == 1:
                    self.spi.analog_output(i, self.da_out[i]['value'])
                    self.da_out[i]['flag'] = 0
                    pass

    def config_sample(self, buf_size, ad_ch_num):
        self.buf_size = buf_size
        self.ad_ch_num = ad_ch_num
        self.spi.chip_select_pic()
        self.spi.SendWord(0x01ff)
        self.spi.SendWord(0x0210)
        self.spi.SendWord(0x0300 | self.buf_size)
        self.spi.chip_release_pic()


def rcv(x):
    print(x)


if __name__ == '__main__':

    raspi_ad = RaspiAD()
    raspi_ad.spi.hard_reset()
    time.sleep(2)
    # raspi_ad.send_sample_data.connect(rcv)
    raspi_ad.start()
    timer = 0

    while True:
        time.sleep(1)
        for i in range(6):
            a = input()
            raspi_ad.spi.analog_output(1, int(i * 204.6))


        #
        # timer += 1
        # if timer == 60:
        #     raspi_ad.spi.hard_reset()
        #     raspi_ad.requestInterruption()
        #     # time.sleep(1)
        #     raspi_ad.deleteLater()
        #     break


