# {{ ansible_managed }}

# Anubis benoetigt diese Header, um Original-Client und Schema zu erkennen.
# Ohne X-Forwarded-Proto bricht Anubis mit einem "admin misconfiguration" Fehler ab.
RequestHeader set "X-Real-Ip" expr=%{REMOTE_ADDR}
RequestHeader set X-Forwarded-Proto "https"
RequestHeader set "X-Http-Version" "%{SERVER_PROTOCOL}s"

ProxyPreserveHost On
ProxyRequests Off
ProxyVia Off

# MediaWiki-Titel koennen kodierte Zeichen enthalten; URL nicht normalisieren.
AllowEncodedSlashes NoDecode

# Der oeffentliche HTTPS-VHost terminiert TLS und leitet an Anubis weiter.
# Anubis prueft die Anfrage und leitet gueltige Anfragen an den internen
# MediaWiki-Backend-VHost auf 127.0.0.1:8081 weiter.
ProxyPass / http://127.0.0.1:8239/ nocanon
ProxyPassReverse / http://127.0.0.1:8239/
