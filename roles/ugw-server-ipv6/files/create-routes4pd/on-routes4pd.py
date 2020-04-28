#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script manages routes for DHCPv6 prefix delegated networks.

In the first step we look at the lease file of DHCPv6 server.
Then we check that all routes are available for all prefix delegated networks.

It is assumed that for each ia-pd an ia-na if available. Therefore each
node getting a prefix delegation should also get a normal address via DHCPv6.
"""

import sys

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 5):
    print("This script requires Python version 3.5") # needed for subprocess.run()
    sys.exit(1)

import re
import argparse
import logging
import pprint
import subprocess

lease_file_name = "/var/lib/dhcp/dhcpd6.leases"
#lease_file_name = "dhcpd6.leases" #for debugging

net_interface = "tap-users-v6"

# init dhcpv6 lease dictionary
# structure: dhcp_lease_dict = { duid : [ { ia-na : STRING } , { ia-pd : STRING } ] }
# structure: dhcp_lease_dict =
#   { duid : {
#       ia-na : STRING,
#       ia-pd : STRING
#    } }
dhcp_lease_dict = {}

logger = logging.getLogger('on_routes4pd')

#
# read DHCPv6 server lease file and find active PD leases
#
def get_leases(duid_dict):
    # open lease file as short as possible
    with open(lease_file_name) as f:
        f_lines = f.readlines()

    # search 'ia-np' or 'ia-ad'
    po_type_duid = re.compile("^(ia-[np][ad])[ ]+\"(.*?)\" ") # precompile pattern object
    # ia-pd marked as active?
    po_active = re.compile("binding state active")
    # address of device which got PD network
    po_addr = re.compile("iaaddr[ ]+([0-9a-f:]+)[ ]+")
    # prefix delegated network
    po_net = re.compile("iaprefix[ ]+([0-9a-f:\/]+)[ ]+")
    # closing bracket
    po_close_bracket = re.compile("^}")

    # init
    type = ""
    duid = ""
    active = False
    ia_na = ""
    ia_pd = ""

    for l in f_lines:
        line = str(l.rstrip())
        logger.debug(line)

        # search 'ia-np' or 'ia-ad'
        m = po_type_duid.search(line)
        if m:
            type = m.group(1)
            duid = m.group(2)
            logger.debug("--" + type + " --" + duid)
            continue

        m = po_active.search(line)
        if m:
            active = True
            logger.debug("-- is active")
            continue

        m = po_addr.search(line)
        if m:
            ia_na = m.group(1)
            logger.debug("-- ia_na: " + ia_na)
            continue

        m = po_net.search(line)
        if m:
            ia_pd = m.group(1)
            logger.debug("- ia_pd: " + ia_pd)
            continue

        m = po_close_bracket.search(line)
        if m:
            if (type == "ia-na" and len(ia_na) > 0) or (type == "ia-pd" and len(ia_pd) > 0):
                if active:
                    if duid not in duid_dict.keys():
                        duid_dict[duid] = {}
                    if type == "ia-na":
                        duid_dict[duid][type] = ia_na
                    else:
                        duid_dict[duid][type] = ia_pd
                    logger.debug("-- set dict values")
                else:
                    # is expired therefore delete any existing entry
                    if duid in duid_dict.keys() and type in duid_dict[duid].keys():
                        del duid_dict[duid][type]
                        logger.debug("-- delete expired " + type)
                        if len(duid_dict[duid]) > 0:
                            # delete dict with duid because it is empty
                            del duid_dict[duid]
            else:
                logger.debug("-- nothing found")
            # new initialization for next block
            type = ""
            duid = ""
            active = False
            ia_na = ""
            ia_pd = ""
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create routes for DHCPv6 Prefix Delegation networks")
    parser.add_argument("-l", "--logfile", help="write logs to given file")
    parser.add_argument("-v", "--verbose", type=int, choices=[1,2],
                        help="print verbose output ( 1 - routing table changes, 2 - debug)")
    args = parser.parse_args()

    if args.verbose:
        if args.verbose == 2:
            logger.setLevel(logging.DEBUG)
        elif args.verbose == 1:
            logger.setLevel(logging.INFO)
    if args.logfile:
        lh = logging.FileHandler(args.logfile)
    else:
        lh = logging.StreamHandler(stream = sys.stdout)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    lh.setFormatter(formatter)
    logger.addHandler(lh)

    #logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
    #                    datefmt='%m/%d/%Y %I:%M:%S %p')

    get_leases(dhcp_lease_dict)

    #make sure that every duid has one ia-na and ia-pd
    keys = list(dhcp_lease_dict) # get shallow copy of keys else error in for loop
    for k in keys:
        if len(dhcp_lease_dict[k]) <= 1:
            del dhcp_lease_dict[k]

    logger.debug(pprint.pformat(dhcp_lease_dict))

    # read routing table
    #
    #  example cmd and output
    #  root@gai:~# ip -6 route show dev tap-users-v6 to root 2a0a:4580:1010:1000::/52
    #  2a0a:4580:1010:1cc0::/60 via 2a0a:4580:1010:2::f64a metric 1024 pref medium
    #  2a0a:4580:1010:1d80::/60 via 2a0a:4580:1010:2::90ba metric 1024 pref medium
    #
    process = subprocess.run(['ip', '-6','route','show','dev',net_interface,'to','root','2a0a:4580:1010:1000::/52'],
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             universal_newlines=True)
    process
    if process.returncode != 0:
        logger.error(process.stderr)
        # we have problems fetching routing table therefore abort
        exit()
    else:
        rt = process.stdout
        logger.debug("-- " + rt)
        if len(rt) == 0:
            logger.info("Routing table has no prefix delegated networks")
            exit()

    # check that all networks mentioned in DHCPv6-PD log have a routing table entry
    for duid in dhcp_lease_dict.keys():
        val = dhcp_lease_dict[duid]
        '''
        example $duid: '\001\000\000\000\000\003\000\001\'
	    example $value: => Array
        		(
		    	[ia-na] => 2a0a:4580:1010:2::90ba
			    [ia-pd] => 2a0a:4580:1010:1d80::/60
			    )
	    '''

        # is destination net in routing table?
        str = val['ia-pd']+" via "
        if str not in rt:
            logger.info("Adding new route: ip -6 route add " + val['ia-pd'] + " dev tap-users-v6 via " + val['ia-na'])
            process = subprocess.run(['ip','-6','route','add',val['ia-pd'],'dev',net_interface,'via',val['ia-na']],
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE,
                                        universal_newlines = True)
            process
            if process.returncode != 0:
                logger.error(process.stderr)
        else:
            # is 'via' the same
            str = val['ia-pd'] + " via " + val['ia-na'] + " "
            if str not in rt:
                # Delete old route and add new one because next hop IP has changed.
                # Maybe network was newly assigned to other user.
                logger.info("Delete old route because router (via) changed: ip -6 route del "+val['ia-pd']+" dev tap-users-v6")
                process = subprocess.run(['ip','-6','route','del',val['ia-pd'],'dev',net_interface],
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE,
                                    universal_newlines = True)
                if process.returncode != 0:
                    logger.error(process.stderr)

                logger.info("Adding new route: ip -6 route add "+val['ia-pd']+" dev tap-users-v6 via "+val['ia-na'])
                process = subprocess.run(['ip','-6','route','add',val['ia-pd'],'dev',net_interface,'via',val['ia-na']],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         universal_newlines=True)
                if process.returncode != 0:
                    logger.error(process.stderr)
            else:
                logger.debug("No new routing table entry needed for "+val['ia-pd']+" via "+val['ia-na'])
