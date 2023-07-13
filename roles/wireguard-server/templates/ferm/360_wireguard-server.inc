###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################


@def $WG_SERVER_IF = {{ wg_interface }};
@def $WG_SERVER_PORT = {{ wg_server_port }};

# Wireguard VPN
domain (ip ip6) table filter chain service-input interface $WG_SERVER_IF proto udp dport $WG_SERVER_PORT ACCEPT;
