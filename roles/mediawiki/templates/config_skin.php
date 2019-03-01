<?php

# {{ ansible_managed }}
# Opennet specific configuration

##
## Skin Configuration
## 

# Vector Skin
$wgVectorUseIconWatch = false;
$wgVectorResponsive = true;

# Allow Pagetitle Overrive, used for Main_Page
$wgRestrictDisplayTitle = false; 

# Use combined Register and Login link
$wgUseCombinedLoginLink = true;

# Hide Page History
function efAddSkinStyles(OutputPage &$out, Skin &$skin) {
  if(!$skin->getUser()->isLoggedIn()) {
    $out->addInlineStyle('#ca-view { display:none; }');
    $out->addInlineStyle('#ca-talk { display:none; }');
    $out->addInlineStyle('#ca-viewsource { display:none; }');
    $out->addInlineStyle('#ca-history { display:none; }');
    $out->addInlineStyle('#mw-mf-last-modified { display:none; }');
    $out->addInlineStyle('#footer-info { display: none; }');
    $out->addInlineStyle('#p-tb { display: none; }');
  }
  return true;
}
$wgHooks['BeforePageDisplay'][] = 'efAddSkinStyles';

?>
