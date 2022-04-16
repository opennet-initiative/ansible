= Überblick =
Diese Rolle hat hauptsächlich zum Ziel die Opennet Mitgliederverwaltung (MoinMoin Wiki) auf einen neuen Server zu übertragen. Desweiteren sollen angepasste Dateien hier im git zur Nachverfolgung hinterlegt werden.

Beim Anwenden dieser Rolle werden alle grundlegenden Dinge für ein neues MoinMoin installiert und konfiguriert. Am Ende ist es jedoch nötig, die Daten des alten MoinMoin manuell zu kopieren.

Eine Anleitung für das manuelle Kopieren der alten MoinMOin Daten auf den neuen Server ist in *manual-create-backup-and-import-to-new.sh* zu finden

Neben dem Daten-Backup gibt es noch einige Configs und selbst entwickelte Macros, welche hier im git gepflegt werden sollen. Mit dem Script *manual-update-git-files-from-current-installation.sh* werden diese Dateien von der bestehenden Installation heruntergeladen, sodass sie ins git eingecheckt werden können.

= Konfiguration =
Der Zugang zum Wiki wird mittels Client-SSL-Zertifikaten geregelt.
Die zulässigen Zertifikats-CNs werden in "mitgliederverwaltung_allowed_users" für den Host festgelegt.

In der Apache Site Config Datei muss die richtige MoinMoin Version stehen (z.B. /moin_static199/ für Version 1.9.9) . Dies ggf. prüfen.

== TODO ==
- moinmoin version automatisch detektieren im apache2-server Rolle
