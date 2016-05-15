#!/bin/env bash

echo "Enter hostname (e.g. rpi01)"
read hostname

apt-get update && apt-get install -y git puppet vim

echo $hostname > /etc/hostname

cat <<EOF >/etc/dhcp/dhclient.conf
option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;

send host-name = gethostname();
supersede domain-name "nastori";
request subnet-mask, broadcast-address, time-offset, routers,
        domain-name-servers, domain-search, interface-mtu,
        rfc3442-classless-static-routes, ntp-servers;
EOF

tmp=$(cat /etc/resolv.conf | grep nameserver)

echo "domain nastori" > /etc/resolv.conf
echo $tmp >> /etc/resolv.conf

/etc/init.d/hostname.sh

cat <<EOF > /etc/hosts
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1       $hostname $hostname.nastori
213.139.165.194 puppet
EOF

puppet agent -t
