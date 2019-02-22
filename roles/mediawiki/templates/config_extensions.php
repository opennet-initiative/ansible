<?php

# {{ ansible_managed }}
# Opennet specific configuration

## 
## Load Extensions
##

# wikimedia extensions
{% for item in mediawiki_extensions_wikimedia %}
wfLoadExtension( '{{ item }}' );
{% endfor %}

# wikimedia extensions old
# TODO: remove if all extensions moved to wfLoadExtension
{% for item in mediawiki_extensions_wikimedia_old %}
require_once ( '{{ mediawiki_path_lib}}/extensions/{{ item }}/{{ item }}.php' );
{% endfor %}

# debian extensions
{% for item in mediawiki_extensions_debian %}
wfLoadExtension( '{{ item }}' );
{% endfor %}

## 
## Configure Extensions
## 

# wikimedia extensions
{% for item in mediawiki_extensions_wikimedia %}
if ( is_file( "{{ mediawiki_path_conf }}/extensions-conf.d/{{ item }}.php" ) ) {
  include "{{ mediawiki_path_conf }}/extensions-conf.d/{{ item }}.php";
}
{% endfor %}

# wikimedia extensions old
# TODO: remove if all extensions moved to wfLoadExtension
{% for item in mediawiki_extensions_wikimedia_old %}
if ( is_file( "{{ mediawiki_path_conf }}/extensions-conf.d/{{ item }}.php" ) ) {
  include "{{ mediawiki_path_conf }}/extensions-conf.d/{{ item }}.php";
}
{% endfor %}

# debian extensions
{% for item in mediawiki_extensions_debian %}
if ( is_file( "{{ mediawiki_path_conf }}/extensions-conf.d/{{ item }}.php" ) ) {
  include "{{ mediawiki_path_conf }}/extensions-conf.d/{{ item }}.php";
}
{% endfor %}

##
## Manual Configs
## 

# TODO: third party extension, other git
wfLoadExtension( 'EmbedVideo' );

?>
