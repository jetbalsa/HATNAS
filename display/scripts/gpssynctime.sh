#!/bin/bash
COLUMNS=16
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
service ntp stop
GPSDATE=`gpspipe -w | head -15 | grep TPV | grep time | sed -r 's/.*"time":"([^"]*)".*/\1/' | head -1`
echo $GPSDATE
date -s "$GPSDATE"
service ntp start
