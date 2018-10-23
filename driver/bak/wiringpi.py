# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_wiringpi', [dirname(__file__)])
        except ImportError:
            import _wiringpi
            return _wiringpi
        if fp is not None:
            try:
                _mod = imp.load_module('_wiringpi', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _wiringpi = swig_import_helper()
    del swig_import_helper
else:
    import _wiringpi
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0



def wiringPiISR(*args):
  return _wiringpi.wiringPiISR(*args)
wiringPiISR = _wiringpi.wiringPiISR

def wiringPiFailure(*args):
  return _wiringpi.wiringPiFailure(*args)
wiringPiFailure = _wiringpi.wiringPiFailure

def wiringPiFindNode(*args):
  return _wiringpi.wiringPiFindNode(*args)
wiringPiFindNode = _wiringpi.wiringPiFindNode

def wiringPiNewNode(*args):
  return _wiringpi.wiringPiNewNode(*args)
wiringPiNewNode = _wiringpi.wiringPiNewNode

def wiringPiVersion(*args):
  return _wiringpi.wiringPiVersion(*args)
wiringPiVersion = _wiringpi.wiringPiVersion

def wiringPiSetup():
  return _wiringpi.wiringPiSetup()
wiringPiSetup = _wiringpi.wiringPiSetup

def wiringPiSetupSys():
  return _wiringpi.wiringPiSetupSys()
wiringPiSetupSys = _wiringpi.wiringPiSetupSys

def wiringPiSetupGpio():
  return _wiringpi.wiringPiSetupGpio()
wiringPiSetupGpio = _wiringpi.wiringPiSetupGpio

def wiringPiSetupPhys():
  return _wiringpi.wiringPiSetupPhys()
wiringPiSetupPhys = _wiringpi.wiringPiSetupPhys

def pinModeAlt(*args):
  return _wiringpi.pinModeAlt(*args)
pinModeAlt = _wiringpi.pinModeAlt

def pinMode(*args):
  return _wiringpi.pinMode(*args)
pinMode = _wiringpi.pinMode

def pullUpDnControl(*args):
  return _wiringpi.pullUpDnControl(*args)
pullUpDnControl = _wiringpi.pullUpDnControl

def digitalRead(*args):
  return _wiringpi.digitalRead(*args)
digitalRead = _wiringpi.digitalRead

def digitalWrite(*args):
  return _wiringpi.digitalWrite(*args)
digitalWrite = _wiringpi.digitalWrite

def pwmWrite(*args):
  return _wiringpi.pwmWrite(*args)
pwmWrite = _wiringpi.pwmWrite

def analogRead(*args):
  return _wiringpi.analogRead(*args)
analogRead = _wiringpi.analogRead

def analogWrite(*args):
  return _wiringpi.analogWrite(*args)
analogWrite = _wiringpi.analogWrite

def piGpioLayout():
  return _wiringpi.piGpioLayout()
piGpioLayout = _wiringpi.piGpioLayout

def piBoardRev():
  return _wiringpi.piBoardRev()
piBoardRev = _wiringpi.piBoardRev

def piBoardId(*args):
  return _wiringpi.piBoardId(*args)
piBoardId = _wiringpi.piBoardId

def wpiPinToGpio(*args):
  return _wiringpi.wpiPinToGpio(*args)
wpiPinToGpio = _wiringpi.wpiPinToGpio

def physPinToGpio(*args):
  return _wiringpi.physPinToGpio(*args)
physPinToGpio = _wiringpi.physPinToGpio

def setPadDrive(*args):
  return _wiringpi.setPadDrive(*args)
setPadDrive = _wiringpi.setPadDrive

def getAlt(*args):
  return _wiringpi.getAlt(*args)
getAlt = _wiringpi.getAlt

def pwmToneWrite(*args):
  return _wiringpi.pwmToneWrite(*args)
pwmToneWrite = _wiringpi.pwmToneWrite

def pwmSetMode(*args):
  return _wiringpi.pwmSetMode(*args)
pwmSetMode = _wiringpi.pwmSetMode

def pwmSetRange(*args):
  return _wiringpi.pwmSetRange(*args)
pwmSetRange = _wiringpi.pwmSetRange

def pwmSetClock(*args):
  return _wiringpi.pwmSetClock(*args)
pwmSetClock = _wiringpi.pwmSetClock

def gpioClockSet(*args):
  return _wiringpi.gpioClockSet(*args)
gpioClockSet = _wiringpi.gpioClockSet

def digitalReadByte():
  return _wiringpi.digitalReadByte()
digitalReadByte = _wiringpi.digitalReadByte

def digitalReadByte2():
  return _wiringpi.digitalReadByte2()
digitalReadByte2 = _wiringpi.digitalReadByte2

def digitalWriteByte(*args):
  return _wiringpi.digitalWriteByte(*args)
digitalWriteByte = _wiringpi.digitalWriteByte

def digitalWriteByte2(*args):
  return _wiringpi.digitalWriteByte2(*args)
digitalWriteByte2 = _wiringpi.digitalWriteByte2

def waitForInterrupt(*args):
  return _wiringpi.waitForInterrupt(*args)
waitForInterrupt = _wiringpi.waitForInterrupt

def piThreadCreate(*args):
  return _wiringpi.piThreadCreate(*args)
piThreadCreate = _wiringpi.piThreadCreate

def piLock(*args):
  return _wiringpi.piLock(*args)
piLock = _wiringpi.piLock

def piUnlock(*args):
  return _wiringpi.piUnlock(*args)
piUnlock = _wiringpi.piUnlock

def piHiPri(*args):
  return _wiringpi.piHiPri(*args)
piHiPri = _wiringpi.piHiPri

def delay(*args):
  return _wiringpi.delay(*args)
delay = _wiringpi.delay

def delayMicroseconds(*args):
  return _wiringpi.delayMicroseconds(*args)
delayMicroseconds = _wiringpi.delayMicroseconds

def millis():
  return _wiringpi.millis()
millis = _wiringpi.millis

def micros():
  return _wiringpi.micros()
micros = _wiringpi.micros

def wiringPiI2CRead(*args):
  return _wiringpi.wiringPiI2CRead(*args)
wiringPiI2CRead = _wiringpi.wiringPiI2CRead

def wiringPiI2CReadReg8(*args):
  return _wiringpi.wiringPiI2CReadReg8(*args)
wiringPiI2CReadReg8 = _wiringpi.wiringPiI2CReadReg8

def wiringPiI2CReadReg16(*args):
  return _wiringpi.wiringPiI2CReadReg16(*args)
wiringPiI2CReadReg16 = _wiringpi.wiringPiI2CReadReg16

def wiringPiI2CWrite(*args):
  return _wiringpi.wiringPiI2CWrite(*args)
wiringPiI2CWrite = _wiringpi.wiringPiI2CWrite

def wiringPiI2CWriteReg8(*args):
  return _wiringpi.wiringPiI2CWriteReg8(*args)
wiringPiI2CWriteReg8 = _wiringpi.wiringPiI2CWriteReg8

def wiringPiI2CWriteReg16(*args):
  return _wiringpi.wiringPiI2CWriteReg16(*args)
wiringPiI2CWriteReg16 = _wiringpi.wiringPiI2CWriteReg16

def wiringPiI2CSetupInterface(*args):
  return _wiringpi.wiringPiI2CSetupInterface(*args)
wiringPiI2CSetupInterface = _wiringpi.wiringPiI2CSetupInterface

def wiringPiI2CSetup(*args):
  return _wiringpi.wiringPiI2CSetup(*args)
wiringPiI2CSetup = _wiringpi.wiringPiI2CSetup

def wiringPiSPIGetFd(*args):
  return _wiringpi.wiringPiSPIGetFd(*args)
wiringPiSPIGetFd = _wiringpi.wiringPiSPIGetFd

def wiringPiSPIDataRW(*args):
  return _wiringpi.wiringPiSPIDataRW(*args)
wiringPiSPIDataRW = _wiringpi.wiringPiSPIDataRW

def wiringPiSPISetupMode(*args):
  return _wiringpi.wiringPiSPISetupMode(*args)
wiringPiSPISetupMode = _wiringpi.wiringPiSPISetupMode

def wiringPiSPISetup(*args):
  return _wiringpi.wiringPiSPISetup(*args)
wiringPiSPISetup = _wiringpi.wiringPiSPISetup

def serialOpen(*args):
  return _wiringpi.serialOpen(*args)
serialOpen = _wiringpi.serialOpen

def serialClose(*args):
  return _wiringpi.serialClose(*args)
serialClose = _wiringpi.serialClose

def serialFlush(*args):
  return _wiringpi.serialFlush(*args)
serialFlush = _wiringpi.serialFlush

def serialPutchar(*args):
  return _wiringpi.serialPutchar(*args)
serialPutchar = _wiringpi.serialPutchar

def serialPuts(*args):
  return _wiringpi.serialPuts(*args)
serialPuts = _wiringpi.serialPuts

def serialPrintf(*args):
  return _wiringpi.serialPrintf(*args)
serialPrintf = _wiringpi.serialPrintf

def serialDataAvail(*args):
  return _wiringpi.serialDataAvail(*args)
serialDataAvail = _wiringpi.serialDataAvail

def serialGetchar(*args):
  return _wiringpi.serialGetchar(*args)
serialGetchar = _wiringpi.serialGetchar

def shiftIn(*args):
  return _wiringpi.shiftIn(*args)
shiftIn = _wiringpi.shiftIn

def shiftOut(*args):
  return _wiringpi.shiftOut(*args)
shiftOut = _wiringpi.shiftOut

def drcSetupSerial(*args):
  return _wiringpi.drcSetupSerial(*args)
drcSetupSerial = _wiringpi.drcSetupSerial

def ads1115Setup(*args):
  return _wiringpi.ads1115Setup(*args)
ads1115Setup = _wiringpi.ads1115Setup

def max31855Setup(*args):
  return _wiringpi.max31855Setup(*args)
max31855Setup = _wiringpi.max31855Setup

def max5322Setup(*args):
  return _wiringpi.max5322Setup(*args)
max5322Setup = _wiringpi.max5322Setup

def mcp23008Setup(*args):
  return _wiringpi.mcp23008Setup(*args)
mcp23008Setup = _wiringpi.mcp23008Setup

def mcp23016Setup(*args):
  return _wiringpi.mcp23016Setup(*args)
mcp23016Setup = _wiringpi.mcp23016Setup

def mcp23017Setup(*args):
  return _wiringpi.mcp23017Setup(*args)
mcp23017Setup = _wiringpi.mcp23017Setup

def mcp23s08Setup(*args):
  return _wiringpi.mcp23s08Setup(*args)
mcp23s08Setup = _wiringpi.mcp23s08Setup

def mcp23s17Setup(*args):
  return _wiringpi.mcp23s17Setup(*args)
mcp23s17Setup = _wiringpi.mcp23s17Setup

def mcp3002Setup(*args):
  return _wiringpi.mcp3002Setup(*args)
mcp3002Setup = _wiringpi.mcp3002Setup

def mcp3004Setup(*args):
  return _wiringpi.mcp3004Setup(*args)
mcp3004Setup = _wiringpi.mcp3004Setup

def mcp3422Setup(*args):
  return _wiringpi.mcp3422Setup(*args)
mcp3422Setup = _wiringpi.mcp3422Setup

def mcp4802Setup(*args):
  return _wiringpi.mcp4802Setup(*args)
mcp4802Setup = _wiringpi.mcp4802Setup

def pcf8574Setup(*args):
  return _wiringpi.pcf8574Setup(*args)
pcf8574Setup = _wiringpi.pcf8574Setup

def pcf8591Setup(*args):
  return _wiringpi.pcf8591Setup(*args)
pcf8591Setup = _wiringpi.pcf8591Setup

def sn3218Setup(*args):
  return _wiringpi.sn3218Setup(*args)
sn3218Setup = _wiringpi.sn3218Setup

def softPwmCreate(*args):
  return _wiringpi.softPwmCreate(*args)
softPwmCreate = _wiringpi.softPwmCreate

def softPwmWrite(*args):
  return _wiringpi.softPwmWrite(*args)
softPwmWrite = _wiringpi.softPwmWrite

def softPwmStop(*args):
  return _wiringpi.softPwmStop(*args)
softPwmStop = _wiringpi.softPwmStop

def softServoWrite(*args):
  return _wiringpi.softServoWrite(*args)
softServoWrite = _wiringpi.softServoWrite

def softServoSetup(*args):
  return _wiringpi.softServoSetup(*args)
softServoSetup = _wiringpi.softServoSetup

def softToneCreate(*args):
  return _wiringpi.softToneCreate(*args)
softToneCreate = _wiringpi.softToneCreate

def softToneStop(*args):
  return _wiringpi.softToneStop(*args)
softToneStop = _wiringpi.softToneStop

def softToneWrite(*args):
  return _wiringpi.softToneWrite(*args)
softToneWrite = _wiringpi.softToneWrite

def sr595Setup(*args):
  return _wiringpi.sr595Setup(*args)
sr595Setup = _wiringpi.sr595Setup

def bmp180Setup(*args):
  return _wiringpi.bmp180Setup(*args)
bmp180Setup = _wiringpi.bmp180Setup

def drcSetupNet(*args):
  return _wiringpi.drcSetupNet(*args)
drcSetupNet = _wiringpi.drcSetupNet

def ds18b20Setup(*args):
  return _wiringpi.ds18b20Setup(*args)
ds18b20Setup = _wiringpi.ds18b20Setup

def htu21dSetup(*args):
  return _wiringpi.htu21dSetup(*args)
htu21dSetup = _wiringpi.htu21dSetup

def pseudoPinsSetup(*args):
  return _wiringpi.pseudoPinsSetup(*args)
pseudoPinsSetup = _wiringpi.pseudoPinsSetup

def rht03Setup(*args):
  return _wiringpi.rht03Setup(*args)
rht03Setup = _wiringpi.rht03Setup

def loadWPiExtension(*args):
  return _wiringpi.loadWPiExtension(*args)
loadWPiExtension = _wiringpi.loadWPiExtension

def ds1302rtcRead(*args):
  return _wiringpi.ds1302rtcRead(*args)
ds1302rtcRead = _wiringpi.ds1302rtcRead

def ds1302rtcWrite(*args):
  return _wiringpi.ds1302rtcWrite(*args)
ds1302rtcWrite = _wiringpi.ds1302rtcWrite

def ds1302ramRead(*args):
  return _wiringpi.ds1302ramRead(*args)
ds1302ramRead = _wiringpi.ds1302ramRead

def ds1302ramWrite(*args):
  return _wiringpi.ds1302ramWrite(*args)
ds1302ramWrite = _wiringpi.ds1302ramWrite

def ds1302clockRead(*args):
  return _wiringpi.ds1302clockRead(*args)
ds1302clockRead = _wiringpi.ds1302clockRead

def ds1302clockWrite(*args):
  return _wiringpi.ds1302clockWrite(*args)
ds1302clockWrite = _wiringpi.ds1302clockWrite

def ds1302trickleCharge(*args):
  return _wiringpi.ds1302trickleCharge(*args)
ds1302trickleCharge = _wiringpi.ds1302trickleCharge

def ds1302setup(*args):
  return _wiringpi.ds1302setup(*args)
ds1302setup = _wiringpi.ds1302setup

def gertboardAnalogWrite(*args):
  return _wiringpi.gertboardAnalogWrite(*args)
gertboardAnalogWrite = _wiringpi.gertboardAnalogWrite

def gertboardAnalogRead(*args):
  return _wiringpi.gertboardAnalogRead(*args)
gertboardAnalogRead = _wiringpi.gertboardAnalogRead

def gertboardSPISetup():
  return _wiringpi.gertboardSPISetup()
gertboardSPISetup = _wiringpi.gertboardSPISetup

def gertboardAnalogSetup(*args):
  return _wiringpi.gertboardAnalogSetup(*args)
gertboardAnalogSetup = _wiringpi.gertboardAnalogSetup

def lcd128x64setOrigin(*args):
  return _wiringpi.lcd128x64setOrigin(*args)
lcd128x64setOrigin = _wiringpi.lcd128x64setOrigin

def lcd128x64setOrientation(*args):
  return _wiringpi.lcd128x64setOrientation(*args)
lcd128x64setOrientation = _wiringpi.lcd128x64setOrientation

def lcd128x64orientCoordinates(*args):
  return _wiringpi.lcd128x64orientCoordinates(*args)
lcd128x64orientCoordinates = _wiringpi.lcd128x64orientCoordinates

def lcd128x64getScreenSize(*args):
  return _wiringpi.lcd128x64getScreenSize(*args)
lcd128x64getScreenSize = _wiringpi.lcd128x64getScreenSize

def lcd128x64point(*args):
  return _wiringpi.lcd128x64point(*args)
lcd128x64point = _wiringpi.lcd128x64point

def lcd128x64line(*args):
  return _wiringpi.lcd128x64line(*args)
lcd128x64line = _wiringpi.lcd128x64line

def lcd128x64lineTo(*args):
  return _wiringpi.lcd128x64lineTo(*args)
lcd128x64lineTo = _wiringpi.lcd128x64lineTo

def lcd128x64rectangle(*args):
  return _wiringpi.lcd128x64rectangle(*args)
lcd128x64rectangle = _wiringpi.lcd128x64rectangle

def lcd128x64circle(*args):
  return _wiringpi.lcd128x64circle(*args)
lcd128x64circle = _wiringpi.lcd128x64circle

def lcd128x64ellipse(*args):
  return _wiringpi.lcd128x64ellipse(*args)
lcd128x64ellipse = _wiringpi.lcd128x64ellipse

def lcd128x64putchar(*args):
  return _wiringpi.lcd128x64putchar(*args)
lcd128x64putchar = _wiringpi.lcd128x64putchar

def lcd128x64puts(*args):
  return _wiringpi.lcd128x64puts(*args)
lcd128x64puts = _wiringpi.lcd128x64puts

def lcd128x64update():
  return _wiringpi.lcd128x64update()
lcd128x64update = _wiringpi.lcd128x64update

def lcd128x64clear(*args):
  return _wiringpi.lcd128x64clear(*args)
lcd128x64clear = _wiringpi.lcd128x64clear

def lcd128x64setup():
  return _wiringpi.lcd128x64setup()
lcd128x64setup = _wiringpi.lcd128x64setup

def lcdHome(*args):
  return _wiringpi.lcdHome(*args)
lcdHome = _wiringpi.lcdHome

def lcdClear(*args):
  return _wiringpi.lcdClear(*args)
lcdClear = _wiringpi.lcdClear

def lcdDisplay(*args):
  return _wiringpi.lcdDisplay(*args)
lcdDisplay = _wiringpi.lcdDisplay

def lcdCursor(*args):
  return _wiringpi.lcdCursor(*args)
lcdCursor = _wiringpi.lcdCursor

def lcdCursorBlink(*args):
  return _wiringpi.lcdCursorBlink(*args)
lcdCursorBlink = _wiringpi.lcdCursorBlink

def lcdSendCommand(*args):
  return _wiringpi.lcdSendCommand(*args)
lcdSendCommand = _wiringpi.lcdSendCommand

def lcdPosition(*args):
  return _wiringpi.lcdPosition(*args)
lcdPosition = _wiringpi.lcdPosition

def lcdCharDef(*args):
  return _wiringpi.lcdCharDef(*args)
lcdCharDef = _wiringpi.lcdCharDef

def lcdPutchar(*args):
  return _wiringpi.lcdPutchar(*args)
lcdPutchar = _wiringpi.lcdPutchar

def lcdPuts(*args):
  return _wiringpi.lcdPuts(*args)
lcdPuts = _wiringpi.lcdPuts

def lcdPrintf(*args):
  return _wiringpi.lcdPrintf(*args)
lcdPrintf = _wiringpi.lcdPrintf

def lcdInit(*args):
  return _wiringpi.lcdInit(*args)
lcdInit = _wiringpi.lcdInit

def maxDetectRead(*args):
  return _wiringpi.maxDetectRead(*args)
maxDetectRead = _wiringpi.maxDetectRead

def readRHT03(*args):
  return _wiringpi.readRHT03(*args)
readRHT03 = _wiringpi.readRHT03

def piGlow1(*args):
  return _wiringpi.piGlow1(*args)
piGlow1 = _wiringpi.piGlow1

def piGlowLeg(*args):
  return _wiringpi.piGlowLeg(*args)
piGlowLeg = _wiringpi.piGlowLeg

def piGlowRing(*args):
  return _wiringpi.piGlowRing(*args)
piGlowRing = _wiringpi.piGlowRing

def piGlowSetup(*args):
  return _wiringpi.piGlowSetup(*args)
piGlowSetup = _wiringpi.piGlowSetup

def setupNesJoystick(*args):
  return _wiringpi.setupNesJoystick(*args)
setupNesJoystick = _wiringpi.setupNesJoystick

def readNesJoystick(*args):
  return _wiringpi.readNesJoystick(*args)
readNesJoystick = _wiringpi.readNesJoystick

def scrollPhatPoint(*args):
  return _wiringpi.scrollPhatPoint(*args)
scrollPhatPoint = _wiringpi.scrollPhatPoint

def scrollPhatLine(*args):
  return _wiringpi.scrollPhatLine(*args)
scrollPhatLine = _wiringpi.scrollPhatLine

def scrollPhatLineTo(*args):
  return _wiringpi.scrollPhatLineTo(*args)
scrollPhatLineTo = _wiringpi.scrollPhatLineTo

def scrollPhatRectangle(*args):
  return _wiringpi.scrollPhatRectangle(*args)
scrollPhatRectangle = _wiringpi.scrollPhatRectangle

def scrollPhatUpdate():
  return _wiringpi.scrollPhatUpdate()
scrollPhatUpdate = _wiringpi.scrollPhatUpdate

def scrollPhatClear():
  return _wiringpi.scrollPhatClear()
scrollPhatClear = _wiringpi.scrollPhatClear

def scrollPhatPutchar(*args):
  return _wiringpi.scrollPhatPutchar(*args)
scrollPhatPutchar = _wiringpi.scrollPhatPutchar

def scrollPhatPuts(*args):
  return _wiringpi.scrollPhatPuts(*args)
scrollPhatPuts = _wiringpi.scrollPhatPuts

def scrollPhatPrintf(*args):
  return _wiringpi.scrollPhatPrintf(*args)
scrollPhatPrintf = _wiringpi.scrollPhatPrintf

def scrollPhatPrintSpeed(*args):
  return _wiringpi.scrollPhatPrintSpeed(*args)
scrollPhatPrintSpeed = _wiringpi.scrollPhatPrintSpeed

def scrollPhatIntensity(*args):
  return _wiringpi.scrollPhatIntensity(*args)
scrollPhatIntensity = _wiringpi.scrollPhatIntensity

def scrollPhatSetup():
  return _wiringpi.scrollPhatSetup()
scrollPhatSetup = _wiringpi.scrollPhatSetup

def piFaceSetup(*args):
  return _wiringpi.piFaceSetup(*args)
piFaceSetup = _wiringpi.piFaceSetup
# wiringPi modes

WPI_MODE_PINS = 0;
WPI_MODE_GPIO = 1;
WPI_MODE_GPIO_SYS = 2;
WPI_MODE_PHYS = 3;
WPI_MODE_PIFACE = 4;
WPI_MODE_UNINITIALISED = -1;

# Pin modes

INPUT = 0;
OUTPUT = 1;
PWM_OUTPUT = 2;
GPIO_CLOCK = 3;
SOFT_PWM_OUTPUT = 4;
SOFT_TONE_OUTPUT = 5;
PWM_TONE_OUTPUT = 6;

LOW = 0;
HIGH = 1;

# Pull up/down/none

PUD_OFF = 0;
PUD_DOWN = 1;
PUD_UP = 2;

# PWM

PWM_MODE_MS = 0;
PWM_MODE_BAL = 1;

# Interrupt levels

INT_EDGE_SETUP = 0;
INT_EDGE_FALLING = 1;
INT_EDGE_RISING = 2;
INT_EDGE_BOTH = 3;

class nes(object):
  def setupNesJoystick(self,*args):
    return setupNesJoystick(*args)
  def readNesJoystick(self,*args):
    return readNesJoystick(*args)

class Serial(object):
  device = '/dev/ttyAMA0'
  baud = 9600
  serial_id = 0
  def printf(self,*args):
    return serialPrintf(self.serial_id,*args)
  def dataAvail(self,*args):
    return serialDataAvail(self.serial_id,*args)
  def getchar(self,*args):
    return serialGetchar(self.serial_id,*args)
  def putchar(self,*args):
    return serialPutchar(self.serial_id,*args)
  def puts(self,*args):
    return serialPuts(self.serial_id,*args)
  def __init__(self,device,baud):
    self.device = device
    self.baud = baud
    self.serial_id = serialOpen(self.device,self.baud)
  def __del__(self):
    serialClose(self.serial_id)

class I2C(object):
  def setupInterface(self,*args):
  	return wiringPiI2CSetupInterface(*args)
  def setup(self,*args):
    return wiringPiI2CSetup(*args)
  def read(self,*args):
    return wiringPiI2CRead(*args)
  def readReg8(self,*args):
    return wiringPiI2CReadReg8(*args)
  def readReg16(self,*args):
    return wiringPiI2CReadReg16(*args)
  def write(self,*args):
    return wiringPiI2CWrite(*args)
  def writeReg8(self,*args):
    return wiringPiI2CWriteReg8(*args)
  def writeReg16(self,*args):
    return wiringPiI2CWriteReg16(*args)

class GPIO(object):
  WPI_MODE_PINS = 0
  WPI_MODE_GPIO = 1
  WPI_MODE_GPIO_SYS = 2
  WPI_MODE_PHYS = 3
  WPI_MODE_PIFACE = 4
  WPI_MODE_UNINITIALISED = -1

  INPUT = 0
  OUTPUT = 1
  PWM_OUTPUT = 2
  GPIO_CLOCK = 3

  LOW = 0
  HIGH = 1

  PUD_OFF = 0
  PUD_DOWN = 1
  PUD_UP = 2

  PWM_MODE_MS = 0
  PWM_MODE_BAL = 1

  INT_EDGE_SETUP = 0
  INT_EDGE_FALLING = 1
  INT_EDGE_RISING = 2
  INT_EDGE_BOTH = 3

  LSBFIRST = 0
  MSBFIRST = 1

  MODE = 0
  def __init__(self,pinmode=0):
    self.MODE=pinmode
    if pinmode==self.WPI_MODE_PINS:
      wiringPiSetup()
    if pinmode==self.WPI_MODE_GPIO:
      wiringPiSetupGpio()
    if pinmode==self.WPI_MODE_GPIO_SYS:
      wiringPiSetupSys()
    if pinmode==self.WPI_MODE_PHYS:
      wiringPiSetupPhys()
    if pinmode==self.WPI_MODE_PIFACE:
      wiringPiSetupPiFace()

  def delay(self,*args):
    delay(*args)
  def delayMicroseconds(self,*args):
    delayMicroseconds(*args)
  def millis(self):
    return millis()
  def micros(self):
    return micros()

  def piHiPri(self,*args):
    return piHiPri(*args)

  def piBoardRev(self):
    return piBoardRev()
  def wpiPinToGpio(self,*args):
    return wpiPinToGpio(*args)
  def setPadDrive(self,*args):
    return setPadDrive(*args)
  def getAlt(self,*args):
    return getAlt(*args)
  def digitalWriteByte(self,*args):
    return digitalWriteByte(*args)

  def pwmSetMode(self,*args):
    pwmSetMode(*args)
  def pwmSetRange(self,*args):
    pwmSetRange(*args)
  def pwmSetClock(self,*args):
    pwmSetClock(*args)
  def gpioClockSet(self,*args):
    gpioClockSet(*args)
  def pwmWrite(self,*args):
    pwmWrite(*args)

  def pinMode(self,*args):
    pinMode(*args)

  def digitalWrite(self,*args):
    digitalWrite(*args)
  def digitalRead(self,*args):
    return digitalRead(*args)
  def digitalWriteByte(self,*args):
    digitalWriteByte(*args)

  def analogWrite(self,*args):
    analogWrite(*args)
  def analogRead(self,*args):
    return analogRead(*args)

  def shiftOut(self,*args):
    shiftOut(*args)
  def shiftIn(self,*args):
    return shiftIn(*args)

  def pullUpDnControl(self,*args):
    return pullUpDnControl(*args)

  def waitForInterrupt(self,*args):
    return waitForInterrupt(*args)
  def wiringPiISR(self,*args):
    return wiringPiISR(*args)

  def softPwmCreate(self,*args):
    return softPwmCreate(*args)
  def softPwmWrite(self,*args):
    return softPwmWrite(*args)

  def softToneCreate(self,*args):
    return softToneCreate(*args)
  def softToneWrite(self,*args):
    return softToneWrite(*args)

  def lcdHome(self,*args):
    return lcdHome(self,*args)
  def lcdCLear(self,*args):
    return lcdClear(self,*args)
  def lcdSendCommand(self,*args):
    return lcdSendCommand(self,*args)
  def lcdPosition(self,*args):
    return lcdPosition(self,*args)
  def lcdPutchar(self,*args):
    return lcdPutchar(self,*args)
  def lcdPuts(self,*args):
    return lcdPuts(self,*args)
  def lcdPrintf(self,*args):
    return lcdPrintf(self,*args)
  def lcdInit(self,*args):
    return lcdInit(self,*args)
  def piGlowSetup(self,*args):
    return piGlowSetup(self,*args)
  def piGlow1(self,*args):
    return piGlow1(self,*args)
  def piGlowLeg(self,*args):
    return piGlowLeg(self,*args)
  def piGlowRing(self,*args):
    return piGlowRing(self,*args)

# This file is compatible with both classic and new-style classes.


