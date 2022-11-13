#!/usr/bin/env python3

import os
import re
import subprocess
import sys


from opennet.addresses import NodeInfo, parse_ipv4_and_net


# Die Portweiterleitungen werden in dieser iptables-Chain hinzugefuegt.
DNAT_CHAIN = "user_dnat"

# Zum Auslesen der aktuellen Verbindungen benoetigen wir die Status-Datei.
OPENVPN_STATUS_FILE = "/var/log/openvpn/opennet_users.status.log"
# Format der CN-Strings (X.YYY.aps.on)
CN_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.aps\.on$")


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
        if node_cn == "UNDEF":
            # Verbindungen im Aufbau (oder Verbindungstests) ignorieren
            continue
        # node_cn sollte eigentlich immer ein gueltiger CN sein - aber wir
        # muessen wohl damit rechnen, dass die openvpn-Status-Datei waehrend
        # einer Aktualisierung unvollstaendig/kaputt ist.
        if CN_REGEX.match(node_cn):
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
            yield ("-A {chain} -p {proto} --dport {port_start}:{port_end} "
                   "-j DNAT --to-destination {target}"
                   .format(chain=DNAT_CHAIN, proto=proto, port_start=node.port_first,
                           port_end=node.port_last, target=str(node.ipv4_address)))
    yield "COMMIT"
    yield "# Completed"


def rebuild_port_forwards(ipv4_base, ipv6_base, nodes):
    port_forwards = os.linesep.join(dump_iptables_rebuild_user_dnat(nodes))
    # Ab Debian 10 wird nftables statt iptables genutzt.
    # Wir nutzen erstmal die alte Syntax (legacy).
    proc = subprocess.Popen(["/usr/sbin/iptables-legacy-restore", "--noflush", "--counters"],
                            stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(port_forwards.encode())
    if (proc.returncode != 0) and stderr:
        print(stderr + os.linesep)
    return proc.returncode


if __name__ == "__main__":
    network_start = sys.argv[1]
    network_netmask = sys.argv[2]
    ipv4_base = parse_ipv4_and_net(network_start, network_netmask)  # bspw: erina -> 10.1.0.0 255.255.0.0
    ipv6_base = None
    try:
        connections = get_current_user_vpn_connections()
    except IOError as exc:
        print("Failed to read the OpenVPN status file ({}): {}".format(OPENVPN_STATUS_FILE, exc),
              file=sys.stderr)
        print("Flushing the port forwarding rules.", file=sys.stderr)
        connections = []
    connected_nodes = [NodeInfo(node_cn, ipv4_base, ipv6_base) for node_cn in connections]
    returncode = rebuild_port_forwards(ipv4_base, ipv6_base, connected_nodes)
    sys.exit(returncode)
