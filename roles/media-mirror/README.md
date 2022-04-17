# Media-Mirror
Bereitstellung eines Freifunk Media CDN Servers zur Ablage und Auslieferung von Media Dateien für das media.freifunk.net Projekt. Basiert auf Mirrorbits. Wird mit der Rolle Apache-Server kombiniert.

# Ablauf
1. Media-Server Gruppe und Benutzer anlegen, als System
2. Rsync installieren, konfigurieren und im Daemon-Mode starten
3. Firewall-Regeln: Port 873 (tcp) erlauben

# Betrieb
Siehe https://media.freifunk.net/about.html
