DocumentRoot /var/www/downloads

Alias /openwrt/testing /var/www/downloads-buildbot

<Directory />
	AllowOverride Indexes 
</Directory>
<Directory /var/www/downloads>
	Options Indexes MultiViews
	Require all granted
	IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
	HeaderName /HEADER.html
	ReadmeName /FOOTER.html
  AddDescription "Ubiquiti Firmware" ubnt
  AddDescription "Opennet Firmware - OpenWrt" openwrt
  AddDescription "Debian Pakete" debian
  AddDescription "Opennet Verein" verein
  AddDescription "Opennet Firmware - Gluon" gluon
  AddDescription "Mikrotik Firmware" mikrotik
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

<Directory /var/www/downloads-buildbot>
  Require all granted
  IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
  HeaderName /HEADER.html
  ReadmeName /FOOTER.html
  IndexOrderDefault Descending Name
</Directory>
