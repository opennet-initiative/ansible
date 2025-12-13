###############################################################################
# TODO autogenerate via ansible
###############################################################################


@def $IF_BRIDGE_MESH_BATMAN = {{ gateway_batman_bridge_interface }};


domain (ip ip6) table filter {
	chain service-input {
		# fastd VPN
		proto udp dport (1705) ACCEPT;

		# erlaube jeglichen Layer2 Traffic per Batman Mesh
		interface $IF_BRIDGE_MESH_BATMAN {
			ACCEPT;
		}
	}
}

domain ip table nat {
	chain POSTROUTING {
		# NAT für Internetzugriff
		outerface $IF_WAN saddr {{ gateway_dhcp4_subnet_prefix }}.0.0/16 MASQUERADE;
	}
}

domain (ip ip6) chain FORWARD outerface $IF_WAN {
	# erlaube Internet ausgehend
	interface $IF_BRIDGE_MESH_BATMAN ACCEPT;
}
