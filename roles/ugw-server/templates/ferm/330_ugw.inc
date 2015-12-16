###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################


@def $LOCAL_HNA_IP = {{ olsr_main_ip }};
@def $IF_ON_USERS = {{ openvpn_users_interface }};
@def $WIFIDOG_SERVER_IP = 192.168.10.3;


# Wir wollen die Portweiterleitungen nach einem Firewall-Restart neu aufbauen
@hook post "/usr/local/bin/rebuild_user_port_forwards.py '{{ openvpn_users_ipv4_base }}' '{{ openvpn_users_ipv4_netmask }}'";


domain (ip ip6) table filter {
	chain INPUT {
		# User-VPN und UGW-VPN
		proto udp dport (1600 1602) ACCEPT;

		# VPN-Status zugaenglich machen
		proto tcp dport http ACCEPT;

		# discard-Dienst fuer Upload-Messungen der UGWs
		proto tcp dport discard ACCEPT;

		# wir bieten NTP und DNS via Tunnel und Mesh an
		interface ($IF_ON_USERS $IF_OLSR) {
			proto udp dport ntp ACCEPT;
			proto (udp tcp) dport domain ACCEPT;
		}

		# ein paar UGW-Firmware-Versionen versuchen DNS und NTP ueber die oeffentliche IP zu erreichen
		interface $IF_WAN proto (udp tcp) dport (domain ntp) REJECT;
	}
}


domain ip chain FORWARD outerface $IF_WAN {
	# keine Weiterleitung an nicht-oeffentliche IP-Bereiche
	# Quelle: RFC6890 bzw. https://en.wikipedia.org/wiki/Reserved_IP_addresses
	daddr (0.0.0.0/8 10.0.0.0/8 100.64.0.0/10 127.0.0.0/8 169.254.0.0/16
		172.16.0.0/12 192.0.0.0/24 192.0.2.0/24 192.88.99.0/24 192.168.0.0/16
		198.18.0.0/15 198.51.100.0/24 203.0.113.0/24 224.0.0.0/4 240.0.0.0/4
		255.255.255.255/32) REJECT;
}


domain (ip ip6) chain FORWARD outerface $IF_WAN {
	# wir sperren schad-typische Zugriffe ins Internet
	interface $IF_ON_USERS jump "on-ugw-block-access";

	# alle anderen Zugriffe aus dem Tunnel-VPN
	interface $IF_ON_USERS ACCEPT;

	# Zugriffe auf ein paar definierte Dienste und Server sind auch ohne VPN erlaubt
	jump on-unauth-forward;
}


domain (ip ip6) chain on-unauth-forward;

domain ip chain on-unauth-forward {
	daddr ({{ ugw_external_forward_allow_ipv4|join(" ") }}) ACCEPT;
}


# Portweiterleitung und DNAT sollten nur fuer IPv4 relevant sein
domain ip table nat {
	# diese Tabelle wird mittels des openvpn-Portweiterleitungsskripts gefuellt
	chain user_dnat;

	chain PREROUTING {
		# Portweiterleitungen fuer Nutzer-Tunnel
                mod addrtype dst-type LOCAL proto (tcp udp) dport 10000:17639 jump user_dnat;
		# ohne diese Regel werden die eigenen Antwort-Pakete mit falschen Quell-IPs verschickt
		interface $IF_OLSR daddr $LOCAL_HNA_IP REDIRECT;
		# DHCP-Anfragen von wifidog-Clients zu inez umlenken
		interface $IF_ON_USERS daddr {{ openvpn_users_ipv4_server }} proto udp dport 67 DNAT to $WIFIDOG_SERVER_IP;
	}

	chain POSTROUTING {
		# private Opennet-IP-Adresse nicht nach aussen dringen lassen
		outerface $IF_WAN saddr (192.168.0.0/16 10.0.0.0/8) MASQUERADE;
	}
}
