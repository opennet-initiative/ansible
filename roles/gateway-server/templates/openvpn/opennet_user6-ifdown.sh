#!/bin/bash

#stop services which rely on this interface
systemctl stop isc-dhcp-server
systemctl stop radvd
