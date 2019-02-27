# {{ ansible_managed }}

DocumentRoot /var/www
RedirectMatch ^/$ /vpnstatus

<Directory /var/www>
  Options FollowSymLinks
  Require all granted
</Directory>
