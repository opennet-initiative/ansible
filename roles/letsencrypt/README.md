= Überblick =
Die letsencrypt-Rolle ermöglicht die automatische Erzeugung von SSL-Zertifikaten via letsencrypt.
Voraussetzungen:
  * der Host ist via Port 80 erreichbar
  * http-Requests für die gewählten Domains müssen bei dem Host ankommen

= Anwendung =
In den Host-Variablen sind Einträge folgender Art anzulegen:

  letsencrypt_certificates:
  - { domains: [ca.opennet-initiative.de, ca.on-i.de] }
  - { on_tld_base: downloads }

Jedes Element der Liste entspricht einem Zertifikat (eventuell mit mehreren Domain-Namen).

Falls "domains" fehlt, dann wird "on_tld_base" mit allen üblichen Top-Level-Domains (siehe
"on_default_top_level_domains") kombiniert.
