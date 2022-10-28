= Überblick =
Diese Rolle installiert die Opennet Homematic Software.
Zusätzlich wird die LIFX Lichtsteuerung hinzugefügt.

Enthalten sind:
* Installation von jq und httpie
* Anlegen eines Systembenutzers
* Anlegen der Verzeichnisse
* Kopieren der Scripte
* Installation lifxctl (https://github.com/JackSteele/lifxctl)

= Konfiguration =

* in der homematic.cfg Daten muss der korrekte CCU Benutzer und Passwort manuell auf dem jeweiligen Host eingetragen werden; die Datei wird ohne Passwort einmalig bereit gestellt
* in der token.txt Datei muss ein gültiger LIFX HTTP API Token eingetragen werden (https://api.lifx.com/)
* über eine Apache2-Server Rolle wird der passender Webserver aufgesetzt

= TODO =
