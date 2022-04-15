= Überblick =

Diese Rolle erstellt einen Buildbot Worker Node. Dieser verbindet sich zu seinem Buildbot Controller (auch bekannt als "Master"). In dieser Rolle werden folgende Aufgaben erledigt:
* Installation der Software
* Anpassung der Dienst-Konfiguration in /etc/default
* Ermittlung des aktuellen Worker Passworts, wird vom Controller abgeholt
* Erstellung einer Buildbot Worker Konfiguration
* Installation notwendiger Software für den Bauvorgang der Opennet Firmware
* Vorbereitung eines Artefakt Upload-Prozesses (SSH Keys etc.) zum Opennet Downloads Server

= Konfiguration =

buildbot_controller_host
 * hier wird der Opennet interne Mesh Hostname hinterlegt
 * zu diesem verbindet sich der erstellte Workernode
 * dort muss die Buildbot Controller Konfiguration vorliegen

buildbot_upload_host
 * hier ist als Standard "downloads.on" hinterlegt
 * die Variable kann bei Bedarf überschrieben werden
 * dies stellt den Artefakt Speicher da (wo der SSH Key Austausch vorbereitet wird)

buildbot_upload_user
 * der lokale Nutzer auf dem Artefakt Speicher

buildbot_upload_dir
 * der Ordner im Home-Verzeichnis des Nutzers, in dem Schreibrechte erforderlich sind
 * hier sollten später die Artefakte abgelegt werden
 * in diesem Ordner wird dann RSYNC mit RW Rechte mittels SSH Key Login ermöglicht

= Betrieb =

* Buildbot Controller: https://dev2.opennet-initiative.de/ (via Reverse Proxy)

= Debugging =

F: Ist der Worker mit dem Controller verbunden?
A: Prüfe unter http://goat.on:8010/#/workers  (wobei goat.on hier der Controller ist)

F: Was kann man prüfen, wenn der Worker sich anscheinend nicht mit dem Controller verbinden?
A: Prüfe auf Worker `systemctl status buildbot-worker@on_worker1`
   Prüfe, ob Prozess läuft `ps -ef | grep buildbot-worker`.
   Prüfe auf Worker Log unter /var/lib/buildbot/workers/on_worker1/twistd.log

