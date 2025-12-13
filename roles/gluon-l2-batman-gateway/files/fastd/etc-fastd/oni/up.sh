#!/bin/sh

#ip link set up dev $INTERFACE
#/sbin/ifup $INTERFACE

/usr/local/sbin/batctl -m bat0 if add $INTERFACE
/sbin/ip link set dev $INTERFACE up
