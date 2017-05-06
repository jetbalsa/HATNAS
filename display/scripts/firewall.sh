#!/bin/bash
echo Starting up!
modprobe zram
echo $((128*1024*1024)) > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon -p 10 /dev/zram0
swapon -s

#Simple Firewall Script.

#Setting up default kernel tunings here (don't worry too much about these right now, they are acceptable defaults) #DROP ICMP echo-requests sent to broadcast/multi-cast addresses.
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts
#DROP source routed packets
echo 0 > /proc/sys/net/ipv4/conf/all/accept_source_route
#Enable TCP SYN cookies
echo 1 > /proc/sys/net/ipv4/tcp_syncookies
#Do not ACCEPT ICMP redirect
echo 0 > /proc/sys/net/ipv4/conf/all/accept_redirects
#Don't send ICMP redirect 
echo 0 >/proc/sys/net/ipv4/conf/all/send_redirects
#Enable source spoofing protection
echo 1 > /proc/sys/net/ipv4/conf/all/rp_filter
#Log impossible (martian) packets
echo 1 > /proc/sys/net/ipv4/conf/all/log_martians

#Flush all existing chains
iptables --flush

#Allow traffic on loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

#Creating default policies
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

#Allow previously established connections to continue uninterupted
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

#Allow outbound connections on the ports we previously decided.
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT #DNS
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT #HTTP
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT #HTTPS
iptables -A OUTPUT -p UDP --dport 67:68 -j ACCEPT #DHCP
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT #DNS



iptables -A INPUT -p tcp --dport 53 -j ACCEPT #DNS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT #HTTP
iptables -A INPUT -p tcp --dport 443 -j ACCEPT #HTTPS
iptables -A INPUT -p UDP --dport 67:68 -j ACCEPT #DHCP
iptables -A INPUT -p udp --dport 53 -j ACCEPT #DNS

iptables -A OUTPUT -o eth0 -j ACCEPT
iptables -A INPUT -i eth0 -j ACCEPT
iptables -t nat -I PREROUTING --src 0/0 --dst 10.13.37.10
iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to 10.13.37.10:80
iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j DNAT --to 10.13.37.10:443
echo =================================================
echo Restarting Services
service hostapd restart
chmod 777 /dev/ttyUSB0
service gpsd restart
service ntp restart
service dnsmasq restart
service nginx restart
service php7.0-fpm restart
