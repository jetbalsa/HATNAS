echo 1 > /proc/sys/net/ipv4/ip_forward
echo 1 > /proc/sys/net/ipv4/tcp_syncookies

echo 1 > /proc/sys/net/ipv6/conf/default/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/enp0s3/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/lo/disable_ipv6

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -m comment --comment "Allow loopback connections" -j ACCEPT
iptables -A INPUT -p icmp -m comment --comment "Allow Ping to work as expected" -j ACCEPT
iptables -A INPUT -p tcp -m multiport --destination-ports 22,53,67,68,80,443 -j ACCEPT
iptables -A INPUT -p udp -m multiport --destination-ports 53,67,68 -j ACCEPT

iptables -t nat -A PREROUTING -i enp0s3 -p udp --dport 53 -j DNAT --to 10.13.37.10
iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 53 -j DNAT --to 10.13.37.10
iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 80 -j DNAT --to 10.13.37.10
iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 443 -j DNAT --to 10.13.37.10

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -A INPUT -j REJECT
iptables -A FORWARD -j REJECT

service dnsmasq restart
service ssh restart
