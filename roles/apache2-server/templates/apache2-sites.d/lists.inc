# {{ ansible_managed }}

Alias /mailman3/static/postorius/img/favicon.ico	/var/www/favicon.ico
Alias /mailman3/static/hyperkitty/img/favicon.ico	/var/www/favicon.ico
Alias /mailman3/static      /var/lib/mailman3/web/static

<Directory "/var/lib/mailman3/web/static">
	Require all granted
</Directory>

<IfModule mod_proxy_uwsgi.c>
	ProxyPass /mailman3/static !
	ProxyPass / unix:/run/mailman3-web/uwsgi.sock|uwsgi://localhost/
</IfModule>
