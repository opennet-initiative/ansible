# Überblick
Diese Rolle installiert und konfiguriert den OLSR2 Deamon.

Mehr zum OLSR2 Debian Paket unter:
https://wiki.opennet-initiative.de/wiki/Server_Installation#OLSRd_v2

# Ablauf

1. Netzwerkschnittstellen konfigurieren
2. OLSR2 Software installieren (via DEB)
3. Policy-Routing konfigurieren (Routing-Tabelle anlegen, zusätzliche Routing-Regeln beim Booten erzeugen)
4. ferm/firewall-Regeln: Markierung von eingehenden Paketen aus nicht-olsr-Schnittstellen (für die obigen Regeln)

# Besonderheiten

Diese Rolle bereitet den Import der DNS Anycast ULA IPv6 vor.

# TODO
* Munin
