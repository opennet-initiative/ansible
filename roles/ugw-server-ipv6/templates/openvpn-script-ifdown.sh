#!/bin/bash

#stop services which rely on this interface
systemctl stop openvpn@opennet_user_l2vpn_v6
systemctl stop radvd
