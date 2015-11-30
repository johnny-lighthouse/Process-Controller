#!/bin/bash

# Local desired on / off hours:
LON=9
LOFFHOUR=16

#Constants
OFFMIN=30
UTCOFFSET=5

#Adjust for UTC
ON=$(($LON + $UTCOFFSET))
OFFH=$(($LOFFHOUR + $UTCOFFSET))
 
SERVICE='omxplayer'

while true; do

H="$(date +%H)"
M="$(date +%M)"

if ((($H >= $ON)) && (($H < $OFFH))) || ((($H == $OFFH)) && (($M < $OFFMIN))) ; then  

     if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
     then
        echo "running" >> /dev/null
     else
        omxplayer /home/pi/engine_sounds.wav &
     fi

     #echo "time condition met. time is $H:$M, On is set to $ON, Off to $OFFH:$OFFMIN"

     sleep 3s

else 
     if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
         then pkill "$SERVICE"

     fi

     #echo "time condition NOT met. time is $H:$M, On is set to $ON, Off to $OFFH:$OFFMIN" 

     sleep 3s

fi

done
