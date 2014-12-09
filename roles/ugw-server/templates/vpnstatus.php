<?php

	$vpn_name = "{{ ansible_hostname }}.on User VPN";
	$vpn_port = 7506;
        include 'openvpn_clients.php';

	$vpn_name = "{{ ansible_hostname }}.on UGW VPN";
	$vpn_port = 7505;
        include 'openvpn_clients.php';
?>

