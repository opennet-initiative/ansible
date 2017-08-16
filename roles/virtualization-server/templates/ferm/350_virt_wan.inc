domain (ip ip6) {
	table filter {
		chain INPUT {
			interface {{ virtualization_wan_bridge_interface }} {
				proto (tcp udp) dport domain ACCEPT;
				proto udp dport bootps ACCEPT;
			}
		}

		chain FORWARD {
			interface {{ virtualization_wan_bridge_interface }} outerface ({{ wan_interface }} $IF_OLSR) ACCEPT;
		}
	}

	table nat chain POSTROUTING {
		saddr {{ virtualization_wan_bridge_address_prefix }}.0/24 outerface ({{ wan_interface }} $IF_OLSR) MASQUERADE;
	}
}
