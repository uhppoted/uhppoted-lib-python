'''
Implements an async Python wrapper around the UHPPOTE TCP/IP access controller API.
'''

from . import decode
from . import encode
from . import tcp_async as tcp
from . import udp_async as udp
from .net import disambiguate


class UhppoteAsync:

    def __init__(self, bind='0.0.0.0', broadcast='255.255.255.255:60000', listen="0.0.0.0:60001", debug=False):
        '''
        Initialises a UhppoteAsync object with the bind address, broadcast address and listen address.

            Parameters:
               bind      (string)  The IPv4 address to which to bind when sending a request.
               broadcast (string)  The IPv4 address:port to which to send broadcast UDP messages.
               listen    (string)  The IPv4 address:port on which to listen for events from the
                                   access controllers.
               debug     (bool)    Enables verbose debugging information.

            Returns:
               Initialised Uhppote object.

            Raises:
               ValueError  If any of the supplied IPv4 values cannot be translated to a valid IPv4 
                           address:port combination.
        '''
        self._udp = udp.UDPAsync(bind, broadcast, listen, debug)
        self._tcp = tcp.TCPAsync(bind, debug)

    async def get_all_controllers(self, timeout=2.5):
        '''
        Retrieves a list of all controllers accessible on the local LAN segment.

            Parameters:
              timeout (float)  Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               []GetControllerResponse  List of get_controller_responses from access controllers 
                                       on the local LAN segment.

            Raises:
               Exception  If any of the responses from the access controllers cannot be decoded.
        '''
        request = encode.get_controller_request(0)
        replies = await self._udp.broadcast(request, timeout=timeout)

        list = []
        for reply in replies:
            list.append(decode.get_controller_response(reply))

        return list

    async def get_controller(self, controller, timeout=2.5):
        '''
        Retrieves the controller information for an access controller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetControllerResponse  Response from access controller to the get-controller request.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_controller_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_controller_response(reply)

        return None

    async def _send(self, request, dest_addr, timeout, protocol):
        '''
        Internal HAL to use either TCP or UDP to send a request to a controller and return the response.

            Parameters:
               dest_addr (string)  Controller IPv4 addess:port. Defaults to broadcast address and port 60000.
               timeout   (float)   Operation timeout (in seconds). Defaults to 2.5s.
               protocol  (string)  'udp' or 'tcp'. Defaults to 'udp'.

            Returns:
               Received response packet (if any) or None (for set-ip request).

            Raises:
               Exception  If request could not be sent or the access controller failed to respond.
        '''
        # if protocol == 'tcp' and dest_addr != None:
        #     return self._tcp.send(request, dest_addr, timeout)
        # else:
        #     return self._udp.send(request, dest_addr=dest_addr, timeout=timeout)

        return await self._udp.send(request, dest_addr=dest_addr, timeout=timeout)
