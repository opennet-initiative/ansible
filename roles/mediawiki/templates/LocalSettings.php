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
#$wgDBpassword = "";

# MySQL specific settings
$wgDBprefix = "";

# MySQL table options to use during installation or update
$wgDBTableOptions = "ENGINE=InnoDB, DEFAULT CHARSET=binary";

# Experimental charset support for MySQL 5.0.
$wgDBmysql5 = false;

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

## Set $wgCacheDirectory to a writable directory on the web server
## to make your wiki go slightly faster. The directory should not
## be publically accessible from the web.
#$wgCacheDirectory = "$IP/cache";

# Site language code, should be one of the list in ./languages/data/Names.php
$wgLanguageCode = "de";

#$wgSecretKey = "";

# Changing this will log out all existing sessions.
$wgAuthenticationTokenVersion = "1";

# Site upgrade key. Must be set to a string (default provided) to turn on the
# web installer while LocalSettings.php is in place
#$wgUpgradeKey = "";

## For attaching licensing metadata to pages, and displaying an
## appropriate copyright notice / icon. GNU Free Documentation
## License and Creative Commons licenses are supported so far.
$wgRightsPage = ""; # Set to the title of a wiki page that describes your license/copyright
$wgRightsUrl = "https://creativecommons.org/licenses/by-nc-sa/4.0/";
$wgRightsText = "''Creative Commons'' „Namensnennung – nicht kommerziell – Weitergabe unter gleichen Bedingungen“";
$wgRightsIcon = "$wgResourceBasePath/resources/assets/licenses/cc-by-nc-sa.png";

# Path to the GNU diff3 utility. Used for conflict resolution.
$wgDiff3 = "/usr/bin/diff3";

# The following permissions were set based on your choice in the installer
$wgGroupPermissions['*']['edit'] = false;

## Default skin: you can change the default skin. Use the internal symbolic
## names, ie 'vector', 'monobook':
$wgDefaultSkin = "vector";

# Enabled skins.
# The following skins were automatically enabled:
#wfLoadSkin( 'MonoBook' );
wfLoadSkin( 'Vector' );
#wfLoadSkin( 'Timeless' );

# End of automatically generated settings.
# Add more configuration options below.

# Debian specific generated settings
# Use system mimetypes
$wgMimeTypeFile = '/etc/mime.types';

# Opennet specific generated settings
if ( is_file( "{{ mediawiki_path_conf }}/config_keys.php" ) ) {
  include "{{ mediawiki_path_conf }}/config_keys.php";
}
if ( is_file( "{{ mediawiki_path_conf }}/config_core.php" ) ) {
  include "{{ mediawiki_path_conf }}/config_core.php";
}
if ( is_file( "{{ mediawiki_path_conf }}/config_skin.php" ) ) {
  include "{{ mediawiki_path_conf }}/config_skin.php";
}
if ( is_file( "{{ mediawiki_path_conf }}/config_extensions.php" ) ) {
  include "{{ mediawiki_path_conf }}/config_extensions.php";
}

?>
