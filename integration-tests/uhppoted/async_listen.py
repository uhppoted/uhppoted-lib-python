"""
UHPPOTE async function tests.

End-to-end tests for the uhppote event listener.
"""

import asyncio
import datetime
import errno
import socket
import time
import unittest

# pylint: disable=import-error
from uhppoted import uhppote_async as uhppote
from uhppoted import structs

# fmt: off
EVENTS = [
    # normal event
    bytes([
        0x17, 0x20, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0x30, 0x26, 0x01, 0x00, 0x03, 0x01, 0x04, 0x02,
        0xa0, 0x7a, 0x99, 0x00, 0x20, 0x24, 0x11, 0x10, 0x12, 0x34, 0x56, 0x06, 0x01, 0x00, 0x01, 0x01,
        0x01, 0x01, 0x00, 0x01, 0x1b, 0x14, 0x37, 0x53, 0xe3, 0x55, 0x00, 0x00, 0x21, 0x00, 0x00, 0x00,
        0x9a, 0x07, 0x09, 0x24, 0x11, 0x13, 0x00, 0x00, 0x93, 0x26, 0x04, 0x88, 0x08, 0x92, 0x00, 0x00,
    ]),

    # v6.62 event
    bytes([
        0x19, 0x20, 0x00, 0x00, 0x41, 0x78, 0x1e, 0x12, 0x30, 0x26, 0x01, 0x00, 0x03, 0x01, 0x04, 0x02,
        0xa0, 0x7a, 0x99, 0x00, 0x20, 0x24, 0x11, 0x10, 0x12, 0x34, 0x56, 0x06, 0x01, 0x00, 0x01, 0x01,
        0x01, 0x01, 0x00, 0x01, 0x1b, 0x14, 0x37, 0x53, 0xe3, 0x55, 0x00, 0x00, 0x21, 0x00, 0x00, 0x00,
        0x9a, 0x07, 0x09, 0x24, 0x11, 0x13, 0x00, 0x00, 0x93, 0x26, 0x04, 0x88, 0x08, 0x92, 0x00, 0x00,
    ]),

    # event without event
    bytes([
        0x17, 0x20, 0x00, 0x00, 0x79, 0x37, 0x2a, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x01,
        0x01, 0x01, 0x00, 0x01, 0x1b, 0x14, 0x37, 0x53, 0xe3, 0x55, 0x00, 0x00, 0x21, 0x00, 0x00, 0x00,
        0x9a, 0x07, 0x09, 0x24, 0x11, 0x13, 0x00, 0x00, 0x93, 0x26, 0x04, 0x88, 0x08, 0x92, 0x00, 0x00,
    ]),

    # error event
    bytes([
        0x17, 0xff, 0x00, 0x00, 0x78, 0x37, 0x2a, 0x18, 0xc8, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x01,
        0x50, 0xff, 0x0f, 0x00, 0x20, 0x24, 0x12, 0x13, 0x10, 0x23, 0x27, 0x12, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x23, 0x27, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x24, 0x12, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]),
]
# fmt: on

EXPECTED = [
    # normal event
    structs.Event(
        controller=405419896,
        system_date=datetime.date(2024, 11, 13),
        system_time=datetime.time(14, 37, 53),
        door_1_open=True,
        door_2_open=False,
        door_3_open=True,
        door_4_open=True,
        door_1_button=True,
        door_2_button=True,
        door_3_button=False,
        door_4_button=True,
        relays=7,
        inputs=9,
        system_error=27,
        special_info=154,
        event_index=75312,
        event_type=3,
        event_access_granted=True,
        event_door=4,
        event_direction=2,
        event_card=10058400,
        event_timestamp=datetime.datetime(2024, 11, 10, 12, 34, 56),
        event_reason=6,
        sequence_no=21987,
    ),
    #  v6.62 event
    structs.Event(
        controller=303986753,
        system_date=datetime.date(2024, 11, 13),
        system_time=datetime.time(14, 37, 53),
        door_1_open=True,
        door_2_open=False,
        door_3_open=True,
        door_4_open=True,
        door_1_button=True,
        door_2_button=True,
        door_3_button=False,
        door_4_button=True,
        relays=7,
        inputs=9,
        system_error=27,
        special_info=154,
        event_index=75312,
        event_type=3,
        event_access_granted=True,
        event_door=4,
        event_direction=2,
        event_card=10058400,
        event_timestamp=datetime.datetime(2024, 11, 10, 12, 34, 56),
        event_reason=6,
        sequence_no=21987,
    ),
    # event without event
    structs.Event(
        controller=405419897,
        system_date=datetime.date(2024, 11, 13),
        system_time=datetime.time(14, 37, 53),
        door_1_open=True,
        door_2_open=False,
        door_3_open=True,
        door_4_open=True,
        door_1_button=True,
        door_2_button=True,
        door_3_button=False,
        door_4_button=True,
        relays=7,
        inputs=9,
        system_error=27,
        special_info=154,
        event_index=0,
        event_type=0,
        event_access_granted=False,
        event_door=0,
        event_direction=0,
        event_card=0,
        event_timestamp=None,
        event_reason=0,
        sequence_no=21987,
    ),
]


class TestAsyncListen(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for the UDP async event listener.
    """

    @classmethod
    def setUpClass(cls):
        bind = "0.0.0.0"
        broadcast = "255.255.255.255:60000"
        listen = "0.0.0.0:60007"
        debug = False

        cls.u = uhppote.UhppoteAsync(bind, broadcast, listen, debug)

        time.sleep(1)

    async def test_listen(self):
        """
        Tests the event listener.
        """
        expected = {
            "events": EXPECTED,
            "errors": ["invalid reply function code (ff)"],
        }

        events = []
        errors = []
        close = asyncio.Event()

        async def stop():
            await asyncio.sleep(1.25)
            close.set()

        async def on_event(event):
            if event is not None:
                events.append(event)

        async def on_error(error):
            if error is not None:
                errors.append(f"{error}")

        async def send():
            for evt in EVENTS:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.sendto(evt, ("127.0.0.1", 60007))
                await asyncio.sleep(0.1)

        stopping = asyncio.create_task(stop())
        listener = asyncio.create_task(self.u.listen(on_event, on_error=on_error, close=close))
        await asyncio.sleep(0.1)
        sender = asyncio.create_task(send())

        await asyncio.gather(stopping, listener, sender)

        self.assertEqual(events, expected["events"])
        self.assertEqual(errors, expected["errors"])

    async def test_address_in_use(self):
        """
        Tests the event listener with a socket that is already in use.
        """
        close = asyncio.Event()

        async def on_event():
            pass

        async def bind():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0) as sock:
                sock.bind(("127.0.0.1", 60007))
                while True:
                    await asyncio.sleep(1)

        bound = asyncio.create_task(bind())
        await asyncio.sleep(0.1)

        with self.assertRaises(OSError) as exc:
            await self.u.listen(on_event, close=close)

        bound.cancel()

        self.assertEqual(exc.exception.errno, errno.EADDRINUSE)
