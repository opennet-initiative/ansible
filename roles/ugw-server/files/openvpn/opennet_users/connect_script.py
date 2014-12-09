#!/usr/bin/python
from connectcalc import *

target_filename = sys.argv[1]
client_cn = os.getenv('common_name')
if not client_cn:
   raise ValueError("Missing env-variable 'common_name'")

# ipv4 calc
ipbase, step, portbase, cn_address = get_targetvalues(client_cn);
targetip, ifconfig_arg_1 = calc_targetip(ipbase, cn_address, step);
targetport_begin, targetport_end = calc_targetports(cn_address, portbase);

# ipv6 calc
ipbase6, step6, cn_address6 = get_targetvalues6(client_cn);
targetip6 = calc_targetip6(ipbase6, cn_address6, step6);

# ipv4 portforwarding
os.system('sudo /sbin/iptables -t nat -A user_dnat -p tcp --dport %s:%s -j DNAT --to-destination %s' % \
			(targetport_begin, targetport_end, targetip))
os.system('sudo /sbin/iptables -t nat -A user_dnat -p udp --dport %s:%s -j DNAT --to-destination %s' % \
			(targetport_begin, targetport_end, targetip))

# push config to ovpn client
target_file = file(target_filename, 'w')
target_file.write('ifconfig-push %s %s\n' % (targetip, ifconfig_arg_1))
target_file.write('ifconfig-ipv6-push %s\n' % targetip6)
if client_cn == '10.mobile.on':
	target_file.write('iroute-ipv6 2a01:a700:4629:fe01::/64')
if client_cn == '195.aps.on':
	target_file.write('iroute-ipv6 2a01:a700:4629:fe02::/64')
if client_cn == '2.50.aps.on':
        target_file.write('iroute-ipv6 2a01:a700:4629:fe03::/64')
target_file.close()
