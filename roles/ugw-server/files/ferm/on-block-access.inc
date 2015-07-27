# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Opennet_ansible

# Die folgenden ausgehenden Verkehrsarten werden von UGW-Servern abgewiesen.
# Typischerweise wollen wir hier nicht-routebare Pakete, eindeutige
# Bot/Schadsoftware-Zugriffe, sowie von unseren Providern beklagte
# Verkehrsarten auffuehren.


############# nicht-oeffentliche IP-Bereiche #################
# Quelle: RFC6890 bzw. https://en.wikipedia.org/wiki/Reserved_IP_addresses
daddr 0.0.0.0/8 REJECT;
daddr 10.0.0.0/8 REJECT;
daddr 100.64.0.0/10 REJECT;
daddr 127.0.0.0/8 REJECT;
daddr 169.254.0.0/16 REJECT;
daddr 172.16.0.0/12 REJECT;
daddr 192.0.0.0/24 REJECT;
daddr 192.0.2.0/24 REJECT;
daddr 192.88.99.0/24 REJECT;
daddr 192.168.0.0/16 REJECT;
daddr 198.18.0.0/15 REJECT;
daddr 198.51.100.0/24 REJECT;
daddr 203.0.113.0/24 REJECT;
daddr 224.0.0.0/4 REJECT;
daddr 240.0.0.0/4 REJECT;
daddr 255.255.255.255/32 REJECT;


########### Allgemein unerwuenschte Verkehrsarten ############

# Windows-Freigaben duerften sich nicht im Internet befinden
proto (tcp udp) dport (135:139 445) DROP;

# Windows-Domain-Controller?
proto (tcp udp) dport 593 DROP;


############### Beschwerden von Providern ####################
# diese Regeln sollten wir regelmaessig begutachten und alte Regeln entfernen

# CERT-Bund#2014111728001208] Schadprogramm-Infektionen in AS39138
# 24.11.2014 - erina
outerface $IF_WAN daddr 217.160.208.160 proto tcp dport 80 DROP;
