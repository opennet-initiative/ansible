# Überblick
Diese Rolle installiert den Opennet SmokePing Dienst zur ICMP Echo (Ping) basierten Überwachung von Servern und Access Points im Opennet Mesh.

Enthalten sind:
* Installation von SmokePing und Apache2 FCGI
* Anpassung der SmokePing Konfiguration
* Anlage Webverzeichnis für Logo und Favicon
* Ablage Generator-Script für SmokePing Targets
* Cron-Job zur Aktualisierung der Targets

Voraussetzungen:
* Apache2 mit Modulen fcgid + suexec 

## Konfiguration

Typische Ansible Host-Konfiguration:

```
letsencrypt_certificates:
  - { on_tld_base: ping }
apache2_sites:
  - { name: ping }
apache2_mods:
 - { name: fcgid }
 - { name: suexec }
```

Benötigte Apache Site Konfiguration:

```
DocumentRoot /usr/share/smokeping/www
ScriptAlias /smokeping.cgi /usr/lib/cgi-bin/smokeping.cgi
Alias /Opennet_logo.png /var/www/ping/Opennet_logo.png
Alias /favicon.ico /var/www/ping/favicon.ico
<Directory />
  Options FollowSymLinks ExecCGI
</Directory>
<Directory /usr/share/smokeping/www>
  Options FollowSymLinks
  Require all granted
</Directory>
<Directory /usr/lib/cgi-bin>
  Require all granted
  <IfModule mod_fcgid.c>
    SetHandler fcgid-script
  </IfModule>
  <IfModule !mod_fcgid.c>
    SetHandler cgi-script
  </IfModule>
</Directory>
```
