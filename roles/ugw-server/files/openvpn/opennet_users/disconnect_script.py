#!/usr/bin/python
from connectcalc import *

client_cn = os.getenv('common_name')
if not client_cn:
   raise ValueError("Missing env-variable 'common_name'")

ipbase, step, portbase, cn_address = get_targetvalues(client_cn);
targetip, ifconfig_arg_1 = calc_targetip(ipbase, cn_address, step);
targetport_begin, targetport_end = calc_targetports(cn_address, portbase);

os.system('sudo /sbin/iptables -t nat -D user_dnat -p tcp --dport %s:%s -j DNAT --to-destination %s' % \
			(targetport_begin, targetport_end, targetip))
os.system('sudo /sbin/iptables -t nat -D user_dnat -p udp --dport %s:%s -j DNAT --to-destination %s' % \
			(targetport_begin, targetport_end, targetip))
