#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#use the common numeration,
#also the one found on the Adafruit Cobbler

led = 21                    # GPIO Port to which the LED is connected
delay = .5
GPIO.setup(led, GPIO.OUT)   # Set 'led' as and Output

while True:
    GPIO.output(led, True)   # led On
    time.sleep(delay)        # wait 'delay' seconds
    GPIO.output(led, False)  # led Off
    time.sleep(delay)        # wait another 'delay' seconds