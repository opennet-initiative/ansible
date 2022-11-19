# Überblick
Diese Rolle installiert einen Opennet Git Server.

Enthalten sind:
* Anlegen eines Git Benutzers
* Vorbereitung der Git Verzeichnisse
* Gitolite Installation
* Gitolite Erst-Konfiguration

## Konfiguration

Manuelle Arbeitsschritte:
* bestehende Git Repositories müssen übertragen werden
* anschließend Gitolite Konfiguration (via push) übernehmen
* Bei Bedarf abschließend "gitolite setup" ausführen

Vorhandenes Git Verzeichnis kopieren:
<new-host># cd /home/git/repositories; rsync -avuz --progress root@<old-host>.on:/var/git/repositories .

Gitolite Konfiguration übernehmen:
<client># git clone git@<old-host>:gitolite-admin; cd gitolite-admin
<client># git remote rename origin old-host
<client># git remote add origin git@<new-host>:gitolite-admin
<client># git push -f origin master

Ggf. Gitolote Hooks aktualisieren:
<new-host># su - git
<new-host># gitolite setup
