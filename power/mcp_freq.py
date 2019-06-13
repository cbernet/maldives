#!/usr/bin/python
#--------------------------------------
# This script reads data from a
# MCP3008 ADC device using the SPI bus.
#
# Analogue joystick version!
#
# Author : Matt Hawkins
# Date   : 17/04/2014
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
 
import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  spi.max_speed_hz=1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define delay between readings (s)
delay = 0.5
sample_period = 10
start = time.time()
n = 0
while 1:
  if time.time()-start>sample_period:
    break
  ReadChannel(0)
  n += 1
freq = float(n) / sample_period / 1000
print(freq, 'kHz')

# while True:
#   print(ReadChannel(0))
   
#   # Wait before repeating loop
#   time.sleep(delay)

