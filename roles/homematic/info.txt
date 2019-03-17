= Überblick =
Diese Rolle installiert die Opennet Homematic Software.

Enthalten sind:
* Installation von jq und httpie
* Anlegen eines Systembenutzers
* Anlegen der Verzeichnisse
* Kopieren der Scripte

= Konfiguration =

* in der homematic.cfg Daten muss der korrekte CCU Benutzer und Passwort manuell auf dem jeweiligen Host eingetragen werden; die Datei wird ohne Passwort einmalig bereit gestellt
* über eine Apache2-Server Rolle wird der passender Webserver aufgesetzt

= TODO =

* Cronjob zum automatischen Schließen der Tür jeden Abend?
