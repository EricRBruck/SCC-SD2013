#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

import time
import spidev
import RPi.GPIO as GPIO
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
import smbus
import threading


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
segment = SevenSegment(address=0x70)  # which I2C address the display is
spi = spidev.SpiDev()
light_adc = 7       # ADC
pot_adc = 1         # ADC
statusLED = 25
button = 23                         # Toggles the display view
kill = 17                           # Red kill switch
state = 0                           # defines what value is displayed
light_Average = []                  # Average list used by the movavg function
l = 0                               # display  value for the light sensor
pot_Average = []                    # Average list used by the movavg function
p = 0                               # display value for the pot
rate = .175                         # The delay between refreshes + .125 seconds
halt = False                        # When set true, the program stops
print "Press CTRL+Z to exit"
GPIO.setup(button, GPIO.IN)
GPIO.setup(kill, GPIO.IN)
GPIO.setup(statusLED, GPIO.OUT)


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


def refresh(delay):
    """
    This function reads and averages the data form the ADC. In this example we have a light sensor and a potentiometer
    connected, on port 7 and 1.
    """
    global l
    global p
    global halt

    while True:
        GPIO.output(statusLED, True)                                # Status Led On
        l = movavg(light_Average, 4, analogRead(light_adc))         # Read the light sensor and calculate the average
        p = movavg(pot_Average, 3, analogRead(pot_adc))             # Read the pot and calculate the average
        time.sleep(.125)                                            # Wait a little
        GPIO.output(statusLED, False)                               # Status Led Off
        time.sleep(delay)                                           # Wait the pre-set delay


refresher = threading.Thread(target=refresh, args=[rate])           # Create the Refresher thread
refresher.daemon = True

if __name__ == '__main__':
    refresher.start()       # Start the Refresher thread
    while True:
        if GPIO.input(button) == False:     # This button controls what is displayed
            state += 1
            while GPIO.input(button) == False:
                time.sleep(.1)
        if GPIO.input(kill) == False:       # This button kills the app
            segment.writeInt(0)
            GPIO.output(statusLED, False)
            quit()
        if state % 2 == 0:                  # Display the Pot data
            segment.writeInt(p)
            segment.writeDigit(4, p % 10, True)  # Turn on the last decimal to indicate that the Pot is being displayed
        if state % 2 == 1:                  # Display the Light Sensor Data
            segment.writeInt(l)
            segment.writeDigit(4, p % 10, False)

        time.sleep(rate)
