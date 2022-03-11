# {{ ansible_managed }}

ProxyRequests Off
<Proxy *>
        Order deny,allow
        Allow from all
</Proxy>

ProxyPass / http://127.0.0.1:8010/
ProxyPassReverse / http://127.0.0.1:8010/
