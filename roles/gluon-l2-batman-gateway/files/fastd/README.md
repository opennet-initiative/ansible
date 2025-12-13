
installiert aus standard Debian Paket

Konfiguration: siehe /etc/fastd/oni/

systemd: 
/etc/systemd/system/multi-user.target.wants/fastd.service
systemctl daemon-reload

Interfacekonfiguration: siehe /etc/network/interfaces.d/fastd

Service starten:
 systemctl start fastd@oni


Weiter Dokus: https://wiki.freifunk-franken.de/w/Freifunk-Gateway_aufsetzen/VPN/fastd 
