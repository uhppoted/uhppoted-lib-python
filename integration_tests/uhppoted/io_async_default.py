"""
UHPPOTE async low-level I/O function tests.

End-to-end tests for the low-level async uhppote functions over broadcast UDP.
"""

import unittest
import socket
import struct
import threading
import time
import datetime

from uhppoted import uhppote_async as uhppote
from uhppoted import io
from uhppoted import structs
from uhppoted.net import dump

from uhppoted.structs import Weekdays
from uhppoted.structs import DoorMode
from uhppoted.structs import FirstCard

from .stub import messages  # pylint: disable=relative-beyond-top-level

CONTROLLER = 405419896
CARD = 8165538
CARD_NOT_FOUND = 10058399
CARD_INDEX = 2
CARD_INDEX_NOT_FOUND = 10001
CARD_INDEX_DELETED = 10002
EVENT_INDEX = 29
EVENT_INDEX_NOT_FOUND = 200
EVENT_INDEX_OVERWRITTEN = 73
TIME_PROFILE = 29
TIME_PROFILE_NOT_FOUND = 92


def handle(sock, bind, debug):
    """
    Replies to received UDP packets with the matching response.
    """
    never = struct.pack("ll", 0, 0)  # (infinite)

    def received(message, addr):
        if debug:
            dump(message)
        for m in messages():
            if bytes(m["request"]) == message:
                response = m["response"]
                if len(response) == 64:
                    sock.sendto(bytes(response), addr)
                else:
                    for packet in response:
                        sock.sendto(bytes(packet), addr)
                break

    try:
        sock.bind(bind)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, never)

        while True:
            message, addr = sock.recvfrom(1024)
            if len(message) == 64:
                received(message, addr)

    except Exception:  # pylint: disable=broad-exception-caught
        pass
    finally:
        sock.close()


class TestAsyncUDP(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for the UDP async transport with controller serial number only.
    """

    @classmethod
    def setUpClass(cls):
        bind = "0.0.0.0"
        broadcast = "255.255.255.255:60000"
        listen = "0.0.0.0:60001"
        debug = False

        cls.u = uhppote.UhppoteAsync(bind, broadcast, listen, debug)
        cls._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        cls._thread = threading.Thread(target=handle, args=(cls._sock, ("0.0.0.0", 60000), False))

        cls._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls._sock.close()
        cls._sock = None

    async def test_set_firstcard(self):
        """
        Tests the set_firstcard function with defaults.
        """
        controller = CONTROLLER
        door = 3

        firstcard = FirstCard(
            start_time=datetime.time(8, 30),
            end_time=datetime.time(17, 45),
            active_mode=DoorMode.NORMALLY_OPEN,
            inactive_mode=DoorMode.FIRSTCARD_ONLY,
            weekdays=Weekdays(
                monday=True,
                tuesday=True,
                wednesday=False,
                thursday=True,
                friday=False,
                saturday=False,
                sunday=True,
            ),
        )

        response = await io.set_firstcard_async(self.u, controller, door, firstcard)
        expected = structs.SetFirstCardResponse(controller=CONTROLLER, ok=True)

        self.assertEqual(response, expected)
