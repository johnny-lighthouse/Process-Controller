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
 * or modify config to add http port and define media and sp.py servies
* ensure mediaplayer installed, have used mpg123 and omxplayer
* install sp.py script
* ensure +x permissions
* touch override file (unless installed via git)
* ensure sp.py started by supervisord
* ensure sshd ecdsa host key turned off in /etc/ssh/sshd_config

####for remote switch:
* install hardware switch
* ensure python-paramiko and supervisor packages installed
* ooa.py must run as root
* ensure no ecdsa keys in /root/.ssh/known_hosts, maybe delete
* as root manually ssh to remote and ensure host key cached
* pull ooa.py script
* ensure +x permissions
* adjust host, user, and password values in ooa.py
* add ooa.py to /etc/supervisor/supervisord.conf
 * [program:ooap.y]
 * command=/home/pi/ooa.py
 * autostart=true
 * autorestart=true

##To DO
* add exception handling
 * network down
 * file missing or unexpected content
* revise hardware switch circuit, @pi & @box
* add volume control, remote volume control?
* logging
* external config file read on everyloop
* write test suite
* handle timezones and dst
* interface with an occupancy indicator, do not run if daylights are not on?

### nice to have
* generalize time condition mechanism to accomodate arbitrarily complex scedules?
* accomodate an arbitray number of processes with different schedules?
* rewrite as monolithic process on remote machine controling supervisord via http??
* * work with multiple remotes?
