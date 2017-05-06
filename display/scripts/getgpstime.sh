GPSDATE=$(gpspipe -w -n 10 | grep TPV | sed -r 's/.*"time":"([^"]*)".*/\1/' | tail -n 1 | sed -e 's/^\(.\{10\}\)T\(.\{8\}\).*/\1 \2/')
echo $GPSDATE
