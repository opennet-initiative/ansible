Benötigte Apache Module fcgid + suexec 

apache2_sites:
  - { name: ping }
apache2_mods:
 - { name: fcgid }
 - { name: suexec }

Benötigte Apache Site Konfiguration:

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
