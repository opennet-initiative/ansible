###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################


@def $WG_SERVER_PORT = {{ wg_server_port }};

# Wireguard VPN 
domain (ip ip6) table filter chain service-input proto tcp dport $WG_SERVER_PORT ACCEPT;
