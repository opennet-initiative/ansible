#!/usr/bin/python

import sys
import os
import re

def extract_numstring_ugws(cn):
   retval = int(cn[:-7])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval
   
def extract_numstring_ugws_long(cn):
	retval = int(cn[2:-7])
	if not (1 <= retval <= 255):
		raise ValueError('Invalid cn %r.' % cn)
	return retval

netmask = '255.255.0.0'
targetipmask = '10.2.%d.%d'
client_cn = os.getenv('common_name')

if (re.match('[0-9][0-9]?[0-9]?\.ugw\.on', client_cn)):
	client_num = extract_numstring_ugws(client_cn)
	client_pre = 1
if (re.match('[12][\._-][0-9][0-9]?[0-9]?\.ugw\.on', client_cn)):
	client_num = extract_numstring_ugws_long(client_cn)
	client_pre = int(client_cn[0])


target_filename = sys.argv[1]

target_file = file(target_filename, 'w')
config_text = 'ifconfig-push %s %s\n' % ((targetipmask % (client_pre,client_num,)), netmask)
target_file.write(config_text)
target_file.close()
