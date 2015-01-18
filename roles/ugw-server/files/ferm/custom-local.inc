# Diese Datei ist der richtige Ort fuer lokal-spezifische Firewall-Regeln.
# Alle anderen ferm-Dateien werden mittels der ansible-Konfigurationsverwaltung gelegentlich ueberschrieben.
# siehe https://wiki.opennet-initiative.de/wiki/Opennet_ansible

table filter {
	chain local-services-input {
		# Regeln fuer zusaetzliche lokale Dienste
	}

	chain local-services-forward {
		# Regeln fuer zusaetzliche Weiterleitungen
	}
}

