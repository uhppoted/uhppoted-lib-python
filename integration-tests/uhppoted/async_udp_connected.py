'''
UHPPOTE UDP async function tests.

End-to-end tests for the uhppote functions over a connected UDP socket.
'''

import unittest
import socket
import struct
import threading
import time
import datetime

from ipaddress import IPv4Address

from uhppoted import uhppote_async as uhppote
from uhppoted import structs
from uhppoted.net import dump

from .stub import messages
from .expected import *

DEST_ADDR = '127.0.0.1:54321'
CONTROLLER = 405419896
CARD = 8165538
CARD_INDEX = 2
EVENT_INDEX = 29
TIME_PROFILE = 29
NO_TIMEOUT = struct.pack('ll', 0, 0)  # (infinite)


def handle(sock, bind, debug):
    '''
    Replies to received UDP packets with the matching response.
    '''
    never = struct.pack('ll', 0, 0)  # (infinite)

    try:
        sock.bind(bind)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, never)

        while True:
            (message, addr) = sock.recvfrom(1024)
            if len(message) == 64:
                if debug:
                    dump(message)
                for m in messages():
                    if bytes(m['request']) == message:
                        response = m['response']
                        if len(response) == 64:
                            sock.sendto(bytes(response), addr)
                        else:
                            for packet in response:
                                sock.sendto(bytes(packet), addr)
                        break
    except Exception as x:
        pass
    finally:
        sock.close()


class TestAsyncUDP(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(clazz):
        bind = '0.0.0.0'
        broadcast = '255.255.255.255:60000'
        listen = '0.0.0.0:60001'
        debug = False

        clazz.u = uhppote.UhppoteAsync(bind, broadcast, listen, debug)
        clazz._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        clazz._thread = threading.Thread(target=handle, args=(clazz._sock, ('0.0.0.0', 54321), False))

        clazz._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(clazz):
        clazz._sock.close()
        clazz._sock = None

    async def test_get_controller(self):
        '''
        Tests the get-controller function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        response = await self.u.get_controller(controller)

        self.assertEqual(response, GetControllerResponse)

    async def test_set_ip(self):
        '''
        Tests the set-ip function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        address = IPv4Address('192.168.1.100')
        netmask = IPv4Address('255.255.255.0')
        gateway = IPv4Address('192.168.1.1')

        response = await self.u.set_ip(controller, address, netmask, gateway)

        self.assertEqual(response, SetIPResponse)

    async def test_get_time(self):
        '''
        Tests the get-time function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        response = await self.u.get_time(controller)

        self.assertEqual(response, GetTimeResponse)

    async def test_set_time(self):
        '''
        Tests the set-time function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        time = datetime.datetime(2021, 5, 28, 14, 56, 14)

        response = await self.u.set_time(controller, time)

        self.assertEqual(response, SetTimeResponse)

    async def test_get_status(self):
        '''
        Tests the get-status function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        response = await self.u.get_status(controller)

        self.assertEqual(response, GetStatusResponse)

    async def test_get_listener(self):
        '''
        Tests the get-listener function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        dest = DEST_ADDR

        response = await self.u.get_listener(controller)

        self.assertEqual(response, GetListenerResponse)

    async def test_set_listener(self):
        '''
        Tests the set-listener function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        address = IPv4Address('192.168.1.100')
        port = 60001
        interval = 15

        response = await self.u.set_listener(controller, address, port, interval)

        self.assertEqual(response, SetListenerResponse)

    async def test_set_listener_without_interval(self):
        '''
        Tests the set-listener function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        address = IPv4Address('192.168.1.100')
        port = 60001

        response = await self.u.set_listener(controller, address, port)

        self.assertEqual(response, SetListenerResponse)

    async def test_get_door_control(self):
        '''
        Tests the get-door-control function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        door = 3

        response = await self.u.get_door_control(controller, door)

        self.assertEqual(response, GetDoorControlResponse)

    async def test_set_door_control(self):
        '''
        Tests the set-door-control function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        door = 3
        delay = 4
        mode = 2

        response = await self.u.set_door_control(controller, door, mode, delay)

        self.assertEqual(response, SetDoorControlResponse)

    async def test_open_door(self):
        '''
        Tests the open-door function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        door = 3

        response = await self.u.open_door(controller, door)

        self.assertEqual(response, OpenDoorResponse)

    async def test_get_cards(self):
        '''
        Tests the get-cards function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        response = await self.u.get_cards(controller)

        self.assertEqual(response, GetCardsResponse)

    async def test_get_card(self):
        '''
        Tests the get-card function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        card = CARD

        response = await self.u.get_card(controller, card)

        self.assertEqual(response, GetCardResponse)

    async def test_get_card_by_index(self):
        '''
        Tests the get-card-by-index function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        index = CARD_INDEX

        response = await self.u.get_card_by_index(controller, index)

        self.assertEqual(response, GetCardByIndexResponse)

    async def test_put_card(self):
        '''
        Tests the put-card function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        card = 123456789
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2025, 12, 31)
        door1 = 1
        door2 = 0
        door3 = 29
        door4 = 1
        PIN = 7531

        response = await self.u.put_card(controller, card, start, end, door1, door2, door3, door4, PIN)

        self.assertEqual(response, PutCardResponse)

    async def test_delete_card(self):
        '''
        Tests the delete-card function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        card = CARD
        response = await self.u.delete_card(controller, card)

        self.assertEqual(response, DeleteCardResponse)

    async def test_delete_all_cards(self):
        '''
        Tests the delete-all-cards function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        response = await self.u.delete_all_cards(controller)

        self.assertEqual(response, DeleteAllCardsResponse)

    async def test_get_event(self):
        '''
        Tests the get-event function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        index = EVENT_INDEX
        response = await self.u.get_event(controller, index)

        self.assertEqual(response, GetEventResponse)

    async def test_get_event_index(self):
        '''
        Tests the get-event-index function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        response = await self.u.get_event_index(controller)

        self.assertEqual(response, GetEventIndexResponse)

    async def test_set_event_index(self):
        '''
        Tests the set-event-index function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        index = EVENT_INDEX
        response = await self.u.set_event_index(controller, index)

        self.assertEqual(response, SetEventIndexResponse)

    async def test_record_special_events(self):
        '''
        Tests the record-special-events function with a valid dest_addr.
        '''
        controller = (CONTROLLER, DEST_ADDR)
        enabled = True
        response = await self.u.record_special_events(controller, enabled)

        self.assertEqual(response, RecordSpecialEventsResponse)
