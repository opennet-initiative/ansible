###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

# Opennet DNS Master Server 
domain (ip ip6) table filter chain service-input proto (udp tcp) dport domain ACCEPT;
