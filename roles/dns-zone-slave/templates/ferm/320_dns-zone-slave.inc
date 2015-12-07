###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################


@def $DNS_ZONE_MASTERS = ({{ dns_zone_masters|join(' ') }});


# DNS-Zonentransfers
table filter chain INPUT saddr $DNS_ZONE_MASTERS proto tcp dport domain ACCEPT;
