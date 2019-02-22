<?php

# {{ ansible_managed }}
# Opennet specific configuration

##
## General Configuration
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
