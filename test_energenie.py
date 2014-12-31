#!/usr/bin/env python3

# test_energenie.py (2014-12-31) - test the Energenie library


# if we're on Python 2.x, import the 3.x print() function

from __future__ import print_function


from energenie import *


# set the input() function to use raw_input() so we can use the former on
# Python 2.x; Python 3.x will fail because raw_input() does not exist, so we
# just skip that

try:
    input = raw_input

except NameError:
    pass


# test switch each of the sockets on and off

try:
    input("hit return key to send socket 1 ON code")
    print("sending code %s socket 1 on" % bin(SOCK1_ON))
    send_code(SOCK1_ON)

    input("hit return key to send socket 1 OFF code")
    print("sending code %s socket 1 off" % bin(SOCK1_OFF))
    send_code(SOCK1_OFF)

    input("hit return key to send socket 2 ON code")
    print("sending code %s socket 2 on" % bin(SOCK2_ON))
    send_code(SOCK2_ON)

    input("hit return key to send socket 2 OFF code")
    print("sending code %s socket 2 off" % bin(SOCK2_OFF))
    send_code(SOCK2_OFF)

    input("hit return key to send ALL ON code")
    print("sending code %s all on" % bin(ALL_ON))
    send_code(ALL_ON)

    input("hit return key to send ALL OFF code")
    print("sending code %s all off" % bin(ALL_OFF))
    send_code(ALL_OFF)

except KeyboardInterrupt:
    # catch the interrupt signal and ignore it
    pass


# clean up the GPIOs

cleanup()
