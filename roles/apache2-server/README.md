= Überblick =
Diese Rolle erleichtert die Konfigurationen von apache2-basierten Webseiten.

Enthalten sind:
* Paketinstallation
* Erzeugen einer Webseiten-Konfiguration:
    * Include-Datei zur Verwendung für http und/oder https
    * domain-spezifische Log-Dateien
    * optionale https-Nutzung (in Abhängigkeit zur letsencrypt Rolle)
    * optionale http->https-Umleitung
    * Verwendung selbstgewählter Domains oder der opennet-typischen Top-Level-Domains
* Ports 80 und 443 erlauben
* Security und Privacy Konfiguration von Apache
* Default Website von Apache entfernen
* Opennet CA Verzeichnis incl. Zertifikathashes anlegen (notwendig für Cert Logins)

= Konfiguration =
Die Rolle wird auf alle Hosts angewandt, für die eine Variable "apache2_sites" definiert ist.
Diese enthält eine Liste von Dictionaries mit folgenden Attributen:
* name:
    * Name der verwendeten Include-Datei und der zu erzeugenden Konfigurationsdatei
    * wird eventuell für die Erzeugung der Liste von Domains verwendet (siehe "domains")
    * der Parameter ist erforderlich
* domains:
    * kann eine Liste von Domain-Namen für die Webseite enthalten
    * falls leer, dann wird der obige "name" mit allen "üblichen" Opennet-Domains kombiniert
      (siehe "on_default_top_level_domains")
    * Vorgabewert: leer
* redirect_http_to_https:
    * erzeuge eine Umlenkung von http-Zugriffen auf https
    * Vorgabewert: true
* redirect_http_to_https_exclude_paths:
    * eine Liste regulärer Ausdrücke für Pfade, die auch via http bedient werden sollen
* https:
    * erzeuge einen VirtualHost-Block fuer https-Zugriffe
    * Vorgabewert: true
* enable_later:
    * wenn diese Variable definiert ist, dann wird die Site nicht aktiviert. Dies ist bspw.
      nötig, wenn DocumentRoot erst in einem späteren Prozess von ansible erstellt wird.
      Ohne diese Option schlägt der Neustart von Apache fehl (und damit auch ansible),
      weil DocumentRoot nicht vorhanden ist.
* certificate:
    * enthält entweder den Text "letsencrypt" oder ein Dictionary mit folgenden Attributen:
        * cert: Dateiname des Zertifikats
          (optional inklusive Vertrauenskette) - siehe SSLCertificateFile)
        * key: Dateiname des privaten Schlüssels
        * chain: Dateiname der Vertrauenskette (siehe SSLCertificateChainFile)
    * falls "letsencrypt", dann werden die üblichen Pfade des letsencrypt-Clients verwendet
    * Vorgabewert: letsencrypt

Außerdem ist eine Include-Datei (roles/apache2_sites/files/apache2-sites.d/NAME.inc) anzulegen,
welche typischerweise folgende Informationen enthält:
* DocumentRoot
* "Directory"-Direktive für das DocumentRoot mit "Require all granted"
* Webseiten-spezifische Details

Neben der Variable "apache2_sites" gibt es weitere Konfigurationsvariablen:
* apache2_mods: Liste von Dictionaries mit folgenden Inhalten zur Aktivierung von apache2-Modulen
    * name: Name des zu aktivierenden apache2-Moduls
* apache2_php: aktiviere PHP-Unterstützung in apache2 via fcgid (boolean; Vorgabe: false)
* apache2_php_filesize: Festlegung der maximalen Dateigröße für PHP-Uploads (Vorgabe: 2M)
* apache2_security_force_nosniff: aktivieren des Headers "X-Content-Type-Options" mit dem Inhalt
  "nosniff" (Vorgabe: true)
* apache2_security_frame_options: verbiete Einbettung von ausgelieferten Inhalten in anderen
  Webseiten (siehe https://developer.mozilla.org/de/docs/Web/HTTP/Headers/X-Frame-Options)
  (Vorgabe: "sameorigin")

= TODO =
* Umgang mit http->https-Umleitung für .on-Domain klären
    * eventuell separaten http-Block verwenden und auf https://FOO.on-i.de umlenken?
    * oder alle http-Anfragen generell auf den ersten Domain-Namen (mit https) umlenken?
    * oder die https-Fehlermeldung für https://FOO.on/ tolerieren?
