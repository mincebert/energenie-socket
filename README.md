ENERGENIE 314 SOCKET CONTROL PYTHON MODULE
==========================================

This a Python 3.x/2.x module for controlling the Energenie 314 GPIO card
for the Raspberry Pi.  The card can switch Energenie mains sockets on and
off via a short range radio signal.

The code was originally based on the Python code supplied with the
Energenie equipment but has since been adapted to use the sysfs interface
so it can run without superuser permissions and operate a as a reusable
module in other code.

Included are two utilities to demonstrate the module:

* test_energnie.py - cycles through turning sockets on and off as a demo
* energenie.py - accepts command line options to choose a socket and action

The module and code have been tested under Python 3.x/2.x and on Raspberry
Pi modules B, 2B and 3B.
