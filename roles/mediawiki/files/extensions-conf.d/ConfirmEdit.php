<?php

# Opennet specific configuration

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

?>
