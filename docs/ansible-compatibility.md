# Ansible-Kompatibilität

Stand: 2026-11-07

Diese Datei ist die zentrale Referenz für die Versionen, mit denen die
Playbooks dieses Repositories betrieben werden (getestet).
Wenn Ansible oder eine Collection aktualisiert wird, muss diese Datei im
selben Commit angepasst werden.

## Control-Nodes

| Control-Node | Python | Status |
| --- | --- | --- |
| Ubuntu 24.04 | 3.12.3 | getestet durch Martin |

Tragt gern eure Systemkonfiguration hier ein.

## Versionen

| Komponente | Getestet / im Einsatz | Erlaubt | Hinweis |
| --- | --- | --- | --- |
| ansible-core | 2.16.3 | 2.16.x | Letzte Linie mit Python-2.7-Zielen (Debian 7) |
| community.general | 10.7.9 (installiert) | >= 10.6.0, < 11.0.0 | Ab 10.6.0 ist der `php_module`-Identifier enthalten; Playbook-Verifikation auf misumaru steht noch aus |
| community.mysql | 3.8.0 | >= 3.8.0, < 4.0.0 | Für `mysql_db` / `mysql_user` (ViMbAdmin) |

## Zielsysteme

| Zielsystem | Python | Mit ansible-core 2.16 | Hinweis |
| --- | --- | --- | --- |
| Debian 7 (wheezy) | 2.7 | ja | Nur noch `crimson`; ab ansible-core 2.17 nicht mehr unterstützt |
| Debian 10 (buster) | 3.7 | ja | |
| Debian 11 (bullseye) | 3.9 | ja | |
| Debian 12 (bookworm) | 3.11 | ja | |
| Debian 13 (trixie) | 3.13 | in diesem Repo getestet | Offiziell unterstützt 2.16 nur Python 3.6–3.12 auf Zielsystemen |

## Warum ansible-core 2.16?

`ansible-core` 2.16 ist die letzte Version, die Python 2.7 auf Zielsystemen
unterstützt. Solange `crimson` (Debian 7) noch verwaltet wird, ist ein Upgrade
auf 2.17 oder neuer nicht möglich, weil diese Versionen Python 2.7 und 3.6 als
Zielsysteme entfernt haben.

ansible-core 2.16 ist seit Juli 2025 EOL. Nach dem Retirement von `crimson`
sollte auf eine aktuelle, unterstützte Version gewechselt werden. Debian 10
bringt Python 3.7 mit, das von 2.17 noch unterstützt wird. Das Upgrade muss
danach mit `--check` auf allen Zielsystemen getestet und hier dokumentiert
werden.

## Installation

Die Installation erfolgt in einer virtuellen Python-Umgebung. Damit sind die
Versionen unabhängig von Debian-, Ubuntu- oder macOS-Paketen.

Empfohlen ist `ansible-core` plus explizit installierte Collections. Das
Community-Paket `ansible` funktioniert nur, wenn seine gebündelten
Collection-Versionen zu dieser Matrix passen; Ubuntu 24.04 liefert zum
Beispiel `community.general` 8.3.0, das zu alt ist.

### Ubuntu 24.04

```bash
apt install ansible-core
ansible-galaxy collection install -r collections/requirements.yml
```

### Debian / Ubuntu (working with all OS versions)

```bash
sudo apt install python3-venv
python3 -m venv ~/.venvs/ansible-opennet
source ~/.venvs/ansible-opennet/bin/activate
pip install -r requirements-ansible.txt
ansible-galaxy collection install -r collections/requirements.yml
```

### macOS

```bash
brew install python@3.12
python3.12 -m venv ~/.venvs/ansible-opennet
source ~/.venvs/ansible-opennet/bin/activate
pip install -r requirements-ansible.txt
ansible-galaxy collection install -r collections/requirements.yml
```

### Prüfen

```bash
ansible --version
ansible-galaxy collection list community.general community.mysql
```

Die Ausgabe muss zu dieser Datei passen. Die Collection-Installation landet im
Benutzerverzeichnis (`~/.ansible/collections`) und hat Vorrang vor einer
älteren, systemweit installierten Version.

## Upgrade-Regeln

- **ansible-core:** Nicht über 2.16.x hinausgehen, solange `crimson`
  (Debian 7) im Inventory ist. Danach auf eine unterstützte Version wechseln.
- **community.general:** Die Untergrenze 10.6.0 ist wegen des
  `php_module`-Identifiers erforderlich. Vor einem Wechsel auf 11.x zuerst
  `--check` auf Debian 12 und 13 testen und die Obergrenze bewusst anheben.
- **community.mysql:** Vor einem Wechsel auf 4.x die ViMbAdmin-Tasks testen
  und die Obergrenze bewusst anheben.
- Änderungen an `requirements-ansible.txt`, `collections/requirements.yml` und
  dieser Datei gehören in denselben Commit.
- In der Commit-Nachricht oder im PR den Testhost und das Datum nennen.

## Bekannte Einschränkungen

- Ubuntu 24.04 liefert über das `ansible`-Paket ansible-core 2.16.3, aber eine
  veraltete `community.general` (8.3.0). Deshalb die Collection immer über
  `ansible-galaxy` in das Benutzerverzeichnis installieren.
- Debian 13 als Control-Node hat Python 3.13; ansible-core 2.16 unterstützt
  offiziell nur Python 3.10–3.12. Dort ein venv mit Python 3.12 verwenden oder
  die Kombination explizit testen.
- macOS-System-Python ist nicht unterstützt. Homebrew-Python 3.12 verwenden.
- Systemweite und benutzerbezogene Collection-Installationen nicht mischen.
  Maßgeblich ist `~/.ansible/collections`.
