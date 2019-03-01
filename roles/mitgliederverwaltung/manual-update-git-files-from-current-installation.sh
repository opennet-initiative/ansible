#
# Diese Skript holt den aktuellen Stand von Konfigurationsdateien von der bestehenden Mitgliederverwaltung und kopiert dies ins ansible git
#

#Ist DocRoot noch leer?
# Wenn ja, alles okay
# Wenn nein, dann muss das ansible angepasst werden, weil bisher kein Inhalt des Verzeichnisses kopiert wird.
ssh root@yurika.opennet-initiative.de ls -l /var/www/mitgliederverwaltung

#Hole individuelle Opennet Makros und kopiere ins git. So kann es eingecheckt werden, falls etwas neu ist.
scp root@yurika.opennet-initiative.de:/var/lib/mitgliederverwaltung/data/plugin/macro/Opennet*py files/macro/

#Hole apache config und kopieren ins git
scp root@yurika.opennet-initiative.de:/etc/apache2/sites-available/wiki-mitgliederverwaltung.conf templates
sed -ie 's/moin_static[0-9]*/moin_static{{ moinmoin_version }}/' templates/wiki-mitgliederverwaltung.conf

echo "Now you should exec 'git diff' and check the diff."
