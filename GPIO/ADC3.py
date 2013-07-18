#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

import time
import spidev
import RPi.GPIO as GPIO
from lib.Char_Plate.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import smbus

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
lcd = Adafruit_CharLCDPlate()
spi = spidev.SpiDev()
light_adc = 1       # ADC
pot_adc = 0         # ADC
statusLED = 23
button = 25                         # Toggles the display view
display = 0                         # defines what value is displayed
light_Average = []                  # Average list used by the movavg function
l = 0                               # display  value for the light sensor
pot_Average = []                    # Average list used by the movavg function
p = 0                               # display value for the pot
rate = .1                           # The delay between refreshes + .125 seconds
print "Press CTRL+Z to exit"
GPIO.setup(button, GPIO.IN)
GPIO.setup(statusLED, GPIO.OUT)

lcd.backlight(lcd.ON)
lcd.clear()


def analogRead(port):
    """
    Read the given ADC port and preform the necessary shifting of bits
    """
    spi.open(0, 0)
    if (port > 7) or (port < 0):
        print 'analogRead -- Port Error, Must use a port between 0 and 7'
        return -1
    r = spi.xfer2([1, (8 + port) << 4, 0])
    value = ((r[1] & 3) << 8) + r[2]
    spi.close()
    return value


def movavg(ave_list, length, value):
    """
    A function that smooths the results by averaging a list
    """
    ave_list.append(value)
    if length < len(ave_list):
        del ave_list[0]
    value = sum(ave_list)
    return value / len(ave_list)


if __name__ == '__main__':
    while True:
        # Change the Back-light based on what button has been pressed
        if lcd.buttonPressed(lcd.UP):
            lcd.backlight(lcd.BLUE)
        if lcd.buttonPressed(lcd.DOWN):
            lcd.backlight(lcd.ON)
        if lcd.buttonPressed(lcd.SELECT):
            lcd.backlight(lcd.OFF)
        if GPIO.input(button):
            lcd.backlight(lcd.GREEN)

        GPIO.output(statusLED, True)                                # Status Led On
        l = movavg(light_Average, 4, analogRead(light_adc))         # Read the light sensor and calculate the average
        time.sleep(rate)                                            # Wait a little
        GPIO.output(statusLED, False)                               # Status Led Off
        time.sleep(rate)                                            # Wait the pre-set delay
        lcd.home()                                                  # Tell the LCD to go back to the first character
        lcd.message('Pot: ' + str(analogRead(pot_adc)) + '         \nLight: ' + str(l) + '       ')  # Print info
        time.sleep(rate)                                            # Wait a little
