# Überblick
Diese Rolle installiert die Opennet Mailinglisten Rolle.

Enthalten sind:
* Paketinstallation
* Grundkonfiguration
* Rolle "fail2ban"

Voraussetzungen:
* Hostname od. Sub-Domain für Mailinglisten-Betrieb im DNS pflegen
* bei Sub-Domain entsprechende MX Records setzen
* Apache2 mit Modulen proxy / proxy_uwsgi

# Konfiguration 

Typische Ansible Host-Konfiguration:

```
letsencrypt_certificates:
  - { on_tld_base: lists }
apache2_sites:
  - { name: lists }
apache2_mods:
 - { name: proxy }
 - { name: proxy_http }
 - { name: proxy_http2 }
 - { name: proxy_uwsgi }
```

Benötigte Apache Site Konfiguration:
(Vorlage in `/etc/mailman3/apache.conf`)

```
Alias /mailman3/favicon.ico /var/lib/mailman3/web/static/postorius/img/favicon.ico
Alias /mailman3/static      /var/lib/mailman3/web/static
<Directory "/var/lib/mailman3/web/static">
  Require all granted
</Directory>
<IfModule mod_proxy_uwsgi.c>
  ProxyPass /mailman3/static !
  ProxyPass / unix:/run/mailman3-web/uwsgi.sock|uwsgi://localhost/
</IfModule>
```

Manuelle Konfigurationsschritte:
* initialen Benutzer (admin) + erreichbare E-Mail-Adresse anlegen via
  ```
  dpkg-reconfigure mailman3-web
  ```
* Domain-Namen via Django-Webinterface setzen: `https://<hostname>/  admin/sites/site/`
  ```
  opennet-initiative.de, Opennet Initiative
  ```

= TODO =

