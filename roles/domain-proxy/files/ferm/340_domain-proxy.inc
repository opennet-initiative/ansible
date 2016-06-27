###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################

# erlaube Zugriffe auf den http- und https-Proxy
domain (ip ip6) table filter chain INPUT proto tcp dport (http https) ACCEPT;
