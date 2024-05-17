'''
UHPPOTE function tests.

End-to-end tests for the uhppote functions.
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
            (message,addr) = sock.recvfrom(1024)
            if len(message) == 64:
                if debug:
                    dump(message)
                for m in messages():
                    if bytes(m['request']) == message:
                        sock.sendto(bytes(m['response']), addr)
                        break
    except Exception as x:
        pass
    finally:
        sock.close()

class TestUhppoteWithDestAddr(unittest.TestCase):
    def setUp(self):
        bind = '0.0.0.0'
        broadcast = '255.255.255.255:60000'
        listen = '0.0.0.0:60001'
        debug = False

        self.u = uhppote.Uhppote(bind, broadcast, listen, debug)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self._thread = threading.Thread(target = handle, args = (self._sock,('127.0.0.1', 54321), False))

        self._thread.start()
        time.sleep(1)


    def tearDown(self):
        self._sock.close()
        pass

    def test_get_controller(self):
        '''
        Tests the get-controller function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR
        response = self.u.get_controller(controller, dest_addr=dest)

        self.assertEqual(response, GetControllerResponse)

    def test_set_ip(self):
        '''
        Tests the set-ip function with a valid dest_addr.
        '''
        controller = CONTROLLER
        address = IPv4Address('192.168.1.100')
        netmask = IPv4Address('255.255.255.0')
        gateway = IPv4Address('192.168.1.1')
        dest = DEST_ADDR

        response = self.u.set_ip(controller, address, netmask, gateway, dest_addr=dest)

        self.assertEqual(response, SetIPResponse)

    def test_get_time(self):
        '''
        Tests the get-time function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.get_time(controller, dest_addr=dest)

        self.assertEqual(response, GetTimeResponse)

    def test_set_time(self):
        '''
        Tests the set-time function with a valid dest_addr.
        '''
        controller = CONTROLLER
        time = datetime.datetime(2021, 5, 28, 14, 56, 14)
        dest = DEST_ADDR

        response = self.u.set_time(controller, time, dest_addr=dest)

        self.assertEqual(response, SetTimeResponse)

    def test_get_status(self):
        '''
        Tests the get-status function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.get_status(controller, dest_addr=dest)

        self.assertEqual(response, GetStatusResponse)

    def test_get_listener(self):
        '''
        Tests the get-listener function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.get_listener(controller, dest_addr=dest)

        self.assertEqual(response, GetListenerResponse)

    def test_set_listener(self):
        '''
        Tests the set-listener function with a valid dest_addr.
        '''
        controller = CONTROLLER
        address = IPv4Address('192.168.1.100')
        port = 60001
        dest = DEST_ADDR

        response = self.u.set_listener(controller, address, port, dest_addr=dest)

        self.assertEqual(response, SetListenerResponse)

    def test_get_door_control(self):
        '''
        Tests the get-door-control function with a valid dest_addr.
        '''
        controller = CONTROLLER
        door = 3
        dest = DEST_ADDR

        response = self.u.get_door_control(controller, door, dest_addr=dest)

        self.assertEqual(response, GetDoorControlResponse)

    def test_set_door_control(self):
        '''
        Tests the set-door-control function with a valid dest_addr.
        '''
        controller = CONTROLLER
        door = 3
        delay = 4
        mode = 2
        dest = DEST_ADDR

        response = self.u.set_door_control(controller, door, mode, delay, dest_addr=dest)

        self.assertEqual(response, SetDoorControlResponse)

    def test_open_door(self):
        '''
        Tests the open-door function with a valid dest_addr.
        '''
        controller = CONTROLLER
        door = 3
        dest = DEST_ADDR

        response = self.u.open_door(controller, door, dest_addr=dest)

        self.assertEqual(response, OpenDoorResponse)

    def test_get_cards(self):
        '''
        Tests the get-cards function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.get_cards(controller, dest_addr=dest)

        self.assertEqual(response, GetCardsResponse)

    def test_get_card(self):
        '''
        Tests the get-card function with a valid dest_addr.
        '''
        controller = CONTROLLER
        card = CARD
        dest = DEST_ADDR

        response = self.u.get_card(controller, card, dest_addr=dest)

        self.assertEqual(response, GetCardResponse)

    def test_get_card_by_index(self):
        '''
        Tests the get-card-by-index function with a valid dest_addr.
        '''
        controller = CONTROLLER
        index = CARD_INDEX
        dest = DEST_ADDR

        response = self.u.get_card_by_index(controller, index, dest_addr=dest)

        self.assertEqual(response, GetCardByIndexResponse)

    def test_put_card(self):
        '''
        Tests the put-card function with a valid dest_addr.
        '''
        controller = CONTROLLER
        card = 123456789
        start = datetime.date(2023,1,1)
        end = datetime.date(2025,12,31)
        door1 = 1
        door2 = 0
        door3 = 29
        door4 = 1
        PIN = 7531
        dest = DEST_ADDR

        response = self.u.put_card(controller, card, start, end, door1, door2, door3, door4, PIN, dest_addr=dest)

        self.assertEqual(response, PutCardResponse)

    def test_delete_card(self):
        '''
        Tests the delete-card function with a valid dest_addr.
        '''
        controller = CONTROLLER
        card = CARD
        dest = DEST_ADDR

        response = self.u.delete_card(controller, card, dest_addr=dest)

        self.assertEqual(response, DeleteCardResponse)

    def test_delete_all_cards(self):
        '''
        Tests the delete-all-cards function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.delete_all_cards(controller, dest_addr=dest)

        self.assertEqual(response, DeleteAllCardsResponse)

    def test_get_event(self):
        '''
        Tests the get-event function with a valid dest_addr.
        '''
        controller = CONTROLLER
        index = EVENT_INDEX
        dest = DEST_ADDR

        response = self.u.get_event(controller, index, dest_addr=dest)

        self.assertEqual(response, GetEventResponse)

    def test_get_event_index(self):
        '''
        Tests the get-event-index function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.get_event_index(controller, dest_addr=dest)

        self.assertEqual(response, GetEventIndexResponse)

    def test_set_event_index(self):
        '''
        Tests the set-event-index function with a valid dest_addr.
        '''
        controller = CONTROLLER
        index = EVENT_INDEX
        dest = DEST_ADDR

        response = self.u.set_event_index(controller, index, dest_addr=dest)

        self.assertEqual(response, SetEventIndexResponse)

    def test_record_special_events(self):
        '''
        Tests the record-special-events function with a valid dest_addr.
        '''
        controller = CONTROLLER
        enabled = True
        dest = DEST_ADDR

        response = self.u.record_special_events(controller, enabled, dest_addr=dest)

        self.assertEqual(response, RecordSpecialEventsResponse)

    def test_get_time_profile(self):
        '''
        Tests the get-time-profile function with a valid dest_addr.
        '''
        controller = CONTROLLER
        profile = TIME_PROFILE
        dest = DEST_ADDR

        response = self.u.get_time_profile(controller, profile, dest_addr=dest)

        self.assertEqual(response, GetTimeProfileResponse)

    def test_set_time_profile(self):
        '''
        Tests the set-time-profile function with a valid dest_addr.
        '''
        controller = CONTROLLER
        profile_id = TIME_PROFILE
        start_date = datetime.date(2021,1,1)
        end_date = datetime.date(2021,12,31)
        monday = True
        tuesday = False
        wednesday = True
        thursday = False
        friday = True
        saturday = False
        sunday = False
        segment_1_start = datetime.time(8,30)
        segment_1_end = datetime.time(11,45)
        segment_2_start = datetime.time(13,15)
        segment_2_end = datetime.time(17,25)
        segment_3_start = None
        segment_3_end = None
        linked_profile_id = 3
        dest = DEST_ADDR

        response = self.u.set_time_profile(
            controller,
            profile_id,
            start_date,
            end_date,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            segment_1_start,
            segment_1_end,
            segment_2_start,
            segment_2_end,
            segment_3_start,
            segment_3_end,
            linked_profile_id,
            dest_addr=dest)

        self.assertEqual(response, SetTimeProfileResponse)

    def test_delete_all_time_profiles(self):
        '''
        Tests the delete-all-time-profiles function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.delete_all_time_profiles(controller, dest_addr=dest)

        self.assertEqual(response, DeleteAllTimeProfilesResponse)

    def test_add_task(self):
        '''
        Tests the add-task function with a valid dest_addr.
        '''
        controller = CONTROLLER
        start_date = datetime.date(2021,1,1)
        end_date = datetime.date(2021,12,31)
        monday = True
        tuesday = False
        wednesday = True
        thursday = False
        friday = True
        saturday = False
        sunday = False
        start_time = datetime.time(8,30)
        door = 3
        task_type = 4
        more_cards = 17
        dest = DEST_ADDR

        response = self.u.add_task(
            controller,
            start_date, end_date, 
            monday, tuesday, wednesday, thursday, friday, saturday, sunday,
            start_time, 
            door, 
            task_type, 
            more_cards,
            dest_addr=dest)

        self.assertEqual(response, AddTaskResponse)

    def test_refresh_tasklist(self):
        '''
        Tests the refresh-tasklist function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.refresh_tasklist(controller, dest_addr=dest)

        self.assertEqual(response, RefreshTaskListResponse)

    def test_clear_tasklist(self):
        '''
        Tests the clear-tasklist function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.clear_tasklist(controller, dest_addr=dest)

        self.assertEqual(response, ClearTaskListResponse)

    def test_set_pc_control(self):
        '''
        Tests the set-pc-control function with a valid dest_addr.
        '''
        controller = CONTROLLER
        enable = True
        dest = DEST_ADDR

        response = self.u.set_pc_control(controller, enable, dest_addr=dest)

        self.assertEqual(response, SetPCControlResponse)

    def test_set_interlock(self):
        '''
        Tests the set-interlock function with a valid dest_addr.
        '''
        controller = CONTROLLER
        interlock = 8
        dest = DEST_ADDR

        response = self.u.set_interlock(controller, interlock, dest_addr=dest)

        self.assertEqual(response, SetInterlockResponse)

    def test_activate_keypads(self):
        '''
        Tests the activate-keypads function with a valid dest_addr.
        '''
        controller = CONTROLLER
        reader1 = True
        reader2 = True
        reader3 = False
        reader4 = True
        dest = DEST_ADDR

        response = self.u.activate_keypads(controller, reader1, reader2, reader3, reader4, dest_addr=dest)

        self.assertEqual(response, ActivateKeypadsResponse)

    def test_set_door_passcodes(self):
        '''
        Tests the set-door-passcodes function with a valid dest_addr.
        '''
        controller = CONTROLLER
        door = 3
        passcode1 = 12345
        passcode2 = 0
        passcode3 = 999999
        passcode4 = 54321
        dest = DEST_ADDR

        response = self.u.set_door_passcodes(controller, door, passcode1,  passcode2, passcode3, passcode4, dest_addr=dest)

        self.assertEqual(response, SetDoorPasscodesResponse)

    def test_restore_default_parameters(self):
        '''
        Tests the restore-default-parameters function with a valid dest_addr.
        '''
        controller = CONTROLLER
        dest = DEST_ADDR

        response = self.u.restore_default_parameters(controller, dest_addr=dest)

        self.assertEqual(response, RestoreDefaultParametersResponse)
