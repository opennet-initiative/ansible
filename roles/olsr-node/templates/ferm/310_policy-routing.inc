# Stelle sicher, dass eingehende Pakete aus nicht-mesh-Schnittstellen bevorzugt
# ueber eine nicht-mesh-Schnittstelle beantwortet werden. Dies verhindert asymmetrische
# Routen, falls die Quell-IP des Anfragenden auch via Mesh route-bar ist.
#
# Testfall:
#  * Host A announciert seine oeffentliche IP im Mesh
#    (z.B. einer der Uni-Server)
#  * Host B hat eine oeffentliche IP und ist gleichzeitig Teil des Mesh
#    (z.B. ein UGW-Server)
#  * Host A sendet Host B ein Paket ueber das Internet
#  * ohne die untenstehenden Regeln sendet Host B seine Antwort ueber das Mesh
#   * diese Asymmetrie kann je nach Firewall-Konfiguration auf dem Weg zwischen
#     B und A zum Verbindungsverlust fuehren
#
# Ablauf der untenstehenden Firewall-Konfiguration:
#  * mit dem ersten Paket einer ueber das WAN eingehenden Verbindung wird
#    diese markiert (ctmark=32)
#  * lokal erzeugte Antwort-Pakete mit dieser Markierung (ctmark==32)
#    uebertragen selbige in das fwmark/nfmark-Feld
#  * die Policy-Routing-Regel "fwmark 32 lookup main" sorgt dafuer, dass das
#    Paket vorrangig ueber nicht-mesh-Schnittstellen geroutet wird
#
# Verbindungen die wie DNAT umgelenkt wurden (wifidog-DHCP, Nutzertunnel-Portweiterleitung)
# wollen wir unbeeinflusst routen lassen. Fuer diese beiden Anwendungsfaelle ist dies die
# richtige Vorgehensweise.
#
# Diese Firewall-Regeln gelten lediglich fuer IPv4-Routing.
# Explizites IPv6-Routing is hoffentlich nicht erforderlich.


# nur fuer Pakete aus nicht-olsr-Schnittstellen:
# * markiere das erste eingehende Paket jeder Verbindung
# * dies gilt fuer lokal zuzustellende Pakete, sowie fuer weiterzuleitende Pakete
#   (PREROUTING betrifft beide Verbindungstypen)
table mangle {
	chain "new_non_olsr_connections";
	chain PREROUTING interface ({{ non_olsr_interfaces|join(' ') }})
		mod conntrack ctstate NEW jump "new_non_olsr_connections";
}


# fuer alle Pakete aus markierten Verbindungen: kopiere die connection-tracking-Markierung in das "fwmark"-Feld
# Dies ermoeglicht das Policy-Routing.
# PREROUTING: fuer weiterzuleitende Pakete, die via connection tracking markiert wurden (siehe zuvor)
# OUTPUT: Antwort-Pakete fuer eingehende Anfragen (lokal erzeugt)
{% for chain_name in ("PREROUTING", "OUTPUT") %}
table mangle chain {{ chain_name }}
	mod connmark mark {{ non_olsr_policy_routing_mark }}/{{ non_olsr_policy_routing_mark }}
	CONNMARK restore-mark mask {{ non_olsr_policy_routing_mark }};
{% endfor %}