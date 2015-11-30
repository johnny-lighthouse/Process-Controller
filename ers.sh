#!/bin/bash

# Local desired on / off hours:
LON=9
LOFFHOUR=16

#Constants
OFFMIN=30
UTCOFFSET=5

#Adjust for UTC
ON=$((10#$LON + 10#$UTCOFFSET))
OFFH=$((10#$LOFFHOUR + 10#$UTCOFFSET))
 
SERVICE='omxplayer'

while true; do

H="$(date +%H)"
M="$(date +%M)"

if (((10#$H >= 10#$ON)) && ((10#$H < 10#$OFFH))) || (((10#$H == 10#$OFFH)) && ((10#$M < 10#$OFFMIN))) ; then  

     if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
     then
        echo "running" >> /dev/null
     else
        $SERVICE /home/pi/engine_sounds.mp3 &
     fi

     #echo "time condition met. time is $H:$M, On is set to $ON, Off to $OFFH:$OFFMIN"

     sleep 1s

else 
     if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
         then pkill "$SERVICE"

     fi

     #echo "time condition NOT met. time is $H:$M, On is set to $ON, Off to $OFFH:$OFFMIN" 

     sleep 3s

fi

done
