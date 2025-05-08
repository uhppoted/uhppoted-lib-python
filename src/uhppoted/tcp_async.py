'''
UHPPOTE TCP asynchronous communications wrapper.

Implements the functionality to send and receive 64 byte TCP packets to/from a UHPPOTE 
access controller.
'''

import socket
import struct
import re
import time
import ipaddress

from . import net


class TCPAsync:

    def __init__(self, bind='0.0.0.0', debug=False):
        '''
        Initialises an asynchronous TCP communications wrapper with the bind address.

            Parameters:
               bind      (string)  The IPv4 address:port to which to bind when sending a request.
               debug     (bool)    Dumps the sent and received packets to the console if enabled.

            Returns:
               Initialised TCP object.

            Raises:
               Exception  If any of the supplied IPv4 values cannot be translated to a valid IPv4 
                          address:port combination.
        '''
        self._bind = (bind, 0)
        self._debug = debug
