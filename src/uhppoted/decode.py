'''
UHPPOTE request packet decoder.

Decodes a UHPPOTE access controller 64 byte UDP response packet into the
equivalent Python object.
'''

import datetime
import struct

from ipaddress import IPv4Address
from dataclasses import dataclass

from .structs import GetControllerResponse
from .structs import GetTimeResponse
from .structs import SetTimeResponse
from .structs import GetStatusResponse
from .structs import GetListenerResponse
from .structs import SetListenerResponse
from .structs import GetDoorControlResponse
from .structs import SetDoorControlResponse
from .structs import OpenDoorResponse
from .structs import GetCardsResponse
from .structs import GetCardResponse
from .structs import GetCardByIndexResponse
from .structs import PutCardResponse
from .structs import DeleteCardResponse
from .structs import DeleteAllCardsResponse
from .structs import GetEventResponse
from .structs import GetEventIndexResponse
from .structs import SetEventIndexResponse
from .structs import RecordSpecialEventsResponse
from .structs import GetTimeProfileResponse
from .structs import SetTimeProfileResponse
from .structs import DeleteAllTimeProfilesResponse
from .structs import AddTaskResponse
from .structs import RefreshTasklistResponse
from .structs import ClearTasklistResponse
from .structs import SetPcControlResponse
from .structs import SetInterlockResponse
from .structs import ActivateKeypadsResponse
from .structs import Event
from .structs import PIN


def get_controller_response(packet):
    '''
    Decodes a get-controller response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetControllerResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x94:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetControllerResponse(
        unpack_uint32(packet, 4),
        unpack_ipv4(packet, 8),
        unpack_ipv4(packet, 12),
        unpack_ipv4(packet, 16),
        unpack_mac(packet, 20),
        unpack_version(packet, 26),
        unpack_date(packet, 28),
    )


def get_time_response(packet):
    '''
    Decodes a get-time response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetTimeResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x32:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetTimeResponse(
        unpack_uint32(packet, 4),
        unpack_datetime(packet, 8),
    )


def set_time_response(packet):
    '''
    Decodes a set-time response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetTimeResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x30:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetTimeResponse(
        unpack_uint32(packet, 4),
        unpack_datetime(packet, 8),
    )


def get_status_response(packet):
    '''
    Decodes a get-status response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetStatusResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x20:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetStatusResponse(
        unpack_uint32(packet, 4),
        unpack_shortdate(packet, 51),
        unpack_time(packet, 37),
        unpack_bool(packet, 28),
        unpack_bool(packet, 29),
        unpack_bool(packet, 30),
        unpack_bool(packet, 31),
        unpack_bool(packet, 32),
        unpack_bool(packet, 33),
        unpack_bool(packet, 34),
        unpack_bool(packet, 35),
        unpack_uint8(packet, 49),
        unpack_uint8(packet, 50),
        unpack_uint8(packet, 36),
        unpack_uint8(packet, 48),
        unpack_uint32(packet, 8),
        unpack_uint8(packet, 12),
        unpack_bool(packet, 13),
        unpack_uint8(packet, 14),
        unpack_uint8(packet, 15),
        unpack_uint32(packet, 16),
        unpack_optional_datetime(packet, 20),
        unpack_uint8(packet, 27),
        unpack_uint32(packet, 40),
    )


def get_listener_response(packet):
    '''
    Decodes a get-listener response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetListenerResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x92:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetListenerResponse(
        unpack_uint32(packet, 4),
        unpack_ipv4(packet, 8),
        unpack_uint16(packet, 12),
    )


def set_listener_response(packet):
    '''
    Decodes a set-listener response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetListenerResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x90:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetListenerResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def get_door_control_response(packet):
    '''
    Decodes a get-door-control response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetDoorControlResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x82:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetDoorControlResponse(
        unpack_uint32(packet, 4),
        unpack_uint8(packet, 8),
        unpack_uint8(packet, 9),
        unpack_uint8(packet, 10),
    )


def set_door_control_response(packet):
    '''
    Decodes a set-door-control response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetDoorControlResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x80:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetDoorControlResponse(
        unpack_uint32(packet, 4),
        unpack_uint8(packet, 8),
        unpack_uint8(packet, 9),
        unpack_uint8(packet, 10),
    )


def open_door_response(packet):
    '''
    Decodes an open-door response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            OpenDoorResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x40:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return OpenDoorResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def get_cards_response(packet):
    '''
    Decodes a get-cards response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetCardsResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x58:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetCardsResponse(
        unpack_uint32(packet, 4),
        unpack_uint32(packet, 8),
    )


