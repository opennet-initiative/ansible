<?php

# {{ ansible_managed }}

# Protect against web entry
if ( !defined( 'MEDIAWIKI' ) ) {
	exit;
}

# Opennet specific configuration

# File Upload
$wgFileExtensions[] = "pdf";

# Anti Spam Extension
wfLoadExtensions([ 'ConfirmEdit', 'ConfirmEdit/QuestyCaptcha' ]);
$wgCaptchaClass = 'QuestyCaptcha';
$arr = array (
  "<strong>Zur Spambek&auml;mpfung bitte hier den Vereinsnamen eintragen<br/> (ein Wort, Hinweis 'Opxxxet')</strong>" => "Opennet",
);
foreach ( $arr as $key => $value ) {
  $wgCaptchaQuestions[] = array( 'question' => $key, 'answer' => $value );
}

?>
