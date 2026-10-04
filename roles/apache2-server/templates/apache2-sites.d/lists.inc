# {{ ansible_managed }}

Alias /mailman3/static/postorius/img/favicon.ico	/var/www/favicon.ico
Alias /mailman3/static/hyperkitty/img/favicon.ico	/var/www/favicon.ico
Alias /mailman3/static      /var/lib/mailman3/web/static

<Directory "/var/lib/mailman3/web/static">
	Require all granted
</Directory>

<IfModule mod_proxy_uwsgi.c>
	ProxyPass /mailman3/static !
	ProxyPass / unix:/run/mailman3-web/uwsgi.sock|uwsgi://localhost/
</IfModule>

# Require an authorized Opennet client certificate for Django admin only.
# client certificate authentication
SSLCACertificateFile {{ apache2_opennetca_dir }}/opennet-root.crt
SSLCACertificatePath {{ apache2_opennetca_dir }}/
SSLCARevocationPath {{ apache2_opennetca_dir }}/
SSLCADNRequestPath {{ apache2_opennetca_dir }}/
SSLCARevocationCheck chain

Options Indexes FollowSymLinks MultiViews
# client cert auth
SSLVerifyClient optional
SSLVerifyDepth 3
# allow access to certificate details
SSLOptions +StdEnvVars

<LocationMatch "^/admin(?:/|$)">
  # allow specific cert CN
  SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ mailman_admin_allowed_users|join('", "') }}" }
</LocationMatch>

# client cert error handling
RewriteEngine on
RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
RewriteRule .? - [F]
ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
