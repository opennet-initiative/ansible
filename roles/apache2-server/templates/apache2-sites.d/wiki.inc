# {{ ansible_managed }}

DocumentRoot /var/www/wiki.opennet-initiative.de

# These headers need to be set or else Anubis will
# throw an "admin misconfiguration" error.
RequestHeader set "X-Real-Ip" expr=%{REMOTE_ADDR}
RequestHeader set X-Forwarded-Proto "http"
RequestHeader set "X-Http-Version" "%{SERVER_PROTOCOL}s"

ProxyPreserveHost On

ProxyRequests Off
ProxyVia Off

ProxyPass / http://127.0.0.1:8239/
ProxyPassReverse / http://127.0.0.1:8239/
