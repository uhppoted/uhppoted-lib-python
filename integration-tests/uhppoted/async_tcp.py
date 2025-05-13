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

DEST_ADDR = '127.0.0.1:12345'
CONTROLLER = 405419896
CARD = 8165538
CARD_INDEX = 2
EVENT_INDEX = 29
TIME_PROFILE = 29
NO_TIMEOUT = struct.pack('ll', 0, 0)  # (infinite)


def handle(sock, bind, debug):
    '''
    Replies to received TCP packets with the matching response.
    '''
    never = struct.pack('ll', 0, 0)  # (infinite)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(bind)
    sock.listen(1)

    try:
        while True:
            (connection, addr) = sock.accept()
            try:
                connection.settimeout(0.5)
                message = connection.recv(1024)

                if len(message) == 64:
                    if debug:
                        dump(message)
                    for m in messages():
                        if bytes(m['request']) == message:
                            connection.sendall(bytes(m['response']))
                            break

            except Exception as x:
                print('WARN', x)
            finally:
                connection.close()
    except Exception as xx:
        pass


class TestAsyncUDP(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(clazz):
        bind = '0.0.0.0'
        broadcast = '255.255.255.255:60000'
        listen = '0.0.0.0:60001'
        debug = False

        clazz.u = uhppote.UhppoteAsync(bind, broadcast, listen, debug)
        clazz._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        clazz._thread = threading.Thread(target=handle, args=(clazz._sock, ('', 12345), False))

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
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        response = await self.u.get_controller(controller)

        self.assertEqual(response, GetControllerResponse)

    async def test_set_ip(self):
        '''
        Tests the set-ip function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        address = IPv4Address('192.168.1.100')
        netmask = IPv4Address('255.255.255.0')
        gateway = IPv4Address('192.168.1.1')

        response = await self.u.set_ip(controller, address, netmask, gateway)

        self.assertEqual(response, SetIPResponse)

    async def test_get_time(self):
        '''
        Tests the get-time function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        response = await self.u.get_time(controller)

        self.assertEqual(response, GetTimeResponse)

    async def test_set_time(self):
        '''
        Tests the set-time function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        time = datetime.datetime(2021, 5, 28, 14, 56, 14)
        response = await self.u.set_time(controller, time)

        self.assertEqual(response, SetTimeResponse)

    async def test_get_status(self):
        '''
        Tests the get-status function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        response = await self.u.get_status(controller)

        self.assertEqual(response, GetStatusResponse)

    async def test_get_listener(self):
        '''
        Tests the get-listener function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        response = await self.u.get_listener(controller)

        self.assertEqual(response, GetListenerResponse)

    async def test_set_listener(self):
        '''
        Tests the set-listener function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        address = IPv4Address('192.168.1.100')
        port = 60001
        interval = 15
        response = await self.u.set_listener(controller, address, port, interval)

        self.assertEqual(response, SetListenerResponse)

    async def test_set_listener_without_interval(self):
        '''
        Tests the set-listener function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        address = IPv4Address('192.168.1.100')
        port = 60001

        response = await self.u.set_listener(controller, address, port)
        self.assertEqual(response, SetListenerResponse)

    async def test_get_door_control(self):
        '''
        Tests the get-door-control function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        door = 3
        response = await self.u.get_door_control(controller, door)

        self.assertEqual(response, GetDoorControlResponse)

    async def test_set_door_control(self):
        '''
        Tests the set-door-control function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        door = 3
        delay = 4
        mode = 2

        response = await self.u.set_door_control(controller, door, mode, delay)

        self.assertEqual(response, SetDoorControlResponse)

    async def test_open_door(self):
        '''
        Tests the open-door function with defaults.
        '''
        controller = (CONTROLLER, DEST_ADDR, 'tcp')
        door = 3
        response = await self.u.open_door(controller, door)

        self.assertEqual(response, OpenDoorResponse)
