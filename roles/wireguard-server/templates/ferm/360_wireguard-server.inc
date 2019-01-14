###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################


@def $WG_SERVER_PORT = {{ wg_server_port }};

# DNS-Zonentransfers
# TODO: zusammenfassen mit der darauffolgenden Regel
#       ab ferm 2.2 (jessie) koennen gemischte IPv4/IPv6-Regeln in einer chain definiert werden
domain ip table filter chain service-input proto tcp dport $WG_SERVER_PORT ACCEPT;
domain ip6 table filter chain service-input proto tcp dport $WG_SERVER_PORT ACCEPT;
