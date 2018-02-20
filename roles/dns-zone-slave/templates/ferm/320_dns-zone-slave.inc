###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################


@def $DNS_ZONE_MASTERS_IPv4 = ({{ dns_zone_masters_ipv4|join(' ') }});
@def $DNS_ZONE_MASTERS_IPv6 = ({{ dns_zone_masters_ipv6|join(' ') }});


# DNS-Zonentransfers
# TODO: zusammenfassen mit der darauffolgenden Regel
#       ab ferm 2.2 (jessie) koennen gemischte IPv4/IPv6-Regeln in einer chain definiert werden
domain ip table filter chain service-input proto tcp dport domain saddr $DNS_ZONE_MASTERS_IPv4 ACCEPT;
domain ip6 table filter chain service-input proto tcp dport domain saddr $DNS_ZONE_MASTERS_IPv6 ACCEPT;
