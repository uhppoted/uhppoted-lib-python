"""
UHPPOTE request packet decoder unit tests.

Tests the packet decoding functions.
"""

import unittest
import datetime

# pylint: disable=import-error
from ipaddress import IPv4Address
from uhppoted import decode


class TestDecode(unittest.TestCase):
    """
    Test suite for the message decoder.
    """

    def test_get_controller_response(self):
        """
        Tests a valid get-controller response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x94, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xc0, 0xa8, 0x01, 0x64, 0xff, 0xff, 0xff, 0x00,
                  0xc0, 0xa8, 0x01, 0x01, 0x00, 0x12, 0x23, 0x34, 0x45, 0x56, 0x08, 0x92, 0x20, 0x18, 0x11, 0x05,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_controller_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.ip_address, IPv4Address("192.168.1.100"))
        self.assertEqual(response.subnet_mask, IPv4Address("255.255.255.0"))
        self.assertEqual(response.gateway, IPv4Address("192.168.1.1"))
        self.assertEqual(response.mac_address, "00:12:23:34:45:56")
        self.assertEqual(response.version, "v8.92")
        self.assertEqual(response.date, datetime.date(2018, 11, 5))

    def test_decode_get_listener_response(self):
        """
        Tests decoding a valid get-listener response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x92, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xc0, 0xa8, 0x01, 0x64, 0x61, 0xea, 0x0f, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_listener_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.address, IPv4Address("192.168.1.100"))
        self.assertEqual(response.port, 60001)
        self.assertEqual(response.interval, 15)

    def test_get_status_response(self):
        """
        Tests a valid get-status response.
        """
        # yapf: disable
        packet = bytearray([
            0x17, 0x20, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x4e, 0x00, 0x00, 0x00, 0x02, 0x01, 0x03, 0x01,
            0xa1, 0x98, 0x7c, 0x00, 0x20, 0x22, 0x08, 0x23, 0x09, 0x47, 0x06, 0x2c, 0x00, 0x01, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0x03, 0x09, 0x49, 0x39, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x27, 0x07, 0x09, 0x22, 0x08, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_status_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.system_date, datetime.date(2022, 8, 23))
        self.assertEqual(response.system_time, datetime.time(9, 49, 39))
        self.assertEqual(response.door_1_open, False)
        self.assertEqual(response.door_2_open, True)
        self.assertEqual(response.door_3_open, False)
        self.assertEqual(response.door_4_open, False)
        self.assertEqual(response.door_1_button, False)
        self.assertEqual(response.door_2_button, False)
        self.assertEqual(response.door_3_button, False)
        self.assertEqual(response.door_4_button, True)
        self.assertEqual(response.relays, 7)
        self.assertEqual(response.inputs, 9)
        self.assertEqual(response.system_error, 3)
        self.assertEqual(response.special_info, 39)
        self.assertEqual(response.event_index, 78)
        self.assertEqual(response.event_type, 2)
        self.assertEqual(response.event_access_granted, True)
        self.assertEqual(response.event_door, 3)
        self.assertEqual(response.event_direction, 1)
        self.assertEqual(response.event_card, 8165537)
        self.assertEqual(response.event_timestamp, datetime.datetime(2022, 8, 23, 9, 47, 6))
        self.assertEqual(response.event_reason, 44)
        self.assertEqual(response.sequence_no, 0)

    def test_get_status_response_with_no_event(self):
        """
        Tests a valid get-status response with no event information in the response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x20, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x01, 0x03, 0x09, 0x49, 0x39, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x27, 0x07, 0x09, 0x22, 0x08, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_status_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.system_date, datetime.date(2022, 8, 23))
        self.assertEqual(response.system_time, datetime.time(9, 49, 39))
        self.assertEqual(response.door_1_open, False)
        self.assertEqual(response.door_2_open, True)
        self.assertEqual(response.door_3_open, False)
        self.assertEqual(response.door_4_open, False)
        self.assertEqual(response.door_1_button, False)
        self.assertEqual(response.door_2_button, False)
        self.assertEqual(response.door_3_button, False)
        self.assertEqual(response.door_4_button, True)
        self.assertEqual(response.relays, 7)
        self.assertEqual(response.inputs, 9)
        self.assertEqual(response.system_error, 3)
        self.assertEqual(response.special_info, 39)
        self.assertEqual(response.event_index, 0)
        self.assertEqual(response.event_type, None)
        self.assertEqual(response.event_access_granted, None)
        self.assertEqual(response.event_door, None)
        self.assertEqual(response.event_direction, None)
        self.assertEqual(response.event_card, None)
        self.assertEqual(response.event_timestamp, None)
        self.assertEqual(response.event_reason, None)
        self.assertEqual(response.sequence_no, 0)

    def test_get_status_response_with_invalid_event_timestamp(self):
        """
        Tests a valid get-status response.
        """
        # yapf: disable
        packet = bytearray([
            0x17, 0x20, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x4e, 0x00, 0x00, 0x00, 0x02, 0x01, 0x03, 0x01,
            0xa1, 0x98, 0x7c, 0x00, 0x20, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x01, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0x03, 0x09, 0x49, 0x39, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x27, 0x07, 0x09, 0x22, 0x08, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_status_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.system_date, datetime.date(2022, 8, 23))
        self.assertEqual(response.system_time, datetime.time(9, 49, 39))
        self.assertEqual(response.door_1_open, False)
        self.assertEqual(response.door_2_open, True)
        self.assertEqual(response.door_3_open, False)
        self.assertEqual(response.door_4_open, False)
        self.assertEqual(response.door_1_button, False)
        self.assertEqual(response.door_2_button, False)
        self.assertEqual(response.door_3_button, False)
        self.assertEqual(response.door_4_button, True)
        self.assertEqual(response.relays, 7)
        self.assertEqual(response.inputs, 9)
        self.assertEqual(response.system_error, 3)
        self.assertEqual(response.special_info, 39)
        self.assertEqual(response.event_index, 78)
        self.assertEqual(response.event_type, 2)
        self.assertEqual(response.event_access_granted, True)
        self.assertEqual(response.event_door, 3)
        self.assertEqual(response.event_direction, 1)
        self.assertEqual(response.event_card, 8165537)
        self.assertEqual(response.event_timestamp, None)
        self.assertEqual(response.event_reason, 44)
        self.assertEqual(response.sequence_no, 0)

    def test_decode_get_time_response(self):
        """
        Tests a get-time response with an invalid date/time.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x32, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x20, 0x23, 0x01, 0x02, 0x12, 0x34, 0x56, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_time_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.datetime, datetime.datetime(2023, 1, 2, 12, 34, 56))

    def test_get_time_response_with_invalid_datetime(self):
        """
        Tests a get-time response with an invalid date/time.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x32, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_time_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.datetime, None)

    def test_get_card_response_with_invalid_dates(self):
        """
        Tests a get-card response with invalid start/end dates.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x5a, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xa0, 0x7a, 0x99, 0x00, 0x20, 0x00, 0x00, 0x00,
                  0x20, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_card_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.card_number, 10058400)
        self.assertEqual(response.start_date, None)
        self.assertEqual(response.end_date, None)
        self.assertEqual(response.door_1, 1)
        self.assertEqual(response.door_2, 1)
        self.assertEqual(response.door_3, 1)
        self.assertEqual(response.door_4, 1)
        self.assertEqual(response.pin, 0)

    def test_get_card_by_index_response_with_invalid_dates(self):
        """
        Tests a get-card-by-index response with invalid start/end dates.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x5c, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xa0, 0x7a, 0x99, 0x00, 0x20, 0x00, 0x00, 0x00,
                  0x20, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_card_by_index_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.card_number, 10058400)
        self.assertEqual(response.start_date, None)
        self.assertEqual(response.end_date, None)
        self.assertEqual(response.door_1, 1)
        self.assertEqual(response.door_2, 1)
        self.assertEqual(response.door_3, 1)
        self.assertEqual(response.door_4, 1)
        self.assertEqual(response.pin, 0)

    def test_get_event_response_with_invalid_timestamp(self):
        """
        Tests a get-event response with an invalid timestamp.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0xb0, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x11, 0x27, 0x00, 0x00, 0x20, 0x01, 0x01, 0x01,
                  0xea, 0xac, 0xcd, 0xe9, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x97, 0x2b, 0x6f, 0x58, 0x0e, 0x10, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_event_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.index, 10001)
        self.assertEqual(response.event_type, 32)
        self.assertEqual(response.access_granted, True)
        self.assertEqual(response.door, 1)
        self.assertEqual(response.direction, 1)
        self.assertEqual(response.card, 3922570474)
        self.assertEqual(response.timestamp, None)
        self.assertEqual(response.reason, 44)

    def test_get_time_profile_response_with_invalid_dates(self):
        """
        Tests a get-time-profile response with an invalid dates.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x98, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x1d, 0x20, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00,
                  0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x08, 0x30, 0x11, 0x30, 0x00, 0x00, 0x00, 0x00,
                  0x13, 0x45, 0x17, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_time_profile_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.profile_id, 29)
        self.assertEqual(response.start_date, None)
        self.assertEqual(response.end_date, None)
        self.assertEqual(response.monday, True)
        self.assertEqual(response.tuesday, False)
        self.assertEqual(response.wednesday, True)
        self.assertEqual(response.thursday, False)
        self.assertEqual(response.friday, True)
        self.assertEqual(response.saturday, False)
        self.assertEqual(response.sunday, False)
        self.assertEqual(response.segment_1_start, datetime.time(8, 30))
        self.assertEqual(response.segment_1_end, datetime.time(11, 30))
        self.assertEqual(response.segment_2_start, datetime.time(0, 0))
        self.assertEqual(response.segment_2_end, datetime.time(0, 0))
        self.assertEqual(response.segment_3_start, datetime.time(13, 45))
        self.assertEqual(response.segment_3_end, datetime.time(17, 0))
        self.assertEqual(response.linked_profile_id, 3)

    def test_decode_restore_default_parameters_response(self):
        """
        Tests a restore-default-parameters response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0xc8, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.restore_default_parameters_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.reset, True)

    # Ref. https://github.com/uhppoted/uhppoted-lib-python/issues/3
    def test_listen_event(self):
        """
        Tests a listen event.
        """
        # yapf: disable
        packet = bytearray([
            0x17, 0x20, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x46, 0x00, 0x00, 0x00, 0x02, 0x01, 0x03, 0x01,
            0x9f, 0x98, 0x7c, 0x00, 0x20, 0x24, 0x02, 0x22, 0x10, 0x23, 0x40, 0x2c, 0x01, 0x00, 0x00, 0x01,
            0x01, 0x00, 0x01, 0x01, 0x03, 0x10, 0x23, 0x40, 0x7b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x27, 0x0a, 0x05, 0x24, 0x02, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        event = decode.event(packet)

        self.assertEqual(event.controller, 405419896)
        self.assertEqual(event.system_date, datetime.date(2024, 2, 22))
        self.assertEqual(event.system_time, datetime.time(10, 23, 40))
        self.assertEqual(event.door_1_open, True)
        self.assertEqual(event.door_2_open, False)
        self.assertEqual(event.door_3_open, False)
        self.assertEqual(event.door_4_open, True)
        self.assertEqual(event.door_1_button, True)
        self.assertEqual(event.door_2_button, False)
        self.assertEqual(event.door_3_button, True)
        self.assertEqual(event.door_4_button, True)
        self.assertEqual(event.relays, 0x0A)
        self.assertEqual(event.inputs, 0x05)
        self.assertEqual(event.system_error, 3)
        self.assertEqual(event.special_info, 39)
        self.assertEqual(event.event_index, 70)
        self.assertEqual(event.event_type, 2)
        self.assertEqual(event.event_access_granted, True)
        self.assertEqual(event.event_door, 3)
        self.assertEqual(event.event_direction, 1)
        self.assertEqual(event.event_card, 8165535)
        self.assertEqual(event.event_timestamp, datetime.datetime(2024, 2, 22, 10, 23, 40))
        self.assertEqual(event.event_reason, 44)
        self.assertEqual(event.sequence_no, 123)

    def test_get_antipassback_response(self):
        """
        Tests a valid get-antipassback response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x86, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.get_antipassback_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.antipassback, 2)

    def test_set_antipassback_response(self):
        """
        Tests a valid set-antipassback response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0x84, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.set_antipassback_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.ok, True)

    def test_restore_default_parameters_response(self):
        """
        Tests a valid restore-default-parameters response.
        """
        # yapf: disable
        packet = bytearray([
                  0x17, 0xc8, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        response = decode.restore_default_parameters_response(packet)

        self.assertEqual(response.controller, 405419896)
        self.assertEqual(response.reset, True)


if __name__ == "__main__":
    unittest.main()
