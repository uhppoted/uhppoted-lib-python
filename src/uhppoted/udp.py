"""
UHPPOTE UDP communications wrapper.

Implements the functionality to send and receive 64 byte UDP packets to/from a UHPPOTE
access controller.
"""

import socket

from . import net


class UDP:
    """
    'sync' implementation of the UDP transport for the UHPPOTE request/response protocol.
    """

    def __init__(self, bind="0.0.0.0", broadcast="255.255.255.255:60000", listen="0.0.0.0:60001", debug=False):
        """
        Initialises a UDP communications wrapper with the bind address, broadcast address and listen address.

            Parameters:
               bind      (string)  The IPv4 address:port to which to bind when sending a request.
               broadcast (string)  The IPv4 address:port to which to send broadcast UDP messages.
               listen    (string)  The IPv4 address:port on which to listen for events from the
                                   access controllers.
               debug     (bool)    Dumps the sent and received packets to the console if enabled.

            Returns:
               Initialised UDP object.

            Raises:
               Exception  If any of the supplied IPv4 values cannot be translated to a valid IPv4
                          address:port combination.
        """
        self._bind = (bind, 0)
        self._broadcast = net.resolve(broadcast)
        self._listen = net.resolve(listen)
        self._debug = debug

    def broadcast(self, request, timeout=2.5):
        """
        Binds to the bind address from the constructor and then broadcasts a UDP request to the broadcast
        address from the constructor and then waits 'timeout' seconds for the replies from any reponding access
        controllers.

            Parameters:
               request  (bytearray)  64 byte request packet.
                timeout (float)      Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               List of received response packets (may be empty).

            Raises:
               Error  For any socket related errors.
        """
        self.dump(request)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        try:
            sock.bind(self._bind)

            # NTS: avoid broadcast-to-self
            _, src_port = sock.getsockname()
            _, dest_port = self._broadcast
            if src_port == dest_port:
                raise RuntimeError(f"invalid UDP bind address (port {src_port} reserved for broadcast)")

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, net.WRITE_TIMEOUT)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, net.READ_TIMEOUT)

            sock.sendto(request, self._broadcast)

            return _read_all(sock, timeout=timeout, debug=self._debug)
        finally:
            sock.close()

    def send(self, request, dest_addr=None, timeout=2.5):
        """
        Binds to the bind address from the constructor and then broadcasts a UDP request to the broadcast,
        and then waits 'timeout' seconds for a reply from the destination access controllers.

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

        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM | socket.SOCK_NONBLOCK)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        try:
            sock.bind(self._bind)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, net.WRITE_TIMEOUT)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, net.READ_TIMEOUT)

            if dest_addr is None:
                sock.sendto(request, self._broadcast)
            else:
                addr = net.resolve(f"{dest_addr}")
                sock.sendto(request, addr)

            if request[1] == 0x96:
                return None

            return _read(sock, timeout=timeout, debug=self._debug)
        finally:
            sock.close()

    def listen(self, on_event):
        """
        Binds to the listen address from the constructor and invokes the events handler for
        any received 64 byte UDP packets. Invalid'ish packets are silently discarded.

            Parameters:
               on_event  (function)  Handler function for received events, with a function signature
                                     f(packet).

            Returns:
               None.

            Raises:
               Error  For any socket related errors.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        try:
            sock.bind(self._listen)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, net.NO_TIMEOUT)

            while True:
                message = sock.recv(1024)
                if len(message) == 64:
                    self.dump(message)
                    on_event(message)
        finally:
            sock.close()

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


def _read_all(sock, timeout=2.5, debug=False):
    """
    Accumulates received 64 byte UDP packets, waiting up to 2.5 seconds for an incoming packet. Prints the
    packet to the console if debug is True.

        Parameters:
            sock    (socket) Initialised and open UDP socket.
            timeout (float)  Optional operation timeout (in seconds). Defaults to 2.5s.
            debug   (bool)   Enables dumping the received packet to the console.

        Returns:
            List of received 64 byte UDP packets (may be empty).
    """
    time_limit = net.timeout_to_seconds(timeout)

    sock.settimeout(time_limit)

    replies = []
    while True:
        try:
            reply = sock.recv(1024)
            if len(reply) == 64:
                replies.append(reply)
                if debug:
                    net.dump(reply)
        except socket.timeout:
            break

    return replies
