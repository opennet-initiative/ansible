###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

# Opennet IRC Server 
domain (ip ip6) table filter chain service-input proto tcp dport (6667 6669 6697) ACCEPT;
domain (ip ip6) table filter chain service-input proto udp dport 43416 ACCEPT;
