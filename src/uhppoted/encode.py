'''
UHPPOTE request packet encoder.

Encodes a UHPPOTE access controller request as a 64 byte UDP packet:

- uint8, uint16, uint24 and uint32 values are encoded as little endian unsigned integers
- datetime, date and time values are encoded as BCD
- boolean values are encoded as 0 (False) or 1 (True)
'''

import struct


def get_controller_request(controller):
    '''
    Encodes a get-controller request.

        Parameters:
            controller (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x94

    pack_uint32(controller, packet, 4)

    return packet


def set_ip_request(controller, address, netmask, gateway):
    '''
    Encodes a set-ip request.

        Parameters:
            controller (uint32)       Controller serial number.
            address    (IPv4Address)  Controller IP address.
            netmask    (IPv4Address)  Controller subnet mask.
            gateway    (IPv4Address)  Controller gateway address.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x96

    pack_uint32(controller, packet, 4)
    pack_IPv4(address, packet, 8)
    pack_IPv4(netmask, packet, 12)
    pack_IPv4(gateway, packet, 16)
    pack_uint32(0x55aaaa55, packet, 20)

    return packet


def get_time_request(controller):
    '''
    Encodes a get-time request.

        Parameters:
            controller (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x32

    pack_uint32(controller, packet, 4)

    return packet


def set_time_request(controller, datetime):
    '''
    Encodes a set-time request.

        Parameters:
            controller (uint32)    Controller serial number.
            datetime   (datetime)  Date and time.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x30

    pack_uint32(controller, packet, 4)
    pack_datetime(datetime, packet, 8)

    return packet


def get_status_request(controller):
    '''
    Encodes a get-status request.

        Parameters:
            controller (uint32) Controller serial number.
 
        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x20

    pack_uint32(controller, packet, 4)

    return packet


def get_listener_request(controller):
    '''
    Encodes a get-listener request.

        Parameters:
            controller (uint32) Controller serial number.
 
        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x92

    pack_uint32(controller, packet, 4)

    return packet


def set_listener_request(controller, address, port):
    '''
    Encodes a set-listener request.

        Parameters:
            controller (uint32)                 Controller serial number.
            address    (ipaddress.IPv4Address)  IP address of event listener.
            port       (uint16)                 UDP port of event listener.
 
        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x90

    pack_uint32(controller, packet, 4)
    pack_IPv4(address, packet, 8)
    pack_uint16(port, packet, 12)

    return packet


def get_door_control_request(controller, door):
    '''
    Encodes a get-door-control request.

        Parameters:
            controller (uint32) Controller serial number.
            door       (uint8)  Door ID [1..4]
 
        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x82

    pack_uint32(controller, packet, 4)
    pack_uint8(door, packet, 8)

    return packet


def set_door_control_request(controller, door, mode, delay):
    '''
    Encodes a set-door-control request.

        Parameters:
            controller (uint32) Controller serial number.
            door       (uint8)  Door ID [1..4]
            mode       (uint8)  Control mode (1: normally open, 2: normally closed, 3: controlled)
            delay      (uint8)   Door unlock duration (seconds)

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x80

    pack_uint32(controller, packet, 4)
    pack_uint8(door, packet, 8)
    pack_uint8(mode, packet, 9)
    pack_uint8(delay, packet, 10)

    return packet


def open_door_request(controller, door):
    '''
    Encodes an open-door request.

        Parameters:
            controller (uint32) Controller serial number.
            door       (uint8)  Door ID [1..4]

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x40

    pack_uint32(controller, packet, 4)
    pack_uint8(door, packet, 8)

    return packet


def get_cards_request(controller):
    '''
    Encodes a get-cards request.

        Parameters:
            controller (uint32) Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x58

    pack_uint32(controller, packet, 4)

    return packet


def get_card_request(controller, card_number):
    '''
    Encodes a get-card request.

        Parameters:
            controller  (uint32) Controller serial number.
            card_number (uint32) Card number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x5a

    pack_uint32(controller, packet, 4)
    pack_uint32(card_number, packet, 8)

    return packet


