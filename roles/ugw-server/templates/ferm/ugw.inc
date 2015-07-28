###############################################################################
# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Opennet_ansible
# Verwende die Datei /etc/ferm/custom-local.inc fuer lokale Anpassungen.
###############################################################################


# Wir wollen die Portweiterleitungen nach einem Firewall-Restart neu aufbauen
@hook post "/etc/openvpn/opennet_users/connection_script.py rebuild_port_forward '{{ openvpn_users_ipv4_base }}' '{{ openvpn_users_ipv4_netmask }}'";


table filter {
	chain on-services-input {
		# User-VPN und UGW-VPN
		proto udp dport (1600 1602) ACCEPT;

		# iperf - manuell zu starten fuer gelegentliche Tests
		proto (udp tcp) dport 5001 ACCEPT;

		# VPN-Status zugaenglich machen
		proto tcp dport http ACCEPT;

		# munin
		proto tcp dport munin ACCEPT;

		# Dienste fuer das Opennet
		interface $IF_MESH {
			# olsrd: Routing
			proto udp dport 698 ACCEPT;
			# olsrd: http-info
			proto tcp dport 8080 ACCEPT;
			# ntp
			proto udp dport ntp ACCEPT;
			# DNS
			proto (udp tcp) dport domain ACCEPT;
		}

		# DNS-Zonentransfers
		saddr $DNS_ZONE_MASTER proto tcp dport domain ACCEPT;

		# Nagios-Ueberwachung via nrpe
		saddr $NAGIOS_SERVER proto tcp dport nrpe ACCEPT;
	}

	chain on-unauth-forward {
		# downloads.openwrt.org
		daddr 78.24.191.177 ACCEPT;
	}

	chain on-services-forward {
		# VPN-Nutzende -> Internet
		interface $IF_ON_USERS outerface $IF_WAN ACCEPT;
		# Verkehr zwischen Opennet-Knoten
		interface $IF_MESH outerface $IF_MESH ACCEPT;
		interface $IF_ON_USERS daddr $WIFIDOG_SERVER_IP proto udp dport 67 ACCEPT;
	}
}


table nat {
	chain PREROUTING {
		jump on-prerouting;
	}

	chain POSTROUTING {
		jump on-postrouting;
	}

	chain user_dnat;

	chain on-prerouting {
		# Portweiterleitungen fuer Nutzer-Tunnel
                mod addrtype dst-type LOCAL proto (tcp udp) dport 10000:17639 jump user_dnat;
		# ohne diese Regel werden die eigenen Antwort-Pakete mit falschen Quell-IPs verschickt
		interface $IF_MESH daddr $LOCAL_HNA_IP REDIRECT;
		# DHCP-Anfragen von wifidog-Clients zu inez umlenken
		interface $IF_ON_USERS daddr 10.1.0.1 proto udp dport 67 DNAT to $WIFIDOG_SERVER_IP;
	}

	chain on-postrouting {
		outerface $IF_WAN saddr (192.168.0.0/16 10.0.0.0/8) MASQUERADE;
	}
}

