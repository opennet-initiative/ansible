# Überblick
Diese Rolle installiert die Opennet Downloads / Opennet DEV Downloads Umgebung.

Enthalten sind:
* Vorbereitung der Downloads Webdienstes
* Syncronisation der Downloads Dateien
* Vorbereitung des Buildbot Download Bereiches

## Konfiguration

Voraussetzungen:
* Downloads Paritionen und Verzeichnisse müssen vorab vorhanden sein

Vorhandenes Downloads Verzeichnis kopieren:
<client># ssh -A <new-host>
<new-host># cd /var/www/downloads; rsync -avuz --progress root@<old-host>.on:/var/www/<old-path>/ .
