# -*- coding: utf-8 -*-

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
    superuser = [u'lars']

    logo_string = u'<img src="https://opennet-initiative.de/w/images/opennetlogo.png" height="90px"/>'

    # use authentication data provided by the SSL client certificate (requires "SSLOptions +StdEnvVars")
    from MoinMoin.auth.sslclientcert import SSLClientCertAuth
    auth = [SSLClientCertAuth(autocreate=True)]

    #enable xmlrpc
    actions_excluded = multiconfig.DefaultConfig.actions_excluded[:]
    #actions_excluded = list(multiconfig.DefaultConfig.actions_excluded)
    actions_excluded.remove('xmlrpc')
    #allow user access via xmlrpc
    acl_rights_default = u"martingarbe.client.on:read,write,delete All:read"
