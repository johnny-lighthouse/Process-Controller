#!/usr/bin/python
# 'On Off Auto' script checks switch state and controls outputs appropriatly
# outputs are 2 LED's and a remote file
# 

import RPi.GPIO as io
import time
import paramiko


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

time.sleep( 30 )

# RPi gpio pin config
io.setup(onLed, io.OUT, initial=True)
io.setup(offLed, io.OUT, initial=True)
io.setup(onSwitch, io.IN)
io.setup(offSwitch, io.IN)

#paramiko ssh config
host = 'rpi06'
port = 22
username = 'pi'
password = 'raspberry'
s = paramiko.SSHClient()
s.load_system_host_keys('/root/.ssh/known_hosts')

state = 'auto' 
last = ''

while True:
    try:
        if (io.input(onSwitch) == False):
            state = 'on'
            io.output(offLed, False)

        elif (io.input(offSwitch) == False):
            state = 'off'
            io.output(onLed, False)

        else:
            # if neither switch is off then toggle is in center auto position
            # leave both LED's on
            state = 'auto'
            io.output(onLed, True)
            io.output(offLed, True)

        if (state != last):
            # paramiko.util.log_to_file('/root/p.log')
            s.connect(host, port, username, password)
            stdin, stdout, stderr = s.exec_command("echo '" + state + "' > /home/pi/sound_mode.txt")
            s.close()

            last = state

        time.sleep( 0.1 )

    except KeyboardInterrupt:
        break

io.cleanup()

