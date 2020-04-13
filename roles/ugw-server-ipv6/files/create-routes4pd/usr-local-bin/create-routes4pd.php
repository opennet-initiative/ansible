<?php
/*
 * This script creates for each DHCPv6-Prefix-Delegation a routing entry.
 * It is assumed that for each ia-pd an ia-na if available. Therefore each
 * node getting a prefix delegation should also get a normal address via DHCPv6.
 *
 */

$leases_file = "/var/lib/dhcp/dhcpd6.leases";
$leasefile = file($leases_file);

foreach($leasefile as $line) {
	//parts of script taken from https://redmine.pfsense.org/issues/2347

        //echo "$line"; //debug
        if(preg_match("/^(ia-[np][ad])[ ]+\"(.*?)\"/i ", $line, $duidmatch)) {
                $type = $duidmatch[1];
                $duid = $duidmatch[2];
                continue;
        }

        /* is it active? otherwise just discard */
        if(preg_match("/binding state active/i", $line, $activematch)) {
                $active = true;
                continue;
        }

        if(preg_match("/iaaddr[ ]+([0-9a-f:]+)[ ]+/i", $line, $addressmatch)) {
                $ia_na = $addressmatch[1];
                continue;
        }

        if(preg_match("/iaprefix[ ]+([0-9a-f:\/]+)[ ]+/i", $line, $prefixmatch)) {
                $ia_pd = $prefixmatch[1];
                continue;
        }

        /* closing bracket */
        if(preg_match("/^}/i ", $line)) {
                switch($type) {
                        case "ia-na":
                                if(isset($ia_na)) {
					$duid_arr[$duid][$type] = $ia_na;
				}
                                break;
                        case "ia-pd":
                                if(isset($ia_pd)) {
					$duid_arr[$duid][$type] = $ia_pd;
				}
                                break;
                }
                unset($type);
                unset($duid);
                unset($active);
                unset($ia_na);
                unset($ia_pd);
                continue;
        }
}

//create new array with all ia-pd which also have a ia-na
foreach($duid_arr as $duid => $value) {
	if(count($value)>1) {
		$duid_arr_filtered[$duid]=$value;
	}
		
}

//print_r($duid_arr);  //debug
//print_r($duid_arr_filtered); //debug

//read routing table
//
//  example cmd and output
//  root@gai:~# ip -6 route show dev tap-users-v6 to root 2a0a:4580:1010:1000::/52
//  2a0a:4580:1010:1cc0::/60 via 2a0a:4580:1010:2::f64a metric 1024 pref medium
//  2a0a:4580:1010:1d80::/60 via 2a0a:4580:1010:2::90ba metric 1024 pref medium
//
$output_rt = shell_exec('ip -6 route show dev tap-users-v6 to root 2a0a:4580:1010:1000::/52');
//print($output_rt); //debug

//get date/time for debug logging entries
$t = new DateTime();
$ts = $t->format('Y-m-d\TH:i:s'); 
echo "Run at ".$ts."\n";

//check that all networks mentioned in DHCPv6-PD log have a routing table entry
foreach($duid_arr_filtered as $duid => $value) {
	/*
	example $duid: '\001\000\000\000\000\003\000\001\'
	example $value: => Array
        		(
			[ia-na] => 2a0a:4580:1010:2::90ba
			[ia-pd] => 2a0a:4580:1010:1d80::/60
			)
	*/

	//is destination net in routing table?
	$ret = strpos($output_rt, $value['ia-pd']." via ");
	if($ret === false) {
		echo "Adding new route: ip -6 route add ".$value['ia-pd']." dev tap-users-v6 via ".$value['ia-na']."\n";
		$output_radd = shell_exec("ip -6 route add ".$value['ia-pd']." dev tap-users-v6 via ".$value['ia-na']);
		if (strlen($output_radd) > 0) {
			echo "Error while adding route: Error message: ".$output_radd."\n";
		}
	} else {
		//is 'via' the same
		$ret = strpos($output_rt, $value['ia-pd']." via ".$value['ia-na']." ");
		if ($ret === false) {
			//Delete old route and add new one because routing partner has changed.
			//Maybe network was newly assigned to other user.
			echo "Delete old route because router (via) changed: ip -6 route del ".$value['ia-pd']." dev tap-users-v6 \n";
			$output_rdel = shell_exec("ip -6 route del ".$value['ia-pd']." dev tap-users-v6");
			if (strlen($output_rdel) > 0) {
				echo "Error while deleting route. Error message: ".$output_rdel."\n";
			}
			echo "Adding new route: ip -6 route add ".$value['ia-pd']." dev tap-users-v6 via ".$value['ia-na']."\n";
			$output_radd = shell_exec("ip -6 route add ".$value['ia-pd']." dev tap-users-v6 via ".$value['ia-na']);
			if (strlen($output_radd) > 0) {
				echo "Error while adding route: Error message: ".$output_radd."\n";
			}		
		} else {
			//for debug
			//echo "No new routing table entry needed for ".$value['ia-pd']." via ".$value['ia-na']."\n";
		}
	}
}

?>
