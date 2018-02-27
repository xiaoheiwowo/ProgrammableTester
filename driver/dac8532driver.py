# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

import time
from driver import wiringpi as wp
import spidev


def debug_print(string=None):
    if True:
        pass
        print("DEBUG: " + string)


class DAC8532:
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
    SPI_RATE = 1000000

    # The RPI GPIO to use for chip select and ready polling
    CS_PIN = 16

    LDA = 0x10
    LDB = 0x20

    SELECT_A = 0x00
    SELECT_B = 0x04

    POWER_DOWN = 0x03

    # 通用定义
    INPUT = 0
    OUTPUT = 1

    LOW = 0
    HIGH = 1

    def __init__(self):
        """
        D
        """

        wp.wiringPiSetupPhys()
        wp.pinMode(self.CS_PIN, self.OUTPUT)
        wp.digitalWrite(self.CS_PIN, self.HIGH)

    def SPI_Init(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 0b01
        self.spi.max_speed_hz = 1000000
        self.spi.cshigh = False

    def spi_close(self):
        self.spi.close()

    def chip_select(self):
        wp.digitalWrite(self.CS_PIN, self.LOW)

    def chip_release(self):
        wp.digitalWrite(self.CS_PIN, self.HIGH)

    def SendByte(self, byte):
        """
        Sends a byte to the SPI bus
        """
        debug_print("Sending: " + str(byte) + " (hex: " + hex(byte[0]) + " " + hex(byte[1]) + " " + hex(byte[2]) + ")")
        # data = chr(byte)

        result = self.spi.xfer2(byte)
        debug_print("Read " + str(result[1]))

    def send_to_dac8532(self, data):

        # Select the dac chip
        self.chip_select()

        # Send the data
        self.SendByte(data)

        # Release the dac chip
        self.chip_release()

    def led_on(self):
        self.send_to_dac8532([self.LDA | self.SELECT_A, 0xff, 0xff])
        self.send_to_dac8532([self.LDB | self.SELECT_B, 0x00, 0x00])

    def led_off(self):
        self.send_to_dac8532([self.LDA | self.SELECT_A, 0x00, 0x00])
        self.send_to_dac8532([self.LDB | self.SELECT_B, 0xff, 0xff])

    def test_led(self):
        self.led_on()
        wp.delay(1000)
        self.led_off()
        wp.delay(1000)

    def test_an(self):

        for i in range(255):
            self.send_to_dac8532([self.LDA | self.SELECT_A, i, i])
            self.send_to_dac8532([self.LDB | self.SELECT_B, 255 - i, 255 - i])
            wp.delay(6)
        for i in range(255):
            self.send_to_dac8532([self.LDA | self.SELECT_A, 255 - i, 255 - i])
            self.send_to_dac8532([self.LDB | self.SELECT_B, i, i])
            wp.delay(6)

if __name__ == '__main__':
    dac = DAC8532()
    dac.SPI_Init()
    try:
        while True:

            # 闪烁
            # dac.test_led()

            # 呼吸灯
            dac.test_an()
    except KeyboardInterrupt:
        dac.spi_close()
        print('[spi close]')
