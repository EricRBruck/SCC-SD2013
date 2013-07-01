#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

import time
import spidev
import RPi.GPIO as GPIO
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
import smbus

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
segment = SevenSegment(address=0x70)  # which port the display is
spi = spidev.SpiDev()
light_adc = 7
l = list()
statusLED = 25
print "Press CTRL+Z to exit"
GPIO.setup(statusLED, GPIO.OUT)


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
    GPIO.output(statusLED, True)                                # Status Led On
    segment.writeInt(movavg(l, 4, analogRead(light_adc)))       # Read analog value and send it to the display
    time.sleep(.125)                                            # Wait a little
    GPIO.output(statusLED, False)                               # Status Led off
    time.sleep(.175)                                            # Wait a bit longer