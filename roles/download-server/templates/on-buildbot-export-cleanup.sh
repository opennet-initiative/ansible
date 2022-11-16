#!/bin/bash

# {{ ansible_managed }}

#
# Opennet buildbot-worker Scripts
# Mathias Mahnke, created 2022/11/16
# Opennet Admin Group <admin@opennet-initiative.de>
#

# stop on error and unset variables
set -eu

# get current script dir
HOME="$(dirname $(readlink -f "$0"))"

# config variables
EXPORT_DIR="{{ downloads_buildbot_export }}"
KEEP_BUILDS="{{ downloads_buildbot_keepbuilds }}"

cd "$HOME/$EXPORT_DIR"

#
# remove old directories
#

# "uniq -u" removed duplicate lines, therefor only old dirs remain
(
  ls -t | head -n "$KEEP_BUILDS"
  ls
) | sort | uniq -u | xargs --delimiter '\n' --no-run-if-empty rm -r

exit 0
