# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

import os

try:
    import spidev
    import wiringpi as wp
except ImportError:
    from driver import wiringpi as wp

    pass


def debug_print(string=None):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        print("DEBUG: " + string)


DAC_A = 0b00100000
DAC_B = 0b01100000
DAC_C = 0b10100000
DAC_D = 0b11100000


class AD5314:
    """ Wiring Diagram
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

    # High Precision AD/DA board
    SPI_MODE = 1
    SPI_CHANNEL = 1
    SPI_RATE = 20000

    # The RPI GPIO to use for chip select and ready polling
    CS_PIN = 16

    POWER_DOWN = 0x03

    # 通用定义
    INPUT = 0
    OUTPUT = 1

    LOW = 0
    HIGH = 1

    def __init__(self):

        wp.wiringPiSetupPhys()
        wp.pinMode(self.CS_PIN, self.OUTPUT)
        wp.digitalWrite(self.CS_PIN, self.HIGH)

    def SPI_Init(self):
        """
        初始化spi
        :return:
        """
        self.spi_bus = spidev.SpiDev()
        self.spi_bus.open(0, 0)
        self.spi_bus.mode = self.SPI_MODE
        self.spi_bus.max_speed_hz = self.SPI_RATE
        self.spi_bus.cshigh = False

    def spi_close(self):
        """
        关闭spi
        :return:
        """

        self.spi_bus.close()

    def chip_select(self):
        """
        使能芯片
        :return:
        """
        wp.digitalWrite(self.CS_PIN, self.LOW)

    def chip_release(self):
        """
        取消使能
        :return:
        """
        wp.digitalWrite(self.CS_PIN, self.HIGH)

    def SendByte(self, byte):
        """
        Sends  byte to the SPI bus
        """
        debug_print("Sending: " + str(byte) + " (hex: " + hex(byte[0]) + " " + hex(byte[1]) + ")")
        # data = chr(byte)

        result = self.spi_bus.xfer2(byte)
        debug_print("Read " + str(result[1]))

    def send_to_ad5314(self, data):
        """

        :param data: list  [0x00, 0x00,...]
        :return:
        """
        # Select the dac chip
        self.chip_select()

        # Send the data
        self.SendByte(data)

        # Release the dac chip
        self.chip_release()

    def output_ac_power(self, vol):
        """

        :param vol: 电压值0~5v
        :return:
        """
        if 0 <= vol <= 5:
            vol_2 = int(vol * 1023 / 5)
            high_bit = DAC_A | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_dc_power(self, vol):
        """

        :param vol:0~5v
        :return:
        """

        if 0 <= vol <= 5:
            vol_2 = int(vol * 1023 / 5)
            high_bit = DAC_B | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_adjust_i(self, current):
        """

        :param current:0~20ma
        :return:
        """
        if 0 <= current <= 20:
            vol_2 = int(current * 1023 / 20)
            high_bit = DAC_C | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_adjust_v(self, vol):
        """

        :param vol:0~10v
        :return:
        """
        if 0 <= vol <= 10:
            vol_2 = int(vol * 1023 / 10)
            high_bit = DAC_D | (vol_2 >> 6)
            low_bit = (vol_2 & 0b0000111111) << 2
            self.send_to_ad5314([high_bit, low_bit])

        else:
            debug_print('error')
            pass

    def output_0(self):
        """
        all channel output 0
        :return:
        """

        self.output_ac_power(0)
        self.output_dc_power(0)
        self.output_adjust_i(0)
        self.output_adjust_v(0)


if __name__ == '__main__':
    dac = AD5314()
    dac.SPI_Init()
    while True:
        try:
            print('Choose a channel...\n'
                  '1 ACPOWER 0~5V\n'
                  '2 DCPOWER 0~5V\n'
                  '3 ADJUST VALVE 0~20mA\n'
                  '4 ADJUST VALVE 0~10V\n')
            channel = input()
            value = input('Input a value\n')
            if channel == '1':
                dac.output_ac_power(float(value))
            elif channel == '2':
                dac.output_dc_power(float(value))
            elif channel == '3':
                dac.output_adjust_i(float(value))
            elif channel == '4':
                dac.output_adjust_v(float(value))
            else:
                pass

        except KeyboardInterrupt:
            dac.output_0()
            dac.spi_close()
            os.system('clear')
            debug_print('spi close')
            break
