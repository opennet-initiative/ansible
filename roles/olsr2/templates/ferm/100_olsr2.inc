###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

@def $IF_OLSR2 = ({{ olsr2_interfaces|map(attribute='name')|join(' ') }});


domain ip6 table filter {
	chain service-input interface $IF_OLSR2 {
		# olsr2 Routing
		proto udp dport 269 ACCEPT;
	}

	# Verkehr zwischen Opennet-Knoten erlauben
	chain FORWARD interface $IF_OLSR2 outerface $IF_OLSR2 ACCEPT;
}
