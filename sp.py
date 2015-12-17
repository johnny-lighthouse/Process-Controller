#!/usr/bin/python
# sp.py soundPlayer
# within given time conditions or according to manual mode setting ensure that background sounds are playing

import time
import xmlrpclib
import datetime

server = xmlrpclib.ServerProxy('http://127.0.0.1:9001')
process = 'mpg123'

def start(process):
   server.supervisor.startProcess(process)

def stop(process):
   server.supervisor.stopProcess(process)

def checkState(process):
   return server.supervisor.getProcessInfo(process)['statename']

# times are stated in UTC and are static with no adjustment for savings time
# local + 5 in est and local + 4 in edt
then = datetime.datetime.now()
on = then.replace(hour=15, minute=0, second=0, microsecond=0)
off = then.replace(hour=21, minute=30, second=0, microsecond=0)

#######################################################

while True:

   file = open('/home/pi/sound_mode.txt', 'r')
   mode = file.read().rstrip()

   if (mode == 'on'):
      #if not running then start sounds
      if (checkState(process) == 'STOPPED'):
         start(process)

   elif (mode == 'off'):
      #if running then stop sounds
      if (checkState(process) == 'RUNNING'):
         stop(process)

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

      else:
         #if running then stop sounds
         if (checkState(process) == 'RUNNING'):
            stop(process)


   file.close()
   time.sleep( 1 )
