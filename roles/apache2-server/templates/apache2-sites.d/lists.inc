# {{ ansible_managed }}

Alias /mailman3/static/postorius/img/favicon.ico	/var/www/favicon.ico
Alias /mailman3/static/hyperkitty/img/favicon.ico	/var/www/favicon.ico
Alias /mailman3/static      /var/lib/mailman3/web/static
Alias /registration-disabled.html /var/www/registration-disabled.html

<Directory "/var/lib/mailman3/web/static">
	Require all granted
</Directory>

<IfModule mod_proxy_uwsgi.c>
	ProxyPass /mailman3/static !
	ProxyPass /registration-disabled.html !
	ProxyPass / unix:/run/mailman3-web/uwsgi.sock|uwsgi://localhost/
</IfModule>

# Anonymous web signup for selected lists is disabled; redirect POSTs to a notice.
RewriteEngine On
RewriteRule ^/postorius/lists/(?:crew|admin|vorstand)\.lists\.opennet-initiative\.de/anonymous_subscribe/?$ /registration-disabled.html [R=303,L]

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

ErrorDocument 403 "An authorized Opennet client certificate is required to access this site."
