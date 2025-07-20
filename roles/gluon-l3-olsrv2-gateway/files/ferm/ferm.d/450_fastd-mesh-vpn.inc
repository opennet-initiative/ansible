###############################################################################
# TODO autogenerate via ansible
###############################################################################


@def $IF_GLUON_MESH_OLSRV2 = (fastd-mesh);


domain (ip ip6) table filter {
	chain service-input {
		# fastd VPN
		proto udp dport (1705) ACCEPT;

		# wir bieten OLSRv2 via Tunnel an
		interface ($IF_GLUON_MESH_OLSRV2) {
			proto udp dport 269 ACCEPT;
		}
	}
}


domain ip6 chain FORWARD outerface $IF_OLSR2 {
	# Weiterleitung von fastd Mesh-VPN nach Opennet Mesh
	interface $IF_GLUON_MESH_OLSRV2 {
		ACCEPT;
	}
}

domain ip6 chain FORWARD outerface $IF_GLUON_MESH_OLSRV2 {
	# Weiterleitung von Opennet Mesh nach fastd Mesh-VPN
	interface $IF_OLSR2 {
		ACCEPT;
	}
}

#domain ip6 chain FORWARD outerface $IF_WAN {
#	# erlaube Internet ausgehend
#	interface $IF_GLUON_MESH_OLSRV2 ACCEPT;
#}
