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
