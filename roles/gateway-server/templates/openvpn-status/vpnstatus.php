<?php
// {{ ansible_managed }}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>

<title>{{ short_hostname }}.on VPN Status</title>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta http-equiv='refresh' content='300' />

<style type="text/css">
table {
    border-collapse: collapse;
}
th {
    background: #73b5e5;
    color: white;
}
tr {
    border-bottom: 1px solid silver;
}
td {
    padding: 0px 10px 0px 10px;
}
</style>

</head>

<body>

<h2>Opennet VPN Service</h2>

<?php
// User VPN IPv4 Tunnel
$vpn_name = "{{ short_hostname }}.on User Connections";
$vpn_port = 7506;
include 'openvpn_clients.php';
{% if gateway_user6_enable == true %}
// User VPN IPv6 Tunnel
$vpn_name = "{{ short_hostname }} User6 Connections";
$vpn_port = 7507;
include 'openvpn_clients.php';
{% endif %}
// UGW VPN IPv4 Tunnel
$vpn_name = "{{ short_hostname }}.on UGW Connections";
$vpn_port = 7505;
include 'openvpn_clients.php';
?>

<p>
All traffic data in KB or KB/s. This page gets reloaded every 3 min. Last update: <b><?php echo date ("
Y-m-d H:i:s") ?></b>
</p>
<p>
Further information: <a href="https://www.opennet-initiative.de">https://www.opennet-initiative.de</a>
</p>
<p>
<img src="Opennet_logo_quer.gif" alt="Opennet Logo"/>
</p>

</body>

</html>
