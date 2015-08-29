# energenie/__init__.py


"""Energenie Radio Controlled Sockets GPIO module.

This module provides functions to control the Energenie 314 GPIO module
used to signal up to four radio controlled power sockets.
"""



import time



__version__ = "0.21"




# --- constants ---



# GPIO pin numbers for the 4 data bits, mode selection (OOK/FSK) and to enable
# and disable the modulator
#
# these pin numbers are Broadcom pin numbers and not the Raspberry Pi pin
# header numbers

_D0_PIN = 17
_D1_PIN = 22
_D2_PIN = 23
_D3_PIN = 27

_MODESEL_PIN = 24

_MODULATOR_PIN = 25


# the two options for the mode selection pin - OOK (On-Off Keying) and FSK
# (Frequency Shift Keying); the board actually only uses OOK, so FSK is
# provided just for completeness

_MODESEL_OOK = "0"
_MODESEL_FSK = "1"


_MODULATOR_OFF = "0"
_MODULATOR_ON = "1"


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


# delay to wait for the encoder to settle, after setting the data bits 

_SETTLE_DELAY = 0.1


# time to enable the modulator for to allow the code to be sent

_MODULATOR_DURATION = 0.25


# directory in sysfs for the GPIO

_GPIO_DIR = "/sys/class/gpio/"


# options for setting GPIO pin direction using _GPIOPin.set_direction()

_GPIO_DIRECTION_OUT = "out"
_GPIO_DIRECTION_IN = "in"


# used by GPIOPin._wait_available() to determine the interval between checks
# and maximum waiting time for an exported GPIO pin to become available

_GPIO_PERMISSION_INTERVAL = 0.02
_GPIO_PERMISSION_TIMEOUT = 0.8



# --- functions ---



class _GPIOPin:
    """Class to model a single GPIO pin.

    Methods should be use from within a 'with' block to open and close the
    resource (export and unexport using the sysfs interface).
    """


    def __init__(self, num):
        # the constructor just stores the pin number and path for directory
        # in sysfs for that pin

        self._num = num
        self._dir = _GPIO_DIR + "gpio%d/" % self._num


        # initialise the 'available' flag to false as we haven't checked
        # that yet (see _wait_available())

        self._available = False


    def __enter__(self):
        # through sysfs, export the pin to be controlled

        with open(_GPIO_DIR + "export", "w") as f:
            f.write(str(self._num))


    def __exit__(self, type, value, traceback):
        # we're finished with the pin so unexport it

        with open(_GPIO_DIR + "unexport", "w") as f:
            f.write(str(self._num))


    def _wait_available(self):
        # this method is called before doing any operation which requires
        # access to the pin's sysfs files - it attempt to open the 'value'
        # file for writing, retrying until it becomes available, aborting if
        # this takes too long
        #
        # the method remembers that the files have become available and will
        # return immediately, if this has already happened

        if self._available:
            return


        total_wait = 0

        while True:
            try:
                with open(self._dir + "value", "w"):
                    break

            except IOError:
                pass


            time.sleep(_GPIO_PERMISSION_INTERVAL)

            total_wait += _GPIO_PERMISSION_INTERVAL
            if total_wait > _GPIO_PERMISSION_TIMEOUT:
                raise IOError("timed out waiting for access to GPIO pin")


        self._available = True


    def set_direction(self, direction):
        """Set the pin communication direction."""

        self._wait_available()

        with open(self._dir + "direction", "w") as f:
            f.write(direction)


    def set_value(self, value):
        """Set the pin output value."""

        self._wait_available()

        with open(self._dir + "value", "w") as f:
            f.write(str(value))


def send_code(code):
    """Send a code to set the socket states.

    The supplied code is a 4-bit value with D0 as the least significant
    bit: '<D3><D2><D1><D0>'.  It will typically be one of the SOCK<n>_-
    {OFF|ON} or ALL_{OFF|ON} constants.
    """


    d0 = _GPIOPin(_D0_PIN)
    d1 = _GPIOPin(_D1_PIN)
    d2 = _GPIOPin(_D2_PIN)
    d3 = _GPIOPin(_D3_PIN)
    modesel = _GPIOPin(_MODESEL_PIN)
    modulator = _GPIOPin(_MODULATOR_PIN)


    # the 'with' block opens and closes the pins

    with d0, d1, d2, d3, modesel, modulator:
        # all the pins we use are used for output
        for pin in [d0, d1, d2, d3, modesel, modulator]:
            pin.set_direction(_GPIO_DIRECTION_OUT)

        # set the GPIO data pins according to the various bits in the supplied
        # code
        d0.set_value(1 if code & 0b0001 else 0)
        d1.set_value(1 if code & 0b0010 else 0)
        d2.set_value(1 if code & 0b0100 else 0)
        d3.set_value(1 if code & 0b1000 else 0)

        # use On-Off Keying (OOK)
        modesel.set_value(_MODESEL_OOK)

        # wait for the encoder to settle
        time.sleep(_SETTLE_DELAY)

        # switch the modulator on then off
        modulator.set_value(_MODULATOR_ON)
        time.sleep(_MODULATOR_DURATION)
        modulator.set_value(_MODULATOR_OFF)
