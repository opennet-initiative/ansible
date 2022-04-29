<?php
// {{ ansible_managed }}
// OpenVPN (php-based) web status script
// 
// This script has been released to the public domain by Pablo Hoffman 
// on February 28, 2007.
//
// Original location: 
// http://pablohoffman.com/software/vpnstatus/vpnstatus.txt

// Configuration values --------
$vpn_host = "localhost";
//$vpn_name = "{{ short_hostname }}.on UGW VPN"; //will be set outside
//$vpn_port = 7505; //will be set outside
// -----------------------------

$fp = fsockopen($vpn_host, $vpn_port, $errno, $errstr, 30);
if (!$fp) {
//    echo "$errstr ($errno)<br />\n";
//    exit;
  return;
}

fwrite($fp, "status\n\n\n");
$clients = array();
$inclients = $inrouting = false;
while (!feof($fp)) {
    $line = fgets($fp, 128);
    if (substr($line, 0, 13) == "ROUTING TABLE") {
        $inclients = false;
	// close the connection
	fwrite($fp, "quit\n\n\n");
    }
    if ($inclients) {
        $cdata = explode(',', $line);
        $clines[$cdata[0]] = array($cdata[2], $cdata[3], $cdata[4]);
    }
    if (substr($line, 0, 11) == "Common Name") {
        $inclients = true;
    }

    if (substr($line, 0, 12) == "GLOBAL STATS") {
        $inrouting = false;
    }
    if ($inrouting) {
        $routedata = explode(',', $line);
        array_push($clients, array_merge($routedata, $clines[$routedata[1]]));
    }
    if (substr($line, 0, 15) == "Virtual Address") {
        $inrouting = true;
    }
}

$headers = array('VPN Address', 'Name', 'Real Address', 'Last Act', 'Recv', 'Sent', 'Connected Since', 'Rate');
$tdalign = array('left', 'right', 'left', 'left', 'right', 'right', 'left', 'right');
/* DEBUG
print "<pre>";
print_r($headers);
print_r($clients);
print_r($clines);
print_r($routedata);
print "</pre>";
*/
fclose($fp);

?> 

<h3><?php echo $vpn_name; ?> (<?php echo count($clients); ?>)</h3>

<table>
<tr>
<?php foreach ($headers as $th) { ?>
<th><?php echo $th?></th>
<?php } ?>
</tr>

<?php foreach ($clients as $client) {
    $time = strtotime($client[3]) - strtotime($client[6]);

    if ($time > 0) {
        $rate = ($client[4] + $client[5]) / $time;
        $client[7] = number_format($rate / 8000, 2, ',', '.');
    } else {
        $rate = FALSE;
        $client[7] = '--';
    }

    $client[3] = date ('Y-m-d H:i', strtotime($client[3]));
    $client[6] = date ('Y-m-d H:i', strtotime($client[6]));
    $client[4] = number_format($client[4] / 8000, 0, '', '.');
    $client[5] = number_format($client[5] / 8000, 0, '', '.');
    $client[2] = str_replace('::', '', $client[2]);
    $client[2] = str_replace('ffff:', '', $client[2]); 
    $client[2] = substr($client[2], 0, strlen($client[2])*0.6) . '***';
    $client[1] = '<a href="https://' . $client[1] . '">' . $client[1] . '</a>';
$i = 0;
?>
<tr>
<?php foreach ($client as $td) { ?>
<td align='<?php echo $tdalign[$i++] ?>'><?php echo $td?></td>
<?php } ?>
</tr>
<?php } ?>

</table>
