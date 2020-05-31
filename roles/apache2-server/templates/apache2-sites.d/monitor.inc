# {{ ansible_managed }}

DocumentRoot /var/cache/munin/www

# Rewrite rules to serve traffic from the root instead of /munin-cgi
RewriteEngine On

# Static files
#RewriteRule ^/favicon.ico /var/cache/munin/www/static/favicon.ico [L]
RewriteRule ^/static/(.*) /var/cache/munin/www/static/$1          [L]
RewriteRule ^/favicon.ico /var/www/html/favicon.ico [L]
RewriteRule ^/robots.txt /var/www/html/robots.txt [L]

# HTML
RewriteRule ^(/.*\.html)?$ /munin-cgi/munin-cgi-html/$1 [PT]
RewriteRule ^(.*/)$ /munin-cgi/munin-cgi-html/$1 [PT]

# Images
RewriteRule ^/munin-cgi/munin-cgi-graph/(.*) /$1
RewriteCond %{REQUEST_URI}                 !^/static
RewriteRule ^/(.*.png)$ /munin-cgi/munin-cgi-graph/$1 [L,PT]

ScriptAlias /munin-cgi/munin-cgi-graph /usr/lib/munin/cgi/munin-cgi-graph
ScriptAlias /munin-cgi/munin-cgi-html /usr/lib/munin/cgi/munin-cgi-html

<Directory /var/cache/munin/www>
    Require all granted
    Options None
    DirectoryIndex index.html
</Directory>

<Directory /usr/lib/munin/cgi>
    Require all granted
    <IfModule mod_fcgid.c>
        SetHandler fcgid-script
    </IfModule>
    <IfModule !mod_fcgid.c>
        SetHandler cgi-script
    </IfModule>
</Directory>
