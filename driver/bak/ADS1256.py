# Python module for ADS1256 

try:
    from driver.bak._bcm2835 import *
except ImportError:
    from libbcm2835._bcm2835 import *

import numpy as np

# define constants

# gain channel
ADS1256_GAIN_E = {'ADS1256_GAIN_1': 0,  # GAIN   1
                  'ADS1256_GAIN_2': 1,  # GAIN   2
                  'ADS1256_GAIN_4': 2,  # GAIN   4
                  'ADS1256_GAIN_8': 3,  # GAIN   8
                  'ADS1256_GAIN_16': 4,  # GAIN  16
                  'ADS1256_GAIN_32': 5,  # GAIN  32
                  'ADS1256_GAIN_64': 6,  # GAIN  64
                  }

# data rate
ADS1256_DRATE_E = {'ADS1256_30000SPS': 0xF0,  # reset the default values
                   'ADS1256_15000SPS': 0xE0,
                   'ADS1256_7500SPS': 0xD0,
                   'ADS1256_3750SPS': 0xC0,
                   'ADS1256_2000SPS': 0xB0,
                   'ADS1256_1000SPS': 0xA1,
                   'ADS1256_500SPS': 0x92,
                   'ADS1256_100SPS': 0x82,
                   'ADS1256_60SPS': 0x72,
                   'ADS1256_50SPS': 0x63,
                   'ADS1256_30SPS': 0x53,
                   'ADS1256_25SPS': 0x43,
                   'ADS1256_15SPS': 0x33,
                   'ADS1256_10SPS': 0x20,
                   'ADS1256_5SPS': 0x13,
                   'ADS1256_2d5SPS': 0x03
                   }

# registration definition
REG_E = {'REG_STATUS': 0,  # x1H
         'REG_MUX': 1,  # 01H
         'REG_ADCON': 2,  # 20H
         'REG_DRATE': 3,  # F0H
         'REG_IO': 4,  # E0H
         'REG_OFC0': 5,  # xxH
         'REG_OFC1': 6,  # xxH
         'REG_OFC2': 7,  # xxH
         'REG_FSC0': 8,  # xxH
         'REG_FSC1': 9,  # xxH
         'REG_FSC2': 10,  # xxH
         }

# command definition
CMD = {'CMD_WAKEUP': 0x00,  # Completes SYNC and Exits Standby Mode 0000  0000 (00h)
       'CMD_RDATA': 0x01,  # Read Data 0000  0001 (01h)
       'CMD_RDATAC': 0x03,  # Read Data Continuously 0000   0011 (03h)
       'CMD_SDATAC': 0x0F,  # Stop Read Data Continuously 0000   1111 (0Fh)
       'CMD_RREG': 0x10,  # Read from REG rrr 0001 rrrr (1xh)
       'CMD_WREG': 0x50,  # Write to REG rrr 0101 rrrr (5xh)
       'CMD_SELFCAL': 0xF0,  # Offset and Gain Self-Calibration 1111    0000 (F0h)
       'CMD_SELFOCAL': 0xF1,  # Offset Self-Calibration 1111    0001 (F1h)
       'CMD_SELFGCAL': 0xF2,  # Gain Self-Calibration 1111    0010 (F2h)
       'CMD_SYSOCAL': 0xF3,  # System Offset Calibration 1111   0011 (F3h)
       'CMD_SYSGCAL': 0xF4,  # System Gain Calibration 1111    0100 (F4h)
       'CMD_SYNC': 0xFC,  # Synchronize the A/D Conversion 1111   1100 (FCh)
       'CMD_STANDBY': 0xFD,  # Begin Standby Mode 1111   1101 (FDh)
       'CMD_RESET': 0xFE,  # Reset to Power-Up Values 1111   1110 (FEh)
       }


