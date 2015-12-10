# background-sound-timer
play a sound file continuously during specified interval, subject to override

This is meant to be run on a raspberry pi to start and stop background sounds.

###sp.py
uses supervisord interface to control media player according to defined time conditions.  reads override status from a local text file.

###ooa.py
reads hardware override switch from RPi gpio pins and controls feedback LED's through same.  On switch change only, uses python-paramiko library to write override status file via ssh.

###supervisord.conf
defines html interface and media player run conditons.

###sound_mode.txt
holds override status from remote, values are: on, off, auto

##Deployment notes:

* ensure supervisor package installed
* copy .config to /etc/supervisor/supervisord.config
 * or modify config to add http port and define service
* ensure mediaplayer installed, have used mpg123 and omxplayer
* install sp.py script
* ensure +x permissions
* touch override file (unless installed via git)
* add crontab line @reboot /home/pi/sp.py &
* ensure sshd ecdsa host key turned off in /etc/ssh/sshd_config

####for remote switch:
* install hardware switch
* ensure python-paramiko package installed
* ooa.py must run as root
* ensure no ecdsa keys in /root/.ssh/known_hosts, maybe delete
* as root manually ssh to remote and ensure host key cached
* pull ooa.py script
* ensure +x permissions
* adjust host, user, and password values in ooa.py
* as root add crontab line @reboot /home/pi/ooa.py &  or appropriate
