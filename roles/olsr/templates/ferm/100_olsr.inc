###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

@def $IF_OLSR = ({{ olsr_interfaces|map(attribute='name')|join(' ') }});


domain ip table filter {
	chain service-input interface $IF_OLSR {
		# OLSR1 IPv4 Routing
		proto udp dport 698 ACCEPT;
		# OLSR1 IPv4 http-info
		proto tcp dport 8080 ACCEPT;
		# munin IPv4
		proto tcp dport munin ACCEPT;
	}

	# Verkehr zwischen Opennet-Knoten erlauben
	chain FORWARD interface $IF_OLSR outerface $IF_OLSR ACCEPT;
}
