"""
UHPPOTE UDP asynchronous communications wrapper.

Implements the functionality to send and receive 64 byte UDP packets to/from a UHPPOTE
access controller.
"""

import asyncio
import socket

from . import net


class BroadcastProtocol(asyncio.Protocol):
    """
    asyncio protocol implementation for UDP broadcast single request/multiple response.
    """

    def __init__(self, request, dest, debug=False):
        self._transport = None
        self._request = request
        self._dest = dest
        self._replies = []
        self._debug = debug
        self._done = asyncio.get_event_loop().create_future()

    def connection_made(self, transport):
        self._transport = transport

        # NTS: avoid broadcast-to-self
        if sock := transport.get_extra_info("socket"):
            _, src_port = sock.getsockname()
            _, dest_port = self._dest
            if src_port == dest_port:
                self._done.set_exception(
                    RuntimeError(f"invalid UDP bind address (port {src_port} reserved for broadcast)")
                )
                self._transport.close()
                return

        self._transport.sendto(self._request, self._dest)

    def datagram_received(self, packet, _addr):
        """
        Collects valid'ish received packets into the 'replies' list that is returned on timeout.
        """
        if len(packet) == 64:
            self._replies.append(packet)
            if self._debug:
                net.dump(packet)

    def connection_lost(self, exc):
        pass

    async def run(self, timeout):
        """
        Returns the collected replies after a delay.
        """
        # await asyncio.sleep(timeout)
        # return self._replies

        try:
            await asyncio.wait_for(self._done, timeout)
        except asyncio.TimeoutError:
            return self._replies

        if self._done.exception():
            raise self._done.exception()

        return self._replies


class SendProtocol(asyncio.Protocol):
    """
    asycnio protocol implementation for UDP connected socket single request/response.
    """

    def __init__(self, request, dest, debug=False):
        self._transport = None
        self._request = request
        self._dest = dest
        self._debug = debug
        self._done = asyncio.get_event_loop().create_future()

    def connection_made(self, transport):
        self._transport = transport
        self._transport.sendto(self._request, self._dest)
        if self._request[1] == 0x96:
            self._done.set_result(None)

    def datagram_received(self, packet, _addr):
        """
        Signals 'done' on receiving a valid'ish packet.
        """
        if len(packet) == 64 and not self._done.done():
            if self._debug:
                net.dump(packet)
            self._done.set_result(packet)

    def connection_lost(self, exc):
        if exc is not None:
            self._done.set_exception(ConnectionResetError())

    async def run(self, timeout):
        """
        Waits for 'done' or timeout, returning the received packet on 'done'.
        """
        try:
            return await asyncio.wait_for(self._done, timeout)
        except asyncio.TimeoutError as exc:
            raise TimeoutError("UDP request timeout") from exc
        except ConnectionResetError as exc:
            raise ConnectionResetError("UDP connection reset") from exc


class EventProtocol(asyncio.DatagramProtocol):
    """
    asycnio protocol implementation for UDP event receive.
    """

    def __init__(self, on_event, debug=False):
        self._transport = None
        self._on_event = on_event
        self._debug = debug

    def connection_made(self, transport):
        self._transport = transport

    def datagram_received(self, data, addr):
        if len(data) == 64:
            if self._debug:
                net.dump(data)
            self._on_event(data)

    def error_received(self, exc):
        pass

    def connection_lost(self, exc):
        pass


class UDPAsync:
    """
    async implementation of the UDP transport for the UHPPOTE request/response protocol.
    """

    def __init__(self, bind="0.0.0.0", broadcast="255.255.255.255:60000", listen="0.0.0.0:60001", debug=False):
        """
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
        """
        self._bind = (bind, 0)
        self._broadcast = net.resolve(broadcast)
        self._listen = net.resolve(listen)
        self._debug = debug

    async def broadcast(self, request, timeout=2.5):
        """
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
        """
        self.dump(request)

        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: BroadcastProtocol(request, self._broadcast, self._debug),
            local_addr=self._bind,
            allow_broadcast=True,
        )

        try:
            return await protocol.run(timeout)
        finally:
            transport.close()

    async def send(self, request, dest_addr=None, timeout=2.5):
        """
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
        """
        self.dump(request)

        loop = asyncio.get_running_loop()

        if dest_addr is None:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: SendProtocol(request, self._broadcast, self._debug), local_addr=self._bind, allow_broadcast=True
            )
        else:
            addr = net.resolve(f"{dest_addr}")
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: SendProtocol(request, addr, self._debug),
                local_addr=self._bind,
                remote_addr=addr,
                allow_broadcast=True,
            )

        try:
            return await protocol.run(timeout)
        finally:
            transport.close()

    async def listen(self, on_event):
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
        loop = asyncio.get_running_loop()

        transport, _ = await loop.create_datagram_endpoint(
            lambda: EventProtocol(on_event, self._debug),
            local_addr=self._listen,
            family=socket.AF_INET,
        )

        try:
            await asyncio.sleep(float("inf"))
        except asyncio.CancelledError:
            pass
        finally:
            transport.close()

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
