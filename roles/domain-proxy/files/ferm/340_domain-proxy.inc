###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

# erlaube Zugriffe auf den http- und https-Proxy
domain (ip ip6) table filter chain service-input proto tcp dport (http https) ACCEPT;
