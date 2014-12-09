# Windows-Freigaben duerften sich nicht im Internet befinden
proto (tcp udp) dport (135:139 445) DROP;

# Windows-Domain-Controller?
proto (tcp udp) dport 593 DROP;

