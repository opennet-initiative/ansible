# {{ ansible_managed }}

DocumentRoot /var/www/domain-proxy.opennet-initiative.de

<Directory /var/www/domain-proxy.opennet-initiative.de>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride Indexes
        Require all granted
        IndexIgnore *.ico Opennet_logo_quer.gif HEADER.html FOOTER.html
        HeaderName /HEADER.html
        ReadmeName /FOOTER.html
</Directory>
