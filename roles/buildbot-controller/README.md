# Überblick

Diese Rolle betreibt den Buildbot Controller Dienst (auch bekannt als "Master"). Zu diesem können sich
dann die Buildbot Worker Nodes verbinden. Folgende Aufgaben werden abgearbeitet:
* Installation der Software (Buildbot Debian, Webinterface via pip)
* Anpassung der Dienst-Konfiguration in /etc/default
* Erstellung einer Buildbot Controller Konfiguration
* Erzeugung des Buildbot Worker Passwortes
* Anpassung der Firewall-Konfiguration für die Webschnittstelle
* Anlage eines Cron-Jobs für die pip-Aktualisierungsüberwachung

# Konfiguration

buildbot_worker_name
 * hier wird der Servername des beteiligten Worker Nodes hinterlegt

# Betrieb

Buildbot Controller: https://dev.opennet-initiative.de/ (via Reverse Proxy)

# Debugging

F: Ist der Controller erfolgreich gestartet?
A: Prüfe erreichbarkeit von http://goat.on:8010/#/workers
   Prüfe `systemctl status buildbot@opennet.service`
   Prüfe, ob Prozess läuft `ps -ef | grep buildbot`.
   Prüfe Log unter /var/lib/buildbot/controllers/opennet/twistd.log

# Wartung

Aktuelle Versionen prüfen:
```
# pip3 list | grep buildbot
buildbot                2.10.1.post1
buildbot-console-view   3.5.0
buildbot-grid-view      3.5.0
buildbot-waterfall-view 3.5.0
buildbot-www            3.5.0
```

Aktualisierungsprüfung:
```
# pip3 list --outdated | grep buildbot
buildbot         2.10.1.post1 3.5.0   wheel
```

Aktualisierung durchführen:
```
# pip3 install --upgrade <package> (--break-system-packages)
```

Eine regelmäßige Prüfroutine via cron ist in dieser Rolle umgesetzt.
