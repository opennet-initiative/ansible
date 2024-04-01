#!/bin/bash

#set IP on interface
ip addr add 2a0a:4580:1010:0002::1/64 dev {{ openvpn_user6_interface }}
#activate interface
ip link set dev {{ openvpn_user6_interface }} up
#add routing for dhcpv6-pd range
ip route add 2a0a:4580:1010:1000::/52 dev {{ openvpn_user6_interface }}

#restart services which rely on this interface
systemctl restart isc-dhcp-server
systemctl restart radvd
