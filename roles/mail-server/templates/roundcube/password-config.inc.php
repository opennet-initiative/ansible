<?php
/**
 * Roundcube Password Plugin Config
 * # {{ ansible_managed }}
 */

$config['password_driver'] = 'sql';

// Connect to vimbadmin DB (using same credentials as vimbadmin)
$config['password_db_dsn'] = 'mysql://{{ mailserver_vmail_db_user }}:{{ mailserver_vmail_db_pass }}@localhost/{{ mailserver_vmail_db }}';

// Update password in mailbox table
$config['password_query'] = 'UPDATE mailbox SET password = %P, modified = NOW() WHERE username = LOWER(%u) AND active = 1';

// Hashing algorithm matching Dovecot BLF-CRYPT (bcrypt)
$config['password_algorithm'] = 'blowfish-crypt';
$config['password_algorithm_prefix'] = '';

// Require current password confirmation and log changes
$config['password_confirm_current'] = true;
$config['password_log'] = true;
