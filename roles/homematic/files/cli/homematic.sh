#/bin/bash

#
# Opennet Homematic Script 
# Mathias Mahnke, created 2019/03/16
# Opennet Admin Group <admin@opennet-initiative.de>
#

# stop on error and unset variables
set -eu

# config file
HOMEMATIC_CFG=homematic.cfg

# get current script dir
HOMEMATIC_HOME="$(dirname $(readlink -f "$0"))"
#HOMEMATIC_HOME="$(cd "$(dirname "$0")" && pwd -P)"

# read variables
. "$HOMEMATIC_HOME/$HOMEMATIC_CFG"

# homematic variables
HOMEMATIC_URL="http://$HOMEMATIC_HOST/api/homematic.cgi"
HOMEMATIC_LOG="$HOMEMATIC_HOME/homematic.log"
HOMEMATIC_LOGIN="Session.login"
HOMEMATIC_LOGOUT="Session.logout"
HOMEMATIC_PROGLIST="Program.getAll"
HOMEMATIC_PROGRUN="Program.execute"
HOMEMATIC_EVENTON="Event.subscribe"
HOMEMATIC_EVENTOFF="Event.unsubscribe"
HOMEMATIC_EVENTPOLL="Event.poll"

# runtime variables
debug=$HOMEMATIC_DEBUG
session=null
program=null
logout=false
status=false

# json-rpc call and return the json response
send_json_rpc() {
  local method="$1"
  local params="$2"
  response="$(http -I POST $HOMEMATIC_URL method="$method" params:=''"$params"'')"
  echo $response
}

# login and get session, set session-id 
exec_login() {
  echo -n "Login... "
  local param="{\"username\":\"$HOMEMATIC_USER\",\"password\":\"$HOMEMATIC_PASS\"}"
  local response="$(send_json_rpc "$HOMEMATIC_LOGIN" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "  
  if [ "$error" = "null" ]; then
    session="$(echo "$response" | jq -r .result)"
    echo "done (Session ID $session)"
  else
    echo "failed:"
    echo "$error"
    exit 2
  fi
} 

# logout and end session, use session-id
exec_logout() {
  echo -n "Logout... "
  local param="{\"_session_id_\":\"$session\"}"
  local response="$(send_json_rpc "$HOMEMATIC_LOGOUT" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "
  if [ "$error" = "null" ]; then
    logout="$(echo "$response" | jq -r .result)"
    echo "done (Status $logout)"
  else
    echo "failed:"
    echo "$error"
    exit 3
  fi
}

# get program list, find by name param, use session-id, set program-id
exec_findprogram() {
  echo -n "Find program... "
  local name="$1"
  local param="{\"_session_id_\":\"$session\"}"
  local response="$(send_json_rpc "$HOMEMATIC_PROGLIST" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "
  if [ "$error" = "null" ]; then
    program="$(echo "$response" | jq -r '.result[] | select(.name=="'$name'") | .id')"
    echo "done (Program $name ID $program)"
  else
    echo "failed:"
    echo "$error"
    exec_logout
    exit 4
  fi
}

# run program, create log entry, use session-id and program-id
exec_runprogram() {
  echo -n "Run program... "
  local param="{\"_session_id_\":\"$session\", \"id\":\"$program\"}"
  local response="$(send_json_rpc "$HOMEMATIC_PROGRUN" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "
  if [ "$error" = "null" ]; then
    status="$(echo "$response" | jq -r .result)"
    echo "done (Status $status)"
    echo "$(date) : $ACTION done - session $session program $program status $status" >> $HOMEMATIC_LOG 2>&1
  else
    echo "failed:"
    echo "$error"
    error="$(echo $error | jq -c .)"
    echo "$(date) : $ACTION failed - session $session program $program - $error" >> $HOMEMATIC_LOG 2>&1
    exec_logout
    exit 5
  fi
}

# subscribe to event list, use session-id
exec_eventon() {
  echo -n "Event on... "
  local param="{\"_session_id_\":\"$session\"}"
  local response="$(send_json_rpc "$HOMEMATIC_EVENTON" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "
  if [ "$error" = "null" ]; then
    eventon="$(echo "$response" | jq -r .result)"
    echo "done (Status $eventon)"
  else
    echo "failed:"
    echo "$error"
  fi
}

