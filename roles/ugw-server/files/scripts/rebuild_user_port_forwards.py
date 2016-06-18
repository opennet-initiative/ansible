#!/usr/bin/env python


import os
import subprocess
import sys


from opennet.addresses import NodeInfo, parse_ipv4_and_net


# Die Portweiterleitungen werden in dieser iptables-Chain hinzugefuegt.
DNAT_CHAIN = "user_dnat"

# Zum Auslesen der aktuellen Verbindungen benoetigen wir die Status-Datei.
OPENVPN_STATUS_FILE = "/var/log/openvpn/opennet_users.status.log"


def get_current_user_vpn_connections():
    """ Auslesen der Common Names der verbundenen Clients """
    for index, line in enumerate(open(OPENVPN_STATUS_FILE, "r").readlines()):
        # die ersten drei Zeilen sind der Header
        if index < 3:
            continue
        # wir ignorieren die zweite Haelfte der Status-Datei
        if line.strip() == "ROUTING TABLE":
            break
        node_cn = line.split(",")[0].strip()
        # node_cn sollte eigentlich nie leer sein - aber wir muessen wohl damit
        # rechnen, dass die openvpn-Status-Datei waehrend einer Aktualisierung
        # unvollstaendig/kaputt ist.
        if node_cn and node_cn != "UNDEF":
            yield node_cn


def dump_iptables_rebuild_user_dnat(nodes):
    """ Die Portweiterleitungsregeln anhand der aktiven OpenVPN-Verbindungen neu aufbauen.
        Der komplette Wiederaufbau stellt sicher, dass wir zwischendurch keine Regeln verlieren,
        falls die Firewall auf dem Server reinitialisiert wird.
        Diese Funktion liefert eine Ausgabe im Format von "iptables-save".
        Sie kann via "iptables-restore" angewandt werden.
    """
    # nat-Tabelle auswaehlen
    yield "*nat"
    # Tabelle loeschen
    yield "-F {chain}".format(chain=DNAT_CHAIN)
    # einzeln alle Regeln neu hinzufuegen
    for node in nodes:
        # Port-Weiterleitungen sind nur fuer IPv4-Adressen relevant
        if not node.ipv4_address:
            continue
        for proto in ("tcp", "udp"):
            yield "-A {chain} -p {proto} --dport {port_start}:{port_end} -j DNAT --to-destination {target}"\
                  .format(chain=DNAT_CHAIN, proto=proto, port_start=node.port_first, port_end=node.port_last, target=str(node.ipv4_address))
    yield "COMMIT"
    yield "# Completed on Wed Oct 14 03:15:50 2015"


def rebuild_port_forwards(ipv4_base, ipv6_base):
    port_forwards = os.linesep.join(dump_iptables_rebuild_user_dnat(connected_nodes))
    proc = subprocess.Popen(["/sbin/iptables-restore", "--noflush", "--counters"], stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(port_forwards)
    if (proc.returncode != 0) and stderr:
        sys.write(stderr + os.linesep)
    return proc.returncode


if __name__ == "__main__":
    network_start = sys.argv[1]
    network_netmask = sys.argv[2]
    ipv4_base = parse_ipv4_and_net(network_start, network_netmask)
    ipv6_base = None
    connected_nodes = [NodeInfo(node_cn, ipv4_base, ipv6_base) for node_cn in get_current_user_vpn_connections()]
    returncode = rebuild_port_forwards(ipv4_base, ipv6_base)
    sys.exit(returncode)
