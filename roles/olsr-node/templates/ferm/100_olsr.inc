###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################

@def $IF_OLSR = ({{ olsr_interfaces|map(attribute='name')|join(' ') }});


domain (ip ip6) table filter {
	chain INPUT interface $IF_OLSR {
		# olsrd: Routing
		proto udp dport 698 ACCEPT;
		# olsrd: http-info
		proto tcp dport 8080 ACCEPT;
		# munin
		proto tcp dport munin ACCEPT;
	}

	# Verkehr zwischen Opennet-Knoten erlauben
	chain FORWARD interface $IF_OLSR outerface $IF_OLSR ACCEPT;
}