# unsubscribe from event list, use session-id
exec_eventoff() {
  echo -n "Event off... "
  local param="{\"_session_id_\":\"$session\"}"
  local response="$(send_json_rpc "$HOMEMATIC_EVENTOFF" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "
  if [ "$error" = "null" ]; then
    eventoff="$(echo "$response" | jq -r .result)"
    echo "done (Status $eventoff)"
  else
    echo "failed:"
    echo "$error"
  fi
}

# unsubscribe from event list, use session-id
# FIXME: currently the CCU API is not providing any poll results
exec_eventpoll() {
  echo -n "Event poll... "
  local param="{\"_session_id_\":\"$session\"}"
  local response="$(send_json_rpc "$HOMEMATIC_EVENTPOLL" "$param")"
  local error="$(echo $response | jq .error)"
  [ $debug = true ] && echo -n "Response: $response - "
  if [ "$error" = "null" ]; then 
    eventpoll="$(echo "$response" | jq -r '.result[] | .data')"
    echo "done (Message $eventpoll)"
  else
    echo "failed:"
    echo "$error"
  fi
}

# retrieve requested action 
ACTION=help
if [ $# -gt 0 ]; then
  ACTION="$1"
  # show debugging info
  [ $debug = true ] && echo "Debugging = true"
fi

# perform action
case "$ACTION" in
  test|--test)
    echo "Action TEST"
    exec_login
    exec_eventon
    exec_eventpoll
    exec_eventoff
    exec_logout
    ;;
  open|open-door|--open|--open-door)
    echo "Action OPEN DOOR"
    exec_login
    # exec_eventon
    exec_findprogram $HOMEMATIC_PRG_DOOR_OPEN
    exec_runprogram
    # exec_eventpoll
    # exec_eventoff
    exec_logout
    ;;
  close|close-door|--close|--close-door)
    echo "Action CLOSE DOOR"
    exec_login
    # exec_eventon
    exec_findprogram $HOMEMATIC_PRG_DOOR_CLOSE
    exec_runprogram
    # exec_eventpoll
    # exec_eventoff
    exec_logout
    ;;
  eco|eco-temp|--eco|--eco-temp)
    echo "Action ECO TEMP"
    exec_login
    # exec_eventon
    exec_findprogram $HOMEMATIC_PRG_TEMP_ECO
    exec_runprogram
    # exec_eventpoll
    # exec_eventoff
    exec_logout
    ;;
  comfort|comfort-temp|--comfort|--comfort-temp)
    echo "Action COMFORT TEMP"
    exec_login
    # exec_eventon
    exec_findprogram $HOMEMATIC_PRG_TEMP_COMFORT
    exec_runprogram
    # exec_eventpoll
    # exec_eventoff
    exec_logout
    ;;
  power-on|on|--on|--power-on)
    echo "Action POWER ON"
    exec_login
    # exec_eventon
    exec_findprogram $HOMEMATIC_PRG_POWER_ON
    exec_runprogram
    # exec_eventpoll
    # exec_eventoff
    exec_logout
    ;;
  power-off|off|--off|--power-off)
    echo "Action POWER OFF"
    exec_login
    # exec_eventon
    exec_findprogram $HOMEMATIC_PRG_POWER_OFF
    exec_runprogram
    # exec_eventpoll
    # exec_eventoff
    exec_logout
    ;;
  help|--help)
    echo "Usage: $(basename "$0")"
    echo "  --test          - perform connecion test, no action"
    echo "  --open-door     - run homematic program to open doorlock"
    echo "  --close-door    - run homematic program to close doorlock"
    echo "  --eco-temp      - run hometatic program for eco temperature"
    echo "  --comfort-temp  - run homematic program for comfort temperature"
    echo "  --power-on      - run homematic program for power on"
    echo "  --power-off     - run homematic program for power off"
    ;;
  *)
    debug=false
    echo >&2 "Invalid action: $ACTION"
    "$0" >&2 help
    exit 1
    ;;
  esac

exit 0
