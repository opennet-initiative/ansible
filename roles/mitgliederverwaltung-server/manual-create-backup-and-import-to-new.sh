#
# Diese Skript erstellt ein Backup der sensiblen Daten von der bestehenden MoinMoin Installation, damit (zusammen mit ansible) eine Kopie aufgesetzt werden kann. 
#

echo "Please customize this file before you run it!"
exit

#current server with mitgliederverwaltung installation
SERVER_OLD=amano.opennet-initiative.de
SERVER_NEW=totallynewawsomeserver.opennet-initiative.de

#
# data Verzeichnis
#
#Hole Backup von data Verzeichnis und speicher es lokal nach /tmp/data.tar.bz2
ssh root@$SERVER_OLD tar -cvjf /tmp/data.tar.bz2 -C /var/lib/mitgliederverwaltung/  data/
scp root@$SERVER_OLD:/tmp/data.tar.bz2 $SERVER_NEW:/tmp/
ssh root@$SERVER_OLD rm /tmp/data.tar.bz2

#Entpacke Backup und lösche Datei anschließend 
ssh root@$SERVER_NEW tar -xvjfC /var/lib/mitgliederverwaltung/data /tmp/data.tar.bz2
ssh root@$SERVER_NEW rm /tmp/data.tar.bz2

#
# htpasswd Datei
#
#Kopiere basic auth config (htpasswd) zu neuem Server
scp root@$SERVER_OLD:/var/www/mitgliederverwaltung.htpasswd root@$SERVER_NEW:/var/www/mitgliederverwaltung.htpasswd

