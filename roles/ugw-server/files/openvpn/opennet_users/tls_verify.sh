#!/bin/bash
#
# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Server_Installation/Ansible
#
# Speicherung aller verwendeten Zertifikate zur Analyse alter/neuer Zertifikate
#
# NICHT MEHR IN VERWENDUNG

filename=$(echo $2 | awk 'BEGIN{RS="[/\\;.?$]";FS="="} {printf $2"_"} END{print".crt"}')
cp $peer_cert /etc/openvpn/opennet_users/certs/${untrusted_ip}$filename

