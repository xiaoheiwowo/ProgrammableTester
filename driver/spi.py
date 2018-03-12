# !/usr/bin/evn python3
# -*- coding: utf-8 -*-

"""
spi
"""

import os
import time

try:
    import spidev
    import wiringpi as wp
except ImportError:
    # from driver import wiringpi as wp
    pass


def debug_print(string=None):
    """
    DEBUG
    :param string:
    :return:
    """
    if True:
        pass
        # print("DEBUG: " + string)


class SPI_Driver:
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
    CS_PIN_AD = 15
    CS_PIN_DA = 18
    DRDY_PIN = 11
    RESET_PIN = 12
    PDWN_PIN = 13

    POWER_DOWN = 0x03

    # 通用定义
    INPUT = 0
    OUTPUT = 1
    LOW = 0
    HIGH = 1

    PUD_OFF = 0
    PUD_DOWN = 1
    PUD_UP = 2

    DAC_A = 0b00100000
    DAC_B = 0b01100000
    DAC_C = 0b10100000
    DAC_D = 0b11100000

    # These options can be adjusted to facilitate specific operation of the
    # ADS1256, the defaults are designed to be compatible with the Waveforms
    # High Precision AD/DA board

    SPI_FREQUENCY = 1000000  # The ADS1256 supports 768kHz to 1.92MHz
    DRDY_TIMEOUT = 0.5  # Seconds to wait for DRDY when communicating
    DATA_TIMEOUT = 0.00001  # 10uS delay for sending data
    SCLK_FREQUENCY = 7680000  # default clock rate is 7.68MHz

    # Register addresses
    REG_STATUS = 0x00
    REG_MUX = 0x01
    REG_ADCON = 0x02
    REG_DRATE = 0x03
    REG_IO = 0x04
    REG_OFC0 = 0x05
    REG_OFC1 = 0x06
    REG_OFC2 = 0x07
    REG_FSC0 = 0x08
    REG_FSC1 = 0x09
    REG_FSC2 = 0x0A
    NUM_REG = 11

    """
    DRATE Register: A/D Data Rate Address 0x03 The 16 valid Data Rate settings are shown below. Make sure to select a
    valid setting as the invalid settings may produce unpredictable results.

    Bits 7-0 DR[7: 0]: Data Rate Setting(1)

        11110000 = 30,000SPS (default)
        11100000 = 15,000SPS
        11010000 = 7,500SPS
        11000000 = 3,750SPS
        10110000 = 2,000SPS
        10100001 = 1,000SPS
        10010010 = 500SPS
        10000010 = 100SPS
        01110010 = 60SPS
        01100011 = 50SPS
        01010011 = 30SPS
        01000011 = 25SPS
        00110011 = 15SPS
        00100011 = 10SPS
        00010011 = 5SPS
        00000011 = 2.5SPS

        (1) for fCLKIN = 7.68MHz. Data rates scale linearly with fCLKIN
    """
    # sample rates
    DRATE_30000 = 0b11110000  # 30,000SPS (default)
    DRATE_15000 = 0b11100000  # 15,000SPS
    DRATE_7500 = 0b11010000  # 7,500SPS
    DRATE_3750 = 0b11000000  # 3,750SPS
    DRATE_2000 = 0b10110000  # 2,000SPS
    DRATE_1000 = 0b10100001  # 1,000SPS
    DRATE_500 = 0b10010010  # 500SPS
    DRATE_100 = 0b10000010  # 100SPS
    DRATE_60 = 0b01110010  # 60SPS
    DRATE_50 = 0b01100011  # 50SPS
    DRATE_30 = 0b01010011  # 30SPS
    DRATE_25 = 0b01000011  # 25SPS
    DRATE_15 = 0b00110011  # 15SPS
    DRATE_10 = 0b00100011  # 10SPS
    DRATE_5 = 0b00010011  # 5SPS
    DRATE_2_5 = 0b00000011  # 2.5SPS

    # Commands
    CMD_WAKEUP = 0x00  # Completes SYNC and exits standby mode
    CMD_RDATA = 0x01  # Read data
    CMD_RDATAC = 0x03  # Start read data continuously
    CMD_SDATAC = 0x0F  # Stop read data continuously
    CMD_RREG = 0x10  # Read from register
    CMD_WREG = 0x50  # Write to register
    CMD_SELFCAL = 0xF0  # Offset and gain self-calibration
    CMD_SELFOCAL = 0xF1  # Offset self-calibration
    CMD_SELFGCAL = 0xF2  # Gain self-calibration
    CMD_SYSOCAL = 0xF3  # System offset calibration
    CMD_SYSGCAL = 0xF4  # System gain calibration
    CMD_SYNC = 0xFC  # Synchronize the A/D conversion
    CMD_STANDBY = 0xFD  # Begin standby mode
    CMD_RESET = 0xFE  # Reset to power-on values

    """
    Status Register Configuration - logically OR all desired options together
    to form a 1 byte command and write it to the STATUS register

    STATUS REGISTER - ADDRESS 0x00
    Bits 7-4 ID3, ID2, ID1, ID0 Factory Programmed Identification Bits 
    (Read Only)

    Bit 3 ORDER: Data Output Bit Order

        0 = Most Significant Bit First (default)
        1 = Least Significant Bit First

        Input data is always shifted in most significant byte and bit first.
        Output data is always shifted out most significant byte first. The
        ORDER bit only controls the bit order of the output data within the
        byte.

    Bit 2 ACAL: Auto-Calibration

        0 = Auto-Calibration Disabled (default)
        1 = Auto-Calibration Enabled

        When Auto-Calibration is enabled, self-calibration begins at the
        completion of the WREG command that changes the PGA (bits 0-2 of ADCON
        register), DR (bits 7-0 in the DRATE register) or BUFEN (bit 1 in the
        STATUS register) values.

    Bit 1 BUFEN: Analog Input Buffer Enable

        0 = Buffer Disabled (default)
        1 = Buffer Enabled

    Bit 0 DRDY: Data Ready (Read Only)

        This bit duplicates the state of the DRDY pin, which is inverted logic.
    """
    STATUS_BUFFER_ENABLE = 0x02
    STATUS_AUTOCAL_ENABLE = 0x04
    STATUS_ORDER_LSB = 0x08

    """
    A/D Control Register - Address 0x02

    Bit 7 Reserved, always 0 (Read Only)

    Bits 6-5 CLK1, CLK0: D0/CLKOUT Clock Out Rate Setting

        00 = Clock Out OFF
    01 = Clock Out Frequency = fCLKIN (default)
    10 = Clock Out Frequency = fCLKIN/2
    11 = Clock Out Frequency = fCLKIN/4

    When not using CLKOUT, it is recommended that it be turned off. These
    bits can only be reset using the RESET pin.

    Bits 4-3 SDCS1, SCDS0: Sensor Detect Current Sources

    00 = Sensor Detect OFF (default)
    01 = Sensor Detect Current = 0.5uA
    10 = Sensor Detect Current = 2uA
    11 = Sensor Detect Current = 10uA

    The Sensor Detect Current Sources can be activated to verify the
    integrity of an external sensor supplying a signal to the ADS1255/6.
    A shorted sensor produces a very small signal while an open-circuit
    sensor produces a very large signal.

    Bits 2-0 PGA2, PGA1, PGA0: Programmable Gain Amplifier Setting
        000 = 1 (default)
        001 = 2
        010 = 4
        011 = 8
        100 = 16
        101 = 32
        110 = 64
        111 = 64
    """
    # Gain levels
    AD_GAIN_1 = 0x00
    AD_GAIN_2 = 0x01
    AD_GAIN_4 = 0x02
    AD_GAIN_8 = 0x03
    AD_GAIN_16 = 0x04
    AD_GAIN_32 = 0x05
    AD_GAIN_64 = 0x06

    # Sensor Detect Current Sources
    AD_SDCS_500pA = 0x08
    AD_SDCS_2uA = 0x10
    AD_SDCS_10uA = 0x18

    # Clock divider
    AD_CLK_EQUAL = 0x20
    AD_CLK_HALF = 0x40
    AD_CLK_FOURTH = 0x60

    # CHANNEL select
    AD_CHANNEL_0 = 0x0f
    AD_CHANNEL_1 = 0x1f
    AD_CHANNEL_2 = 0x2f
    AD_CHANNEL_3 = 0x3f
    AD_CHANNEL_4 = 0x4f

    # The RPI GPIO to use for chip select and ready polling
    def __init__(self):
        # Set up the wiringpi object to use physical pin numbers
        wp.wiringPiSetupPhys()

        # Initialize the DRDY pin
        wp.pinMode(self.DRDY_PIN, self.INPUT)

        # Initialize the reset pin
        wp.pinMode(self.RESET_PIN, self.OUTPUT)
        wp.digitalWrite(self.RESET_PIN, self.HIGH)

        # Initialize PDWN pin
        wp.pinMode(self.PDWN_PIN, self.OUTPUT)
        wp.digitalWrite(self.PDWN_PIN, self.HIGH)

        # Initialize CS pin for ADS1256
        wp.pinMode(self.CS_PIN_AD, self.OUTPUT)
        wp.digitalWrite(self.CS_PIN_AD, self.HIGH)

        # Initialize CS pin for AD5314
        wp.pinMode(self.CS_PIN_DA, self.OUTPUT)
        wp.digitalWrite(self.CS_PIN_DA, self.HIGH)

        # Initialize the spidev SPI setup
        self.spi_bus = spidev.SpiDev()
        self.spi_init()
        debug_print("SPI success " + str(self.spi_bus))

    def spi_init(self):
        """
        初始化spi
        :return:
        """
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

    def chip_select_da(self):
        """
        使能芯片
        :return:
        """
        wp.digitalWrite(self.CS_PIN_DA, self.LOW)
        self.delay_us(5)

    def chip_release_da(self):
        """
        取消使能
        :return:
        """
        wp.digitalWrite(self.CS_PIN_DA, self.HIGH)
        self.delay_us(5)

    def SendWord(self, word):
        """
        Sends  byte to the SPI bus
        """
        debug_print("Sending: " + str(word) + " (hex: " + hex(word[0]) + " " + hex(word[1]) + ")")
        # data = chr(byte)

        result = self.spi_bus.xfer2(word)
        debug_print("Read " + str(result[1]))

    def send_to_ad5314(self, data):
        """

        :param data: list  [0x00, 0x00,...]
        :return:
        """
        # Select the dac chip
        self.chip_select_da()

        # Send the data
        self.SendWord(data)

        # Release the dac chip
        self.chip_release_da()

    def output_ac_power(self, vol):
        """

        :param vol: 电压值0~5v
        :return:
        """
        if 0 <= vol <= 5:
            vol_2 = int(vol * 1023 / 5)
            high_bit = self.DAC_A | (vol_2 >> 6)
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
            high_bit = self.DAC_B | (vol_2 >> 6)
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
            high_bit = self.DAC_C | (vol_2 >> 6)
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
            high_bit = self.DAC_D | (vol_2 >> 6)
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

    # ADS1256
    def chip_select_ad(self):
        """

        :return:
        """
        wp.digitalWrite(self.CS_PIN_AD, self.LOW)
        self.delay_us(5)

    def chip_release_ad(self):
        """

        :return:
        """
        wp.digitalWrite(self.CS_PIN_AD, self.HIGH)
        self.delay_us(5)

    def WaitDRDY(self):
        """
        Delays until DRDY line goes low, allowing for automatic calibration
        """
        start = time.time()
        elapsed = time.time() - start

        # Waits for DRDY to go to zero or TIMEOUT seconds to pass
        drdy_level = wp.digitalRead(self.DRDY_PIN)

        while (drdy_level == self.HIGH) and (elapsed < self.DRDY_TIMEOUT):
            elapsed = time.time() - start
            drdy_level = wp.digitalRead(self.DRDY_PIN)
        if elapsed >= self.DRDY_TIMEOUT:
            print("WaitDRDY() Timeout\r\n")

    def SendByte(self, byte):
        """
        Sends a byte to the SPI bus
        :param byte:
        :return:
        """

        debug_print("Sending: " + str(byte) + " (hex " + hex(byte) + ")")

        result = self.spi_bus.xfer2([byte])
        debug_print("Read " + str(result[0]))

    def ReadByte(self):
        """
        Reads a byte from the SPI bus
        :returns: byte read from the bus
        """
        byte = self.spi_bus.xfer2([0xff])
        debug_print("ReadByte: byte[0]" + str(byte[0]) + " (hex " + hex(byte[0]) + ")")
        # print(byte)
        return byte[0]  # JKR

    def DataDelay(self):
        """
        Delay from last SCLK edge to first SCLK rising edge

        Master clock rate is typically 7.68MHz, this is adjustable through the
        SCLK_FREQUENCY variable

        Datasheet states that the delay between requesting data and reading the
        bus must be minimum 50x SCLK period, this function reads data after
        60 x SCLK period.
        """
        # timeout = (60 / self.SCLK_FREQUENCY)

        start = time.time()
        elapsed = time.time() - start

        # Wait for TIMEOUT to elapse
        while elapsed < self.DATA_TIMEOUT:
            elapsed = time.time() - start

    def ReadReg(self, start_reg):
        """
        Read the provided register, implements:

        RREG: Read from Registers

        Description: Output the data from up to 11 registers starting with the
        register address specified as part of the command. The number of
        registers read will be one plus the second byte of the command. If the
        count exceeds the remaining registers, the addresses will wrap back to
        the beginning.

        1st Command Byte: 0001 rrrr where rrrr is the address of the first
        register to read.

        2nd Command Byte: 0000 nnnn where nnnn is the number of bytes to read
        1. See the Timing Characteristics for the required delay between the
        end of the RREG command and the beginning of shifting data on DOUT: t6.
        """

        # Pull the SPI bus low
        self.chip_select_ad()

        # Send the byte command
        self.SendByte(self.CMD_RREG | start_reg)
        self.SendByte(0x00)

        # Wait for appropriate data delay
        self.DataDelay()

        # Read the register contents
        idreturn = self.ReadByte()
        debug_print("idreturn: " + str(idreturn) + " (hex " + hex(idreturn) + ")")

        # Release the SPI bus
        self.chip_release_ad()

        return idreturn

    def WriteReg(self, register, data):
        """
        Writes data to the register, implements:

        WREG: Write to Register

        Description: Write to the registers starting with the register
        specified as part of the command. The number of registers that
        will be written is one plus the value of the second byte in the
        command.

        1st Command Byte: 0101 rrrr where rrrr is the address to the first
        register to be written.

        2nd Command Byte: 0000 nnnn where nnnn is the number of bytes-1 to be
        written

        DO Implement multiple register write
        """

        # Select the ADS chip
        self.chip_select_ad()

        # Tell the ADS chip which register to start writing at
        self.SendByte(self.CMD_WREG | register)

        # Tell the ADS chip how many additional registers to write
        self.SendByte(0x00)

        # Send the data
        self.SendByte(data)

        # Release the ADS chip
        self.chip_release_ad()

    def ReadADC(self):
        """
        Reads ADC data, implements:

        RDATA: Read Data

        Description: Issue this command after DRDY goes low to read a single
        conversion result. After all 24 bits have been shifted out on DOUT,
        DRDY goes high. It is not necessary to read back all 24 bits, but DRDY
        will then not return high until new data is being updated. See the
        Timing Characteristics for the required delay between the end of the
        RDATA command and the beginning of shifting data on DOUT: t6
        """

        # Pull the SPI bus low
        self.chip_select_ad()

        # Wait for data to be ready
        self.WaitDRDY()

        # Send the read command
        self.SendByte(self.CMD_RDATA)

        # Wait through the data pause
        self.DataDelay()

        # The result is 24 bits
        result1 = self.ReadByte()
        result2 = self.ReadByte()
        result3 = self.ReadByte()
        debug_print('ReadADC result bytes: ' + hex(result1) + ' ' + hex(result2) + ' ' + hex(result3))

        # Release the SPI bus
        self.chip_release_ad()

        # Concatenate the bytes
        total = (result1 << 16) + (result2 << 8) + result3

        # return total
        return round(total * 5 / 2 ** 23, 3)

    def ReadID(self):
        """
        Read the ID from the ADS chip
        :returns: numeric identifier of the ADS chip
        """
        self.WaitDRDY()
        myid = self.ReadReg(self.REG_STATUS)
        return myid >> 4

    def read_all_reg(self):
        """
        读取所有寄存器
        :return:
        """
        print('++++++++++++++++++++++++++++++++++++')
        for j in range(11):
            print('REG: 0' + str(hex(j)[-1]) + 'H   ' + str(hex(self.ReadReg(j))))

        print('++++++++++++++++++++++++++++++++++++')

    def ADS1256_Init(self):
        """
        不用
        :return:
        """
        # 高位在前、不使用校准、不使用缓冲
        self.WriteReg(self.REG_STATUS, 0x00)

        # 初始化端口A0为‘+’，AINCOM位‘-’
        self.WriteReg(self.REG_MUX, 0x08)

        # 放大倍数1
        self.WriteReg(self.REG_ADCON, 0X00)

        # SPS 1000
        self.WriteReg(self.REG_DRATE, self.DRATE_1000)

    def ads1256_cfg(self):
        """
        ADS1256初始化
        :return:
        """
        """
        buf[0]:高位在前、不使用校准、不使用缓冲
        buf[1]:初始化端口A0为‘+’，AINCOM位‘-’
        buf[2]:放大倍数1
        buf[3]:SPS 1000
        """
        buf = [0x00, 0x08, 0x00, self.DRATE_1000]
        self.WaitDRDY()
        self.chip_select_ad()

        # reset
        self.SendByte(self.CMD_RESET)
        self.delay_us(50)
        self.SendByte(self.CMD_WREG)
        self.SendByte(0x03)
        self.SendByte(buf[0])
        self.SendByte(buf[1])
        self.SendByte(buf[2])
        self.SendByte(buf[3])
        self.chip_release_ad()
        self.delay_us(50)

    def ads1256_one_shot(self, index):
        """

        :param index: int 0~4 ---- ad0~ad4
        :return:
        """
        channel_list = [0x0f, 0x1f, 0x2f, 0x3f, 0x4f]
        self.chip_select_ad()
        self.SendByte(self.CMD_WREG | 0x01)
        self.SendByte(0x00)
        self.SendByte(channel_list[index])
        self.delay_us(15)
        self.SendByte(self.CMD_SYNC)
        self.delay_us(5)
        self.SendByte(self.CMD_WAKEUP)
        self.delay_us(25)
        self.chip_release_ad()

    @staticmethod
    def delay_us(_us):
        """

        :param _us:
        :return:
        """
        wp.delayMicroseconds(_us)

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


