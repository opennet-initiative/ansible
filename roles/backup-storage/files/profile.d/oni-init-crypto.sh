# dem root-Nutzer Hinweis fuer crypto-Partition anzeigen, falls sie noch nicht offen ist
if [ "$(id -u)" = "0" ] && ! oni-init-crypto status; then
	echo
	echo '    ****************************************************'
	echo '    * die Crypto-Partition muss noch geoeffnet werden: *'
	echo '    *              oni-init-crypto start               *'
	echo '    ****************************************************'
	echo
fi
