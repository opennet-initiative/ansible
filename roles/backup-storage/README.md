= Backup-Storage =
Konfiguration von Backup-Servern im Opennet.


= Schlüssel und Zugänge =
* auf dem Backup-Server wird ein SSH-Schlüssel erzeugt (siehe backup_storage_ssh_public_key_path)
* auf allen zu sichernden Hosts wird der ssh-Schlüssel für den root-Login importiert (beschränkt
  auf das rrsync-Kommando)
* die öffentlichen Schlüssel der SSH-Server der zu sichernden Hosts werden auf dem Backup-Server
  in die known_hosts-Datei importiert


= Verschlüsselter Backup-Datenträger =
Die Backup-Daten können auf einem verschlüsselten Datenträger gespeichert werden. Dieser
Datenträger muss natürlich nach jedem Boot-Vorgang manuell geöffnet werden.

Vorbereitungsschritte:
1. Crypto-Blockdevice erzeugen (Datenträger wird gelöscht):
   cryptsetup luksFormat /dev/sdX
   cryptsetup luksOpen /dev/sdX backup-storage
   mkfs.ext4 /dev/mapper/backup-storage
2. Eintrag zur /etc/fstab hinzufügen:
   /dev/mapper/backup-storage /media/backup auto noauto,noatime,nofail
3. Eintrag zur /etc/crypttab hinzufügen:
   backup-storage /dev/sdX none luks,noauto
4. das Unterverzeichnis "rsnapshot" im Crypto-Container anlegen:
   (daran erkennt rsnapshot ob das Crypto-Volume gemountet ist)
   oni-init-crypto start

Erweiterung der Ansible-Konfiguration des Backup-Servers (host_vars/HOSTNAME):
   backup_storage_crypto_device: backup-storage
   backup_storage_crypto_mount_points:
     - /media/backup

Beim ssh-Login (als root) auf dem Backup-Server wird ein Hinweis angezeigt, falls der
verschlüsselte Datenträger nicht gemountet ist.