#/bin/bash

#
# Opennet Smokeping Targets Generator
# Mathias Mahnke, created 2022/12/29
# Opennet Admin Group <admin@opennet-initiative.de>
#

# stop on error and unset variables
set -eu

# variables
DEBUG=false
#DEBUG=true
API_URL="{{ smokeping_apiurl }}"
API_ONLINE="accesspoint/?status=online"
API_FLAPPING="accesspoint/?status=flapping"
API_MAXTIME="5"
FILE_PATH="{{ smokeping_path_config }}"
FILE_ONLINE="$FILE_PATH/oni-accesspoints-online"
FILE_FLAPPING="$FILE_PATH/oni-accesspoints-flapping"
JSON_FIELD="opennet_id"
MIN_ONLINE="100"
MIN_FLAPPING="1"

## request list from opennet API
# create ap_list based on opennet_id with line-based format "X.Y.aps.on"
# return an error if API server is not reachable or result is empty
get_ap_list() {
  local url="$API_URL/$1"
  echo "Request list from Opennet API ..."
  echo " * Start API request."
  if ! ap_list="$( curl --no-progress-meter --max-time $API_MAXTIME $url \
    | jq -r '.[].opennet_id | select( . != null ) | select( . != "" ) | . + ".aps.on"' )"; 
  then
    echo >&2 "Error: Failed to parse API result."
    exit 1
  fi
  echo " * Finished API request."
  if [ -z "$ap_list" ]; then
    echo >&2 "Error: Got an empty API result."
    exit 2
  fi
  [ "$DEBUG" = true ] && echo -e " Debug: ap_list = \n$ap_list"
  return 0
}

## check ap list against minimum entry size
# verify the number of entries in the ap_list variable
# return an error if we are not found the minimum entry number
check_ap_list() {
  local num="$1"
  local aps="$ap_list"
  local lines_str=$( echo "$aps" | wc -l )
  local lines=$(( $lines_str ))
  echo "Check result ..."
  if [ "$lines" -lt "$num" ]; then
    echo >&2 "Error: Number of results ($lines) are below minimum ($num)."
    exit 3
  fi
  [ "$DEBUG" = true ] && echo "Debug: lines = $lines, min = $num"
  return 0
}

## generate smokeping targets config
# written to an temp file, will be moved during service reload
# will be included in the main targets configuration
generate_config() {
  local file="$1"
  local aps="$ap_list"
  echo "Generate target config file ..."
  config=$( echo "$aps" | sort -V | while read -r line; do echo "++ ${line//[\.]/-}\nhost = $line"; done )
  [ "$DEBUG" = true ] && echo -e "Debug: config = \n$config"
  echo " * Create $file.tmp"
  echo -e "$config" > "$file.tmp"
  return 0
}

## reload smokeping service to use new target config
# use the temp file and compare it to the current configuration
# if config change is detected use the new file and reload the service
# otherwise cleanup temp file at the end of the operation
reload_service() {
  local file="$1"
  echo "Reload smokeping service ..."
  echo " * Check for systemctl (systemd)"
  if command -v systemctl >/dev/null; then
    [ "$DEBUG" = true ] && echo "Debug: Found systemd systemctl"
  else
    echo >&2 "Error: Missing systemd systemctl"
    rm "$file.tmp"
    exit 4
  fi
  echo " * Compare to $file"
  if [ -f "$file" ] && ( cmp -s "$file" "$file.tmp" ); then
    [ "$DEBUG" = true ] && echo "Debug: No config change detected"
    echo " * Unchanged, remove $file.tmp"
    rm "$file.tmp"
  else
    [ "$DEBUG" = true ] && echo "Debug: Detected config change"
    echo " * Changed, write to $file"
    mv "$file.tmp" "$file"
    echo " * Start service reload."
    systemctl reload smokeping || ( echo >&2 "Error: Reload via systemctl not successfull"; exit 4 )
    [ "$DEBUG" = true ] && ( echo "Debug: service status:"; systemctl status smokeping --no-pager )
    echo " * Finished service reload."
  fi
  return 0
}

# run online aps action
action_online_aps() {
  echo "Action ONLINE"
  get_ap_list "$API_ONLINE"
  check_ap_list "$MIN_ONLINE"
  generate_config "$FILE_ONLINE"
  reload_service "$FILE_ONLINE"
  echo "Action ONLINE done."
}

# run flapping aps action
action_flapping_aps() {
  echo "Action FLAPPING"
  get_ap_list "$API_FLAPPING"
  check_ap_list "$MIN_FLAPPING"
  generate_config "$FILE_FLAPPING"
  reload_service "$FILE_FLAPPING"
  echo "Action FLAPPING done."
}

# retrieve requested action 
ACTION=help
if [ $# -gt 0 ]; then
  ACTION="$1"
fi

# perform action
case "$ACTION" in
  online|--online)
    action_online_aps
    ;;
  flapping|--flapping)
    action_flapping_aps
    ;;
  batch|--batch)
    action_online_aps
    action_flapping_aps
    ;;
  cron|--cron)
    action_online_aps >/dev/null
    action_flapping_aps >/dev/null
    ;;
  help|--help)
    echo "Usage: $(basename "$0")"
    echo "  --online   - generate smokeping target config for online access points"
    echo "  --flapping - generate smokeping target config for flapping access points"
    echo "  --batch    - run online and flapping action as batch, verbose operation"
    echo "  --cron     - run online and flapping action as batch, silent operation"
    ;;
  *)
    echo >&2 "Invalid action: $ACTION"
    "$0" >&2 help
    exit 1
    ;;
  esac

exit 0
