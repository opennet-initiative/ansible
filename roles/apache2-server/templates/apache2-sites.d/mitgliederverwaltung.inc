# {{ ansible_managed }}

DocumentRoot	/var/www/mitgliederverwaltung/

<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>

Alias		/opennetlogo.png		/var/www/mitgliederverwaltung/opennetlogo.png
Alias		/favicon.ico		/var/www/mitgliederverwaltung/favicon.ico
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

# client certificate authentication
SSLCACertificateFile {{ apache2_opennetca_dir }}/opennet-root.crt
SSLCACertificatePath {{ apache2_opennetca_dir }}/
SSLCARevocationPath {{ apache2_opennetca_dir }}/
SSLCADNRequestPath {{ apache2_opennetca_dir }}/
SSLCARevocationCheck chain


<Location />
        Options Indexes FollowSymLinks MultiViews
        Require all granted

        # client cert auth
        SSLVerifyClient optional
        SSLVerifyDepth 3
        # allow access to certificate details for Moin's authorization
        SSLOptions +StdEnvVars
        # allow specific cert CN
        SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ mitgliederverwaltung_allowed_users|join('", "') }}" }

        # client cert error handling
        RewriteEngine on
        RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
        RewriteRule .? - [F]
        ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
</Location>
