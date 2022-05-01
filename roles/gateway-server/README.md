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

# Besonderheiten IPv6 Tunnel

Benutzern soll per VPN IPv6 Konnektivität zur Verfügung gestellt werden.

Dieser Teil ist im ersten Schritt experimentell. Es wird gewiss noch viele Änderungen am VPN Konzept und vielen anderen Stellen geben, bevor es großflächig ausgerollt werden kann.

Im ersten Schritt wird folgendes implementiert - auf IPv6 UGW Server (derzeit gai, Stand Dez 2019) wird folgendes installiert:
* radvd
* DHCPv6 Server (auch für Prefix Delegation)
* OpenVPN (für Layer2 Tunnel)

# TODO

* Zertifikate erzeugen (Schlüssel und Zertifikat müssen aktuell per Hand erzeugt und auf den Server übertragen werden)
