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

# client certificate authentication
SSLCACertificateFile /etc/apache2/ssl/root.crt
SSLCACertificatePath /etc/apache2/ssl/
SSLCARevocationPath /etc/apache2/ssl/
SSLCADNRequestPath /etc/apache2/ssl/
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
        SSLRequire %{SSL_CLIENT_S_DN_CN} in { \
          "mathiasmahnke.client.on", \
          "larskruse.client.on", \
          "martingarbe.client.on", \
          "janconrads.client.on" \
        }

        # client cert error handling
        RewriteEngine on
        RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
        RewriteRule .? - [F]
        ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
</Location>
