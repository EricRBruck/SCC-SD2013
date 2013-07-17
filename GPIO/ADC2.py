#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

import time
import spidev
import RPi.GPIO as GPIO
from lib.Char_Plate.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import smbus

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
lcd = Adafruit_CharLCDPlate(busnum=0)
spi = spidev.SpiDev()
light_adc = 1
l = list()
statusLED = 23
print "Press CTRL+Z to exit"
GPIO.setup(statusLED, GPIO.OUT)
lcd.backlight(lcd.ON)
lcd.clear()


def analogRead(port):
    """Read the given ADC port and preform the necessary shifting of bits"""
    spi.open(0, 0)
    if (port > 7) or (port < 0):
        print 'analogRead -- Port Error, Must use a port between 0 and 7'
        return -1
    r = spi.xfer2([1, (8 + port) << 4, 0])
    value = ((r[1] & 3) << 8) + r[2]
    spi.close()
    return value


def movavg(ave_list, length, value):
    """A function that smooths the results by averaging a list"""
    ave_list.append(value)
    if length < len(ave_list):
        del ave_list[0]
    value = 0
    for x in ave_list[:]:
        value += x
    return value / len(ave_list)


while True:
    lcd.home()
    GPIO.output(statusLED, True)                                # Status Led On
    lcd.message('Light Sensor:\n' + str(
        movavg(l, 4, analogRead(light_adc))) + '     ')   # Read analog value and send it to the display
    time.sleep(.1)                                              # Wait a little
    GPIO.output(statusLED, False)                               # Status Led off
    time.sleep(.155)                                            # Wait a bit longer