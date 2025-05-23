# {{ ansible_managed }}

DocumentRoot /var/www/mail

Alias /vimbadmin /var/www/vimbadmin/public
<Directory /var/www/vimbadmin/public>
  Options FollowSymLinks
  AllowOverride FileInfo
  Require all granted    
</Directory>

Redirect /rspamd /rspamd/
RewriteEngine On
RewriteRule ^/rspamd/favicon.ico$ /favicon.ico [PT]
RewriteRule ^/rspamd/(.*) http://127.0.0.1:11334/$1 [P,L]
<Location /rspamd>
  Options FollowSymLinks
  Require all granted
</Location>

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

<Location />
  # allow specific cert CN
  SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ vimbadmin_allowed_users|join('", "') }}" }
</Location>

# client cert error handling
RewriteEngine on
RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
RewriteRule .? - [F]
ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
