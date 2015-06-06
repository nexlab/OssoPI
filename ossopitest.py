#!/usr/bin/env python
"""
OssoPI test script.
This is a test script to demostrate the use
of the OssoPI board on raspberry pi version 1B+ and 2

It must work out of the box on any recent raspbian install,
it uses python Rpi.GPIO library, installed by default on raspbian.


"""

import sys, time
import RPi.GPIO as GPIO

INPUTS={
         1:12,
         2:16,
         3:18,
         4:22,
         5:11,
         6:13,
         7:15,
         8:29
      }

RELAYS={
         1:32,
         2:36,
         3:38,
         4:40,
         5:31,
         6:33,
         7:35,
         8:37
      }

GPIO.setmode(GPIO.BOARD)

def printhelp():
   print "Usage:", sys.argv[0], "<input|relay>"
   print
   print "Example:"
   print
   print sys.argv[0], "input 3"
   print
   print sys.argv[0], "relay 2"
   print
def initialize():
   for i in INPUTS.values():
      GPIO.setup(i, GPIO.IN)
      #print i, GPIO.gpio_function(i)
      #time.sleep(1)
   for i in RELAYS.values():
      GPIO.setup(i, GPIO.OUT)
      GPIO.output(i,  GPIO.LOW)
      #print i, GPIO.gpio_function(i)
      #time.sleep(1)

def relay(rel):
   GPIO.output(RELAYS[rel], GPIO.HIGH)
   print 'RELAY', rel, 'IS NOW ON (ctrl+C to exit, on exit any relay will be switched off)'
   while 1: time.sleep(1)

def digitalinp(inp):
   print 'INPUT', inp, 'IS', 'open' if GPIO.input(INPUTS[inp]) else 'close'
   print
   print 'Waiting for a state change... (or ctrl+C to exit)'
   GPIO.wait_for_edge(INPUTS[inp], GPIO.BOTH)
   time.sleep(.01) # Adafruit library needs a little time to detect right status
   print 'INPUT', inp, 'IS NOW', 'open' if GPIO.input(INPUTS[inp]) else 'close'

def custom_excepthook(type, value, traceback):
   if type is KeyboardInterrupt:
      print 'Exit.'
      GPIO.cleanup()
      return # do nothing
   else:
      sys.__excepthook__(type, value, traceback)

if __name__=='__main__':
   print GPIO.RPI_INFO
   try:
      if (len(sys.argv)>=3
         and sys.argv[1]=='relay'
         and int(sys.argv[2]) in range(1, 9)):
         initialize()
         relay(int(sys.argv[2]))
         sys.exit(0)
      elif (len(sys.argv)>=3
         and sys.argv[1]=='input'
         and int(sys.argv[2]) in range(1, 9)):
         initialize()
         digitalinp(int(sys.argv[2]))
         sys.exit(0)
   except KeyboardInterrupt:
      GPIO.cleanup()
      sys.exit(0)
   printhelp()
   sys.exit(1)

