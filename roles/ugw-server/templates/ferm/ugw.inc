###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################


@def $LOCAL_HNA_IP = {{ main_ip }};
@def $IF_ON_USERS = tun-users;
@def $WIFIDOG_SERVER_IP = 192.168.10.3;


# Wir wollen die Portweiterleitungen nach einem Firewall-Restart neu aufbauen
@hook post "/etc/openvpn/opennet_users/connection_script.py rebuild_port_forward '{{ openvpn_users_ipv4_base }}' '{{ openvpn_users_ipv4_netmask }}'";


table filter {
	chain INPUT {
		# User-VPN und UGW-VPN
		proto udp dport (1600 1602) ACCEPT;

		# VPN-Status zugaenglich machen
		proto tcp dport http ACCEPT;
	}

	chain FORWARD {
		outerface $IF_WAN {
			# wir sperren schad-typische Zugriffe ins Internet
			interface $IF_ON_USERS jump "on-ugw-block-access";
			# alle anderen Zugriffe aus dem Tunnel-VPN
			interface $IF_ON_USERS ACCEPT;
			# Zugriffe auf ein paar definierte Dienste und Server sind auch ohne VPN erlaubt
			jump on-unauth-forward;
		}
	}

	chain on-unauth-forward {
		# downloads.openwrt.org
		daddr 78.24.191.177 ACCEPT;
	}
}


table nat {
	# diese Tabelle wird mittels des openvpn-Portweiterleitungsskripts gefuellt
	chain user_dnat;

	chain PREROUTING {
		# Portweiterleitungen fuer Nutzer-Tunnel
                mod addrtype dst-type LOCAL proto (tcp udp) dport 10000:17639 jump user_dnat;
		# ohne diese Regel werden die eigenen Antwort-Pakete mit falschen Quell-IPs verschickt
		interface $IF_MESH daddr $LOCAL_HNA_IP REDIRECT;
		# DHCP-Anfragen von wifidog-Clients zu inez umlenken
		interface $IF_ON_USERS daddr 10.1.0.1 proto udp dport 67 DNAT to $WIFIDOG_SERVER_IP;
	}
}
