###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

domain (ip ip6) table filter chain service-input proto tcp dport ({{ apache2_port_http }} {{ apache2_port_https }}) ACCEPT;
