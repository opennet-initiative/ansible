#!/usr/bin/python

import sys
import os
import socket
import struct
import re
import ipaddr

#config

def extract_numstring_aps(cn):
   retval = int(cn[:-7])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval
   
def extract_numstring_aps_long(cn):
	retval = int(cn[2:-7])
	if not (1 <= retval <= 255):
		raise ValueError('Invalid cn %r.' % cn)
	return retval

def extract_numstring_mobile(cn):
   retval = int(cn[:-10])
   if not (1 <= retval <= 255):
      raise ValueError('Invalid cn %r.' % cn)
   return retval

client_ranges = {
   '[0-9][0-9]?[0-9]?\.aps\.on': (167838718, 4, 10000, extract_numstring_aps),		#10.1.4.0
   '1[\._-][0-9][0-9]?[0-9]?\.aps\.on': (167838718, 4, 10000, extract_numstring_aps_long),		#10.1.4.0
   '2[\._-][0-9][0-9]?[0-9]?\.aps\.on': (167841790, 4, 15100, extract_numstring_aps_long),		#10.1.16.0
   '[0-9][0-9]?[0-9]?\.mobile\.on': (167839742, 4, 12550, extract_numstring_mobile),	#10.1.8.0
   }

# ipv6 prefix erina 2a01:a700:4629:fe00::/64
client_ranges6 = {
   '[0-9][0-9]?[0-9]?\.aps\.on': (55836155303943527445734511195122040832, 65536, extract_numstring_aps),     	     	#<prefix>:1:1::
   '1[\._-][0-9][0-9]?[0-9]?\.aps\.on': (55836155303943527445734511195122040832, 65536, extract_numstring_aps_long),	#<prefix>:1:1::
   '2[\._-][0-9][0-9]?[0-9]?\.aps\.on': (55836155303943527445734511199417008128, 65536, extract_numstring_aps_long),	#<prefix>:1:2::
   '[0-9][0-9]?[0-9]?\.mobile\.on': (55836155303943527445734792670098751488, 65536, extract_numstring_mobile),		#<prefix>:2:1::
   }

# /config

# ipv4
def iplongtostring(longip):
   return socket.inet_ntop(socket.AF_INET,struct.pack('>L',longip))

# ipv6
def iplongtostring6(longip):
   return ipaddr.IPAddress(longip)

# ipv4
def get_targetvalues(client_cn):
        ipbase = 0;
        for cn_schema in client_ranges:
                if (re.match(cn_schema, client_cn)):
                        (ipbase, step, portbase, ns_extractor) = client_ranges[cn_schema]
                        cn_address = ns_extractor(client_cn);
                        break
        if not ipbase:
                raise ValueError('Invalid CN %r.' % client_cn)
        return (ipbase, step, portbase, cn_address);

# ipv6
def get_targetvalues6(client_cn):
        ipbase = 0;
        for cn_schema in client_ranges6:
                if (re.match(cn_schema, client_cn)):
                        (ipbase, step, ns_extractor) = client_ranges6[cn_schema]
                        cn_address = ns_extractor(client_cn);
                        break
        if not ipbase:
                raise ValueError('Invalid CN %r.' % client_cn)
        return (ipbase, step, cn_address);

# ipv4
def calc_targetip(ipbase, cn_address, step):
	targetip_long = ipbase + cn_address*step;
	targetip =  iplongtostring(targetip_long);
	ifconfig_arg_1 = iplongtostring(targetip_long-1);
	return (targetip, ifconfig_arg_1);
	
# ipv6
def calc_targetip6(ipbase, cn_address, step):
        targetip_long = ipbase + cn_address*step;
        targetip =  iplongtostring6(targetip_long);
        return (targetip);

# ipv4 (not needed for ipv6, no nat)
def calc_targetports(cn_address, portbase):
	targetport_begin = portbase + (cn_address-1)*10;
	targetport_end = targetport_begin+9;
	return (targetport_begin, targetport_end);
