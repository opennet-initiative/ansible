# Gateway für Opennet Gluon

* siehe auch https://wiki.opennet-initiative.de/wiki/Gluon_Batman_Firmware_Test

Die Rolle ist noch im Aufbau...

## Konzept der Netzwerk-Interfaces
* Batman Bridge Interface (`br-mesh-bat`)
  * ist immer vorhanden
  * hat die erste IP im Netz
* Batman Interface (`bat0`)  
  * ist extra Kernel Modul
  * wird der obigen Bridge hinzugefügt
* fastd VPN Interface (`fastd-mesh`)   
  * wird über `batctl` mit Batman Interface verknüpft
