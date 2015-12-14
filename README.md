# Process-Controller
Run an arbitrary process during specified interval or according to hardware override device

This is meant to be run on a raspberry pi to start and stop a media player

###sp.py
uses supervisord interface to control media player process according to defined time conditions.  reads override status from a local text file.

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

##To DO
* add exception handling
 * network down
 * file missing or unexpected content
* write test suite
* revise hardware switch circuit
* handle timezones and dst
* move script control from crontab to supervisord
* rewrite as monolithic process on remote machine controling supervisord via http??
* work better with multiple remotes?
* try with alternate media player?
* add volume control, remote volume control?
* feedback to user at remote
* logging
* external config file read on everyloop
* set all LEDs when setting, maybe on every loop

### nice to have
* generalize time condition mechanism to accomodate arbitrarily complex scedules?
* accomodate an arbitray number of processes with different schedules?
