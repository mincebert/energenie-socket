#!/usr/bin/env python3

from energenie import *

# We will just loop round switching the units on and off
try:
    input('hit return key to send socket 1 ON code')
    # Set K0-K3
    print("sending code 1111 socket 1 on")
    signal_code(SOCK1_ON)

    input('hit return key to send socket 1 OFF code')
    # Set K0-K3
    print("sending code 0111 Socket 1 off")
    signal_code(SOCK1_OFF)

    input('hit return key to send socket 2 ON code')
    # Set K0-K3
    print("sending code 1110 socket 2 on")
    signal_code(SOCK2_ON)

    input('hit return key to send socket 2 OFF code')
    # Set K0-K3
    print("sending code 0110 socket 2 off")
    signal_code(SOCK2_OFF)

    input('hit return key to send ALL ON code')
    # Set K0-K3
    print("sending code 1011 ALL on")
    signal_code(ALL_ON)

    input('hit return key to send ALL OFF code')
    # Set K0-K3
    print("sending code 0011 All off")
    signal_code(ALL_OFF)

except KeyboardInterrupt:
    pass

# Clean up the GPIOs for next time
#except KeyboardInterrupt:
cleanup()
