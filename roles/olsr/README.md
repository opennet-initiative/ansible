= Überblick =
Diese Rolle installiert den OLSR Deamon.

Enthalten sind:
* Paketinstallation
* Erzeugen einer OLSR Konfiguration:
    * Verwendung selbstgewählter Announcements oder Announcements auf Basis der opennet-typischen Top-Level-Domains
* Firewall einrichten:
  * OLSRv1/v2 (udp/269, udp/698)
  * OLSR HTTP-Info (tcp/8080)
  * Munin erlauben
  * Datenverkehr zwischen Opennet Knoten erlauben
* Policy-Routing konfigurieren
* Munin einrichten, zusätzliches Plugin

= Konfiguration =
olsr_nameservice_announcements
  * konfiguriert das Senden von Diensten per OLSR Nameservice Plugin
  * Dienste können entweder einzeln explizit aufgeführt werden
  * oder per "on_tld_base: <hostname/cname>" definitiert werden
    (siehe "on_default_top_level_domains")
  * Vorgabewert: leer

= TODO =
* Dokumentation der weiteren Parameter dieser Rolle