def get_card_by_index_request(controller, card_index):
    '''
    Encodes a get-card-by-index request.

        Parameters:
            controller  (uint32) Controller serial number.
            card_index  (uint32) Index into controller cards list.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x5c

    pack_uint32(controller, packet, 4)
    pack_uint32(card_index, packet, 8)

    return packet


def put_card_request(controller, card_number, start_date, end_date, door_1, door_2, door_3, door_4, pin):
    '''
    Encodes a put-card request.

        Parameters:
            controller  (uint32)  Controller serial number.
            card_number (uint32)  Card number.
            start_date  (date)    Card 'valid from' date.
            end_date    (date)    Card 'valid until' date.
            door_1      (uint8)   Card access permissions for door 1 (0: none, 1: all, 2-254: time profile ID)
            door_2      (uint8)   Card access permissions for door 2 (0: none, 1: all, 2-254: time profile ID)
            door_3      (uint8)   Card access permissions for door 3 (0: none, 1: all, 2-254: time profile ID)
            door_4      (uint8)   Card access permissions for door 4 (0: none, 1: all, 2-254: time profile ID)
            pin         (uint24)  Card access keypad PIN code

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x50

    pack_uint32(controller, packet, 4)
    pack_uint32(card_number, packet, 8)
    pack_date(start_date, packet, 12)
    pack_date(end_date, packet, 16)
    pack_uint8(door_1, packet, 20)
    pack_uint8(door_2, packet, 21)
    pack_uint8(door_3, packet, 22)
    pack_uint8(door_4, packet, 23)
    pack_pin(pin, packet, 24)

    return packet


