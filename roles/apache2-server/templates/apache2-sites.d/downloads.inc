DocumentRoot /var/www/downloads.opennet-initiative.de
Alias /openwrt/testing /home/trac-bitten-slave/export/

<Directory />
	Options FollowSymLinks
	AllowOverride Indexes 
</Directory>
<Directory /var/www/downloads.opennet-initiative.de>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride Indexes
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
</Directory>
<Directory /home/trac-bitten-slave/export>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride Indexes
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
	IndexOrderDefault Descending Date
</Directory>
