# {{ ansible_managed }}

# config taken from http://docs.buildbot.net/current/manual/configuration/www.html#reverse-proxy-configuration

# replace with actual port of your Buildbot master
ProxyPass /ws ws://127.0.0.1:8010/ws
ProxyPassReverse /ws ws://127.0.0.1:8010/ws
ProxyPass / http://127.0.0.1:8010/
ProxyPassReverse / http://127.0.0.1:8010/
