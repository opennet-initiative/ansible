#!/usr/bin/python
#changes by janc for the 192.168.2.x net
import sys
import os
import socket
import struct

#config

def extract_numstring_aps(cn):
   retval = int(cn[:-7])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval

#2-xxx.aps.on
def extract_numstring_2_aps(cn):
   cn = (cn[2:])
   retval = int(cn[:-7])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval


   
def extract_numstring_mobile(cn):
   retval = int(cn[:-10])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval

def extract_numstring_admin(cn):
   retval = int(cn[:-9])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval


client_ranges = {
   '.admin.on': (167840770, 4, extract_numstring_admin),	#10.1.12.0
   '.aps.on': (167838718, 4, extract_numstring_aps),		#10.1.4.0
   '.mobile.on': (167839742, 4, extract_numstring_mobile),	#10.1.8.0
   '2-xxx.aps.on': (167841790, 4, extract_numstring_2_aps),	#10.1.16.0
   }
#167841790 for 16 use ipcalc to turn the ip in binary and then convert to dec and sub 2
# /config

def iplongtostring(longip):
   return socket.inet_ntop(socket.AF_INET,struct.pack('>L',longip))

target_filename = sys.argv[1]
client_cn = os.getenv('common_name')
if not client_cn:
   raise ValueError("Missing env-variable 'common_name'")

for cn_schema in client_ranges:
   if (client_cn.endswith(cn_schema)):
#some extra work to decide between the diffrent aps.on ranges 
      if "2-"==(client_cn[:2]):
        (ipbase, step, ns_extractor) = client_ranges["2-xxx.aps.on"]
      else:
        (ipbase, step, ns_extractor) = client_ranges[cn_schema]
      targetip_long = ipbase + ns_extractor(client_cn)*step
      targetip = iplongtostring(targetip_long)
      ifconfig_arg_1 = iplongtostring(targetip_long-1)
      break

else:
     raise ValueError('Invalid CN %r.' % client_cn)


target_file = file(target_filename, 'w')
target_file.write('ifconfig-push %s %s\n' % (targetip, ifconfig_arg_1))
target_file.close()
