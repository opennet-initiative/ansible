DocumentRoot /var/www/downloads
Alias /openwrt/testing /var/lib/buildbot/export

<Directory />
	Options FollowSymLinks
	AllowOverride Indexes 
</Directory>
<Directory /var/www/downloads>
	Options Indexes FollowSymLinks MultiViews
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
  AddDescription "Ubiquity Firmware" ubnt
  AddDescription "OpenWrt Firmware" openwrt
  AddDescription "Opennet Debian Pakete" debian
  IndexOrderDefault Descending Date
</Directory>
<Directory /var/www/downloads/openwrt>
  AddDescription "Opennet Firmware 2006-2010" attic
  AddDescription "Opennet Firmware (Current Releases)" stable
  AddDescription "Opennet Firmware (Development Builds)" testing
</Directory>
<Directory /var/www/downloads/openwrt/stable>
  IndexOrderDefault Descending Name
</Directory>
<Directory /var/www/downloads/openwrt/attic>
  IndexOrderDefault Descending Name
</Directory>
<Directory /var/www/downloads/ubnt/airos>
  IndexOrderDefault Descending Name
</Directory>
<Directory /var/lib/buildbot/export>
	Options Indexes FollowSymLinks MultiViews
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
	IndexOrderDefault Descending Date
</Directory>
