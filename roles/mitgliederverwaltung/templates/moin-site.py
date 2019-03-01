# -*- coding: utf-8 -*-
# {{ ansible_managed }}

from MoinMoin.config import multiconfig
from farmconfig import FarmConfig

class Config(FarmConfig):
    sitename = u'Mitgliederverwaltung'
    interwikiname = u'mitgliederverwaltung'

    language_default = 'de'
    charset = 'utf-8'
    page_front_page = u"StartSeite"
    data_dir = '/var/lib/mitgliederverwaltung/data/'
    data_underlay_dir = '/var/lib/mitgliederverwaltung/underlay'
    navi_bar = [u'Mitglieder', u'AktuelleÄnderungen', u'SeiteFinden', u'HilfeInhalt']
    # enable temporarily for administrative actions
    #superuser = [u'foo.client.on']

    logo_string = u'<img src="/opennetlogo.png" height="90px"/>'

    # use authentication data provided by the SSL client certificate (requires "SSLOptions +StdEnvVars")
    from MoinMoin.auth.sslclientcert import SSLClientCertAuth
    auth = [SSLClientCertAuth(autocreate=True)]

    # XMLRPC is used remotely via helper scripts (e.g. "search for members")
    # enable xmlrpc
    actions_excluded = list(multiconfig.DefaultConfig.actions_excluded)
    actions_excluded.remove('xmlrpc')
    # allow read access via xmlrpc
    acl_rights_default = u"{{ mitgliederverwaltung_allowed_users|join(',') }}:read,write,delete All:read"
