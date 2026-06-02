"""
UHPPOTE low-level I/O function tests.

End-to-end tests for the uhppote functions over TCP/IP.
"""

import unittest
import socket
import threading
import time
import datetime

from uhppoted import uhppote
from uhppoted.net import dump
from uhppoted import io
from uhppoted import structs

from uhppoted.structs import Weekdays
from uhppoted.structs import DoorMode
from uhppoted.structs import FirstCard

from .stub import messages  # pylint: disable=relative-beyond-top-level

DEST_ADDR = "127.0.0.1:12345"
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
    Replies to received TCP packets with the matching response.
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(bind)
    sock.listen(1)

    def received(message):
        if debug:
            dump(message)
        for m in messages():
            if bytes(m["request"]) == message:
                connection.sendall(bytes(m["response"]))
                break

    try:
        while True:
            connection, _ = sock.accept()
            try:
                connection.settimeout(0.5)
                message = connection.recv(1024)

                if len(message) == 64:
                    received(message)

            except Exception as exc:  # pylint: disable=broad-exception-caught
                print("WARN", exc)
            finally:
                connection.close()
    except Exception:  # pylint: disable=broad-exception-caught
        pass


class TestUhppoteWithTCP(unittest.TestCase):
    """
    Test suite for the TCP transport.
    """

    @classmethod
    def setUpClass(cls):
        bind = "0.0.0.0"
        broadcast = "255.255.255.255:60000"
        listen = "0.0.0.0:60001"
        debug = False

        cls.u = uhppote.Uhppote(bind, broadcast, listen, debug)
        cls._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        cls._thread = threading.Thread(target=handle, args=(cls._sock, ("", 12345), False))

        cls._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls._sock.close()
        cls._sock = None

    def test_set_firstcard(self):
        """
        Tests the set_firstcard function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
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

        response = io.set_firstcard(self.u, controller, door, firstcard)
        expected = structs.SetFirstCardResponse(controller=CONTROLLER, ok=True)

        self.assertEqual(response, expected)
