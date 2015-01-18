# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Opennet_ansible

# Windows-Freigaben duerften sich nicht im Internet befinden
proto (tcp udp) dport (135:139 445) DROP;

# Windows-Domain-Controller?
proto (tcp udp) dport 593 DROP;

# CERT-Bund#2014111728001208] Schadprogramm-Infektionen in AS39138
# 24.11.2014 - erina
outerface $IF_WAN daddr 217.160.208.160 proto tcp dport 80 DROP;

