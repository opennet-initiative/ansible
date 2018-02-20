###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################

domain (ip ip6) table filter chain service-input proto tcp dport (http https) ACCEPT;
