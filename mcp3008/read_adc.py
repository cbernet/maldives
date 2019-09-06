#!/usr/bin/python
import spidev
import time
import os
import math
import pprint
import datetime

import influx

# connect to database

influx.dbname = 'power'
influx.measurement = 'adc'
influx.connect_db('influxdb', 8086)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

def read_channel(channel):
  '''Function to read SPI data from MCP3008 chip
  Channel must be an integer 0-7
  '''
  spi.max_speed_hz=50000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


# Define delay between readings (s)
nsamples = 1000
delay = 1.
channel = 0
while 1:
  data = []
  for i in range(nsamples):
    data.append(read_channel(channel))
  # now compute summary information
  agg = 0
  minadc = 1024
  maxadc = -1
  for sample in data:
    agg += sample
    if sample > maxadc:
      maxadc = sample
    elif sample < minadc:
      minadc = sample
  mean = float(agg) / nsamples
  # standard deviation
  agg = 0
  for sample in data:
    agg += (sample - mean)**2
  rms = math.sqrt(agg/nsamples)
  # mean = data.mean()
  # rms = data.std()
  # minadc = data.min()
  # maxadc = data.max()
  now = time.time()
  print(len(data))
  to_write = [
    {
      'measurement' : influx.measurement, 
      'time' : datetime.datetime.now(),
      'tags' : {'channel':channel}, 
      'fields' : {
        'mean':mean,
        'rms':rms,
        'minadc':minadc,
        'maxadc':maxadc,
        'time':now
      }
    }
  ]
  influx.client.write_points(to_write)
  pprint.pprint(to_write[0])  

