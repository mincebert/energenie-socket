# energenie/__init__.py


"""Energenie Radio Controlled Sockets GPIO module.

This module provides functions to control the Energenie 314 GPIO module
used to signal up to four radio controlled power sockets.
"""



import RPi.GPIO as GPIO

import time



__version__ = "0.1"




# --- constants ---



# GPIO pin numbers for the 4 data bits used to send the socket control codes

D0_PIN = 11
D1_PIN = 15
D2_PIN = 16
D3_PIN = 13


# GPIO mode selection pin to choose signalling method

MODESEL_PIN = 18


# GPIO signalling pin used to turn the transmitting modulator on and off

SIGNAL_PIN = 22


# codes to send to switch the various sockets off and on, in the form of a
# binary value '0b<D3><D2><D1><D0>', corresponding to the data pins above
#
# note that each of the bits in this value do NOT directly correspond to each
# of the sockets

ALL_OFF = 0b0011
SOCK1_OFF = 0b0111
SOCK2_OFF = 0b0110
SOCK3_OFF = 0b0101
SOCK4_OFF = 0b0100

ALL_ON = 0b1011
SOCK1_ON = 0b1111
SOCK2_ON = 0b1110
SOCK3_ON = 0b1101
SOCK4_ON = 0b1100


# the two options for the mode selection pin - OOK (On-Off Keying) and FSK
# (Frequency Shift Keying); the board actually only uses OOK, so FSK is
# provided just for completeness

MODESEL_OOK = False
MODESEL_FSK = True


# delay to wait for the encoder to settle, after setting the data bits 

SETTLE_DELAY = 0.1


# time to enable the modulator for to allow the code to be sent

SIGNAL_DELAY = 0.25



# --- functions ---



def set_code(code):
    """Sets a code in the encoder, ready to be sent.

    The supplied code is a 4-bit value with D0 as the least significant
    bit: '<D3><D2><D1><D0>'.
    """


    # set each of the pins according to the status of the bits in the supplied
    # code
    GPIO.output(D0_PIN, code & 0b0001)
    GPIO.output(D1_PIN, code & 0b0010)
    GPIO.output(D2_PIN, code & 0b0100)
    GPIO.output(D3_PIN, code & 0b1000)

    # wait for the encoder to settle
    time.sleep(SETTLE_DELAY)



def signal_code(code):
    """Set the specified code and signal the modulator.

    This function calls set_code() to set the supplied code and then
    switches on the modulator to send the code to the sockets.
    """


    set_code(code)

    GPIO.output(SIGNAL_PIN, True)
    time.sleep(SIGNAL_DELAY)
    GPIO.output(SIGNAL_PIN, False)



def cleanup():
    """Clean up after using the module.

    This function should be called when finished with the module to clean
    up the GPIO module.
    """


    GPIO.cleanup()



# --- init ---



# set the GPIO pin numbering mode
GPIO.setmode(GPIO.BOARD)

# set the pins we're going to use on the GPIO connector to output mode
for _pin in [D0_PIN, D1_PIN, D2_PIN, D3_PIN, MODESEL_PIN, SIGNAL_PIN]:
    GPIO.setup(_pin, GPIO.OUT)

# disable the modulator
GPIO.output(SIGNAL_PIN, False)

# set the modulator to OOK (On-Off Keying) signalling mode
GPIO.output(MODESEL_PIN, MODESEL_OOK)

# initialise the encoder to all zeroes
set_code(0b0000)
