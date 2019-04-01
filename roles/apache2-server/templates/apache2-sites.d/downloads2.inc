DocumentRoot /var/www/downloads
Alias /openwrt/testing /var/lib/buildbot/export

<Directory />
	Options FollowSymLinks
	AllowOverride Indexes 
</Directory>
<Directory /var/www/downloads>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride Indexes
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
  AddDescription "Ubiquity Firmware" ubnt
  AddDescription "OpenWrt Firmware" openwrt
  AddDescription "Opennet Debian Pakete" debian
  IndexOrderDefault Descending Date
</Directory>
<Directory /var/lib/buildbot/export>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride Indexes
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
	IndexOrderDefault Descending Date
</Directory>