def get_card_response(packet):
    '''
    Decodes a get-card response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetCardResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x5a:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetCardResponse(
        unpack_uint32(packet, 4),
        unpack_uint32(packet, 8),
        unpack_optional_date(packet, 12),
        unpack_optional_date(packet, 16),
        unpack_uint8(packet, 20),
        unpack_uint8(packet, 21),
        unpack_uint8(packet, 22),
        unpack_uint8(packet, 23),
        unpack_pin(packet, 24),
    )


def get_card_by_index_response(packet):
    '''
    Decodes a get-card-by-index response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetCardByIndexResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x5c:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetCardByIndexResponse(
        unpack_uint32(packet, 4),
        unpack_uint32(packet, 8),
        unpack_optional_date(packet, 12),
        unpack_optional_date(packet, 16),
        unpack_uint8(packet, 20),
        unpack_uint8(packet, 21),
        unpack_uint8(packet, 22),
        unpack_uint8(packet, 23),
        unpack_pin(packet, 24),
    )


def put_card_response(packet):
    '''
    Decodes a put-card response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            PutCardResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x50:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return PutCardResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def delete_card_response(packet):
    '''
    Decodes a delete-card response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            DeleteCardResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x52:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return DeleteCardResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def delete_all_cards_response(packet):
    '''
    Decodes a delete-all-cards response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            DeleteAllCardsResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x54:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return DeleteAllCardsResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def get_event_response(packet):
    '''
    Decodes a get-event response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetEventResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xb0:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetEventResponse(
        unpack_uint32(packet, 4),
        unpack_uint32(packet, 8),
        unpack_uint8(packet, 12),
        unpack_bool(packet, 13),
        unpack_uint8(packet, 14),
        unpack_uint8(packet, 15),
        unpack_uint32(packet, 16),
        unpack_optional_datetime(packet, 20),
        unpack_uint8(packet, 27),
    )


def get_event_index_response(packet):
    '''
    Decodes a get-event-index response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetEventIndexResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xb4:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetEventIndexResponse(
        unpack_uint32(packet, 4),
        unpack_uint32(packet, 8),
    )


def set_event_index_response(packet):
    '''
    Decodes a set-event-index response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetEventIndexResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xb2:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetEventIndexResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def record_special_events_response(packet):
    '''
    Decodes a record-special-events response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            RecordSpecialEventsResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x8e:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return RecordSpecialEventsResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def get_time_profile_response(packet):
    '''
    Decodes a get-time-profile response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            GetTimeProfileResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x98:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return GetTimeProfileResponse(
        unpack_uint32(packet, 4),
        unpack_uint8(packet, 8),
        unpack_optional_date(packet, 9),
        unpack_optional_date(packet, 13),
        unpack_bool(packet, 17),
        unpack_bool(packet, 18),
        unpack_bool(packet, 19),
        unpack_bool(packet, 20),
        unpack_bool(packet, 21),
        unpack_bool(packet, 22),
        unpack_bool(packet, 23),
        unpack_hhmm(packet, 24),
        unpack_hhmm(packet, 26),
        unpack_hhmm(packet, 28),
        unpack_hhmm(packet, 30),
        unpack_hhmm(packet, 32),
        unpack_hhmm(packet, 34),
        unpack_uint8(packet, 36),
    )


def set_time_profile_response(packet):
    '''
    Decodes a set-time-profile response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetTimeProfileResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x88:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetTimeProfileResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def delete_all_time_profiles_response(packet):
    '''
    Decodes a delete-all-time-profiles response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            DeleteAllTimeProfilesResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x8a:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return DeleteAllTimeProfilesResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def add_task_response(packet):
    '''
    Decodes an add-task response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            AddTaskResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xa8:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return AddTaskResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def refresh_tasklist_response(packet):
    '''
    Decodes a refresh-tasklist response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            RefreshTasklistResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xac:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return RefreshTasklistResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def clear_tasklist_response(packet):
    '''
    Decodes a clear-tasklist response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            ClearTasklistResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xa6:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return ClearTasklistResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def set_pc_control_response(packet):
    '''
    Decodes a set-pc-control response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetPcControlResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xa0:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetPcControlResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def set_interlock_response(packet):
    '''
    Decodes a set-interlock response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            SetInterlockResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xa2:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return SetInterlockResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def activate_keypads_response(packet):
    '''
    Decodes an activate-keypads response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            ActivateKeypadsResponse initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0xa4:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return ActivateKeypadsResponse(
        unpack_uint32(packet, 4),
        unpack_bool(packet, 8),
    )


def event(packet):
    '''
    Decodes an event packet response.

        Parameters:
            packet  (bytearray)  64 byte UDP packet.

        Returns:
            Event initialised from the UDP packet.

        Raises:
            ValueError If the packet is not 64 bytes, has an invalid start-of-message byte or has
                       the incorrect message type.
    '''
    if len(packet) != 64:
        raise ValueError(f'invalid reply packet length ({len(packet)})')

    # Ref. v6.62 firmware event
    if packet[0] != 0x17 and (packet[0] != 0x19 or packet[1] != 0x20):
        raise ValueError(f'invalid reply start of message byte ({packet[0]:02x})')

    if packet[1] != 0x20:
        raise ValueError(f'invalid reply function code ({packet[1]:02x})')

    return Event(
        unpack_uint32(packet, 4),
        unpack_uint32(packet, 8),
        unpack_uint8(packet, 12),
        unpack_bool(packet, 13),
        unpack_uint8(packet, 14),
        unpack_uint8(packet, 15),
        unpack_uint32(packet, 16),
        unpack_datetime(packet, 20),
        unpack_uint8(packet, 27),
        unpack_shortdate(packet, 51),
        unpack_time(packet, 37),
        unpack_uint8(packet, 36),
        unpack_bool(packet, 28),
        unpack_bool(packet, 29),
        unpack_bool(packet, 30),
        unpack_bool(packet, 31),
        unpack_bool(packet, 32),
        unpack_bool(packet, 33),
        unpack_bool(packet, 34),
        unpack_bool(packet, 35),
        unpack_uint8(packet, 49),
        unpack_uint8(packet, 50),
        unpack_uint8(packet, 48),
        unpack_uint32(packet, 40),
    )


