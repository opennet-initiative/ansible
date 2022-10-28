#!/usr/bin/env python3
import argparse
import requests
import urllib.parse

#
# Opennet Lifxctl Script
# Jack Steele, created 2021/12/10 - https://github.com/JackSteele/lifxctl
# Mathias Mahnke, modified 2022/10/27
# Opennet Admin Group <admin@opennet-initiative.de>
#

parser = argparse.ArgumentParser(description="LIFX cloud light controller")

parser.add_argument("--token", dest="token", type=str, help="Provide LIFX HTTP API token")
parser.add_argument("--debug", action="store_true", help="")
sel_group = parser.add_mutually_exclusive_group()

sel_group.add_argument("-r", "--room",
                    help="Room to control")
sel_group.add_argument("-rid", "--roomid",
                    help="Room ID to control")
sel_group.add_argument("-l", "--light",
                    help="Light to control")
sel_group.add_argument("-lid", "--lightid",
                    help="Light ID to control")
parser.add_argument(
    "--listraw", help="List all lights and groups affiliated with token", action="store_true")
power_group = parser.add_mutually_exclusive_group()
power_group.add_argument("-1", "--on", help="Turn light(s) off", action="store_true")
power_group.add_argument("-0", "--off", help="Turn light(s) off", action="store_true")
power_group.add_argument("-t", "--toggle", help="Toggle light(s)", action="store_true")
args = parser.parse_args()

token = f"{args.token}"

headers = {
    "Authorization": "Bearer %s" % token,
}

def send_state(sel, power):
    payload = {
        "power": power,
    }
    response = requests.put(
        f'https://api.lifx.com/v1/lights/{sel}/state', data=payload, headers=headers)
    if args.debug:
        print(response.text)

def send_toggle(sel):
    response = requests.post(
        f'https://api.lifx.com/v1/lights/{sel}/toggle', headers=headers)
    if args.debug:
        print(response.text)

if args.listraw:
    response = requests.get(
        'https://api.lifx.com/v1/lights/all', headers=headers)
    print(response.text)

sel = "all"

if args.room:
    sel = f"group:{args.room}"
elif args.roomid:
    sel = f"group_id:{args.roomid}"
elif args.light:
    sel = f""

sel = urllib.parse.quote(sel)

if args.debug:
    print(sel)

if args.on:
    send_state(sel, "on")
elif args.off:
    send_state(sel, "off")
elif args.toggle:
    send_toggle(sel)
else:
    send_toggle(sel)
