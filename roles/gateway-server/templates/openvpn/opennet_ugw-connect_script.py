#!/usr/bin/env python3
# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Server_Installation/Ansible
"""
Ermittle anhand des Zertifikats-CN eines OpenVPN-Clients die IP-Adresse, die
der OpenVPN-Server ihm zuweisen soll.
Das Ergebnis wird - entsprechend der OpenVPN-Konvention - in die Datei geschrieben,
deren Name als erster Parameter an das Skript uebergeben wurde.
"""

import sys
import os
from packaging.version import Version


NETMASK = '255.255.0.0'
CLIENT_IP_TEMPLATE = '10.2.{major}.{minor}'
SERVER_VERSION = "{{ openvpn_server_version.stdout }}"


if __name__ == "__main__":
    client_cn = os.getenv('common_name')

    if not client_cn.endswith(".ugw.on"):
        sys.stderr.write("Invalid Client Certificate CN: '%s'%s" % (client_cn, os.linesep))
        sys.exit(1)

    # das ".ugw.on"-Suffix entfernen
    cn_prefix = client_cn[:-len(".ugw.on")]

    # fuehrende "1" hinzufuegen, falls das Zertifikats-CN dem alten Schema folgt ('X.ugw.on' statt 'Y.X.ugw.on')
    if not "." in cn_prefix:
        cn_prefix = "1." + cn_prefix

    # IP-Adresse ermitteln
    client_major, client_minor = [int(value) for value in cn_prefix.split(".")]
    client_ip = CLIENT_IP_TEMPLATE.format(major=client_major, minor=client_minor)

    target_filename = sys.argv[1]
    target_file = open(target_filename, 'w')
    config_items = []
    config_items.append('ifconfig-push {ip} {netmask}'.format(ip=client_ip, netmask=NETMASK))
    target_file.write(os.linesep.join(config_items))
    target_file.close()
