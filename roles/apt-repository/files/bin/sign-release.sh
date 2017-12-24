#!/bin/sh
[ -r "$1" ] || exit
rm -f Release.asc Release.gpg
gpg --sign --detach-sign -o Release.gpg "$1"
gpg --clearsign -o Release.asc "$1"
