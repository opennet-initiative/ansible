# {{ ansible_managed }}

DocumentRoot /var/lib/mediawiki

#RewriteEngine On
#RewriteRule ^/(.*):(.*) /index.php/$1:$2

<Directory /var/lib/mediawiki/>
	Options +FollowSymLinks
	AllowOverride All
	<IfVersion >= 2.3>
		Require all granted
	</IfVersion>
	<IfVersion < 2.3>
		order allow,deny
		allow from all
	</IfVersion>
</Directory>

# some directories must be protected
<Directory /var/lib/mediawiki/config>
	Options -FollowSymLinks
	AllowOverride None
    <IfModule mod_php7.c>
        php_admin_flag engine off
    </IfModule>
    <IfModule mod_php5.c>
        php_admin_flag engine off
    </IfModule>
</Directory>
<Directory /var/lib/mediawiki/images>
	Options -FollowSymLinks
	AllowOverride None
    <IfModule mod_php7.c>
        php_admin_flag engine off
    </IfModule>
    <IfModule mod_php5.c>
        php_admin_flag engine off
    </IfModule>
</Directory>
<Directory /var/lib/mediawiki/upload>
	Options -FollowSymLinks
	AllowOverride None
    <IfModule mod_php7.c>
        php_admin_flag engine off
    </IfModule>
    <IfModule mod_php5.c>
        php_admin_flag engine off
    </IfModule>
</Directory>
