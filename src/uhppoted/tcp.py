"""
UHPPOTE TCP communications wrapper.

Implements the functionality to send and receive 64 byte TCP packets to/from a UHPPOTE
access controller.
"""

import socket
import struct
import re
import time
import ipaddress

from . import net


class TCP:

    def __init__(self, bind="0.0.0.0", debug=False):
        """
        Initialises a TCP communications wrapper with the bind address.

            Parameters:
               bind      (string)  The IPv4 address:port to which to bind when sending a request.
               debug     (bool)    Dumps the sent and received packets to the console if enabled.

            Returns:
               Initialised TCP object.

            Raises:
               Exception  If any of the supplied IPv4 values cannot be translated to a valid IPv4
                          address:port combination.
        """
        self._bind = (bind, 0)
        self._debug = debug

    def send(self, request, dest_addr, timeout=2.5):
        """
        Binds to the bind address from the constructor and connects to the access controller after which it sends
        the request and waits 'timeout' seconds for the reply (if any).

            Parameters:
               request   (bytearray)  64 byte request packet.
               dest_addr (string)     Optional IPv4 address:port of the controller. Defaults to port 60000
                                      if dest_addr does not include a port.
               timeout   (float)      Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               Received response packet (if any) or None (for set-ip request).

            Raises:
               Error  For any socket related errors.
        """
        self.dump(request)

        addr = net.resolve(f"{dest_addr}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, net.WRITE_TIMEOUT)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, net.READ_TIMEOUT)

            if not is_INADDR_ANY(self._bind):
                sock.bind(self._bind)

            sock.connect(addr)
            sock.sendall(request)

            if request[1] == 0x96:
                return None
            else:
                return _read(sock, timeout=timeout, debug=self._debug)

    def dump(self, packet):
        """
        Prints a packet to the console as a formatted hexadecimal string if debug was enabled in the
        constructor.

            Parameters:
               packet  (bytearray)  64 byte UDP packet.

            Returns:
               None.
        """
        if self._debug:
            net.dump(packet)


def is_INADDR_ANY(addr):
    if addr == None:
        return True

    if f"{addr}" == "":
        return True

    if addr == (("0.0.0.0", 0)):
        return True

    return False


# TODO convert to asyncio
def _read(sock, timeout=2.5, debug=False):
    """
    Waits 2.5 seconds for a single 64 byte packet to be received on the socket. Prints the packet to the console
    if debug is True.

        Parameters:
            sock    (socket)  Initialised and open UDP socket.
            timeout (float)   Optional operation timeout (in seconds). Defaults to 2.5s.
            debug   (bool)    Enables dumping the received packet to the console.

        Returns:
            Received 64 byte UDP packet (or None).
    """
    time_limit = net.timeout_to_seconds(timeout)

    sock.settimeout(time_limit)

    while True:
        reply = sock.recv(1024)
        if len(reply) == 64:
            if debug:
                net.dump(reply)
            return reply

    return None
