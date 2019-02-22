<?php

# Opennet specific configuration

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

?>
