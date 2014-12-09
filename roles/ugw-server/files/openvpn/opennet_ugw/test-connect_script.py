#!/usr/bin/python

import sys
import os

netmask = '255.255.0.0'


target_filename = sys.argv[1]

client_cn = os.getenv('common_name')
if "2-"==(client_cn[:2]):
        targetipmask = '10.2.2.%d'      
        client_cn = (client_cn[2:])
        assert client_cn.endswith('ugw.on')
        client_numstring =  client_cn[:-7]
else:
        targetipmask = '10.2.1.%d'
        assert client_cn.endswith('ugw.on')
        client_numstring =  client_cn[:-7]

assert client_numstring.isdigit()
client_num = int(client_numstring)
   
target_file = file(target_filename, 'w')
config_text = 'ifconfig-push %s %s\n' % ((targetipmask % (client_num,)), netmask)
target_file.write(config_text)
target_file.close()
