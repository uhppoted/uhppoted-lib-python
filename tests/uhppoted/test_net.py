"""
UDP unit tests.

Tests the internal conversion functions.
"""

import unittest

from uhppoted.net import timeout_to_seconds
from uhppoted.net import disambiguate
from uhppoted.net import Controller


class TestNet(unittest.TestCase):

    def test_timeout_to_seconds(self):
        """
        Tests the conversion of valid and invalid timeout values.
        """
        tests = [
            (1, 1),
            (0.05, 0.05),
            (30, 30),
            (0, 2.5),
            (60, 2.5),
            ("12.5", 12.5),
            (None, 2.5),
            ("qwerty", 2.5),
            ("5s", 2.5),
        ]

        for test in tests:
            self.assertEqual(timeout_to_seconds(test[0]), test[1])

    def test_disambiguate(self):
        """
        Tests disambiguating a controller arg to a 'Controller' named tuple with id, address and
        protocol fields.
        """
        tests = [
            (405419896, Controller(405419896, None, "udp")),
            ((405419896, "192.168.1.100", "udp"), Controller(405419896, "192.168.1.100", "udp")),
            ((405419896, "192.168.1.100", "UDP"), Controller(405419896, "192.168.1.100", "udp")),
            ((405419896, "192.168.1.100", "tcp"), Controller(405419896, "192.168.1.100", "tcp")),
            ((405419896, "192.168.1.100", "TCP"), Controller(405419896, "192.168.1.100", "tcp")),
            ((405419896, "192.168.1.100", "noeyedeer"), Controller(405419896, "192.168.1.100", "udp")),
            ((405419896, "192.168.1.100"), Controller(405419896, "192.168.1.100", "udp")),
            ((405419896), Controller(405419896, None, "udp")),
            (Controller(405419896, "192.168.1.100", "udp"), Controller(405419896, "192.168.1.100", "udp")),
            (Controller(405419896, "192.168.1.100", "tcp"), Controller(405419896, "192.168.1.100", "tcp")),
        ]

        for test in tests:
            self.assertEqual(disambiguate(test[0]), test[1])


if __name__ == "__main__":
    unittest.main()
