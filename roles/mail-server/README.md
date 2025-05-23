# Überblick
Diese Rolle installiert die Opennet Mail-Server Rolle.

Enthalten sind:
* Paketinstallation
  * MTA: postfix, postfix-mysql
  * DB: mariadb-server, automysqlbackup
  * LDA/IMPA: dovecot-core, dovecot-imapd, dovecot-sieve, dovecot-managesieved, dovecot-lmtpd, dovecot-mysql
  * Anti-Spam: rspamd, redis-server, bind9
  * Anti-Virus: clamav-daemon, clamav-freshclam
  * Webmail: roundcube, roundcube-mysql, roundcube-plugins
  * Admin: vimbadmin, composer, memcached, php-memcache
* Grundkonfiguration
  * vimbadmin - Anpassung der Konfigurationsdateien und Anlage der Datenbank
  * rpsamd - Anpassung der Konfigurationsdateien und Erstellung des DKIM Keys
  * clamav - Dienst-Anbindung an rspamd und automatische Signatur-Aktualisierung
  * roundcube - Anpassung der Konfigurationsdateien und Deaktivierung Standard Apache2-Conf
  * dehydrated - Zusätzliche Hook-Funktion für die Maildienste nach Zertifikatserneuerung
  * web - Bereitstellung einer Opennet Mail Portalseite sowie Mail Autokonfiguration via XML
* Rolle "fail2ban"

Voraussetzungen:
* DNS-Server Konfiguration (MX Records, DMARC, DKIM)
* Apache2 mit PHP-Unterstützung und Proxy-Modulen

# Konfiguration 

Typische Ansible Host-Konfiguration:
```
letsencrypt_certificates:
  - { on_tld_base: mail }
  - { on_tld_base: mail-internal }
apache2_sites:
  - { name: mail }
  - { name: mail-internal }
apache2_mods:
 - { name: proxy }
 - { name: proxy_http }
 - { name: proxy_http2 }
apache2_php: true
mail_server: true
vimbadmin_allowed_users:
  - <mailadmin>.client.on
```

Benötigte Apache Site Konfiguration für "mail":
```
DocumentRoot /var/www/mail
Alias /roundcube /var/lib/roundcube/public_html
<Directory /var/lib/roundcube/public_html/>
  Options +FollowSymLinks
  # This is needed to parse /var/lib/roundcube/.htaccess. 
  AllowOverride All
  Require all granted
</Directory>
<Directory /var/lib/roundcube/config>
  Options -FollowSymLinks
  AllowOverride None
</Directory>
<Directory /var/lib/roundcube/temp>
  Options -FollowSymLinks
  AllowOverride None
  Require all denied
</Directory>
<Directory /var/lib/roundcube/logs>
  Options -FollowSymLinks
  AllowOverride None
  Require all denied
</Directory>
```

Benötigte Apache Site Konfiguration für "mail-internal":
```
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
```

Manuelle Konfigurationsschritte:
* vimbadmin
  * Anlegen des Superusers (admin@) via Webinterface (mit Anpassung Konfigurationsdatei)
  * Anlegen der Domain via Webinterface
* rspamd
  * DKIM Selektor (als aktuelle Jahreszahl) ist in der Rolle via rspamd_config_dkim_selector definiertbar
  * die erzeugten DKIM Public Keys im DNS eintragen, Vorlage: TXT in /var/lib/rspamd/dkim

# Sonstiges

Bereinigung einer vimbadmin-Installation:
```
mysql -e 'drop database vimbadmin;'
mysql -e 'drop user 'vimbadmin'@'localhost';'
rm -rf /var/www/vimbadmin
```

Recursive (Caching) Resolver ist notwendig für die rspamd Anfragen. Es wird daher ein Bind9 mit installiert.

Clamav wird als Dienst mit Stream-Listener auf TCP-Port 3310 gestartet zur Anbindung an Rspamd.
