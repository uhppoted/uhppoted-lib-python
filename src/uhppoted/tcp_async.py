'''
UHPPOTE TCP asynchronous communications wrapper.

Implements the functionality to send and receive 64 byte TCP packets to/from a UHPPOTE 
access controller.
'''

import asyncio
import socket
import struct
import re
import time
import ipaddress

from . import net


class SendProtocol(asyncio.Protocol):

    def __init__(self, request, debug=False):
        self._transport = None
        self._request = request
        self._debug = debug
        self._done = asyncio.get_event_loop().create_future()
        self._buffer = bytearray()

    def connection_made(self, transport):
        self._transport = transport
        self._transport.write(self._request)
        if self._request[1] == 0x96:
            self._done.set_result(None)

    def data_received(self, data):
        self._buffer.extend(data)
        if len(self._buffer) >= 64 and not self._done.done():
            packet = bytes(self._buffer[:64])
            if self._debug:
                net.dump(packet)
            self._done.set_result(packet)

    def eof_received(self):
        if not self._done.done():
            self._done.set_exception(EOFError())

    def connection_lost(self, exception):
        if exception is not None and not self._done.done():
            self._done.set_exception(ConnectionResetError())
        elif not self._done.done():
            self._done.set_exception(EOFError())

    async def run(self, timeout):
        try:
            return await asyncio.wait_for(self._done, timeout)
        except asyncio.TimeoutError:
            raise TimeoutError('TCP request timeout')
        except ConnectionResetError:
            raise ConnectionResetError('TCP connection reset')
        except EOFError:
            raise EOFError('TCP connection closed')


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

    async def send(self, request, dest_addr, timeout=2.5):
        '''
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
        '''
        self.dump(request)

        (host, port) = net.resolve(f'{dest_addr}')
        loop = asyncio.get_running_loop()

        if is_INADDR_ANY(self._bind):
            transport, protocol = await loop.create_connection(lambda: SendProtocol(request, self._debug), host, port)
        else:
            transport, protocol = await loop.create_connection(lambda: SendProtocol(request, self._debug),
                                                               host,
                                                               port,
                                                               local_addr=self._bind)

        # FIXME sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            return await protocol.run(timeout)
        finally:
            transport.close()

    def dump(self, packet):
        '''
        Prints a packet to the console as a formatted hexadecimal string if debug was enabled in the
        constructor.

            Parameters:
               packet  (bytearray)  64 byte TCP packet.

            Returns:
               None.
        '''
        if self._debug:
            net.dump(packet)


def is_INADDR_ANY(addr):
    if addr == None:
        return True

    if f'{addr}' == '':
        return True

    if addr == (('0.0.0.0', 0)):
        return True

    return False
