#!/bin/bash

PIDFILE=/var/run/on-routes4pd-wrapper.pid

#
# Make sure that there is only one of this processes running.
# This is needed because when using "on commit" hooks in ISC DHCPd6 then
# this script is started quickly one after another and the python script then 
# is raising errors.
#
# Note: If you rename this file then you need to fix the appamor config of dhcpd.
#

if [ -f "$PIDFILE" ] ; then
  PID=$(cat $PIDFILE)
  RUNCMD=$(ps -q $PID -o comm | grep -v COMMAND)
  if [ -z "$RUNCMD" ] ; then
    #there is a PID file but there is no process running. delete PID file.
    rm $PIDFILE
    echo "Delete $PIDFILE because there is no running process."
  fi
fi

if [ ! -f "$PIDFILE" ] ; then
  /bin/sh -c "sleep 5 && /usr/local/bin/on-routes4pd.py -v 1 -l /var/log/create-routes4pd.log && rm $PIDFILE" &
  PID=$!
  echo $PID > "$PIDFILE"
  echo "wrote: $PID > $PIDFILE"
fi

