# {{ ansible_managed }}

DocumentRoot	/var/www/opennetca/

# client certificate authentication
SSLCACertificateFile {{ apache2_opennetca_dir }}/opennet-root.crt
SSLCACertificatePath {{ apache2_opennetca_dir }}/
SSLCARevocationPath {{ apache2_opennetca_dir }}/
SSLCADNRequestPath {{ apache2_opennetca_dir }}/
SSLCARevocationCheck chain

<Location /internal>
        Options Indexes FollowSymLinks MultiViews
        Require all granted
        # client cert auth
        SSLVerifyClient optional
        SSLVerifyDepth 3
        # allow access to certificate details
        SSLOptions +StdEnvVars
        # allow specific cert CN
        SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ opennetca_allowed_users|join('", "') }}" }
        # client cert error handling
        RewriteEngine on
        RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
        RewriteRule .? - [F]
        ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
</Location>
