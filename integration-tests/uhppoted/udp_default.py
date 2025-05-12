'''
UHPPOTE function tests.

End-to-end tests for the uhppote functions over broadcast UDP.
'''

import unittest
import socket
import struct
import threading
import time
import datetime

from ipaddress import IPv4Address

from uhppoted import uhppote
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


class TestUDPWithDestAddr(unittest.TestCase):

    @classmethod
    def setUpClass(clazz):
        bind = '0.0.0.0'
        broadcast = '255.255.255.255:60000'
        listen = '0.0.0.0:60001'
        debug = False

        clazz.u = uhppote.Uhppote(bind, broadcast, listen, debug)
        clazz._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        clazz._thread = threading.Thread(target=handle, args=(clazz._sock, ('0.0.0.0', 60000), False))

        clazz._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(clazz):
        clazz._sock.close()
        clazz._sock = None

    def test_get_all_controllers(self):
        '''
        Tests the get-all-controllers function with defaults.
        '''
        controller = CONTROLLER
        response = self.u.get_all_controllers()

        self.assertEqual(response, GetControllersResponse)

    def test_get_controller(self):
        '''
        Tests the get-controller function with defaults.
        '''
        controller = CONTROLLER
        response = self.u.get_controller(controller)

        self.assertEqual(response, GetControllerResponse)

    def test_set_ip(self):
        '''
        Tests the set-ip function with defaults.
        '''
        controller = CONTROLLER
        address = IPv4Address('192.168.1.100')
        netmask = IPv4Address('255.255.255.0')
        gateway = IPv4Address('192.168.1.1')

        response = self.u.set_ip(controller, address, netmask, gateway)

        self.assertEqual(response, SetIPResponse)

    def test_get_time(self):
        '''
        Tests the get-time function with defaults.
        '''
        controller = CONTROLLER
        response = self.u.get_time(controller)

        self.assertEqual(response, GetTimeResponse)

    def test_set_time(self):
        '''
        Tests the set-time function with defaults.
        '''
        controller = CONTROLLER
        time = datetime.datetime(2021, 5, 28, 14, 56, 14)

        response = self.u.set_time(controller, time)

        self.assertEqual(response, SetTimeResponse)

    def test_get_status(self):
        '''
        Tests the get-status function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.get_status(controller)

        self.assertEqual(response, GetStatusResponse)

    def test_get_listener(self):
        '''
        Tests the get-listener function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.get_listener(controller)

        self.assertEqual(response, GetListenerResponse)

    def test_set_listener(self):
        '''
        Tests the set-listener function with defaults.
        '''
        controller = CONTROLLER
        address = IPv4Address('192.168.1.100')
        port = 60001
        interval = 15

        response = self.u.set_listener(controller, address, port, interval)

        self.assertEqual(response, SetListenerResponse)

    def test_set_listener_without_interval(self):
        '''
        Tests the set-listener function with defaults.
        '''
        controller = CONTROLLER
        address = IPv4Address('192.168.1.100')
        port = 60001

        response = self.u.set_listener(controller, address, port)

        self.assertEqual(response, SetListenerResponse)

    def test_get_door_control(self):
        '''
        Tests the get-door-control function with defaults.
        '''
        controller = CONTROLLER
        door = 3

        response = self.u.get_door_control(controller, door)

        self.assertEqual(response, GetDoorControlResponse)

    def test_set_door_control(self):
        '''
        Tests the set-door-control function with defaults.
        '''
        controller = CONTROLLER
        door = 3
        delay = 4
        mode = 2

        response = self.u.set_door_control(controller, door, mode, delay)

        self.assertEqual(response, SetDoorControlResponse)

    def test_open_door(self):
        '''
        Tests the open-door function with defaults.
        '''
        controller = CONTROLLER
        door = 3

        response = self.u.open_door(controller, door)

        self.assertEqual(response, OpenDoorResponse)

    def test_get_cards(self):
        '''
        Tests the get-cards function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.get_cards(controller)

        self.assertEqual(response, GetCardsResponse)

    def test_get_card(self):
        '''
        Tests the get-card function with defaults.
        '''
        controller = CONTROLLER
        card = CARD

        response = self.u.get_card(controller, card)

        self.assertEqual(response, GetCardResponse)

    def test_get_card_by_index(self):
        '''
        Tests the get-card-by-index function with defaults.
        '''
        controller = CONTROLLER
        index = CARD_INDEX

        response = self.u.get_card_by_index(controller, index)

        self.assertEqual(response, GetCardByIndexResponse)

    def test_put_card(self):
        '''
        Tests the put-card function with defaults.
        '''
        controller = CONTROLLER
        card = 123456789
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2025, 12, 31)
        door1 = 1
        door2 = 0
        door3 = 29
        door4 = 1
        PIN = 7531

        response = self.u.put_card(controller, card, start, end, door1, door2, door3, door4, PIN)

        self.assertEqual(response, PutCardResponse)

    def test_delete_card(self):
        '''
        Tests the delete-card function with defaults.
        '''
        controller = CONTROLLER
        card = CARD

        response = self.u.delete_card(controller, card)

        self.assertEqual(response, DeleteCardResponse)

    def test_delete_all_cards(self):
        '''
        Tests the delete-all-cards function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.delete_all_cards(controller)

        self.assertEqual(response, DeleteAllCardsResponse)

    def test_get_event(self):
        '''
        Tests the get-event function with defaults.
        '''
        controller = CONTROLLER
        index = EVENT_INDEX

        response = self.u.get_event(controller, index)

        self.assertEqual(response, GetEventResponse)

    def test_get_event_index(self):
        '''
        Tests the get-event-index function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.get_event_index(controller)

        self.assertEqual(response, GetEventIndexResponse)

    def test_set_event_index(self):
        '''
        Tests the set-event-index function with defaults.
        '''
        controller = CONTROLLER
        index = EVENT_INDEX

        response = self.u.set_event_index(controller, index)

        self.assertEqual(response, SetEventIndexResponse)

    def test_record_special_events(self):
        '''
        Tests the record-special-events function with defaults.
        '''
        controller = CONTROLLER
        enabled = True

        response = self.u.record_special_events(controller, enabled)

        self.assertEqual(response, RecordSpecialEventsResponse)

    def test_get_time_profile(self):
        '''
        Tests the get-time-profile function with defaults.
        '''
        controller = CONTROLLER
        profile = TIME_PROFILE

        response = self.u.get_time_profile(controller, profile)

        self.assertEqual(response, GetTimeProfileResponse)

    def test_set_time_profile(self):
        '''
        Tests the set-time-profile function with defaults.
        '''
        controller = CONTROLLER
        profile_id = TIME_PROFILE
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 12, 31)
        monday = True
        tuesday = False
        wednesday = True
        thursday = False
        friday = True
        saturday = False
        sunday = False
        segment_1_start = datetime.time(8, 30)
        segment_1_end = datetime.time(11, 45)
        segment_2_start = datetime.time(13, 15)
        segment_2_end = datetime.time(17, 25)
        segment_3_start = None
        segment_3_end = None
        linked_profile_id = 3

        response = self.u.set_time_profile(controller, profile_id, start_date, end_date, monday, tuesday, wednesday,
                                           thursday, friday, saturday, sunday, segment_1_start, segment_1_end,
                                           segment_2_start, segment_2_end, segment_3_start, segment_3_end,
                                           linked_profile_id)

        self.assertEqual(response, SetTimeProfileResponse)

    def test_delete_all_time_profiles(self):
        '''
        Tests the delete-all-time-profiles function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.delete_all_time_profiles(controller)

        self.assertEqual(response, DeleteAllTimeProfilesResponse)

    def test_add_task(self):
        '''
        Tests the add-task function with defaults.
        '''
        controller = CONTROLLER
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 12, 31)
        monday = True
        tuesday = False
        wednesday = True
        thursday = False
        friday = True
        saturday = False
        sunday = False
        start_time = datetime.time(8, 30)
        door = 3
        task_type = 4
        more_cards = 17

        response = self.u.add_task(controller, start_date, end_date, monday, tuesday, wednesday, thursday, friday,
                                   saturday, sunday, start_time, door, task_type, more_cards)

        self.assertEqual(response, AddTaskResponse)

    def test_refresh_tasklist(self):
        '''
        Tests the refresh-tasklist function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.refresh_tasklist(controller)

        self.assertEqual(response, RefreshTaskListResponse)

    def test_clear_tasklist(self):
        '''
        Tests the clear-tasklist function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.clear_tasklist(controller)

        self.assertEqual(response, ClearTaskListResponse)

    def test_set_pc_control(self):
        '''
        Tests the set-pc-control function with defaults.
        '''
        controller = CONTROLLER
        enable = True

        response = self.u.set_pc_control(controller, enable)

        self.assertEqual(response, SetPCControlResponse)

    def test_set_interlock(self):
        '''
        Tests the set-interlock function with defaults.
        '''
        controller = CONTROLLER
        interlock = 8

        response = self.u.set_interlock(controller, interlock)

        self.assertEqual(response, SetInterlockResponse)

    def test_activate_keypads(self):
        '''
        Tests the activate-keypads function with defaults.
        '''
        controller = CONTROLLER
        reader1 = True
        reader2 = True
        reader3 = False
        reader4 = True

        response = self.u.activate_keypads(controller, reader1, reader2, reader3, reader4)

        self.assertEqual(response, ActivateKeypadsResponse)

    def test_set_door_passcodes(self):
        '''
        Tests the set-door-passcodes function with defaults.
        '''
        controller = CONTROLLER
        door = 3
        passcode1 = 12345
        passcode2 = 0
        passcode3 = 999999
        passcode4 = 54321

        response = self.u.set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4)

        self.assertEqual(response, SetDoorPasscodesResponse)

    def test_get_antipassback(self):
        '''
        Tests the get_antipassback function with defaults.
        '''
        controller = CONTROLLER
        response = self.u.get_antipassback(controller)

        self.assertEqual(response, GetAntiPassbackResponse)

    def test_set_antipassback(self):
        '''
        Tests the set_antipassback function with defaults.
        '''
        controller = CONTROLLER
        antipassback = 2
        response = self.u.set_antipassback(controller, antipassback)

        self.assertEqual(response, SetAntiPassbackResponse)

    def test_restore_default_parameters(self):
        '''
        Tests the restore-default-parameters function with defaults.
        '''
        controller = CONTROLLER

        response = self.u.restore_default_parameters(controller)

        self.assertEqual(response, RestoreDefaultParametersResponse)
