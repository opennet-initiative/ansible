# {{ ansible_managed }}

DocumentRoot /var/www/wiki.opennet-initiative.de

<Directory /var/www/wiki.opennet-initiative.de>
    Require all granted

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteBase /

        # Redirect all requests to index.html
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^ index.html [L]
    </IfModule>

</Directory>
