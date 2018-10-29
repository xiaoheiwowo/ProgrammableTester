# /usr/bin/python3
# -*- coding: utf-8 -*-
import time

try:
    import spidev
    import wiringpi as wp
    import RPi.GPIO as GPIO
except ImportError:
    print("No spidev, RPi and wiringpi")


def debug_print(string=None):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        # print("DEBUG: " + string)


class SPIDriver(object):
    """ Wiring Diagram   Using BCM index
     +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
     | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
     +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
     |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
     |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
     |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
     |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
     |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
     |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 1 | IN   | GPIO. 1 | 1   | 18  |
     |  27 |   2 | GPIO. 2 |   IN | 1 | 13 || 14 |   |      | 0v      |     |     |
     |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
     |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
     |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
     |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
     |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
     |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
     |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
     |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
     |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
     |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
     |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
     |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
     |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
     +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
     | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
     +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
    """

    SPI_MODE = 2
    SPI_CHANNEL = 1
    SPI_RATE = 4000000

    CE0 = 24
    INT_AD = 35
    RESET = 37

    CE1 = 18

    # 通用定义
    INPUT = 0
    OUTPUT = 1
    LOW = 0
    HIGH = 1

    DAC = [0b0110, 0b0010, 0b1010, 0b1110]

    # The RPI GPIO to use for chip select and ready polling
    def __init__(self):
        try:
            # Set up the wiringpi object to use physical pin numbers
            wp.wiringPiSetupPhys()

            # Initialize CE0 pin
            wp.pinMode(self.CE0, self.OUTPUT)
            wp.digitalWrite(self.CE0, self.HIGH)

            # Initialize CE1 pin
            wp.pinMode(self.CE1, self.OUTPUT)
            wp.digitalWrite(self.CE1, self.HIGH)

            # RESET
            wp.pinMode(self.RESET, self.OUTPUT)
            wp.digitalWrite(self.RESET, self.HIGH)

            wp.pinMode(self.INT_AD, self.INPUT)

            # Initialize the spidev SPI setup
            self.spi_bus = spidev.SpiDev()
            self.spi_init()
            # self.init_gpio_int()
            debug_print("SPI success " + str(self.spi_bus))
        except:
            pass

    @staticmethod
    def delay_us(_us):
        """

        :param _us:
        :return:
        """
        try:
            wp.delayMicroseconds(_us)
        except:
            pass

    @staticmethod
    def delay_ms(_ms):
        """

        :param _ms:
        :return:
        """
        start = time.time()
        end = time.time()

        while end - start < 0.001 * _ms:
            end = time.time()

    def spi_init(self):
        """
        初始化spi
        :return:
        """
        try:
            self.spi_bus.open(0, 0)
            self.spi_bus.mode = self.SPI_MODE
            self.spi_bus.max_speed_hz = self.SPI_RATE
            self.spi_bus.cshigh = False
        except:
            pass

    def spi_close(self):
        """
        关闭spi
        :return:
        """
        try:
            self.spi_bus.close()
        except:
            pass

    def chip_select_pic(self):
        """
        使能芯片
        :return:
        """
        try:
            wp.digitalWrite(self.CE0, self.LOW)
            self.delay_us(5)
        except:
            pass

    def chip_release_pic(self):
        """
        取消使能
        :return:
        """
        try:
            wp.digitalWrite(self.CE0, self.HIGH)
            self.delay_us(5)
        except:
            pass

    def SendWord(self, word):
        """
        Send a word to the SPI bus and read a word from spi
        """
        try:
            first_byte = word >> 8
            second_byte = word & 0x00FF
            debug_print("Send ==> {0} {1}".format(hex(first_byte), hex(second_byte)))
            result = list()
            result.append(self.spi_bus.xfer2([first_byte]))
            result.append(self.spi_bus.xfer2([second_byte]))
            debug_print('Read <== {0} {1}'.format(hex(result[0][0]), hex(result[1][0])))
            return (result[0][0] << 8) + result[1][0]
        except:
            pass

    def read_int_pin(self):
        try:
            a = wp.digitalRead(self.INT_AD)
            self.delay_ms(1)
            return a * wp.digitalRead(self.INT_AD)
        except:
            return 0

    def hard_reset(self):
        try:
            wp.digitalWrite(self.RESET, self.LOW)
            self.delay_ms(2)
            wp.digitalWrite(self.RESET, self.HIGH)
        except:
            pass

    def chip_select_da(self):
        """
        使能芯片
        :return:
        """
        try:
            wp.digitalWrite(self.CE1, self.LOW)
            self.delay_us(5)
        except:
            pass

    def chip_release_da(self):
        """
        取消使能
        :return:
        """
        try:
            wp.digitalWrite(self.CE1, self.HIGH)
            self.delay_us(5)
        except:
            pass

    def analog_output(self, _ch, _bit):
        """

        :param _ch: 通道
        :param _bit: 0x0 ~ 0x3ff
        :return:
        """

        if 0 <= _bit <= 0x3ff:
            # print(bin(_bit))
            # print(bin(self.DAC[_ch] << 12 | _bit << 2))
            self.chip_select_da()
            self.SendWord(self.DAC[_ch] << 12 | _bit << 2)
            self.chip_release_da()
        else:
            debug_print('Value Error')


if __name__ == '__main__':
    spi = SPIDriver()
    while True:
        ret = []
        for i in range(500):
            ret.append(spi.SendWord(0xaaaa))
        print(ret)
        time.sleep(1)
    # spi = SPIDriver()
    # spi.analog_output(0, 0x3ff)
    # for i in range(11):
    #     spi.analog_output(0, i * 100)
    #     a = input(str(i * 100))
    # spi.SendWord(0x7f01)

