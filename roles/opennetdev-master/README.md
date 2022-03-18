# Überblick
Diese Rolle installiert die Opennet DEV Umgebung.

Enthalten sind:
* Anlegen eines Git Benutzers
* Vorbereitung der Gitolite Installation
* Bereitstellung der Git Repositories via HTTPS

## Konfiguration

Manuelle Arbeitsschritte:
* bestehende Git Repositories müssen manuell übertragen werden
* Gitolite Installation muss via dpkg bereit gestellt werden
* anschließend Gitolite Konfiguration (via push) übernehmen
* abschließend "gitolite setup" ausführen
* Übernahme der Datenbank und Anhängen aus vorhandenem Trac

TODO -- Anleitung verbessern....
Vorhandenes Git Verzeichnis kopieren:
<new-host># cd /home/git; rsync -avuz --progress root@<old-host>.on:/var/git/ .

Gitolite Initialisierung:
<new-host># dpkg-reconfigure gitolite3
  System username for gitolite: git
  Repository path: /home/git/repositories
  Admin User: <keys/vornamenachname.pub>

Gitolite Konfiguration übernehmen:
<client># git clone git@<old-host>:gitolite-admin; cd gitolite-admin
<client># git remote rename origin old-host
<client># git remote add origin git@<new-host>:gitolite-admin
<client># git push -f origin master

Gitolote Hooks aktualisieren:
<new-host># su - git
<new-host># gitolite setup

# TODO
