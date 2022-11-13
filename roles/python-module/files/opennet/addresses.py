# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Server_Installation/Ansible
"""
Dieses Python-Modul stellt Funktionen zur IP-Ermittlung basierend auf Client-Zertifikaten bereit.
"""

import re
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network, ip_address


# Jedem Client werden zehn Ports zugeteilt.
PORTS_PER_HOST = 10

# Wir benoetigen fuer IPv4 einen /30-Netzbereich pro OpenVPN-Client.
# Siehe "--topology net30" in der OpenVPN-Dokumentation.
IPV4_FACTOR = 4

# bisher ungenutzt - unklar, ob der Wert plausibel ist
IPV6_FACTOR = 65536


# Wir ermitteln den IP-Bereich fuer den Client, sowie den Beginn des Portbereichs fuer
# Weiterleitungen anhand der Zertifikats-CN des Clients. Die IP-Bereiche sind dabei
# jeweils Offsets gegenueber der Basis-IP des VPN-Servers. Die Basis-IP des Servers ist in
# der OpenVPN-Server-Konfiguration als Parameter des connection-Skript-Aufrufs zu finden.
CN_REGEX_TO_IP_PORT_MAPPING = {
    r'^1\.(?P<id>[0-9]{1,3})\.aps\.on$': (IPv4Address("0.0.4.0"), IPv6Address('::1:1:0:0'), 10000),
    r'^(?P<id>[0-9]{1,3})\.mobile\.on$': (IPv4Address("0.0.8.0"), IPv6Address('::2:1:0:0'), 12550),
    r'^2\.(?P<id>[0-9]{1,3})\.aps\.on$': (IPv4Address("0.0.16.0"), IPv6Address('::1:2:0:0'), 15100),
    # Der 3er-Portbereich beginnt bei 20200 weil dies in der Firmware ab v0.5 so verwendet wurde.
    # Somit sind die Ports 17650..20199 noch ungenutzt.
    r'^3\.(?P<id>[0-9]{1,3})\.aps\.on$': (IPv4Address("0.0.20.0"), IPv6Address('::1:3:0:0'), 20200),
}


class NodeInfo(object):

    def __init__(self, client_cn, ipv4_base, ipv6_base):
        # Suche den ersten passenden regulaeren Ausdruck fuer den CN des Client-Zertifikats.
        # Daraus ergibt sich der IP-Offset (relativ zur Basis-IP dieses Servers) und der
        # Bereich der Portweiterleitung.
        for cn_schema in CN_REGEX_TO_IP_PORT_MAPPING:
            match = re.match(cn_schema, client_cn)
            if match:
                (ipv4_offset, ipv6_offset, port_base) = CN_REGEX_TO_IP_PORT_MAPPING[cn_schema]
                cn_address = int(match.groupdict()["id"])
                break
        else:
            raise ValueError('Invalid CN %r.' % client_cn)
        if ipv4_base:
            # wir beginnen mit der zweiten IP des Netzwerks (die erste verwendet der Server)
            self.ipv4_address = ip_address(int(ipv4_base) + int(ipv4_offset) + IPV4_FACTOR * (cn_address - 1) + 2)
        else:
            self.ipv4_address = None
        if ipv6_base:
            self.ipv6_address = ipv6_base + int(ipv6_offset) + IPV6_FACTOR * cn_address
        else:
            self.ipv6_address = None
        self.port_first = port_base + (cn_address - 1) * PORTS_PER_HOST
        self.port_last = self.port_first + PORTS_PER_HOST - 1

    def __str__(self):
        return "NodeInfo(ipv4_address='%s', ipv6_address='%s', port_first=%d, port_last=%d)" % \
                (self.ipv4_address, self.ipv6_address, self.port_first, self.port_last)


def parse_ipv4_and_net(ip, netmask):
    return IPv4Network("%s/%s" % (ip, netmask), strict=False).network_address


def parse_ipv6_and_net(ip):
    return IPv6Network(ip, strict=False).network_address
