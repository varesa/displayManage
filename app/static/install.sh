#!/bin/env bash

echo "Enter hostname (e.g. rpi01)"
read hostname

apt-get update && apt-get install -y git puppet

echo $hostname > /etc/hostname

cat <<EOF >/etc/dhcp/dhclient.conf
option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;

send host-name = gethostname();
supersede domain-name "fugue.com home.vix.com";
request subnet-mask, broadcast-address, time-offset, routers,
        domain-name-servers, domain-search, interface-mtu,
        rfc3442-classless-static-routes, ntp-servers;
EOF

tmp=$(cat /etc/resolv.conf | grep nameserver)

echo "domain nastori" > /etc/resolv.conf
echo $tmp >> /etc/resolv.conf

/etc/init.d/hostname.sh

echo "213.139.165.194 puppet" >> /etc/hosts

puppet agent -t
