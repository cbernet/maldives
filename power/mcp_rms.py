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
import numpy as np
import pymongo
import pprint

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  spi.max_speed_hz=50000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# setup database access

db = 'sqlite'

if db == 'mongo':
  client = pymongo.MongoClient('localhost',27017)
  mydb = client['power']
  adc = mydb['adc']
elif db == 'sqlite':
  import db_sqlite
  
# Define delay between readings (s)
nsamples = 1000
delay = 1.
data = np.zeros((nsamples,))
while 1:
  for i in range(nsamples):
    data[i] = ReadChannel(0)
    # time.sleep(0.0005)
  mean = data.mean()
  rms = data.std()
  minadc = data.min()
  maxadc = data.max()
  now = time.time()
#   print('read', nsamples, 'samples', mean, rms, minadc, maxadc, time)
  summary = {
    'channel':0,
    'mean':mean,
    'rms':rms,
    'minadc':minadc,
    'maxadc':maxadc,
    'time':now
  }
  pprint.pprint(summary)  
  if db == 'mongo':
    adc.insert(summary)
    time.sleep(delay)
  elif db == 'sqlite':
    db_sqlite.insert(summary)
  
# while True:
#   print(ReadChannel(0))
   
#   # Wait before repeating loop
#   time.sleep(delay)

