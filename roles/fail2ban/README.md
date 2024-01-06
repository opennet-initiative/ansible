= Überblick =
Diese Rolle installiert den lokalen fail2ban Dienst auf einem Sever.

Gesetzte Parameter:
* Unterstützung von systemd Logging (Workaround, da Auto-Mode nicht ausreichend)
* Aktivierung von IPv6 (Workaround, vermeiden von Warning)
* Parsen der Webserver Logdateien (da nicht via systemd)

Weiterhin wird eine Bereinigung der älteren fail2ban Datenbank-Dateien regelmäßig vorgenommen.
