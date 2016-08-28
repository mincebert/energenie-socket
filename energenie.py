#!/usr/bin/env python3

# energenie.py (2016-08-27) - utility to control Energnie radio sockets



# if we're on Python 2.x, import the 3.x print() function

from __future__ import print_function


from energenie import *

import argparse



__version__ = "0.11 (2016-08-28)"



# parse the command line arguments (and offer help)

parser = argparse.ArgumentParser()

parser.add_argument(
    "-d", "--debug",
    action="store_true",
    help="display code sent to GPIO")

parser.add_argument(
    "socket", choices=["1", "2", "3", "4", "all"],
    help="socket number to switch or 'all'")

parser.add_argument(
    "state", choices=["off", "on"],
    help="new state for socket")

parser.add_argument(
    "-v", "--version",
    action="version", version="%(prog)s " + __version__)

args = parser.parse_args()


# select the required code and send the signal to the socket

code = SOCK[args.socket][args.state]

if args.debug:
   print("Switching socket %s to %s = code 0x%x" %
             (args.socket, args.state, code))

send_code(SOCK[args.socket][args.state])
