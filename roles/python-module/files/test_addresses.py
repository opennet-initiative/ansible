#!/usr/bin/env python3

#
# Unit tests
#

from ipaddress import IPv4Network, IPv4Address, IPv6Network, IPv6Address
import unittest
from opennet.addresses import NodeInfo, parse_ipv4_and_net, parse_ipv6_and_net

class TestAddresses(unittest.TestCase):
    def test_parse_ipv4_and_net(self):
        self.assertEqual(parse_ipv4_and_net("10.1.0.0", "8"), IPv4Address("10.0.0.0"))
        self.assertEqual(parse_ipv4_and_net("10.1.2.0", "16"), IPv4Address("10.1.0.0"))
        self.assertEqual(parse_ipv4_and_net("10.1.2.3", "32"), IPv4Address("10.1.2.3"))
        self.assertEqual(parse_ipv4_and_net("192.168.3.0", "24"), IPv4Address("192.168.3.0"))

    def test_parse_ipv6_and_net(self):
        self.assertEqual(parse_ipv6_and_net("1111:2222:3333:4444::/64"), IPv6Address("1111:2222:3333:4444::"))
        self.assertEqual(parse_ipv6_and_net("1111:2222:3333:4444:5:6:7:8/64"), IPv6Address("1111:2222:3333:4444::"))
        self.assertEqual(parse_ipv6_and_net("1111:2222:3333::/64"), IPv6Address("1111:2222:3333::"))
        self.assertEqual(parse_ipv6_and_net("1111:2222:3333::999/64"), IPv6Address("1111:2222:3333::"))

    def test_NodeInfo(self):
        # live examples:
        #  $ cat /var/log/openvpn/opennet_users.status.log
        #     10.1.4.114,1.29.aps.on,139.30.241.206:45279,Mon Oct  3 22:10:42 2022
        #  $ iptables -t nat -L | less
        #     DNAT       tcp  --  anywhere             anywhere             tcp dpts:10280:10289 to:10.1.4.114
        self.assertEqual(str(NodeInfo("1.29.aps.on", IPv4Address("10.1.0.0"), IPv6Address("2001:db8::"))),
            "NodeInfo(ipv4_address='10.1.4.114', ipv6_address='2001:db8::1:1:1d:0', port_first=10280, port_last=10289)")
        self.assertEqual(str(NodeInfo("1.29.aps.on", parse_ipv4_and_net("10.1.2.0", "16"),  parse_ipv6_and_net("2001:db8::/64"))),
            "NodeInfo(ipv4_address='10.1.4.114', ipv6_address='2001:db8::1:1:1d:0', port_first=10280, port_last=10289)")
        
        # 10.1.19.170,2.235.aps.on,31.17.105.163:47823,Mon Oct  3 23:10:34 2022
        # DNAT       tcp  --  anywhere             anywhere             tcp dpts:17440:17449 to:10.1.19.170
        self.assertEqual(str(NodeInfo("2.235.aps.on", IPv4Address("10.1.0.0"), IPv6Address("2001:db8::"))),
            "NodeInfo(ipv4_address='10.1.19.170', ipv6_address='2001:db8::1:2:eb:0', port_first=17440, port_last=17449)")
        
        # 10.1.19.70,2.210.aps.on,62.214.244.79:43629,Mon Oct  3 23:10:31 2022
        # DNAT       tcp  --  anywhere             anywhere             tcp dpts:17190:17199 to:10.1.19.70
        self.assertEqual(str(NodeInfo("2.210.aps.on", IPv4Address("10.1.0.0"), IPv6Address("2001:db8::"))),
            "NodeInfo(ipv4_address='10.1.19.70', ipv6_address='2001:db8::1:2:d2:0', port_first=17190, port_last=17199)")
        
        # 10.1.18.62,2.144.aps.on,213.254.32.26:36666,Mon Oct  3 23:10:34 2022
        # DNAT       tcp  --  anywhere             anywhere             tcp dpts:16530:16539 to:10.1.18.62
        self.assertEqual(str(NodeInfo("2.144.aps.on", IPv4Address("10.1.0.0"), IPv6Address("2001:db8::"))),
            "NodeInfo(ipv4_address='10.1.18.62', ipv6_address='2001:db8::1:2:90:0', port_first=16530, port_last=16539)")
        
        # 10.1.6.190,1.176.aps.on,91.52.158.122:42354,Mon Oct  3 23:10:11 2022
        # DNAT       tcp  --  anywhere             anywhere             tcp dpts:11750:11759 to:10.1.6.190
        self.assertEqual(str(NodeInfo("1.176.aps.on", IPv4Address("10.1.0.0"), IPv6Address("2001:db8::"))),
            "NodeInfo(ipv4_address='10.1.6.190', ipv6_address='2001:db8::1:1:b0:0', port_first=11750, port_last=11759)")
        
        # 10.1.20.22,3.6.aps.on,62.214.245.132:39189,Mon Oct  3 23:10:35 2022
        # DNAT       udp  --  anywhere             anywhere             udp dpts:20250:20259 to:10.1.20.22
        self.assertEqual(str(NodeInfo("3.6.aps.on", IPv4Address("10.1.0.0"), IPv6Address("2001:db8::"))),
            "NodeInfo(ipv4_address='10.1.20.22', ipv6_address='2001:db8::1:3:6:0', port_first=20250, port_last=20259)")
        

if __name__ == "__main__":
    unittest.main()
