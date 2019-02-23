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

?>
