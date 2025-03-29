# {{ ansible_managed }}

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
