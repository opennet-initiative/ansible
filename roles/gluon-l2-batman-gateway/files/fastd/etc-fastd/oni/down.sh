#!/bin/sh

#/sbin/ifdown $INTERFACE

/sbin/ip link set dev $INTERFACE down
/usr/local/sbin/batctl -m bat0 if del $INTERFACE


