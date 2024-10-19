###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################


@def $IF_WG_ON_USERS = {{ wg_interface }};
@def $WG_SERVER_PORT = {{ wg_server_port }};

# Wireguard VPN
domain (ip ip6) table filter chain service-input interface $IF_WAN proto udp dport $WG_SERVER_PORT ACCEPT;

domain ip chain FORWARD outerface $IF_OLSR {
	# Weiterleitung von User-VPN nach Opennet Mesh
	interface $IF_WG_ON_USERS {
		# - Sonderfall VPN von externen Mobilen VPN-Clients (192.168.7.0/24):
		saddr 10.1.8.0/22 daddr 192.168.0.0/16 ACCEPT;
		# - kein Verkehr anderer Clients (z.B. offener Zugangspunkte) in Richtung regulaerer Mesh-IPs
		daddr 192.168.0.0/16 REJECT;
		# - alle anderen (HNA-) IPs sind jedoch erreichbar
		#   Beispiel-Ziele: Opennet-Server mit oeffentlicher IP im Mesh-Routing
		#   Dies ist noetig fuer:
		#     - offene Zugangspunkte: leiten ihren gesamten Verkehr in den Tunnel
		#     - Firmware vor v0.5.x: jeglicher Verkehr (bis auf 192.168.0.0/16 als Ziel) geht in den Tunnel
		ACCEPT;
	}
}

domain (ip ip6) chain FORWARD outerface $IF_WAN {
	# wir sperren schad-typische Zugriffe ins Internet
	interface $IF_WG_ON_USERS jump "on-ugw-block-access";

	# alle anderen Zugriffe aus dem Tunnel-VPN
	interface $IF_WG_ON_USERS ACCEPT;

	# Zugriffe auf ein paar definierte Dienste und Server sind auch ohne VPN erlaubt
	jump on-unauth-forward;
}