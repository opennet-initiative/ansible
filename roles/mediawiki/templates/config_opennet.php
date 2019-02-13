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

# File Upload
{% for item in mediawiki_upload_filetypes %}
$wgFileExtensions[] = "{{ item }}";
{% endfor %}
?>
