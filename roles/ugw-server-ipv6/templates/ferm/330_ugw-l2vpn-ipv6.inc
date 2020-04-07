###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################


@def $LOCAL_HNA_IPv6 = {{ olsr_main_ipv6 }};
@def $IF_ON_USERS_V6 = {{ openvpn_users_l2_v6_interface }};

domain ip6 table filter {
	chain service-input {
		# Layer2 User-VPN fuer IPv6
		proto udp dport (1700) ACCEPT;

		# VPN-Status zugaenglich machen
		proto tcp dport http ACCEPT;

		# discard-Dienst fuer Upload-Messungen der UGWs
		proto tcp dport discard ACCEPT;

		# wir bieten NTP + DNS + DHCPv6-PD via Tunnel und Mesh an
		interface ($IF_ON_USERS_V6) {
			proto udp dport ntp ACCEPT;
			proto (udp tcp) dport domain ACCEPT;
			proto udp dport 547 ACCEPT;
		}
	}
}

#Workaround: Erlaube auch Verbindungen via IPv4 zum OpenVPN Server.
#Allgemein praeferieren wir IPv6 aber es gibt (Stand April 2020) noch viele IPv4-only Verbindungen im Mesh.
#Nutzer hinter diesen Knoten koennten diesen Dienst hier nicht nutzen, wenn er nur per IPv6 erreichbar waere.
#TODO: so frueh wie moeglich diese Firewallregel hier deaktivieren.
domain ip table filter {
	chain service-input {
		# Layer2 User-VPN fuer IPv6
		proto udp dport (1700) ACCEPT;
	}
}


domain ip6 chain FORWARD outerface $IF_WAN {
	# wir sperren schad-typische Zugriffe ins Internet
	interface $IF_ON_USERS_V6 jump "on-ugw-v6-block-access";

	# alle anderen Zugriffe aus dem Tunnel-VPN
	interface $IF_ON_USERS_V6 ACCEPT;

	# Zugriffe auf ein paar definierte Dienste und Server sind auch ohne VPN erlaubt
	jump on-unauth-forward-v6;
}


domain ip6 chain on-unauth-forward-v6 {
	daddr ({{ ugw_external_forward_allow_ipv6|join(" ") }}) ACCEPT;
}
