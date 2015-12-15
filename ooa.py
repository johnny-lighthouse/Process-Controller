#!/usr/bin/python
# 'On Off Auto' script checks switch state and controls outputs appropriatly
# outputs are 2 LED's and a remote file
# 

import RPi.GPIO as io
import time
import paramiko
import xmlrpclib

#supervisord interface set up
server = xmlrpclib.ServerProxy('http://:9001')
process = 'mpg123'

def checkState(process):
   return server.supervisor.getProcessInfo(process)['statename']

# board mode means we refer to pins relative to position in rpi gpio header, not pin on broadcom chip
io.setmode(io.BOARD)

#io.setwarnings(False)

# Raspberry Pi gpio pin assignmets
onLed = 11
offLed = 15
onSwitch = 7
offSwitch = 13

# NB switch logic is reversed
# gpio pins are normally on when switch NOT selected
# pin state false means that that switch position has been selected

# sleep until network is up after reboot
time.sleep( 30 )

# RPi gpio pin config
io.setup(onLed, io.OUT, initial=True)
io.setup(offLed, io.OUT, initial=True)
io.setup(onSwitch, io.IN)
io.setup(offSwitch, io.IN)

#paramiko ssh config
host = ''
port = 22
username = ''
password = ''
s = paramiko.SSHClient()
s.load_system_host_keys('/root/.ssh/known_hosts')

state = 'auto' 
last = ''

while True:
    try:
        # determine switch state
        if (io.input(onSwitch) == False):
            state = 'on'

        elif (io.input(offSwitch) == False):
            state = 'off'

        else:
            # if neither switch is off then toggle is in center auto position
            # leave both LED's on
            state = 'auto'

        # if switch state has changed, write to remote unit
        if (state != last):
            # paramiko.util.log_to_file('/root/p.log')
            s.connect(host, port, username, password)
            stdin, stdout, stderr = s.exec_command("echo '" + state + "' > /home/pi/sound_mode.txt")
            s.close()

            last = state

        # check remote state and set LED's
        if (checkState(process) == 'STOPPED') and (state == 'off'):
            io.output(onLed, False)
            io.output(offLed, True)

        elif (checkState(process) == 'RUNNING') and (state == 'on'):
            io.output(onLed, True)
            io.output(offLed, False)
 
        elif (checkState(process) == 'RUNNING') and (state == 'auto'):
            io.output(onLed, True)
            io.output(offLed, True)

        else:
            #something is wrong
            io.output(onLed, False)
            io.output(offLed, False)

        time.sleep( 0.1 )

    except KeyboardInterrupt:
        break

io.cleanup()

