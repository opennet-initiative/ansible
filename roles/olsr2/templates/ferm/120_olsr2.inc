###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

@def $IF_OLSR2 = ({{ olsr_interfaces|map(attribute='name')|join(' ') }});


domain ip6 table filter {
	chain service-input interface $IF_OLSR2 {
		# OLSR2 IPv6 Routing
		proto udp dport 269 ACCEPT;
    # munin IPv6
    proto tcp dport munin ACCEPT;
	}

	# Verkehr zwischen Opennet-Knoten erlauben
	chain FORWARD interface $IF_OLSR2 outerface $IF_OLSR2 ACCEPT;
}
