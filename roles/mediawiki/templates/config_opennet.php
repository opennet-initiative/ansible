<?php

# {{ ansible_managed }}

# Protect against web entry
if ( !defined( 'MEDIAWIKI' ) ) {
	exit;
}

# Opennet specific configuration

## 
## Load Extensions
##

# wikimedia extensions
{% for item in mediawiki_extensions_wikimedia %}
wfLoadExtension( '{{ item }}' );
{% endfor %}

# debian extensions
{% for item in mediawiki_extensions_debian %}
wfLoadExtension( '{{ item }}' );
{% endfor %}

# TODO: some REL1_27 extension does not support wfLoadExtension yet
require_once ( '{{ mediawiki_path_lib}}/extensions/ContactPage/ContactPage.php' );
require_once ( '{{ mediawiki_path_lib}}/extensions/TitleKey/TitleKey.php' );
require_once ( '{{ mediawiki_path_lib}}/extensions/NoTitle/NoTitle.php' );
require_once ( '{{ mediawiki_path_lib}}/extensions/UserFunctions/UserFunctions.php' );

# TODO: third party extension, other git
wfLoadExtension( 'EmbedVideo' );

## 
## Configure Extensions
## 

# Config ConfirmEdit Extension
wfLoadExtensions([ 'ConfirmEdit', 'ConfirmEdit/QuestyCaptcha' ]);
$wgCaptchaClass = 'QuestyCaptcha';
$arr = array (
  "<strong>Zur Spambek&auml;mpfung bitte hier den Vereinsnamen eintragen<br/> (ein Wort, Hinweis 'Opxxxet')</strong>" => "Opennet",
);
foreach ( $arr as $key => $value ) {
  $wgCaptchaQuestions[] = array( 'question' => $key, 'answer' => $value );
}
$wgEmailConfirmToEdit = true;

# Config MobileFrontend Extension
$wgMFAutodetectMobileView = true;

# Config User Functions (depends Parser Functions)
# needed for MediaWiki:Sidebar customization
$wgEnableSidebarCache = false;
$wgUFAllowedNamespaces[NS_MAIN] = true;

# Contact Page
# a valid WikiUser is required, please create before
# TODO: OpennetContactForm scripting?
$wgContactConfig['default'] = array(
  'RecipientUser' => 'Mathias', 
  'SenderName' => $wgSitename . ' Kontaktformular', 
  'SenderEmail' => null, // Defaults to $wgPasswordSender
  'RequireDetails' => true, 
  'IncludeIP' => false, 
  'AdditionalFields' => array(
    'Text' => array(
      'label-message' => 'emailmessage',
      'type' => 'textarea',
      'rows' => 15,
      'required' => true, 
    ),
  ),
  'DisplayFormat' => 'table',  
  'RLModules' => array(),  
  'RLStyleModules' => array()
);
$wgCaptchaTriggers['contactpage'] = true;

##
## Other Configuration
## 

# File Upload
{% for item in mediawiki_upload_filetypes %}
$wgFileExtensions[] = "{{ item }}";
{% endfor %}

# Vector Skin
#$wgVectorUseSimpleSearch = true;
$wgVectorUseIconWatch = true;
$wgVectorResponsive = true;

# Favicon
$wgFavicon = "$wgResourceBasePath/images/favicon.ico";

# Short URLs
# based on https://shorturls.redwerks.org/
## The URL base path to the directory containing the wiki;
## defaults for all runtime URL paths are based off of this.
## For more information on customizing the URLs please see:
## http://www.mediawiki.org/wiki/Manual:Short_URL
$wgScriptExtension = ".php";
$wgArticlePath = "/$1";
$wgUsePathInfo = true;

# Allow Pagetitle Overrive
# used for Main_Page
$wgRestrictDisplayTitle = false; 

# Hide Page History
function efAddSkinStyles(OutputPage &$out, Skin &$skin) {
  if(!$skin->getUser()->isLoggedIn()) {
    $out->addInlineStyle('#ca-view { display:none; }');
    $out->addInlineStyle('#ca-viewsource { display:none; }');
    $out->addInlineStyle('#ca-history { display:none; }');
    $out->addInlineStyle('#mw-mf-last-modified { display:none; }');
    $out->addInlineStyle('#footer-info { display: none; }');
    $out->addInlineStyle('#p-tb { display: none; }');
  }
  return true;
}
$wgHooks['BeforePageDisplay'][] = 'efAddSkinStyles';

# Html / Embedded iFrames, needed? 
#$wgRawHtml = true;
#$wgAllowExternalImages = true;

?>
