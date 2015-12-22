#!/usr/bin/python
# sp.py soundPlayer
# within given time conditions or according to manual mode setting ensure that background sounds are playing

import RPi.GPIO as io
import time
import xmlrpclib
import datetime

# board mode means we refer to pins relative to position in rpi gpio header, not pin on broadcom chip
io.setmode(io.BOARD)

#io.setwarnings(False)

# Raspberry Pi gpio pin assignmets
relayPin = 15

# RPi gpio pin config
io.setup(relayPin, io.OUT, initial=False)

# supervisord set up
server = xmlrpclib.ServerProxy('http://127.0.0.1:9001')
process = 'mpg123'

#######################################################

def start(proc):
   server.supervisor.startProcess(proc)

def relayOn(pin):
   io.output(pin, True)

def stop(proc):
   server.supervisor.stopProcess(proc)

def relayOff(pin):
   io.output(pin, False)

def checkState(proc):
   return server.supervisor.getProcessInfo(proc)['statename']

#######################################################

# times are stated in UTC and are static with no adjustment for savings time
# local + 5 in est and local + 4 in edt

then = datetime.datetime.now()
on = then.replace(hour=15, minute=0, second=0, microsecond=0)
off = then.replace(hour=21, minute=30, second=0, microsecond=0)

#######################################################

while True:
   try:
      file = open('/home/pi/sound_mode.txt', 'r')
      mode = file.read().rstrip()

      if (mode == 'on'):
         #if not running then start sounds
         if (checkState(process) == 'STOPPED'):
            start(process)
         relayOn(relayPin)

      elif (mode == 'off'):
         #if running then stop sounds
         if (checkState(process) == 'RUNNING'):
            stop(process)
         relayOff(relayPin)

      elif (mode != 'auto'):
         #bad file, run away?
         pass

      else:
         # if we got to here mode must be == 'auto'
         # check time conditions and run if within

         now = datetime.datetime.now()

         if (now.time() > on.time()) and (now.time() < off.time()):
            #if not running then start sounds
            if (checkState(process) == 'STOPPED'):
               start(process)
            relayOn(relayPin)

         else:
            #if running then stop sounds
            if (checkState(process) == 'RUNNING'):
               stop(process)
            relayOff(relayPin)

      file.close()
      time.sleep( 1 )

   except KeyboardInterrupt:
       break

io.cleanup()
