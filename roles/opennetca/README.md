= Überblick =
Diese Rolle installiert die Opennet CA Verwaltung.

Enthalten sind:
* Paketinstallation
* Anlegen der CA und Sub-CA
* Ablegen des Webinterfaces (Public, Internal, CSR)
* Erstellen der Cronjobs

= Konfiguration =

Manuelle Arbeitsschritte:
* für jede CA / Sub-CA muss der Key/Zertifikat erzeugt werden 
* eventuell vorhandene CA Informationen müssen kopiert werden
* bestehende CSR Daten müssen hinzugefügt werden

Backup einer vorhandenen Opennet CA erstellen:
$ cd /home/opennetca; tar --exclude='old' --exclude='opennet*.cfg' --exclude='*.sh' --exclude='.git' -zcf ca_backup_$(date '+%Y%m%d').tar.gz ca

Restore in neuer Opennet CA durchführen:
$ cd /home/opennetca; tar xfz ca_backup_<date>.tar.gz

Backup der CSR Daten erstellen:
$ cd /var/www; tar -zcf csr_backup_$(date '+%Y%m%d').tar.gz opennetca_upload

Restore der CSR Daten durchführen:
$ cd /var/www; tar xfz csr_backup_<date>.tar.gz

= TODO =

* API wird derzeit nicht installiert, da nicht fertig gestellt
