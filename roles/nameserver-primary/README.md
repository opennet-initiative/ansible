= Überblick =
Diese Rolle installiert die Opennet Nameserver Master Rolle.

Enthalten sind:
* Paketinstallation
* Grundkonfiguration von BIND
* Cron-Job für automatische Erstellung Mesh IPv6 Zone
* Erweiterung des Munin Monitoring

= Konfiguration =

Manuelle Arbeitsschritte:
* BIND Opennet DNS Key auf Server erstellen (notwendig für Slaves)
* BIND Opennet DNS Zonen auf Server ablegen - /etc/bind/zones

= TODO =
* BIND Statistiken verschieben? /var/run/named/stats
* DNS over TLS hinzufügen: https://kb.isc.org/docs/aa-01386
