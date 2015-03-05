<?php
	// {{ ansible_managed }}

	$vpn_name = "{{ short_hostname }}.on User VPN";
	$vpn_port = 7506;
        include 'openvpn_clients.php';

	$vpn_name = "{{ short_hostname }}.on UGW VPN";
	$vpn_port = 7505;
        include 'openvpn_clients.php';
?>

