'''
UHPPOTE request packet encoder unit tests.

Tests the packet encoding functions.
'''

import unittest
import datetime

from ipaddress import IPv4Address
from uhppoted import encode


class TestEncode(unittest.TestCase):

    def test_set_listener_request(self):
        '''
        Tests message encoding for a set-listener request without an auto-send interval.
        '''
        # yapf: disable
        expected = bytearray([
            0x17, 0x90, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xc0, 0xa8, 0x01, 0x64, 0x61, 0xea, 0x0f, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        request = encode.set_listener_request(405419896, IPv4Address('192.168.1.100'), 60001, 15)

        self.assertEqual(request, expected)

    def test_set_listener_request_without_interval(self):
        '''
        Tests message encoding for a set-listener request without an auto-send interval.
        '''
        # yapf: disable
        expected = bytearray([
            0x17, 0x90, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xc0, 0xa8, 0x01, 0x64, 0x61, 0xea, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        request = encode.set_listener_request(405419896, IPv4Address('192.168.1.100'), 60001)

        self.assertEqual(request, expected)

    def test_get_antipassback_request(self):
        '''
        Tests message encoding for a get-antipassback request.
        '''
        # yapf: disable
        expected = bytearray([
            0x17, 0x86, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        request = encode.get_antipassback_request(405419896)

        self.assertEqual(request, expected)

    def test_set_antipassback_request(self):
        '''
        Tests message encoding for a set-antipassback request.
        '''
        # yapf: disable
        expected = bytearray([
            0x17, 0x84, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        request = encode.set_antipassback_request(405419896, 2)

        self.assertEqual(request, expected)

    def test_restore_default_parameters_request(self):
        '''
        Tests message encoding for a restore-default-parameters request.
        '''
        # yapf: disable
        expected = bytearray([
            0x17, 0xc8, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x55, 0xaa, 0xaa, 0x55, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        # yapf: enable

        request = encode.restore_default_parameters_request(405419896)

        self.assertEqual(request, expected)


if __name__ == '__main__':
    unittest.main()
