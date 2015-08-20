#!/bin/bash

cat >/etc/sysconfig/network-scripts/ifcfg-eth0 <<EOL
DEVICE=eth0
BOOTPROTO=static
HWADDR=$1
IPADDR=$2
NETMASK=255.255.255.0
GATEWAY=192.168.2.1
DNS1=208.67.222.222
DNS2=208.67.220.220
ONBOOT=yes
EOL

