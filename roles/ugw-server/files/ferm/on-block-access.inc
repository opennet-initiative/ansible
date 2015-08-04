###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/conf.d/ abgelegt werden.
###############################################################################

# Die folgenden ausgehenden Verkehrsarten werden von UGW-Servern abgewiesen.
# Typischerweise wollen wir hier nicht-routebare Pakete, eindeutige
# Bot/Schadsoftware-Zugriffe, sowie von unseren Providern beklagte
# Verkehrsarten auffuehren.
chain "on-ugw-block-access" {

	########### Allgemein unerwuenschte Verkehrsarten ############

	# Windows-Freigaben und Domain Controller duerften sich nicht im Internet befinden
	proto (tcp udp) dport (135:139 445 593) DROP;


	############### Beschwerden von Providern ####################
	# diese Regeln sollten wir regelmaessig begutachten und alte Eintraege entfernen

	# CERT-Bund#2014111728001208] Schadprogramm-Infektionen in AS39138
	# 24.11.2014 - erina
	daddr 217.160.208.160 proto tcp dport 80 DROP;
}
