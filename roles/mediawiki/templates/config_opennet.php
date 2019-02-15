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
require_once "{{ mediawiki_path_lib}}/extensions/ContactPage/ContactPage.php";
require_once "{{ mediawiki_path_lib}}/extensions/TitleKey/TitleKey.php";

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

# Config MobileFrontend Extension
$wgMFAutodetectMobileView = true;

##
## Other Configuration
## 

# Contact Page
$wgContactUser = 'OpennetContactForm';
$wgContactSender = $wgPasswordSender;
$wgContactSenderName = $wgSitename . ' Kontaktformular';
$wgCaptchaTriggers['contactpage'] = true;
$wgContactRequireAll = true;

# File Upload
{% for item in mediawiki_upload_filetypes %}
$wgFileExtensions[] = "{{ item }}";
{% endfor %}

# Vector Skin
$wgVectorUseSimpleSearch = true;
$wgVectorUseIconWatch = true;
$wgVectorResponsive = true;

# Favicon
$wgFavicon = "$wgResourceBasePath/images/favicon.ico";

?>
