###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################


@def $DNS_ZONE_MASTERS_IPv4 = ({{ dns_zone_masters_ipv4|join(' ') }});
@def $DNS_ZONE_MASTERS_IPv6 = ({{ dns_zone_masters_ipv6|join(' ') }});


# DNS-Zonentransfers
domain ip table filter chain INPUT proto tcp dport domain saddr $DNS_ZONE_MASTERS_IPv4 ACCEPT;
domain ip6 table filter chain INPUT proto tcp dport domain saddr $DNS_ZONE_MASTERS_IPv6 ACCEPT;
