# Überblick

Diese Rolle verwenden wir für die neuen Gateway-Server seit 2015.

Wähle einen geeigneten Zeitpunkt für die Anwendung dieser Konfiguration aus. Vor allem die Änderung der openvpn-Konfiguration führt zu einer kurzzeitigen Trennung aller Clients.

Ablauf:
1. Netzwerk-Konfiguration
2. DNS-Server (bzw. Zonen-Slave)
3. spezifische Firewall-Details
4. OpenVPN (Konfiguration, Skripte, Zertifikate)
5. OpenVPN-Statusseite (z.B. https://erina.opennet-initiative.de/vpnstatus)
6. opennet-spezifische Munin-Plugins für UGW-Server
7. Dateien für Download-Tests erzeugen

# Konfiguration

Optionaler User6 Layer2 VPN Tunnel:
* gateway_user6_enable - Aktiviere User6 Layer 2 VPN Tunnel Lösung (true/false)
* gateway_dhcp6_pd_subnet - ISC DHCPd Prefix Delegation Subnetz (2a0a:4580:1010:2::)
* gateway_dhcp6_prefix_start - ISC DHCPd Beginn der Präfixe für VPN Clients (2a0a:4580:1010:1000::)
* gateway_dhcp6_prefix_end - ISC DHCPd Ende der Präfixe für VPN Clients (2a0a:4580:1010:1ff0::)
* gateway_dhcp6_prefix_len - ISC DHCPd Gesamte Präfix-Länge (/60)

# Besonderheiten User6 Layer2 IPv6 Tunnel

Benutzern soll per VPN IPv6 Konnektivität zur Verfügung gestellt werden.

Dieser Teil ist im ersten Schritt experimentell. Es wird gewiss noch viele Änderungen am VPN Konzept und vielen anderen Stellen geben, bevor es großflächig ausgerollt werden kann.

Im ersten Schritt wird folgendes implementiert - auf IPv6 UGW Server (derzeit gai, Stand Dez 2019) wird folgendes installiert:
* radvd
* DHCPv6 Server (auch für Prefix Delegation)
* OpenVPN (für Layer2 Tunnel)

# TODO

* Zertifikate erzeugen (Schlüssel und Zertifikat müssen aktuell per Hand erzeugt und auf den Server übertragen werden)