def delete_card_request(controller, card_number):
    '''
    Encodes a delete-card request.

        Parameters:
            controller  (uint32)  Controller serial number.
            card_number (uint32)  Card number to delete.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x52

    pack_uint32(controller, packet, 4)
    pack_uint32(card_number, packet, 8)

    return packet


def delete_cards_request(controller):
    '''
    Encodes a delete-cards request.

        Parameters:
            controller  (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x54

    pack_uint32(controller, packet, 4)
    pack_uint32(0x55aaaa55, packet, 8)

    return packet


def get_event_request(controller, event_index):
    '''
    Encodes a get-event request.

        Parameters:
            controller  (uint32)  Controller serial number.
            event_index (uint32)  Index of event in controller events list.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xb0

    pack_uint32(controller, packet, 4)
    pack_uint32(event_index, packet, 8)

    return packet


def get_event_index_request(controller):
    '''
    Encodes a get-event-index request.

        Parameters:
            controller  (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xb4

    pack_uint32(controller, packet, 4)

    return packet


def set_event_index_request(controller, event_index):
    '''
    Encodes a set-event-index request.

        Parameters:
            controller  (uint32)  Controller serial number.
            event_index (uint32)  Index from which to start retrieving events.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xb2

    pack_uint32(controller, packet, 4)
    pack_uint32(event_index, packet, 8)
    pack_uint32(0x55aaaa55, packet, 12)

    return packet


def record_special_events_request(controller, enable):
    '''
    Encodes a record-special-events request.

        Parameters:
            controller  (uint32)  Controller serial number.
            enable      (bool)    Enables/disables door and pushbutton events.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x8e

    pack_uint32(controller, packet, 4)
    pack_bool(enable, packet, 8)

    return packet


def get_time_profile_request(controller, profile_id):
    '''
    Encodes a get-time-profile request.

        Parameters:
            controller  (uint32)  Controller serial number.
            profile_id  (uint8)   Time profile ID [2..254]

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x98

    pack_uint32(controller, packet, 4)
    pack_uint8(profile_id, packet, 8)

    return packet


def set_time_profile_request(controller, profile_id, start_date, end_date, monday, tuesday, wednesday, thursday, friday,
                             saturday, sunday, segment_1_start, segment_1_end, segment_2_start, segment_2_end,
                             segment_3_start, segment_3_end, linked_profile_id):
    '''
    Encodes a set-time-profile request.

        Parameters:
            controller        (uint32)  Controller serial number.
            profile_id        (uint8)   Time profile ID [2..254]
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

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x88

    pack_uint32(controller, packet, 4)
    pack_uint8(profile_id, packet, 8)
    pack_date(start_date, packet, 9)
    pack_date(end_date, packet, 13)
    pack_bool(monday, packet, 17)
    pack_bool(tuesday, packet, 18)
    pack_bool(wednesday, packet, 19)
    pack_bool(thursday, packet, 20)
    pack_bool(friday, packet, 21)
    pack_bool(saturday, packet, 22)
    pack_bool(sunday, packet, 23)
    pack_HHmm(segment_1_start, packet, 24)
    pack_HHmm(segment_1_end, packet, 26)
    pack_HHmm(segment_2_start, packet, 28)
    pack_HHmm(segment_2_end, packet, 30)
    pack_HHmm(segment_3_start, packet, 32)
    pack_HHmm(segment_3_end, packet, 34)
    pack_uint8(linked_profile_id, packet, 36)

    return packet


def delete_all_time_profiles_request(controller):
    '''
    Encodes a delete-all-time-profiles request.

        Parameters:
            controller  (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0x8a

    pack_uint32(controller, packet, 4)
    pack_uint32(0x55aaaa55, packet, 8)

    return packet


def add_task_request(controller, start_date, end_date, monday, tuesday, wednesday, thursday, friday, saturday, sunday,
                     start_time, door, task_type, more_cards):
    '''
    Encodes an add-task request.

        Parameters:
            controller  (uint32)  Controller serial number.
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

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xa8

    pack_uint32(controller, packet, 4)
    pack_date(start_date, packet, 8)
    pack_date(end_date, packet, 12)
    pack_bool(monday, packet, 16)
    pack_bool(tuesday, packet, 17)
    pack_bool(wednesday, packet, 18)
    pack_bool(thursday, packet, 19)
    pack_bool(friday, packet, 20)
    pack_bool(saturday, packet, 21)
    pack_bool(sunday, packet, 22)
    pack_HHmm(start_time, packet, 23)
    pack_uint8(door, packet, 25)
    pack_uint8(task_type, packet, 26)
    pack_uint8(more_cards, packet, 27)

    return packet


def refresh_tasklist_request(controller):
    '''
    Encodes a refresh-tasklist request.

        Parameters:
            controller  (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xac

    pack_uint32(controller, packet, 4)
    pack_uint32(0x55aaaa55, packet, 8)

    return packet


def clear_tasklist_request(controller):
    '''
    Encodes a clear-tasklist request.

        Parameters:
            controller  (uint32)  Controller serial number.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xa6

    pack_uint32(controller, packet, 4)
    pack_uint32(0x55aaaa55, packet, 8)

    return packet


def set_pc_control_request(controller, enable):
    '''
    Encodes a set-pc-control request.

        Parameters:
            controller  (uint32)  Controller serial number.
            enable      (bool)    Remote access control enabled/disabled.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xa0

    pack_uint32(controller, packet, 4)
    pack_uint32(0x55aaaa55, packet, 8)
    pack_bool(enable, packet, 12)

    return packet


def set_interlock_request(controller, interlock):
    '''
    Encodes a set-interlock request.

        Parameters:
           controller  (uint32)  Controller serial number (expected to be greater than 0).
           interlock   (uint8)   Door interlock mode:
                                 0:  none
                                 1:  doors 1 and 2 interlocked
                                 2:  doors 2 and 3 interlocked
                                 3:  doors 1 and 2 interlocked, doors 3 and 4 interlocked
                                 4:  doors 1 and 2 and 3 interlocked
                                 8:  doors 1 and 2 and 3 and 4 interlocked

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xa2

    pack_uint32(controller, packet, 4)
    pack_uint8(interlock, packet, 8)

    return packet


def activate_keypads_request(controller, reader_1, reader_2, reader_3, reader_4):
    '''
    Encodes an activate-keypads request.

        Parameters:
           controller (uint32)  Controller serial number (expected to be greater than 0).
           reader_1   (bool)    Enables/disable reader 1 access keypad.
           reader_2   (bool)    Enables/disable reader 2 access keypad.
           reader_3   (bool)    Enables/disable reader 3 access keypad.
           reader_4   (bool)    Enables/disable reader 4 access keypad.

        Returns:
            64 byte UDP packet.
    '''
    packet = bytearray(64)

    packet[0] = 0x17
    packet[1] = 0xa4

    pack_uint32(controller, packet, 4)
    pack_bool(reader_1, packet, 8)
    pack_bool(reader_2, packet, 9)
    pack_bool(reader_3, packet, 10)
    pack_bool(reader_4, packet, 11)

    return packet


def pack_uint8(v, packet, offset):
    '''
    'in-place' packs a uint8 value as a byte into the packet at the offset.

        Parameters:
           v      (uint8)      uint8 value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    packet[offset] = v


def pack_uint16(v, packet, offset):
    '''
    'in-place' packs a uint16 value as a 2-byte little endian value into the packet 
    at the offset.

        Parameters:
           v      (uint16)     uint16 value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    struct.pack_into('<H', packet, offset, v)


def pack_uint32(v, packet, offset):
    '''
    'in-place' packs a uint16 value as a 4-byte little endian value into the packet 
    at the offset.

        Parameters:
           v      (uint32)     uint32 value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    struct.pack_into('<L', packet, offset, v)


def pack_IPv4(v, packet, offset):
    '''
    'in-place' packs an IPv4Address value 4-byte address into the packet at the offset.

        Parameters:
           v      (IPv4Address)  IP address to encode.
           packet (bytearray)    64 byte array.
           offset (int)          Value location in array.
    '''
    packet[offset:offset + 4] = v.packed


def pack_date(v, packet, offset):
    '''
    'in-place' packs a date value as a 4-byte BCD encoded YYYYMMDD value into the packet at the offset.

        Parameters:
           v      (date)       Date value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    bcd = f'{v:%Y%m%d}'
    packet[offset:offset + 4] = bytes.fromhex(bcd)


def pack_datetime(v, packet, offset):
    '''
    'in-place' packs a date value as a 7s-byte BCD encoded YYYYMMDDHHmmss value into the packet at 
    the offset.

        Parameters:
           v      (datetime)   Date and time value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    bcd = f'{v:%Y%m%d%H%M%S}'
    packet[offset:offset + 7] = bytes.fromhex(bcd)


def pack_HHmm(v, packet, offset):
    '''
    'in-place' packs a short time value as a 2-byte BCD encoded HHmm value into the packet at the offset.

        Parameters:
           v      (time)       Time value to encode. Only the hours and minutes are encoded.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    bcd = f'{v:%H%M}'
    packet[offset:offset + 2] = bytes.fromhex(bcd)


def pack_bool(v, packet, offset):
    '''
    'in-place' packs a boolean value as a byte value into the packet at the offset. False is encoded
    as 0, True as 1.

        Parameters:
           v      (bool)       Boolean value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    packet[offset] = 0x00 if not v else 0x01


def pack_pin(v, packet, offset):
    '''
    'in-place' packs a 24-bit PIN value as a 3-byte little-endian value into the packet at the offset.

        Parameters:
           v      (uint24)     24-bit PIN value to encode.
           packet (bytearray)  64 byte array.
           offset (int)        Value location in array.
    '''
    packet[offset] = (v >> 0) & 0x00ff
    packet[offset + 1] = (v >> 8) & 0x0ff
    packet[offset + 2] = (v >> 16) & 0x0ff
