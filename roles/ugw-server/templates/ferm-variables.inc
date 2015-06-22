# {{ ansible_notice }}
# Verwende die Datei /etc/ferm/custom-local.inc fuer lokale Anpassungen.

@def $LOCAL_HNA_IP = {{ main_ip }};
@def $WIFIDOG_SERVER_IP = 192.168.10.3;
# heartofgold.on-i.de ist der primary DNS-Server
@def $DNS_ZONE_MASTER = ({{ dns_zone_masters|join(' ') }});
# NRPE-Zugriffe von goat.on-i.de aus
@def $NAGIOS_SERVER = 46.4.52.102;

@def $IF_ON_USERS = tun-users;
@def $IF_MESH = tap-mesh;
@def $IF_WAN = {{ wan_interface }};

