#!/bin/bash
filename=$(echo $2 | awk 'BEGIN{RS="[/\\;.?$]";FS="="} {printf $2"_"} END{print".crt"}')
cp $peer_cert /etc/openvpn/opennet_users/certs/${untrusted_ip}$filename

