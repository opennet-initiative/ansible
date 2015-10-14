#!/usr/bin/python
# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Server_Installation/Ansible
"""
Dieses Skript wird beim Aufbau und bei der Trennung einer Nutzer-Tunnel-OpenVPN-Verbindung ausgefuehrt.
Es ermittelt die zu vergebende IP des OpenVPN-Clients anhand des CN seines Zertifikats und berechnet ausserdem
die Portbereich, der dem Client fuer die Portweiterleitung zugeordnet ist.

Ausserdem wird dieses Skript als Start-Hook von ferm mit dem Argument "rebuild_port_forward" aufgerufen,
um die Portweiterleitungsregeln nach einem Flush der Firewall-Regeln anhand der openvpn-Status-Datei
neu zu erstellen.
"""

import sys
import os
from connectcalc import NodeInfo, parse_ipv4_and_net, parse_ipv6_and_net, rebuild_port_forwards, add_port_forward, del_port_forward


# Debugging?
#sys.stderr = file("/tmp/vpn-connect.log", "w")


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
        add_port_forward(node)
        # push config to ovpn client
        target_filename = sys.argv[1]
        with file(target_filename, 'w') as target_file:
            if node.ipv4_address:
                target_file.write('ifconfig-push %s %s\n' % (node.ipv4_address, node.ipv4_address-1))
            if node.ipv6_address:
                target_file.write('ifconfig-ipv6-push %s\n' % str(node.ipv6_address))
                # TODO: dies sind alte erina-Adressen?
                if client_cn == '10.mobile.on':
                    target_file.write('iroute-ipv6 2a01:a700:4629:fe01::/64')
                if client_cn == '195.aps.on':
                    target_file.write('iroute-ipv6 2a01:a700:4629:fe02::/64')
                if client_cn == '2.50.aps.on':
                    target_file.write('iroute-ipv6 2a01:a700:4629:fe03::/64')
    else:
        # wir wurden als "client-disconnect"-Skript aufgerufen
        del_port_forward(node)


if __name__ == "__main__":
    client_cn = os.getenv('common_name')
    if client_cn:
        # Das Skript wurde aufgrund des Verbindungsaufbaus oder der Trennung eines
        # OpenVPN-Clients gestartet.
        process_openvpn_connection_event(client_cn)
    else:
        # Das Skript wurde nicht vom OpenVPN-Server gestartet.
        action = sys.argv[1]
        if action == "rebuild_port_forward":
            # Diese Aktion wird beim Neustart von ferm (Firewall-Builder) als Hook ausgeloest.
            network_start = sys.argv[2]
            network_netmask = sys.argv[3]
            ipv4_base = parse_ipv4_and_net(network_start, network_netmask)
            ipv6_base = None
            rebuild_port_forwards(ipv4_base, ipv6_base)
        else:
            sys.stderr.write("Unknown action: %s\n" % str(action))
