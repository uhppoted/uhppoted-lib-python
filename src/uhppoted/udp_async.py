'''
UHPPOTE UDP asynchronous communications wrapper.

Implements the functionality to send and receive 64 byte UDP packets to/from a UHPPOTE 
access controller.
'''

import asyncio
import socket
import struct
import re
import time
import ipaddress

from . import net


class BroadcastProtocol(asyncio.Protocol):

    def __init__(self, request, dest, debug=False):
        self._transport = None
        self._request = request
        self._dest = dest
        self._replies = []
        self._debug = debug
        self._done = asyncio.get_event_loop().create_future()

    def connection_made(self, transport):
        self._transport = transport
        self._transport.sendto(self._request, self._dest)

    def datagram_received(self, packet, addr):
        if len(packet) == 64:
            self._replies.append(packet)
            if self._debug:
                net.dump(packet)

    def connection_lost(self, exc):
        pass

    async def run(self, timeout):
        await asyncio.sleep(timeout)
        return self._replies

    # async def run(self, timeout):
    #     try:
    #         await asyncio.wait_for(self._done, timeout)
    #     except asyncio.TimeoutError:
    #         self.timeout()
    #
    #     return self._replies


class UDPAsync:

    def __init__(self, bind='0.0.0.0', broadcast='255.255.255.255:60000', listen="0.0.0.0:60001", debug=False):
        '''
        Initialises an asynchronous UDP communications wrapper with the bind address, broadcast address
        and listen address.

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
        '''
        self._bind = (bind, 0)
        self._broadcast = net.resolve(broadcast)
        self._listen = net.resolve(listen)
        self._debug = debug

    async def broadcast(self, request, timeout=2.5):
        '''
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
        '''
        self.dump(request)

        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: BroadcastProtocol(request, self._broadcast, self._debug),
            local_addr=self._bind,
            allow_broadcast=True)

        try:
            return await protocol.run(timeout)
        finally:
            transport.close()

    def dump(self, packet):
        '''
        Prints a packet to the console as a formatted hexadecimal string if debug was enabled in the
        constructor.

            Parameters:
               packet  (bytearray)  64 byte UDP packet.

            Returns:
               None.
        '''
        if self._debug:
            net.dump(packet)
