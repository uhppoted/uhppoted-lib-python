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

    async def set_ip(self, controller, address, netmask, gateway, timeout=2.5):
        '''
        Sets the controller IPv4 address, netmask and gateway address.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               address    (IPv4Address)  Controller IPv4 address.
               netmask    (IPv4Address)  Controller IPv4 subnet mask.
               gateway    (IPv4Address)  Controller IPv4 gateway address.
               timeout    (float)        Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               True  For (probably) internal reasons the access controller does not respond to this command.

            Raises:
               Exception  If the request failed for any reason.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_ip_request(id, address, netmask, gateway)
        reply = await self._send(request, addr, timeout, protocol)

        return True

    async def get_time(self, controller, timeout=2.5):
        '''
        Retrieves the access controller current date/time.

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
               GetTimeResponse  Controller current date/time.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_time_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_time_response(reply)

        return None

    async def set_time(self, controller, datetime, timeout=2.5):
        '''
        Sets the access controller current date/time.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               datetime   (dateime)  Date/time to set.
               timeout    (float)    Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetTimeResponse  Controller current date/time.

            Raises:
               Exception  If the datetime format cannot be encoded or the response from the 
                          access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_time_request(id, datetime)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_time_response(reply)

        return None

    async def get_status(self, controller, timeout=2.5):
        '''
        Retrieves the current status of an access controller.

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
               GetStatusResponse  Current controller status.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_status_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_status_response(reply)

        return None

    async def get_listener(self, controller, timeout=2.5):
        '''
        Retrieves the configured event listener address:port from an access controller.

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
               GetListenerResponse  Current controller event listener UDP address and port.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_listener_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_listener_response(reply)

        return None

    async def set_listener(self, controller, address, port, interval=0, timeout=2.5):
        '''
        Sets an access controller event listener IPv4 address and port.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               address    (IPv4Address)  IPv4 address of event listener.
               port       (uint16)       UDP port of event listener.
               interval   (uint8)        Auto-send interval (seconds). Defaults t0 0 (disabled).
               timeout    (float)        Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetListenerResponse  Success/fail response from controller.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_listener_request(id, address, port, interval)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_listener_response(reply)

        return None

    async def get_door_control(self, controller, door, timeout=2.5):
        '''
        Gets the door delay and control mode for an access controller door.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               door       (uint8)   Door [1..4]
               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetDoorControlResponse  Door delay and control mode.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_door_control_request(id, door)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_door_control_response(reply)

        return None

    async def set_door_control(self, controller, door, mode, delay, timeout=2.5):
        '''
        Sets the door delay and control mode for an access controller door.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               door       (uint8)   Door [1..4]
               mode       (uint8)   Control mode (1: normally open, 2: normally closed, 3: controlled)
               delay      (uint8)   Door unlock duration (seconds)
               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetDoorControlResponse  Door delay and control mode.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_door_control_request(id, door, mode, delay)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_door_control_response(reply)

        return None

    async def open_door(self, controller, door, timeout=2.5):
        '''
        Remotely opens a door controlled by an access controller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               door       (uint8)   Door [1..4]
               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               OpenDoorResponse  Door open success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.open_door_request(id, door)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.open_door_response(reply)

        return None

    async def get_cards(self, controller, timeout=2.5):
        '''
        Retrieves the number of cards stored in the access controller.

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
               GetCardsResponse  Number of cards stored locally in controller.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_cards_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_cards_response(reply)

        return None

    async def get_card(self, controller, card_number, timeout=2.5):
        '''
        Retrieves the card access record for a card number from the access controller.
            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields).
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults
                                             to 'udp'.

               card_number (uint32)  Access card number.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetCardResponse  Card information associated with the card number.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_card_request(id, card_number)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_card_response(reply)

        return None

    async def get_card_by_index(self, controller, card_index, timeout=2.5):
        '''
        Retrieves the card access record for a card record from the access controller.
            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               index       (uint32)  Controller card list record number.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetCardByIndexResponse  Card information associated with the card number.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_card_by_index_request(id, card_index)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_card_by_index_response(reply)

        return None

    async def put_card(self,
                       controller,
                       card_number,
                       start_date,
                       end_date,
                       door_1,
                       door_2,
                       door_3,
                       door_4,
                       pin,
                       timeout=2.5):
        '''
        Adds (or updates) a card record stored on the access controller.
            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               card_number (uint32)  Access card number.
               start_date  (date)    Card 'valid from' date (YYYYMMDD).
               end_date    (date)    Card 'valid until' date (YYYYMMDD).
               door_1      (uint8)   Card access permissions for door 1 (0: none, 1: all, 2-254: time profile ID)
               door_2      (uint8)   Card access permissions for door 2 (0: none, 1: all, 2-254: time profile ID)
               door_3      (uint8)   Card access permissions for door 3 (0: none, 1: all, 2-254: time profile ID)
               door_4      (uint8)   Card access permissions for door 4 (0: none, 1: all, 2-254: time profile ID)
               pin         (uint24)  Card access keypad PIN code (0 for none)
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               PutCardResponse  Card record add/update success/fail.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.put_card_request(id, card_number, start_date, end_date, door_1, door_2, door_3, door_4, pin)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.put_card_response(reply)

        return None

    async def delete_card(self, controller, card_number, timeout=2.5):
        '''
        Deletes the card record from the access controller.
            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               card_number (uint32)  Access card number to delete.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               DeleteCardResponse  Card record delete success/fail.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.delete_card_request(id, card_number)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.delete_card_response(reply)

        return None

    async def delete_all_cards(self, controller, timeout=2.5):
        '''
        Deletes all card records stored on the access controller.
            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               DeleteAllCardsResponse  Clear card records success/fail.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.delete_cards_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.delete_all_cards_response(reply)

        return None

    async def get_event(self, controller, event_index, timeout=2.5):
        '''
        Retrieves a stored event from the access controller.
            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               event_index (uint32)  Index of event in controller list.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetEventResponse  Event information.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_event_request(id, event_index)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_event_response(reply)

        return None

    async def get_event_index(self, controller, timeout=2.5):
        '''
        Retrieves the 'last downloaded event' index from the controller. The downloaded event index
        is a single utility register on the controller that is managed by an application (not by the
        controller).

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetEventIndexResponse  Current value of downloaded event index.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_event_index_request(id)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_event_index_response(reply)

        return None

    async def set_event_index(self, controller, event_index, timeout=2.5):
        '''
        Sets the 'last downloaded event' index on the controller. The downloaded event index is a 
        single utility register on the controller that is managed by an application (not by the
        controller).

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               event_index (uitn32)  Event index to which to set the 'downloaded event' index.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetEventIndexResponse  Set event index success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_event_index_request(id, event_index)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_event_index_response(reply)

        return None

    async def record_special_events(self, controller, enable, timeout=2.5):
        '''
        Enables or disables door open and close and pushbutton press events.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               enable      (bool)    Includes door open and close and pushbutton events in the
                                     events stored and broadcast by the controller.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               RecordSpecialEventsResponse  Record special events success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.record_special_events_request(id, enable)
        reply = await self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.record_special_events_response(reply)

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
        if protocol == 'tcp' and dest_addr != None:
            return await self._tcp.send(request, dest_addr, timeout)
        else:
            return await self._udp.send(request, dest_addr=dest_addr, timeout=timeout)
