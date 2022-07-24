###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

# Die folgenden ausgehenden Verkehrsarten werden von UGW-Servern abgewiesen.
# Typischerweise wollen wir hier nicht-routebare Pakete, eindeutige
# Bot/Schadsoftware-Zugriffe, sowie von unseren Providern beklagte
# Verkehrsarten auffuehren.

# IPv6-only Regeln. Wir nehmen an, dass IPv4 hier nicht genutzt wird.
domain (ip6) chain "on-ugw-v6-block-access" {

	########### Allgemein unerwuenschte Verkehrsarten ############

	# Windows-Freigaben und Domain Controller duerften sich nicht im Internet befinden
	proto (tcp udp) dport (135:139 445 593) DROP;
}
