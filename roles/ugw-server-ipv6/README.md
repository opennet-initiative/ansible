Benutzern soll per VPN IPv6 Konnektivität zur Verfügung gestellt werden.

Diese Rolle ist im ersten Schritt experimentell. Es wird gewiss noch viele Änderungen am VPN Konzept und vielen anderen Stellen geben, bevor es großflächig ausgerollt werden kann.

Im ersten Schritt wird folgendes implementiert:
- auf IPv6 UGW Server (derzeit gai, Stand Dez 2019) wird folgendes installiert
-- radvd
-- DHCPv6 Server (auch für Prefix Delegation)
-- OpenVPN (für Layer2 Tunnel)
