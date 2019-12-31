#!/bin/bash

#set IP on interface
ip addr add 2a0a:4580:1010:0002::1/64 dev {{ openvpn_users_l2_v6_interface }}
#set IF up
ip link set dev tap-users-v6 up

#restart services which rely on this interface
systemctl restart openvpn@opennet_user_l2vpn_v6
systemctl restart radvd
