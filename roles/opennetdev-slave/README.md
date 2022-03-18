# Überblick
Diese Rolle installiert die Opennet DEV Slave / Downloads Umgebung.

Enthalten sind:
* Vorbereitung der Downloads Webdienstes

## Konfiguration

Vorhandenes Downloads Verzeichnis kopieren:
<client># ssh -A <new-host>
<new-host># cd /var/www/downloads; rsync -avuz --progress root@<old-host>.on:/var/www/<old-path>/ .
