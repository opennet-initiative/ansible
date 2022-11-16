# Überblick
Diese Rolle installiert die Opennet Downloads / Opennet DEV Downloads Umgebung.

Enthalten sind:
* Vorbereitung der Downloads Webdienstes
* Vorbereitung des Buildbot Download Bereiches
* Setzen der Eigner/Gruppen der Verzeichnisse
* Anlage eines Buildbot Export Nutzers (Verwendung für SSH-Rsync Upload)
* Erstellung Cron-Job zur Bereinigung im Buildbot Export Verzeichnis

Voraussetzungen:
* Downloads Paritionen und Verzeichnisse müssen vorab vorhanden sein

## Konfiguration

Es werden einige wenige Variablen für die Verzeichnisstruktur und Cron-Job verwendet.

* downloads_path
  * Pfad zum Verzeichnis für allgemeine (statische) Opennet Downloads
* downloads_user
  * Eigner- und Gruppenname für 'downloads_path', typischer Weise 'www-data'
* downloads_buildbot_path
  * Pfad zum Verzeichnis für das Buildbot Export Nutzerverzeichnis
  * Hier wird ebenfalls das Script zur Bereinigung des Export Verzeichnisses abgelegt
* downloads_buildbot_user
  * Eigner- und Gruppenname für 'downloads_buildbot_path'
  * Hiermit wird gleichzeitig ein System-Nutzer angelegt (SSH/Rsync, Bash)
  * Unter diesem Nutzer wird der Cron-Job für Bereinigung des Export-Verzeichnisses abgelegt
* downloads_buildbot_export
  * Unterverzeichnis von 'downloads_buildbot_path'
  * Genutzt zur Einbettung der (nicht-statischen) Opennet Downloads
  * derzeit Verwendet für die Buildbot Opennet Firmware Testing Ausgaben
* downloads_buildbot_keepbuilds
  * Anzahl der Unterverzeichnisse im Export-Verzeichnisse die bei einer Bereinigung bestehen bleiben

Vorhandenes Downloads Verzeichnis kopieren:
```
<client># ssh -A <new-host>
<new-host># cd /var/www/downloads; rsync -avuz --progress root@<old-host>.on:/var/www/<old-path>/ .
```
