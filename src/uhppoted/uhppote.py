'''
Implements a Python wrapper around the UHPPOTE TCP/IP access controller API.
'''

from . import decode
from . import encode
from . import tcp
from . import udp
from .net import disambiguate


class Uhppote:

    def __init__(self, bind='0.0.0.0', broadcast='255.255.255.255:60000', listen="0.0.0.0:60001", debug=False):
        '''
        Initialises a Uhppote object with the bind address, broadcast address and listen address.

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
        self._udp = udp.UDP(bind, broadcast, listen, debug)
        self._tcp = tcp.TCP(bind, debug)

    def get_all_controllers(self, timeout=2.5):
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
        replies = self._udp.broadcast(request, timeout=timeout)

        list = []
        for reply in replies:
            list.append(decode.get_controller_response(reply))

        return list

    def get_controller(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_controller_response(reply)

        return None

    def set_ip(self, controller, address, netmask, gateway, timeout=2.5):
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
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_ip_request(id, address, netmask, gateway)
        reply = self._send(request, addr, timeout, protocol)

        return True

    def get_time(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_time_response(reply)

        return None

    def set_time(self, controller, datetime, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_time_response(reply)

        return None

    def get_status(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_status_response(reply)

        return None

    def get_listener(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_listener_response(reply)

        return None

    def set_listener(self, controller, address, port, interval=0, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_listener_response(reply)

        return None

    def get_door_control(self, controller, door, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_door_control_response(reply)

        return None

    def set_door_control(self, controller, door, mode, delay, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_door_control_response(reply)

        return None

    def open_door(self, controller, door, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.open_door_response(reply)

        return None

    def get_cards(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_cards_response(reply)

        return None

    def get_card(self, controller, card_number, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_card_response(reply)

        return None

    def get_card_by_index(self, controller, card_index, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_card_by_index_response(reply)

        return None

    def put_card(self, controller, card_number, start_date, end_date, door_1, door_2, door_3, door_4, pin, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.put_card_response(reply)

        return None

    def delete_card(self, controller, card_number, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.delete_card_response(reply)

        return None

    def delete_all_cards(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.delete_all_cards_response(reply)

        return None

    def get_event(self, controller, event_index, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_event_response(reply)

        return None

    def get_event_index(self, controller, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_event_index_response(reply)

        return None

    def set_event_index(self, controller, event_index, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_event_index_response(reply)

        return None

    def record_special_events(self, controller, enable, timeout=2.5):
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
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.record_special_events_response(reply)

        return None

    def get_time_profile(self, controller, profile_id, timeout=2.5):
        '''
        Retrieves a time profile from an access conntroller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               profile_id  (uint8)   Time profile ID [2..254] to retrieve.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetTimeProfileResponse  Time profile information for the profile ID.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_time_profile_request(id, profile_id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_time_profile_response(reply)

        return None

    def set_time_profile(self,
                         controller,
                         profile_id,
                         start_date,
                         end_date,
                         monday,
                         tuesday,
                         wednesday,
                         thursday,
                         friday,
                         saturday,
                         sunday,
                         segment_1_start,
                         segment_1_end,
                         segment_2_start,
                         segment_2_end,
                         segment_3_start,
                         segment_3_end,
                         linked_profile_id,
                         timeout=2.5):
        '''
        Creates (or updates) a time profile on an access conntroller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               profile_id        (uint8)   Time profile ID [2..254] to retrieve.
               start_date        (date)    Time profile 'valid from' date.
               end_date          (date)    Time profile 'valid until' date.
               monday            (bool)    Time profile enabled on Monday.
               tuesday           (bool)    Time profile enabled on Tuesday.
               wednesday         (bool)    Time profile enabled on Wednesday.
               thursday          (bool)    Time profile enabled on Thursday.
               friday            (bool)    Time profile enabled on Friday.
               saturday          (bool)    Time profile enabled on Saturday.
               sunday            (bool)    Time profile enabled on Sunday.
               segment_1_start   (time)    Time profile segment 1 start time (HHmm).
               segment_1_end     (time)    Time profile segment 1 end time (HHmm).
               segment_2_start   (time)    Time profile segment 2 start time (HHmm).
               segment_2_end     (time)    Time profile segment 2 end time (HHmm).
               segment_3_start   (time)    Time profile segment 3 start time (HHmm).
               segment_3_end     (time)    Time profile segment 3 end time (HHmm).
               linked_profile_id (uint8)   Next profile ID in chain (0 if none).
               timeout           (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetTimeProfileResponse  Set time profile success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_time_profile_request(id, profile_id, start_date, end_date, monday, tuesday, wednesday,
                                                  thursday, friday, saturday, sunday, segment_1_start, segment_1_end,
                                                  segment_2_start, segment_2_end, segment_3_start, segment_3_end,
                                                  linked_profile_id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_time_profile_response(reply)

        return None

    def delete_all_time_profiles(self, controller, timeout=2.5):
        '''
        Clears all time profiles from an access conntroller.

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
               DeleteAllTimeProfilesResponse  Clear time profiles success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.delete_all_time_profiles_request(id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.delete_all_time_profiles_response(reply)

        return None

    def add_task(self,
                 controller,
                 start_date,
                 end_date,
                 monday,
                 tuesday,
                 wednesday,
                 thursday,
                 friday,
                 saturday,
                 sunday,
                 start_time,
                 door,
                 task_type,
                 more_cards,
                 timeout=2.5):
        '''
        Creates a scheduled task on an access conntroller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               start_date  (datetime)  Task 'valid from' date.
               end_date    (datetime)  Task 'valid until' date.
               monday      (bool)      Task enabled on Monday.
               tuesday     (bool)      Task enabled on Tuesday.
               wednesday   (bool)      Task enabled on Wednesday.
               thursday    (bool)      Task enabled on Thursday.
               friday      (bool)      Task enabled on Friday.
               saturday    (bool)      Task enabled on Saturday.
               sunday      (bool)      Task enabled on Sunday.
               start_time  (time)      Task 'run at' time (HHmm).
               door        (uint8)     Door [1..4] to which task is assigned.
               task_type   (uint8)     Task type
                                       0:  door controlled
                                       1:  door unlocked
                                       2:  door locked
                                       3:  disable time profile
                                       4:  enable time profile
                                       5:  card, no password
                                       6:  card, IN password
                                       7:  card, password
                                       8:  enable 'more cards'
                                       9:  disable 'more cards'
                                       10: trigger once
                                       11: disable pushbutton
                                       12: enable pushbutton
               more_cards  (uint8)     Number of cards for the 'more cards' task.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               AddTaskResponse  Add task success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.add_task_request(id, start_date, end_date, monday, tuesday, wednesday, thursday, friday,
                                          saturday, sunday, start_time, door, task_type, more_cards)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.add_task_response(reply)

        return None

    def refresh_tasklist(self, controller, timeout=2.5):
        '''
        Updates the active tasklist to include tasks added by add_task.

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
               RefreshTasklistResponse  Refresh tasklist success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.refresh_tasklist_request(id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.refresh_tasklist_response(reply)

        return None

    def clear_tasklist(self, controller, timeout=2.5):
        '''
        Clears all active and pending tasks.

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
               ClearTasklistResponse  Clear tasklist success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.clear_tasklist_request(id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.clear_tasklist_response(reply)

        return None

    def set_pc_control(self, controller, enable, timeout=2.5):
        '''
        Defers access control decisions to a remote host. The remote host is expected to 
        interact with the controller at least once every 30 seconds (typically by enabling
        set_pc_control), failing which the access controller will fallback to the internal
        access control list.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               enable      (bool)    Enables remote control of access.
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetPcControlResponse  Enable PC control success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_pc_control_request(id, enable)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_pc_control_response(reply)

        return None

    def set_interlock(self, controller, interlock, timeout=2.5):
        '''
        Sets the door interlock mode for an access controller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               interlock   (uint8)   Door interlock mode:
                                     0:  none
                                     1:  doors 1 and 2 interlocked
                                     2:  doors 2 and 3 interlocked
                                     3:  doors 1 and 2 interlocked, doors 3 and 4 interlocked
                                     4:  doors 1 and 2 and 3 interlocked
                                     8:  doors 1 and 2 and 3 and 4 interlocked
               timeout     (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetInterlockResponse  Set interlock success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_interlock_request(id, interlock)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_interlock_response(reply)

        return None

    def activate_keypads(self, controller, reader1, reader2, reader3, reader4, timeout=2.5):
        '''
        Enables (or disables) the keypad associated with an access reader.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               reader1    (bool)    Enables/disable reader 1 access keypad
               reader2    (bool)    Enables/disable reader 2 access keypad
               reader3    (bool)    Enables/disable reader 3 access keypad
               reader4    (bool)    Enables/disable reader 4 access keypad
               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               ActivateKeypadsResponse  Activate keypads success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.activate_keypads_request(id, reader1, reader2, reader3, reader4)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.activate_keypads_response(reply)

        return None

    def set_door_passcodes(self, controller, door, passcode1, passcode2, passcode3, passcode4, timeout=2.5):
        '''
        Sets up to four supervisor passcodes for a door. The passcodes override any other access 
        restrictions and a valid passcode is in the range [0..999999], with 0 corresponding to 
        'no code'.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               door       (uint8)   Door ID [1..4].
               passcode1  (uint32)  Passcode [0..999999].
               passcode2  (uint32)  Passcode [0..999999].
               passcode3  (uint32)  Passcode [0..999999].
               passcode4  (uint32)  Passcode [0..999999].
               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               SetDoorPasscodesResponse  Set door passcodes success/fail response.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_door_passcodes_request(id, door, passcode1, passcode2, passcode3, passcode4)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_door_passcodes_response(reply)

        return None

    def get_antipassback(self, controller, timeout=2.5):
        '''
        Retrieves the anti-passback mode for an access controller.

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
               GetAntiPassbackResponse  Response from access controller to the get-antipassback request.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.get_antipassback_request(id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.get_antipassback_response(reply)

        return None

    def set_antipassback(self, controller, antipassback, timeout=2.5):
        '''
        Retrieves the anti-passback mode for an access controller.

            Parameters:
               controller (uint32|tuple)  Controller serial number or tuple with (id,address,protocol fields). 
                                          The controller serial number is expected to be greater than 0.
                                          If the controller is a tuple:
                                          - 'id' is the controller serial number
                                          - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                             UDP broadcast address and port 60000.
                                          - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults 
                                             to 'udp'.

               antipassback (uint8) Anti-passback mode:
                                    - 0: disabled
                                    - 1: (1:2);(3:4)
                                    - 2: (1,3):(2,4)
                                    - 3: 1:(2,3)
                                    - 4: 1:(2,3,4)

               timeout    (float)   Optional operation timeout (in seconds). Defaults to 2.5s.

            Returns:
               GetAntiPassbackResponse  Response from access controller to the get-antipassback request.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.set_antipassback_request(id, antipassback)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.set_antipassback_response(reply)

        return None

    def restore_default_parameters(self, controller, timeout=2.5):
        '''
        Resets a controller to the manufacturer default configuratio, protocol='udp'n.
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
               RestoreDefaultParametersResponse  Reset success/fail.

            Raises:
               Exception  If the response from the access controller cannot be decoded.
        '''
        (id, addr, protocol) = disambiguate(controller)
        request = encode.restore_default_parameters_request(id)
        reply = self._send(request, addr, timeout, protocol)

        if reply != None:
            return decode.restore_default_parameters_response(reply)

        return None

    def listen(self, onEvent):
        '''
        Establishes a listener for events from the access controllers by binding to the UDP listen 
        address from the constructor.

            Parameters:
               onEvent  (function)  Handler function for received events, with a function signature 
                                    f(event).

            Returns:
               None
        '''

        def handler(packet):
            try:
                onEvent(decode.event(packet))
            except BaseException as err:
                print('   *** ERROR {}'.format(err))

        self._udp.listen(lambda packet: handler(packet))

        return None

    def _send(self, request, dest_addr, timeout, protocol):
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
            return self._tcp.send(request, dest_addr, timeout)
        else:
            return self._udp.send(request, dest_addr=dest_addr, timeout=timeout)
