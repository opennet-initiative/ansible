#/bin/bash

#
# Opennet lifxctl Script 
# Mathias Mahnke, created 2022/10/27
# Opennet Admin Group <admin@opennet-initiative.de>
#

# stop on error and unset variables
set -eu

# config file
LIFXCTL_CFG=lifxctl.cfg

# get current script dir
LIFXCTL_HOME="$(dirname $(readlink -f "$0"))"
#LIFXCTL_HOME="$(cd "$(dirname "$0")" && pwd -P)"

# read variables
. "$LIFXCTL_HOME/$LIFXCTL_CFG"

# retrieve requested action 
ACTION=help
if [ $# -gt 0 ]; then
  ACTION="$1"
fi

# perform action
case "$ACTION" in
  on|--on)
    echo "Action ON"
    echo -n "Switching lights on... "
    $LIFXCTL_HOME/lifxctl.py --token "$LIFXCTL_TOKEN" --room "$LIFXCTL_ROOM" --on
    echo "done"
    ;;
  off|--off)
    echo "Action OFF"
    echo -n "Switching lights off... "
    $LIFXCTL_HOME/lifxctl.py --token "$LIFXCTL_TOKEN" --room "$LIFXCTL_ROOM" --off
    echo "done"
    ;;
  help|--help)
    echo "Usage: $(basename "$0")"
    echo "  --on  - run lifxctl programm to switch lights on"
    echo "  --off - run lifxctl programm to switch lights off"
    ;;
  *)
    debug=false
    echo >&2 "Invalid action: $ACTION"
    "$0" >&2 help
    exit 1
    ;;
  esac

exit 0
