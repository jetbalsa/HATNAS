cat /dev/urandom | tr -dc A-Za-z0-9 | head -c${1:-32} > /tmp/key1
cat /dev/urandom | tr -dc A-Za-z0-9 | head -c${1:-32} > /tmp/key2
modprobe zram
echo $((256*1024*1024)) > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon -p 10 /dev/zram0
swapon -s
logrotate -f /etc/logrotate.conf
/bin/bash /opt/hatnas/net/iptables.sh
timedatectl set-ntp false
if [[ $(curl -s --head https://jrwr.io | grep ^date: | sed 's/date: //g') ]]; then
date -s "$(curl -s --head https://jrwr.io | grep ^date: | sed 's/date: //g')"
date
fi
if [[ $(curl -s --head https://jrwr.io | grep ^Date: | sed 's/Date: //g') ]]; then
date -s "$(curl -s --head https://jrwr.io | grep ^Date: | sed 's/Date: //g')"
date
fi

