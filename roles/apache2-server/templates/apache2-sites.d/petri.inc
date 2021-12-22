# {{ ansible_managed }}

DocumentRoot /var/www/petri.opennet-initiative.de

<Directory />
	Options FollowSymLinks
	AllowOverride Indexes 
</Directory>
<Directory /var/www/petri.opennet-initiative.de>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride Indexes
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
</Directory>

# Petri Kamera Image Cache
Alias /cache /var/www/html/petri.opennet-initiative.de/cache
<Directory /var/www/html/petri.opennet-initiative.de/cache>
	Order allow,deny
	Allow from all
</Directory>
ProxyPass /cache !

# Petri Kamera Reverse Proxy for HTTPS
ProxyPass / http://kamera-petri.opennet-initiative.de/
ProxyPassReverse / http://kamera-petri.opennet-initiative.de/
