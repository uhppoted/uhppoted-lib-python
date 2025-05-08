'''
UHPPOTE async function tests.

End-to-end tests for the uhppote functions.
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
        clazz._thread = threading.Thread(target=handle, args=(clazz._sock, ('0.0.0.0', 60000), False))

        clazz._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(clazz):
        clazz._sock.close()
        clazz._sock = None

    async def test_get_all_controllers(self):
        '''
        Tests the get-all-controllers function with defaults.
        '''
        controller = CONTROLLER
        response = await self.u.get_all_controllers()

        self.assertEqual(response, GetControllersResponse)
