def set_firstcard(uhppote, controller, door, firstcard, timeout=2.5):
    """
    Sets the first-card configuration for a controller managed door.

        Parameters:
           uhppoted   (Uhppote)       Initialised Uhppote struct with the operation configuration.
           controller (uint32|tuple)  Controller serial number or tuple with (controller_id,address,protocol)
                                      fields. The controller serial number is expected to be greater than 0.
                                      If the controller is a tuple:
                                      - 'controller_id' is the controller serial number
                                      - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                         UDP broadcast address and port 60000.
                                      - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults
                                         to 'udp'.

           door       (uint8)        Door [1..4]
           firstcard  (FirstCard)    First-card configuration.
           timeout    (float)        Optional operation timeout (in seconds). Defaults to 2.5s.

        Returns:
           response   (SetFirstCardResponse)  Returns the unvalidated response from the controller (or None).

       Raises:
           Exception  If the request failed for any reason.
    """
    controller_id, addr, protocol = disambiguate(controller)
    request = encode.set_firstcard_request(controller_id, door, firstcard)

    if reply := u._send(request, addr, timeout, protocol):
        return decode.set_firstcard_response(reply)

    return None


async def set_firstcard_async(uhppote, controller, door, firstcard, timeout=2.5):
    """
    Sets the first-card configuration for a controller managed door.

       Parameters:
           uhppoted   (UhppoteAsync)  Initialised UhppoteAsync struct with the operation configuration.
           controller (uint32|tuple)  Controller serial number or tuple with (controller_id,address,protocol)
                                      fields. The controller serial number is expected to be greater than 0.
                                      If the controller is a tuple:
                                      - 'controller_id' is the controller serial number
                                      - 'address' is the optional controller IPv4 addess:port. Defaults to the
                                         UDP broadcast address and port 60000.
                                      - 'protocol' is an optional transport protocol ('udp' or 'tcp'). Defaults
                                         to 'udp'.

           door       (uint8)        Door [1..4]
           firstcard  (FirstCard)    First-card configuration.
           timeout    (float)        Optional operation timeout (in seconds). Defaults to 2.5s.

       Returns:
           response   (SetFirstCardResponse)  Returns the unvalidated response from the controller (or None).

       Raises:
           Exception  If the request failed for any reason.
    """
    controller_id, addr, protocol = disambiguate(controller)
    request = encode.set_firstcard_request(controller_id, door, firstcard)
    reply = await self._send(request, addr, timeout, protocol)

    if reply is not None:
        return decode.set_firstcard_response(reply)

    return None