if __name__ == '__main__':
    ad_da = SPI_Driver()
    # ad_da.ADS1256_Init()
    # ad_da.read_all_reg()
    ad_da.ads1256_cfg()

    while True:
        try:
            print('Choose a channel...\n'
                  '1 ACPOWER 0~5V\n'
                  '2 DCPOWER 0~5V\n'
                  '3 ADJUST VALVE 0~20mA\n'
                  '4 ADJUST VALVE 0~10V\n'
                  '5 AD TEST\n')
            channel = input()
            value = input('Input a value\n')
            if channel == '1':
                ad_da.output_ac_power(float(value))
            elif channel == '2':
                ad_da.output_dc_power(float(value))
            elif channel == '3':
                ad_da.output_adjust_i(float(value))
            elif channel == '4':
                ad_da.output_adjust_v(float(value))
            elif channel == '5':
                while True:
                    try:
                        if not input(''):
                            os.system('clear')
                            for i in range(5):
                                ad_da.ads1256_one_shot(i)
                                print('AD' + str(i) + ': ' + str(ad_da.ReadADC()))
                                # ad_da.read_all_reg()
                                time.sleep(0.005)
                            time.sleep(1)
                        else:
                            pass
                    except KeyboardInterrupt:
                        break
        except KeyboardInterrupt:
            ad_da.output_0()
            ad_da.spi_close()
            os.system('clear')
            debug_print('[spi close]')
            break
