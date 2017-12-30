#
# Diese Skript erstellt ein Backup der sensiblen Daten von der bestehenden MoinMoin Installation, damit (zusammen mit ansible) eine Kopie aufgesetzt werden kann. 
#

#Hole Archiv von data Verzeichnis und kopiere es nach /tmp/data.tar.bz2
ssh root@yurika.on-i.de tar -cvjf /tmp/data.tar.bz2 -C /var/lib/mitgliederverwaltung/  data/
scp root@yurika.on-i.de:/tmp/data.tar.bz2 files-tmp/
ssh root@yurika.on-i.de rm /tmp/data.tar.bz2
#   ...
#tar -xvjfC /var/lib/mitgliederverwaltung/data /tmp/data.tar.bz2
#   ...
echo "Do not forget to: rm files-tmp/data.tar.bz2 "

#Hole basic auth config (htpasswd) und kopiere nach /tmp
scp root@yurika.on-i.de:/etc/apache2/wiki-mitgliederverwaltung.htpasswd files-tmp/
#...do something
echo "Do not forget to: rm files-tmp/wiki-mitgliederverwaltung.htpasswd"

