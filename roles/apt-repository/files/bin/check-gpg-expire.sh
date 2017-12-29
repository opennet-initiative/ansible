#!/bin/sh

#
# Opennet Apt Repository GPG Keys Expire Check
# Mathias Mahnke, created 2017/12/27
# Opennet Admin Group <admin@opennet-initiative.de>
#
# based on https://github.com/cz8s/gpg_key_expiration_check
#
# requires:
# * check-gpg-expire.cfg - config file
# * bc - date calculation
# * mutt - send mail (if needed put "set crypt_use_gpgme=no" in ~/.muttrc
#

# stop on error and unset variables
set -eu

# get current script dir
GPG_EXP_HOME="$(dirname $(readlink -f "$0"))"

# config file
GPG_EXP_CFG="$GPG_EXP_HOME/check-gpg-expire.cfg"

# read variables
. "$GPG_EXP_CFG"

# compose and send out a mail with attachment
send_mail() {
  local from="$1"
  local to="$2"
  local subject="$3"
  local message="$4"
  echo -n "Send mail to '$to'... "
  echo "$message" | EMAIL="$from" mutt -s "$subject" -- "$to" && echo "done." || echo "failed."
}

# walk thru all local gpg keys and return a lost of almost expired certs
# input 1 - number of weeks to warning before expiration
# input 2 - gpg command to be used
# input 3 (optional) - key-id to use instead of all keys
# return - list of keys-ids
get_expired_key_list() {
  # get input
  local due_weeks="$1"
  local gpg_command="$2"
  local key_list="$3"
  # init expired
  local exp_list=""
  local exp_key=""
  # prepare key list if not already provided
  [ -z "$3" ] && key_list="$($gpg_command | grep '^pub' | cut -d':' -f 5)"
  # prepare due date for key expiration warning
  local due_date="$(echo "$(date +%s) + $due_weeks*604800" | bc)"
  # walk thru all keys
  for key in $key_list; do
    local expired=0
    # walk thru all sub-keys for each key in list
    for subkey in "$($gpg_command $key | grep -e '^pub' -e '^sub')"; do
      subkey_expire="$(echo $subkey | cut -d':' -f 7)"
      if [ -n "$subkey_expire" ]; then
        # warn if expire is in relevant timeframe (in the future, after due date)
        if [ "$subkey_expire" -gt "$(date +%s)" ] && [ "$subkey_expire" -le "$due_date" ]; then
          expired=1
        fi
      fi
    done
    # compile list if expiring keys
    if [ "$expired" -gt 0 ]; then
      exp_key="$(echo $key | cut -d':' -f 5)"
      exp_list="$exp_list $exp_key"
    fi 
  done
  # return list if expiringkeys
  echo "$exp_list"
}

# create human readable list of keys including key detailes
# input 1 - list of key-ids
# input 2 - heading
# inout 3 - gpg command to be used
# return - list of key-ids and list of key details
get_expired_key_output() {
  # get input
  local exp_list="$1"
  local heading="$2"
  local gpg_command="$3"
  # return key list and details
  if [ -n "$exp_list" ]; then
    echo "$heading $exp_list\n"
    for exp_key in $exp_list; do
      echo "$($gpg_command $exp_key)\n"
    done
  fi
}

# main function, prepare output for actions
# input - key-id (leave empty all keys to be checked)
get_action_output() {
  local list="$(get_expired_key_list "$GPG_WARN_WEEKS" "$GPG_CMD_IN" "$1")"
  local output="$(get_expired_key_output "$list" "$GPG_LIST" "$GPG_CMD_OUT")"
  echo "$output"
}


# retrieve requested action 
ACTION=help
[ $# -gt 0 ] && ACTION="$1" && shift

# so action (all, mail, key) or show usage information
case "$ACTION" in
  all|--all)
    # retrieve optional due weeks if provided
    [ $# -gt 0 ] && GPG_WARN_WEEKS="$1"
    # check key status
    OUT="$(get_action_output "")"
    # provide info via CLI
    [ ! -n "$OUT" ] && OUT="No gpg keys expiring."
    echo "$OUT"
    ;;
  mail|--mail)
    # retrieve optional due weeks if provided
    [ $# -gt 0 ] && GPG_WARN_WEEKS="$1"
    # check key status
    OUT="$(get_action_output "")"
    # provide info via mail
    if [ ! -n "$OUT" ]; then
      echo -n "No gpg keys expiring. No mail sent.\n"
    else
      MAIL="$GPG_MAIL_TEXT\n\n$OUT\n\n$GPG_MAILFOOTER"
      send_mail "$GPG_MAILFROM" "$GPG_MAILTO" "$GPG_MAILSUBJECT" "$MAIL"
    fi 
    ;;
  key|--key)
    if [ $# -gt 0 ]; then
      # retrieve key-id on key action
      KEY="$1" && shift  
      # retrieve optional due weeks if provided
      [ $# -gt 0 ] && GPG_WARN_WEEKS="$1"
      # check key status
      OUT="$(get_action_output "$KEY")"
      [ ! -n "$OUT" ] && OUT="No gpg keys expiring."
      echo "$OUT"
    else
      echo >&2 "Invalid action: Missing parameter KEY-ID for $ACTION."
      "$0" >&2 help
      exit 1
    fi
    ;; 
  help|--help)
    echo "Usage: $(basename "$0")"
    echo "  all|--all [<DUE-WEEKS>]          - check all keys, output list directly"
    echo "  mail|--mail [<DUE-WEEKS>]        - check all keys, send list via mail"
    echo "  key|--key <KEY-ID> [<DUE-WEEKS>] - check only one key, output directly"
    echo "  help|--help                      - show this help"
    ;;
  *)
    echo >&2 "Invalid action: $ACTION"
    "$0" >&2 help
    exit 1
    ;;
  esac

exit 0
