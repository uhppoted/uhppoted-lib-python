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


class SendToProtocol(asyncio.Protocol):

    def __init__(self, request, dest, debug=False):
        self._transport = None
        self._request = request
        self._dest = dest
        self._debug = debug
        self._done = asyncio.get_event_loop().create_future()

    def connection_made(self, transport):
        self._transport = transport
        self._transport.sendto(self._request, self._dest)

    def datagram_received(self, packet, addr):
        if len(packet) == 64 and not self._done.done():
            if self._debug:
                net.dump(packet)
            self._done.set_result(packet)

    def connection_lost(self, exc):
        if exc is not None:
            self._done.set_exception(ConnectionResetError())

    async def run(self, timeout):
        try:
            return await asyncio.wait_for(self._done, timeout)
        except asyncio.TimeoutError:
            raise TimeoutError('UDP request timeout')
        except ConnectionResetError:
            raise ConnectionResetError('UDP connection reset')


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
        address from the constructor and then waits 'timeout' seconds for the replies from any reponding
        access controllers.

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

    async def send(self, request, dest_addr=None, timeout=2.5):
        '''
        Binds to the bind address from the constructor and then broadcasts a UDP request to the broadcast,
        and then waits 'timeout seconds for a reply from the destination access controllers.

            Parameters:
               request   (bytearray)  64 byte request packet.
               dest_addr (string)     Optional IPv4 address:port of the controller. Defaults to port 60000
                                      if dest_addr does not include a port.
               timeout   (float)      Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               Received response packet (if any) or None (for set-ip request).

            Raises:
               Error  For any socket related errors.
        '''
        self.dump(request)

        loop = asyncio.get_running_loop()

        if dest_addr is None:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: SendToProtocol(request, self._broadcast, self._debug),
                local_addr=self._bind,
                allow_broadcast=True)
        else:
            addr = net.resolve(f'{dest_addr}')
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: SendToProtocol(request, addr, self._debug),
                local_addr=self._bind,
                remote_addr=addr,
                allow_broadcast=True)

        # if request[1] == 0x96:
        #     return None

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
