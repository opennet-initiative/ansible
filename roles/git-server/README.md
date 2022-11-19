# Überblick
Diese Rolle installiert einen Opennet Git Server.

Enthalten sind:
* Anlegen eines Git Benutzers
* Vorbereitung der Git Verzeichnisse
* Gitolite Installation
* Gitolite Erst-Konfiguration

## Konfiguration

Es werden einige Variablen zur Konfiguration des Git/Gitolite-Servers verwendet.

* gitserver_allowed_users
  * Legt die administrativen Nutzer der Git-Verwaltung (Repo 'gitolite-admin') fest
  * Der erste Nutzer wird der initiale Berechtigte im Git via SSH
* gitserver_git_user
  * Benutzername unter dem der Git-Server laufen wird
  * typischer Weise "git" (Debian Standard derzeit gitolite3)
* gitserver_git_path
  * Heimatverzeichnis des Git-Servers/Git-Benutzers
  * typischer Weise "/home/<gitserver_git_user>" (Debian Standard derzeit /var/lib/gitolite3)
* gitserver_git_mode / gitserver_git_umask
  * Dateirechte für den Git-Server

## Erstinstallation / Migration

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

## Hinweis

Derzeit wird nur der erste Benutzer der 'gitserver_allowed_users' Konfiguration als initialer Bearbeiter des 'gitolite-admin' Repositories gesetzt. Alle weiteren müssen innerhalb des Repos hinzugefügt werden. Dies liegt an den Beschränkungen des 'gitolite setup' Kommandos.
