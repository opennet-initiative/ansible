###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

domain (ip ip6) table filter chain service-input proto tcp dport {{ mailserver_port_imap }} ACCEPT;
domain (ip ip6) table filter chain service-input proto tcp dport {{ mailserver_port_smtp }} ACCEPT;
domain (ip ip6) table filter chain service-input proto tcp dport {{ mailserver_port_submission }} ACCEPT;
