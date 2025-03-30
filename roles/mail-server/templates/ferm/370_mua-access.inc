###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

domain (ip ip6) table filter chain service-input proto tcp dport 993 ACCEPT;

domain (ip ip6) table filter chain service-input proto tcp dport 465 ACCEPT;
