###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

@def $DNS_ZONE_PRIMARIES_IPv4 = ({{ dns_zone_primaries_ipv4|join(' ') }});
@def $DNS_ZONE_PRIMARIES_IPv6 = ({{ dns_zone_primaries_ipv6|join(' ') }});

# DNS-Zonentransfers
domain ip table filter chain service-input proto tcp dport domain saddr $DNS_ZONE_PRIMARIES_IPv4 ACCEPT;
domain ip6 table filter chain service-input proto tcp dport domain saddr $DNS_ZONE_PRIMARIES_IPv6 ACCEPT;