# ADS1256 Python Module
class ADS1256:
    """
    in
    """

    def __init__(self, ch_num=0, gain='ADS1256_GAIN_1', rate='ADS1256_100SPS'):

        # data storage
        if gain in ADS1256_GAIN_E:
            self.Gain = ADS1256_GAIN_E[gain]
        else:
            self.Gain = ADS1256_GAIN_E['ADS1256_GAIN_1']  # GAIN  1
        if rate in ADS1256_DRATE_E:
            self.DataRate = ADS1256_DRATE_E[rate]
        else:
            self.DataRate = ADS1256_DRATE_E['ADS1256_100SPS']  # DATA output speed

        self.AdcNow = [0, 0, 0, 0, 0, 0, 0, 0]  # ADC  Conversion value
        self.Channel = ch_num  # The current channel
        self.ScanMode = 0  # Scanning mode_ 0 : Single-ended input  8 channel; 1 : Differential input  4 channel

        # define constants for future usage
        self.DRDY = RPI_GPIO_P1_11  # P0
        self.RST = RPI_GPIO_P1_12  # P1
        self.SPICS = RPI_GPIO_P1_15  # P3

        # adc chip initialization
        if not bcm2835_init():
            return
        self.chipInit()
        self.ADS1256_CfgADC(self.Gain, self.DataRate)
        self.ADS1256_StartScan(0, self.Channel)

    def chipInit(self):
        """
        configure the chip before data transmission
        :return:
        """
        if bcm2835_spi_begin():
            print('ddd')

        # default setting from motor control
        # Edited follow Arduino command
        bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST)
        # Set Register x00 to set bit order
        bcm2835_spi_setDataMode(BCM2835_SPI_MODE3)  # Edited follow Arduino Command
        bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_4096)

        bcm2835_gpio_fsel(self.SPICS, BCM2835_GPIO_FSEL_OUTP)
        bcm2835_gpio_write(self.SPICS, HIGH)
        bcm2835_gpio_fsel(self.DRDY, BCM2835_GPIO_FSEL_INPT)
        bcm2835_gpio_set_pud(self.DRDY, BCM2835_GPIO_PUD_UP)

    def set_CS_High(self):
        """
        set CS to HIGH
        :return:
        """
        bcm2835_gpio_write(self.SPICS, HIGH)

    def set_CS_Low(self):
        """
        set CS to LOW
        :return:
        """
        bcm2835_gpio_write(self.SPICS, LOW)

    def dataReady_is_Low(self):
        """
        check if data is ready
        :return:
        """
        return bcm2835_gpio_lev(self.DRDY) == 0

    def set_RST_High(self):
        """
        set RST to HIGH
        :return:
        """
        bcm2835_gpio_write(self.RST, HIGH)

    def set_RST_Low(self):
        """
        set RST to LOW
        :return:
        """

        bcm2835_gpio_write(self.RST, LOW)

    @staticmethod
    def bsp_DelayUS(micros):
        """
        delay for microseconds before procede
        :param micros:
        :return:
        """
        bcm2835_delayMicroseconds(micros)

    @staticmethod
    def bsp_InitADS1256():
        """
        SOFT SPI?
        :return:
        """
        print("SOFT SPI? NOT IMPLEMENTED YET")

    def ADS1256_StartScan(self, uc_scan_mode, _ch_num):
        """
        Configuration DRDY PIN for external interrupt is triggered
        :param uc_scan_mode:
        :param _ch_num:
        :return:
        """
        self.ScanMode = uc_scan_mode
        self.Channel = _ch_num
        self.ADS1256_SetChannel(self.Channel)
        self.AdcNow = [0, 0, 0, 0, 0, 0, 0, 0]  # reset
        # print self.AdcNow

    def ADS1256_Send8Bit(self, _data):
        """
        SPI bus to send 8 bit data
        :param _data:
        :return:
        """
        self.bsp_DelayUS(2)
        bcm2835_spi_transfer(_data)

    def ADS1256_CfgADC(self, _gain, _data_rate):
        """
        The configuration parameters of ADC, gain and data rate
        :param _gain:
        :param _data_rate:
        :return:
        """
        self.Gain = _gain
        self.DataRate = _data_rate

        self.ADS1256_WaitDRDY()

        # Storage ads1256 register configuration parameters
        buf = [0x00, 0x00, 0x00, 0x00]

        '''
        ### Status register define
        Bits 7-4 ID3, ID2, ID1, ID0  Factory Programmed Identification Bits (Read Only)
        
        Bit 3 ORDER: Data Output Bit Order
        0 = Most Significant Bit First (default)
        1 = Least Significant Bit First
        Input data  is always shifted in most significant byte and bit first. Output data is always shifted 
        out most significant
        byte first. The ORDER bit only controls the bit order of the output data within the byte.
        
        Bit 2 ACAL : Auto-Calibration
        0 = Auto-Calibration Disabled (default)
        1 = Auto-Calibration Enabled
        When Auto-Calibration is enabled, self-calibration begins at the completion of the WREG command that changes
        the PGA (bits 0-2 of ADCON register), DR (bits 7-0 in the DRATE register) or 
        BUFEN (bit 1 in the STATUS register)
        values.
        
        Bit 1 BUFEN: Analog Input Buffer Enable
        0 = Buffer Disabled (default)
        1 = Buffer Enabled
        
        Bit 0 DRDY :  Data Ready (Read Only)
        This bit duplicates the state of the DRDY pin.
        
        ACAL=1  enable  calibration
        
        buf[0] = (0 << 3) | (1 << 2) | (1 << 1);//enable the internal buffer
        '''

        # 0000 0100: MSBF, Auto-cal, Buffer disabled, Data Ready
        buf[0] = (0 << 3) | (1 << 2) | (0 << 1)

        # MUX: Input multiplexer Control register (Address 01h)
        # Bits 7-4: Positive Input Channel (0-7 = AIN0-7, 1xxx = AINCOM)
        # Bits 3-0: Negative Input Channel (0-7 = AIN0-7, 1xxx = AINCOM)

        # Positive Input Channel: AIN0, Negative Input Channel: AINCOM
        buf[1] = 0x08

        '''
        /*	ADCON: A/D Control Register (Address 02h)
        Bit 7 Reserved, always 0 (Read Only)
        Bits 6-5 CLK1, CLK0 : D0/CLKOUT Clock Out Rate Setting
        00 = Clock Out OFF
        01 = Clock Out Frequency = fCLKIN (default)
        10 = Clock Out Frequency = fCLKIN/2
        11 = Clock Out Frequency = fCLKIN/4
        
        When not using CLKOUT, it is recommended that it be turned off. 
        These bits can only be reset using the RESET pin.
        
        Bits 4-3 SDCS1, SCDS0: Sensor Detect Current Sources
        00 = Sensor Detect OFF (default)
        01 = Sensor Detect Current = 0.5 A
        10 = Sensor Detect Current = 2 A
        11 = Sensor Detect Current = 10 A
        
        The Sensor Detect Current Sources can be activated to verify  
        the integrity of an external sensor supplying a signal to the
        ADS1255/6. A shorted sensor produces a very small signal while 
        an open-circuit sensor produces a very large signal.
        
        Bits 2-0 PGA2, PGA1, PGA0: Programmable Gain Amplifier Setting
        000 = 1 (default)
        001 = 2
        010 = 4
        011 = 8
        100 = 16
        101 = 32
        110 = 64
        111 = 64
        '''

        # Clock out off, Sensor detect off, gain = 1
        buf[2] = (0 << 5) | (0 << 3) | (_gain << 0)
        # ADS1256_WriteReg(REG_ADCON, (0 << 5) | (0 << 2) | (GAIN_1 << 1));	/*choose 1: gain 1 ;input 5V/
        # ADS1256_DRATE_E[_drate]
        buf[3] = self.DataRate

        self.set_CS_Low()
        self.ADS1256_Send8Bit(CMD['CMD_WREG'] | 0)  # Write register, starting with register address 0
        self.ADS1256_Send8Bit(0x03)  # number of bytes to be sent: 4 (writing 4 registers), set the number = 4 - 1

        self.ADS1256_Send8Bit(buf[0])  # Set the status register
        self.ADS1256_Send8Bit(buf[1])  # Set the input channel parameters
        self.ADS1256_Send8Bit(buf[2])  # Set the ADCON control register,gain
        self.ADS1256_Send8Bit(buf[3])  # Set the output rate

        self.set_CS_High()  # SPI  cs = 1

        self.bsp_DelayUS(50)

        # print hex(buf[0]), hex(buf[1]), hex(buf[2]), hex(buf[3])

    def ADS1256_DelayDATA(self):
        """
        Delay from last SCLK edge for DIN to first SCLK rising edge
        for DOUT: RDATA, RDATAC,RREG Commands. Minimum  50   CLK = 50 * 0.13uS = 6.5uS
        :return:
        """
        self.bsp_DelayUS(10)  # The minimum time delay 6.5us

    @staticmethod
    def ADS1256_Receive8Bit():
        """
        Receive 8 bit
        :return:
        """
        return bcm2835_spi_transfer(0xff)

    def ADS1256_WriteReg(self, _reg_id, _reg_value):
        """
        Write the corresponding register
        :param _reg_id:
        :param _reg_value:
        :return:
        """
        self.set_CS_Low()
        self.ADS1256_Send8Bit(CMD['CMD_WREG'] | _reg_id)  # Write command register
        self.ADS1256_Send8Bit(0x00)  # Write the register number

        self.ADS1256_Send8Bit(_reg_value)  # send register value
        self.set_CS_High()

    def ADS1256_ReadReg(self, _reg_id):
        """
        Read  the corresponding register
        :param _reg_id:
        :return:
        """
        self.set_CS_Low()
        self.ADS1256_Send8Bit(CMD['CMD_RREG'] | _reg_id)
        self.ADS1256_Send8Bit(0x00)

        self.ADS1256_DelayDATA()

        read = self.ADS1256_Receive8Bit()
        self.set_CS_High()

        return read

    def ADS1256_WriteCmd(self, _cmd):
        """
        Sending a single byte order
        :param _cmd:
        :return:
        """
        self.set_CS_Low()
        self.ADS1256_Send8Bit(_cmd)
        self.set_CS_High()

    def ADS1256_ReadChipID(self):
        """
        Read the chip ID
        :return:
        """
        self.ADS1256_WaitDRDY()
        chipID = self.ADS1256_ReadReg(REG_E['REG_STATUS'])
        return chipID >> 4

    def ADS1256_SetChannel(self, _ch):
        """
        Configuration channel number
        :param _ch:
        :return:
        """
        '''
        #	Bits 7-4 PSEL3, PSEL2, PSEL1, PSEL0: Positive Input Channel (AINP) Select
        #		0000 = AIN0 (default)
        #		0001 = AIN1
        #		0010 = AIN2 (ADS1256 only)
        #		0011 = AIN3 (ADS1256 only)
        #		0100 = AIN4 (ADS1256 only)
        #		0101 = AIN5 (ADS1256 only)
        #		0110 = AIN6 (ADS1256 only)
        #		0111 = AIN7 (ADS1256 only)
        #		1xxx = AINCOM (when PSEL3 = 1, PSEL2, PSEL1, PSEL0 are dont care)
        #
        #		NOTE: When using an ADS1255 make sure to only select the available inputs.
        #
        #	Bits 3-0 NSEL3, NSEL2, NSEL1, NSEL0: Negative Input Channel (AINN)Select
        #		0000 = AIN0
        #		0001 = AIN1 (default)
        #		0010 = AIN2 (ADS1256 only)
        #		0011 = AIN3 (ADS1256 only)
        #		0100 = AIN4 (ADS1256 only)
        #		0101 = AIN5 (ADS1256 only)
        #		0110 = AIN6 (ADS1256 only)
        #		0111 = AIN7 (ADS1256 only)
        #		1xxx = AINCOM (when NSEL3 = 1, NSEL2, NSEL1, NSEL0 are dont care)'''

        ch_list = [0x0f, 0x1f, 0x2f, 0x3f, 0x4f]
        if _ch > 7:
            return
        self.ADS1256_WriteReg(REG_E['REG_MUX'], ch_list[_ch])  # Bit3 = 1, AINN connection AINCOM
        self.Channel = _ch

    def ADS1256_SetDiffChannel(self, _ch):
        """
        The configuration difference channel
        :param _ch:
        :return:
        """

        '''
        Bits 7-4 PSEL3, PSEL2, PSEL1, PSEL0: Positive Input Channel (AINP) Select
            0000 = AIN0 (default)
            0001 = AIN1
            0010 = AIN2 (ADS1256 only)
            0011 = AIN3 (ADS1256 only)
            0100 = AIN4 (ADS1256 only)
            0101 = AIN5 (ADS1256 only)
            0110 = AIN6 (ADS1256 only)
            0111 = AIN7 (ADS1256 only)
            1xxx = AINCOM (when PSEL3 = 1, PSEL2, PSEL1, PSEL0 are dont't care)
        
            NOTE: When using an ADS1255 make sure to only select the available inputs.
        
        Bits 3-0 NSEL3, NSEL2, NSEL1, NSEL0: Negative Input Channel (AINN)Select
            0000 = AIN0
            0001 = AIN1 (default)
            0010 = AIN2 (ADS1256 only)
            0011 = AIN3 (ADS1256 only)
            0100 = AIN4 (ADS1256 only)
            0101 = AIN5 (ADS1256 only)
            0110 = AIN6 (ADS1256 only)
            0111 = AIN7 (ADS1256 only)
            1xxx = AINCOM (when NSEL3 = 1, NSEL2, NSEL1, NSEL0 are don't care)
        '''

        if _ch == 0:
            # DiffChannel  AIN0 - AIN1
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (0 << 4) | 1)
        elif _ch == 1:
            # DiffChannel   AIN2 - AIN3
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (2 << 4) | 3)
        elif _ch == 2:
            # DiffChannel    AIN4 - AIN5
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (4 << 4) | 5)
        elif _ch == 3:
            # DiffChannel   AIN6 - AIN7
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (6 << 4) | 7)

        if _ch in [0, 1, 2, 3]:
            self.Channel = _ch

    def ADS1256_WaitDRDY(self):
        """
        delay time  wait for automatic calibration
        :return:
        """
        for i in range(400000):
            if self.dataReady_is_Low():
                break
        if i >= 400000:
            print("ADS1256_WaitDRDY() Time Out ...\n")

    def ADS1256_ReadData(self):
        """
        read ADC value
        :return:
        """
        # read = 0
        buf = [0x00, 0x00, 0x00]

        self.set_CS_Low()

        self.ADS1256_Send8Bit(CMD['CMD_RDATA'])  # read ADC command
        self.ADS1256_DelayDATA()  # delay time

        # Read the sample results 24-bit
        buf[0] = self.ADS1256_Receive8Bit()
        buf[1] = self.ADS1256_Receive8Bit()
        buf[2] = self.ADS1256_Receive8Bit()

        read = (np.int32(buf[0] << 16)) & 0x00FF0000
        read |= (buf[1] << 8)  # Pay attention to It is wrong   read |= (buf[1] << 8) */
        read |= buf[2]

        self.set_CS_High()

        return read

        # Extend a signed number
        # if read & 0x800000:
        #     read |= 0xFF000000
        #
        # return np.int32(read)

    def ADS1256_GetAdc(self, _ch):
        """
        read stored ADC value
        :param _ch:
        :return:
        """
        if _ch > 7:
            return 0

        return self.AdcNow[_ch]

    def ADS1256_OneShot(self, _ch):
        """
        one shot read channel
        :param _ch:
        :return:
        """
        if _ch != self.Channel:
            self.ADS1256_SetChannel(self.Channel)
            self.bsp_DelayUS(5)

        self.ADS1256_WriteCmd(CMD['CMD_SYNC'])
        self.bsp_DelayUS(5)

        self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])
        self.bsp_DelayUS(25)

        _data = self.ADS1256_ReadData()
        return _data

        # self.AdcNow[self.Channel] = self.ADS1256_ReadData()

        # return self.Data_To_Volt(self.AdcNow[self.Channel])

    def ADS1256_ISR(self):
        """
        Collection procedures
        :return:
        """
        # 0  Single-ended input  8 channel
        if self.ScanMode == 0:
            # Switch channel mode
            self.ADS1256_SetChannel(self.Channel)
            self.bsp_DelayUS(5)

            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])
            self.bsp_DelayUS(5)

            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])
            self.bsp_DelayUS(25)

            if self.Channel == 0:
                self.AdcNow[self.Channel] = self.ADS1256_ReadData()
            else:
                self.AdcNow[self.Channel] = self.ADS1256_ReadData()

            self.Channel += 1
            if self.Channel >= 8:
                self.Channel = 0

        else:  # 1 Differential input  4 channel
            self.ADS1256_SetDiffChannel(self.Channel)  # change DiffChannel
            self.bsp_DelayUS(5)

            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])
            self.bsp_DelayUS(5)

            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])
            self.bsp_DelayUS(25)

            if self.Channel == 0:
                self.AdcNow[3] = self.ADS1256_ReadData()
            else:
                self.AdcNow[self.Channel - 1] = self.ADS1256_ReadData()

            self.Channel += 1
            if self.Channel >= 4:
                self.Channel = 0

    def ADS1256_Scan(self):
        """
        Scan function
        :return:
        """
        if self.dataReady_is_Low():  # Data is ready, collect data
            self.ADS1256_ISR()
            return 1
        return 0

    def Write_DAC8552(self, _channel, _data):
        """
        DAC send data
        :param _channel:
        :param _data:
        :return:
        """
        print("DAC send data: NOT IMPLEMENTED YET")

    @staticmethod
    def Voltage_Convert(vref, voltage):
        """
        Voltage value conversion function. Vref : The reference voltage 3.3V or 5V
        voltage : output DAC value
        :param vref:
        :param voltage:
        :return:
        """
        return np.int16(65536 * voltage / vref)

    @staticmethod
    def Data_To_Volt(val):
        """
        Convert 24 bits to voltage
        :param val:
        :return:
        """
        return (val * 100) / 167 / 1000000.0


if __name__ == '__main__':
    print("TESTING STARTS!")

    if not bcm2835_init():
        print('d')
    try:
        ch_num = 1
        adc = ADS1256(ch_num)
        print(adc.ADS1256_ReadData())

        # readout_val = [0, 0, 0, 0, 0, 0, 0, 0]  # -1.0
        # volt_val = [0, 0, 0, 0, 0, 0, 0, 0]  # -2.0
        # while True:
        #     for i in range(5):
        #         print('ad' + str(i) + ' ' + str(adc.ADS1256_OneShot(i)))
            # adc.ADS1256_OneShot(0)
            # print([adc.Data_To_Volt(val) for val in adc.AdcNow])
            # adc.bsp_DelayUS(1000000)  # (100000) # limited sampling rate
    finally:
        bcm2835_spi_end()
        bcm2835_close()
        print("TESTING ENDS")
