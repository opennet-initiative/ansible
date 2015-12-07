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


# markiere alle eingehenden Pakete dieser Verbindung (die nat-Tabelle wird nur beim ersten Paket der Verbindung durchlaufen)
table mangle chain INPUT interface ({{ non_olsr_interfaces|join(' ') }}) mod conntrack ctstate NEW
		CONNMARK set-mark {{ non_olsr_policy_routing_mark }}/{{ non_olsr_policy_routing_mark }};

# fuer alle Pakete aus markierten Verbindungen: kopiere die connection-tracking-Markierung in das "fwmark"-Feld
# Dier ermoeglicht das Policy-Routing.
table mangle chain OUTPUT mod connmark mark {{ non_olsr_policy_routing_mark }}/{{ non_olsr_policy_routing_mark }}
		CONNMARK restore-mark mask {{ non_olsr_policy_routing_mark }};