def unpack_uint8(packet, offset):
    '''
    Unpacks the uint8 value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           uint8 value.
    '''
    return packet[offset]


def unpack_uint16(packet, offset):
    '''
    Unpacks the 2-byte little endian uint16 value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           uint16 value.
    '''
    return struct.unpack_from('<H', packet, offset)[0]


def unpack_uint32(packet, offset):
    '''
    Unpacks the 4-byte little endian uint32 value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           uint32 value.
    '''
    return struct.unpack_from('<L', packet, offset)[0]


def unpack_ipv4(packet, offset):
    '''
    Unpacks the 4-byte IP address value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           IPv4Address value.
    '''
    return IPv4Address(packet[offset:offset + 4])


def unpack_mac(packet, offset):
    '''
    Unpacks the 6-byte MAC address value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           MAC address as a colon-seperated hexadecimal string.
    '''
    return '{:02x}:{:02x}:{:02x}:{:02x}::{:02x}:{:02x}'.format(*packet[offset:offset + 7])


def unpack_version(packet, offset):
    '''
    Unpacks the 2-byte BCD encoded version value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           Version string.
    '''
    return 'v{:x}.{:02x}'.format(*packet[offset:offset + 2])


def unpack_date(packet, offset):
    '''
    Unpacks the 4-byte BCD encoded YYYYMMDD value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.
    '''
    bcd = '{:02x}{:02x}{:02x}{:02x}'.format(*packet[offset:offset + 4])

    return datetime.datetime.strptime(bcd, '%Y%m%d').date()


def unpack_shortdate(packet, offset):
    '''
    Unpacks the 3-byte BCD encoded YYMMDD value from the packet at the offset,
    automatically adding the CC value.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.
    '''
    bcd = '20{:02x}{:02x}{:02x}'.format(*packet[offset:offset + 3])

    return datetime.datetime.strptime(bcd, '%Y%m%d').date()


def unpack_optional_date(packet, offset):
    '''
    Unpacks the 4-byte BCD encoded YYYYMMDD value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.

        Raises:
           ValueError if the date value is invalid.
    '''
    bcd = '{:02x}{:02x}{:02x}{:02x}'.format(*packet[offset:offset + 4])

    try:
        return datetime.datetime.strptime(bcd, '%Y%m%d').date()
    except ValueError as x:
        return None


def unpack_datetime(packet, offset):
    '''
    Unpacks the 7-byte BCD encoded YYYYMMDDHHmmss value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.
    '''
    bcd = '{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}'.format(*packet[offset:offset + 7])

    return datetime.datetime.strptime(bcd, '%Y%m%d%H%M%S')


def unpack_optional_datetime(packet, offset):
    '''
    Unpacks the 7-byte BCD encoded YYYYMMDDHHmmss value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.

        Raises:
           ValueError if the date value is invalid.
    '''
    bcd = '{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}'.format(*packet[offset:offset + 7])

    try:
        return datetime.datetime.strptime(bcd, '%Y%m%d%H%M%S')
    except ValueError as x:
        return None


def unpack_time(packet, offset):
    '''
    Unpacks the 3-byte BCD encoded HHmmss value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.
    '''
    bcd = '{:02x}{:02x}{:02x}'.format(*packet[offset:offset + 3])

    return datetime.datetime.strptime(bcd, '%H%M%S').time()


def unpack_hhmm(packet, offset):
    '''
    Unpacks the 2-byte BCD encoded HHmm value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.
    '''
    bcd = '{:02x}{:02x}'.format(*packet[offset:offset + 2])

    return datetime.datetime.strptime(bcd, '%H%M').time()


def unpack_bool(packet, offset):
    '''
    Unpacks the byte from the packet at the offset as a boolean value. 0 is translated
    to False and 'not zero' to True. The access controller should only fill this field
    with either a one or a zero.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           datetime value.
    '''
    return packet[offset] != 0x00


def unpack_pin(packet, offset):
    '''
    Unpacks the 3-byte PIN value from the packet at the offset.

        Parameters:
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.

        Returns:
           PIN  value.
    '''
    v = packet[offset + 2] & 0x0ff
    v <<= 8
    v |= packet[offset + 1] & 0x0ff
    v <<= 8
    v |= packet[offset] & 0x00ff

    return v
