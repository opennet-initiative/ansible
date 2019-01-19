#!/usr/bin/python
# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Server_Installation/Ansible
"""
Dieses Skript wird beim Aufbau und bei der Trennung einer Nutzer-Tunnel-OpenVPN-Verbindung ausgefuehrt.
Es ermittelt die zu vergebende IP des OpenVPN-Clients anhand des CN seines Zertifikats.
"""

import sys
import os
from opennet.addresses import NodeInfo, parse_ipv4_and_net, parse_ipv6_and_net

SERVER_VERSION = "{{ openvpn_server_version.stdout }}".split(".")[:2]


# optionale Log-Ausgabe fuer Debugging
# Dies funktioniert nur bei direkter Ausfuehrung ("openvpn CONFIG_FILE"), da die systemd-Unit ein
# privates /tmp erzeugt.
#sys.stderr = file("/tmp/vpn-connect.log", "w")


# siehe Code-Kopie in roles/ugw-server/templates/openvpn/opennet_users/connect_script.py
def get_compression_config_lines():
    # parse die ersten beiden Versions-Zahlen
    client_version = os.getenv("IV_VER").split(".")[:2]
    # ermittle die passende Kombination von Server- und Client-Kompression
    if SERVER_VERSION < (2, 4):
        # older server version supporting only lzo
        if client_version < (2, 4):
            compression = ("comp-lzo", "comp-lzo")
        else:
            compression = ("comp-lzo", "compress lzo")
    else:
        # modern server version supporting all compression algorithms
        if os.getenv("IV_LZ4v2") == "1":
            compression = ("compress lz4-v2", "compress lz4-v2")
        elif os.getenv("IV_LZ4") == "1":
            compression = ("compress lz4", "compress lz4")
        elif client_version < (2, 4):
            compression = ("compress lzo", "comp-lzo")
        else:
            compression = ("compress lzo", "compress lzo")
    yield compression[0]
    yield 'push "{}"'.format(compression[1])


def process_openvpn_connection_event(client_cn):
    ipv4_base = None
    ipv6_base = None
    if os.getenv("ifconfig_local"):
        ipv4_base = parse_ipv4_and_net(os.getenv("route_network_1"), os.getenv("route_netmask_1"))
    if os.getenv("ifconfig_ipv6_local"):
        ipv6_base = parse_ipv6_and_net(os.getenv("route_ipv6_network_1"))

    node = NodeInfo(client_cn, ipv4_base, ipv6_base)

    if os.getenv("bytes_received") is None:
        # wir wurden als "client-connect"-Skript aufgerufen
        # push config to ovpn client
        target_filename = sys.argv[1]
        with file(target_filename, 'w') as target_file:
            config_items = []
            if node.ipv4_address:
                config_items.append('ifconfig-push {} {}'
                                    .format(node.ipv4_address, node.ipv4_address - 1))
            #if node.ipv6_address:
                #config_items.append('ifconfig-ipv6-push {}'.format(node.ipv6_address))
                # TODO: dies sind alte erina-Adressen?
                #if client_cn == '10.mobile.on':
                #    target_file.write('iroute-ipv6 2a01:a700:4629:fe01::/64')
                #if client_cn == '195.aps.on':
                #    target_file.write('iroute-ipv6 2a01:a700:4629:fe02::/64')
                #if client_cn == '2.50.aps.on':
                #    target_file.write('iroute-ipv6 2a01:a700:4629:fe03::/64')
            config_items.extend(get_compression_config_lines())
            target_file.write(os.linesep.join(config_items))
    else:
        # wir wurden als "client-disconnect"-Skript aufgerufen
        pass


if __name__ == "__main__":
    client_cn = os.getenv('common_name')
    if client_cn:
        # Das Skript wurde aufgrund des Verbindungsaufbaus oder der Trennung eines
        # OpenVPN-Clients gestartet.
        process_openvpn_connection_event(client_cn)
    else:
        sys.stderr.write("Unknown certificate CN" + os.linesep)
        sys.exit(1)
