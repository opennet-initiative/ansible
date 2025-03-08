# Überblick
Diese Rolle installiert die Opennet Mail-Server Rolle.

Enthalten sind:
* Paketinstallation
  * postfix, postfix-mysql
  * mariadb-server, automysqlbackup
  * dovecot-core, dovecot-imapd, dovecot-sieve, dovecot-managesieved, dovecot-lmtpd, dovecot-mysql
  * rspamd, clamav, clamsmtp, redis-server
  * roundcube, roundcube-mysql, roundcube-plugins,
  * vimbadmin, composer, memcached, php-memcache
* Grundkonfiguration
  * vimbadmin - Anpassung der Konfigurationsdateien und Anlage der Datenbank
* Rolle "fail2ban"

Voraussetzungen:
* DNS-Server Konfiguration (MX Records, DMARC)
* Apache2 mit PHP-Unterstützung

# Konfiguration 

Typische Ansible Host-Konfiguration:
```
letsencrypt_certificates:
  - { on_tld_base: mail2 }
  - { on_tld_base: mail-internal }
apache2_sites:
  - { name: mail2 }
  - { name: mail-internal }
apache2_php: true
mail_server: true
vimbadmin_allowed_users:
  - mathiasmahnke.client.on
  - martingarbe.client.on
```

Benötigte Apache Site Konfiguration für "mail-internal":
```
DocumentRoot /var/www/vimbadmin/public
<Directory /var/www/vimbadmin/public>
  Options FollowSymLinks
  AllowOverride FileInfo
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
<Location />
  # allow specific cert CN
  SSLRequire %{SSL_CLIENT_S_DN_CN} in { "{{ vimbadmin_allowed_users|join('", "') }}" }
</Location>
# client cert error handling
RewriteEngine on
RewriteCond %{SSL:SSL_CLIENT_VERIFY} !=SUCCESS
RewriteRule .? - [F]
ErrorDocument 403 "You need a certificate issued by Opennet Client Sub-CA to access this site."
```

Manuelle Konfigurationsschritte:
* vimbadmin
  * Anlegen des Superusers (admin@) via Webinterface (mit Anpassung Konfigurationsdatei)
  * Anlegen der Domain via Webinterface
