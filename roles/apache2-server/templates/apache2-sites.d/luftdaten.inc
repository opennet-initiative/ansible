# {{ ansible_managed }}

DocumentRoot /var/www/luftdaten.opennet-initiative.de

<Directory />
	Options FollowSymLinks
	AllowOverride Indexes 
</Directory>
<Directory /var/www/luftdaten.opennet-initiative.de>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride Indexes
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
</Directory>

# AmKabutzenhof Image Cache
Alias /amkabutzenhof /var/www/html/amkabutzenhof
<Directory /var/www/html/amkabutzenhof>
	Order allow,deny
	Allow from all
</Directory>
ProxyPass /amkabutzenhof !

# InfluxDB
ProxyPass /db/ http://localhost:8086/
ProxyPassReverse /db/ http://localhost:8086/

# Grafana
ProxyPass / http://localhost:3000/
ProxyPassReverse / http://localhost:3000/
