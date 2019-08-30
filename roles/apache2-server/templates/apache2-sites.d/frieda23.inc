# {{ ansible_managed }}

DocumentRoot /var/www/homematic

<Directory /var/www/homematic>
  Options -Indexes
  Require all granted
</Directory>

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

<Location /internal>
        # allow specific cert CN
        SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ homematic_allowed_users|join('", "') }}" }
</Location>

# client cert error handling
RewriteEngine on
RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
RewriteRule .? - [F]
ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
