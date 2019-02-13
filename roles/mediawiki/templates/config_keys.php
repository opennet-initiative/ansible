<?php

# {{ ansible_managed }}
# This file is only created by Ansible but never been overwritten!
# Please insert correct data manually.

# Protect against web entry
if ( !defined( 'MEDIAWIKI' ) ) {
	exit;
}

# Please insert valid keys

$wgDBpassword = "{{ mediawiki_database }}";
$wgSecretKey = "";
$wgUpgradeKey = "";

?>
