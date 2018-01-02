# {{ ansible_managed }}

DocumentRoot	/var/www/mitgliederverwaltung/

<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>

Alias		/moin_static199/applets/FCKeditor/	/usr/share/fckeditor/
Alias		/moin_static199/			/usr/share/moin/htdocs/
ScriptAlias	/					/usr/share/moin/server/moin.cgi/

<Directory /usr/share>
        AllowOverride None
        Require all granted
</Directory>

# siehe https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=782525
# sonst gibt es Fehler beim Besuchen von Wiki-Seiten mit Umlauten (z.B. AktuelleAenderungen)
SetEnv LANG C.UTF-8

<Location />
	AuthType		basic
	AuthName		"Opennet Mitgliederverwaltung"
	AuthBasicProvider	file
	AuthUserFile		/var/www/mitgliederverwaltung.htpasswd
	Require			valid-user
</Location>

