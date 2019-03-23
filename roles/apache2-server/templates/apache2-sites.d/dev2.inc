# {{ ansible_managed }}

WSGIScriptAlias / /var/www/trac/cgi-bin/trac.wsgi
Alias /chrome/ /var/www/trac/htdocs/
Alias /robots.txt /var/www/trac/htdocs/site/robots.txt
Alias /favicon.ico /var/www/trac/htdocs/site/favicon.ico
<Directory /var/www/trac/trac.wsgi>
        WSGIProcessGroup trac
	      WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
</Directory>

# client certificate authentication
SSLCACertificateFile {{ apache2_opennetca_dir }}/opennet-root.crt
SSLCACertificatePath {{ apache2_opennetca_dir }}/
SSLCARevocationPath {{ apache2_opennetca_dir }}/
SSLCADNRequestPath {{ apache2_opennetca_dir }}/
SSLCARevocationCheck chain

<Location /login>
        Options Indexes FollowSymLinks MultiViews
        Require all granted
        # client cert auth
        SSLVerifyClient optional
        SSLVerifyDepth 3
        # allow access to certificate details
        SSLOptions +StdEnvVars
        # forward auth to cgi
        SSLUserName SSL_CLIENT_S_DN_CN
        # allow specific cert CN
        SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ opennetdev_allowed_users|join('", "') }}" }
        # client cert error handling
        RewriteEngine on
        RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
        RewriteRule .? - [F]
        ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
</Location>

Alias /git/ /var/www/git/

<Location /git>
        Options Indexes FollowSymLinks MultiViews
        Order deny,allow
        Allow from all
	      HeaderName /git/HEADER.html
	      ReadmeName /git/FOOTER.html
</Location>
<Directory /var/www/git>
        IndexIgnore Opennet_logo_quer.gif HEADER.html FOOTER.html
</Directory>
