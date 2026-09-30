<?php
# {{ ansible_managed }}

# Further documentation for configuration settings may be found at:
# https://www.mediawiki.org/wiki/Manual:Configuration_settings

# Protect against web entry
if ( !defined( 'MEDIAWIKI' ) ) {
	exit;
}

## Uncomment this to disable output compression
# $wgDisableOutputCompression = true;

$wgSitename = "{{ mediawiki_sitename }}";

## The URL base path to the directory containing the wiki;
## defaults for all runtime URL paths are based off of this.
## For more information on customizing the URLs
## (like /w/index.php/Page_title to /wiki/Page_title) please see:
## https://www.mediawiki.org/wiki/Manual:Short_URL
$wgScriptPath = ""; 
# only serve the articles via /wiki/ subpath
$wgArticlePath = "/wiki/$1";
# force standard path for system script so not "/wiki/$1" is used
$wgScript = "{$wgScriptPath}/index.php";
$wgLoadScript = "{$wgScriptPath}/load.php";

## The protocol and server name to use in fully-qualified URLs
$wgServer = "https://{{ mediawiki_hostname }}.opennet-initiative.de";

## The URL path to static resources (images, scripts, etc.)
$wgResourceBasePath = $wgScriptPath;

## The URL path to the logo.  Make sure you change this from the default,
## or else you'll overwrite your logo when you upgrade!
$wgLogo = "$wgResourceBasePath/images/{{ mediawiki_logo }}";

## UPO means: this is also a user preference option

$wgEnableEmail = {{ mediawiki_mail_enable }};
$wgEnableUserEmail = {{ mediawiki_mail_enable }}; # UPO

$wgEmergencyContact = "{{ mediawiki_mail_address }}";
$wgPasswordSender = "{{ mediawiki_mail_address }}";

$wgEnotifUserTalk = {{ mediawiki_mail_enable }}; # UPO
$wgEnotifWatchlist = {{ mediawiki_mail_enable }}; # UPO
$wgEmailAuthentication = true;

## Database settings
$wgDBtype = "mysql";
$wgDBserver = "localhost";
$wgDBname = "{{ mediawiki_database }}";
$wgDBuser = "{{ mediawiki_database }}";
#$wgDBpassword = "";  # see config_keys.php

# MariaDB specific settings
$wgDBprefix = "";

# MariaDB table options to use during installation or update
$wgDBTableOptions = "ENGINE=InnoDB, DEFAULT CHARSET=binary";

## Shared memory settings
$wgMainCacheType = CACHE_ACCEL;
$wgMemCachedServers = [];

## To enable image uploads, make sure the 'images' directory
## is writable, then set this to true:
$wgEnableUploads = true;
$wgUseImageMagick = true;
$wgImageMagickConvertCommand = "/usr/bin/convert";

# InstantCommons allows wiki to use images from https://commons.wikimedia.org
$wgUseInstantCommons = true;

## If you use ImageMagick (or any other shell command) on a
## Linux server, this will need to be set to the name of an
## available UTF-8 locale
$wgShellLocale = "de_DE.utf8";

# Site language code, should be one of the list in ./languages/data/Names.php
$wgLanguageCode = "de";

#$wgSecretKey = "";  # see config_keys.php

# Changing this will log out all existing sessions.
$wgAuthenticationTokenVersion = "1";

## For attaching licensing metadata to pages, and displaying an
## appropriate copyright notice / icon. GNU Free Documentation
## License and Creative Commons licenses are supported so far.
$wgRightsPage = ""; # Set to the title of a wiki page that describes your license/copyright
$wgRightsUrl = "https://creativecommons.org/licenses/by-nc-sa/4.0/";
$wgRightsText = "''Creative Commons'' „Namensnennung – nicht kommerziell – Weitergabe unter gleichen Bedingungen“";
$wgRightsIcon = "$wgResourceBasePath/resources/assets/licenses/cc-by-nc-sa.png";

# Path to the GNU diff3 utility. Used for conflict resolution.
$wgDiff3 = "/usr/bin/diff3";

# Requires that a user be registered before they can edit. 
$wgGroupPermissions['*']['edit'] = false;

# SPAM prevention: Prevent new user registrations except by sysops
# We (Opennet) need some protection against SPAM bots. In the old Wiki there was a modification with password hint. When we have this here also, then opening the registration is possible.
$wgGroupPermissions['*']['createaccount'] = false;

# Erzwingen von E-Mail Verfication
$wgEmailConfirmToEdit = true;

## Default skin: you can change the default skin. Use the internal symbolic
## names, ie 'vector', 'monobook':
$wgDefaultSkin = "vector-2022";

# Enabled skins.
# The following skins were automatically enabled:
#wfLoadSkin( 'MonoBook' );
wfLoadSkin( 'Vector' );
#wfLoadSkin( 'Timeless' );

# Enable extensions
wfLoadExtension( 'VisualEditor' ); 

# End of automatically generated settings.
# Add more configuration options below.

# Debian specific generated settings
# Use system mimetypes
$wgMimeTypeFile = '/etc/mime.types';

# Opennet specific generated settings
if ( is_file( "{{ mediawiki_path_conf }}/config_keys.php" ) ) {
  include "{{ mediawiki_path_conf }}/config_keys.php";
}

?>
