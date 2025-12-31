# pylint: disable=too-many-public-methods

"""
UHPPOTE UDP function tests.

End-to-end tests for the uhppote functions over a connected UDP socket.
"""

import unittest
import socket
import struct
import threading
import time
import datetime

from ipaddress import IPv4Address

# pylint: disable=import-error
from uhppoted import uhppote
from uhppoted.net import dump

from uhppoted.structs import Card
from uhppoted.structs import TimeProfile
from uhppoted.structs import Task
from uhppoted.structs import Weekdays
from uhppoted.structs import TimeSegment

from uhppoted.errors import CardNotFound
from uhppoted.errors import CardDeleted
from uhppoted.errors import EventNotFound
from uhppoted.errors import EventOverwritten
from uhppoted.errors import TimeProfileNotFound
from uhppoted.errors import InvalidResponse

# pylint: disable=relative-beyond-top-level
from .stub import messages
from . import expected  # pylint: disable=no-name-in-module

DEST_ADDR = "127.0.0.1:54321"
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

    try:
        sock.bind(bind)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, never)

        while True:
            (message, addr) = sock.recvfrom(1024)
            if len(message) == 64:
                if debug:
                    dump(message)
                for m in messages():
                    if bytes(m["request"]) == message:
                        sock.sendto(bytes(m["response"]), addr)
                        break
    except Exception:  # pylint: disable=broad-exception-caught
        pass
    finally:
        sock.close()


class TestUDPWithDestAddr(unittest.TestCase):
    """
    Test suite for the UDP transport with a connected socket.
    """

    @classmethod
    def setUpClass(cls):
        bind = "0.0.0.0"
        broadcast = "255.255.255.255:60000"
        listen = "0.0.0.0:60001"
        debug = False

        cls.u = uhppote.Uhppote(bind, broadcast, listen, debug)
        cls._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        cls._thread = threading.Thread(target=handle, args=(cls._sock, ("127.0.0.1", 54321), False))

        cls._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls._sock.close()
        cls._sock = None

    def test_get_controller(self):
        """
        Tests the get-controller function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.get_controller(controller)

        self.assertEqual(response, expected.GetControllerResponse)

    def test_set_ip(self):
        """
        Tests the set-ip function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        address = IPv4Address("192.168.1.100")
        netmask = IPv4Address("255.255.255.0")
        gateway = IPv4Address("192.168.1.1")

        response = self.u.set_ip(controller, address, netmask, gateway)

        self.assertEqual(response, expected.SetIPResponse)

    def test_get_time(self):
        """
        Tests the get-time function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.get_time(controller)

        self.assertEqual(response, expected.GetTimeResponse)

    def test_set_time(self):
        """
        Tests the set-time function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        now = datetime.datetime(2021, 5, 28, 14, 56, 14)

        response = self.u.set_time(controller, now)

        self.assertEqual(response, expected.SetTimeResponse)

    def test_get_status(self):
        """
        Tests the get-status function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.get_status(controller)

        self.assertEqual(response, expected.GetStatusResponse)

    def test_get_status_record(self):
        """
        Tests the get-status-record function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        record = self.u.get_status_record(controller)

        self.assertEqual(record, expected.GetStatusRecord)

    def test_get_status_record_no_event(self):
        """
        Tests the get-status-record function with no events on the controller.
        """
        controller = (303986753, DEST_ADDR)

        record = self.u.get_status_record(controller)

        self.assertEqual(record, expected.GetStatusRecordNoEvent)

    def test_get_status_record_invalid_controller_response(self):
        """
        Tests the get-status-record function with an incorrect controller in the response.
        """
        controller = (201020304, DEST_ADDR)

        self.assertRaisesRegex(InvalidResponse, r"invalid controller \(405419896\)", self.u.get_status_record, controller)

    def test_get_listener(self):
        """
        Tests the get-listener function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)

        response = self.u.get_listener(controller)

        self.assertEqual(response, expected.GetListenerResponse)

    def test_set_listener(self):
        """
        Tests the set-listener function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        address = IPv4Address("192.168.1.100")
        port = 60001
        interval = 15

        response = self.u.set_listener(controller, address, port, interval)

        self.assertEqual(response, expected.SetListenerResponse)

    def test_set_listener_without_interval(self):
        """
        Tests the set-listener function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        address = IPv4Address("192.168.1.100")
        port = 60001

        response = self.u.set_listener(controller, address, port)

        self.assertEqual(response, expected.SetListenerResponse)

    def test_get_door_control(self):
        """
        Tests the get-door-control function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        door = 3

        response = self.u.get_door_control(controller, door)

        self.assertEqual(response, expected.GetDoorControlResponse)

    def test_set_door_control(self):
        """
        Tests the set-door-control function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        door = 3
        delay = 4
        mode = 2

        response = self.u.set_door_control(controller, door, mode, delay)

        self.assertEqual(response, expected.SetDoorControlResponse)

    def test_open_door(self):
        """
        Tests the open-door function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        door = 3

        response = self.u.open_door(controller, door)

        self.assertEqual(response, expected.OpenDoorResponse)

    def test_get_cards(self):
        """
        Tests the get-cards function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.get_cards(controller)

        self.assertEqual(response, expected.GetCardsResponse)

    def test_get_card(self):
        """
        Tests the get-card function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = CARD

        response = self.u.get_card(controller, card)

        self.assertEqual(response, expected.GetCardResponse)

    def test_get_card_record(self):
        """
        Tests the get-card-record function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = CARD

        record = self.u.get_card_record(controller, card)

        self.assertEqual(record, expected.GetCardRecord)

    def test_get_card_record_not_found(self):
        """
        Tests the get-card-record function with a missing card.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = CARD_NOT_FOUND

        self.assertRaises(CardNotFound, self.u.get_card_record, controller, card)

    def test_get_card_record_invalid_controller_response(self):
        """
        Tests the get-card-record function with an incorrect controller in the response.
        """
        controller = (303986753, DEST_ADDR)
        card = CARD

        with self.assertRaisesRegex(InvalidResponse, r"invalid controller \(405419896\)"):
            self.u.get_card_record(controller, card)

    def test_get_card_record_invalid_card_response(self):
        """
        Tests the get-card-record function with an incorrect card in the response.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = 10058398

        with self.assertRaisesRegex(InvalidResponse, r"invalid card \(8165538\)"):
            self.u.get_card_record(controller, card)

    def test_get_card_by_index(self):
        """
        Tests the get-card-by-index function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = CARD_INDEX

        response = self.u.get_card_by_index(controller, index)

        self.assertEqual(response, expected.GetCardByIndexResponse)

    def test_get_card_record_by_index(self):
        """
        Tests the get-card-record-by-index function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = CARD_INDEX

        record = self.u.get_card_record_by_index(controller, index)

        self.assertEqual(record, expected.GetCardRecordByIndex)

    def test_get_card_record_by_index_not_found(self):
        """
        Tests the get-card-record function with a missing card.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = CARD_INDEX_NOT_FOUND

        self.assertRaises(CardNotFound, self.u.get_card_record_by_index, controller, index)

    def test_get_card_record_by_index_deleted(self):
        """
        Tests the get-card-record function with a deleted card.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = CARD_INDEX_DELETED

        self.assertRaises(CardDeleted, self.u.get_card_record_by_index, controller, index)

    def test_get_card_record_by_index_invalid_controller_response(self):
        """
        Tests the get-card-record-by-index function with an incorrect controller in the response.
        """
        controller = (303986753, DEST_ADDR)
        index = CARD_INDEX

        with self.assertRaisesRegex(InvalidResponse, r"invalid controller \(405419896\)"):
            self.u.get_card_record_by_index(controller, index)

    def test_put_card(self):
        """
        Tests the put-card function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = 123456789
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2025, 12, 31)
        door1 = 1
        door2 = 0
        door3 = 29
        door4 = 1
        pin = 7531

        response = self.u.put_card(controller, card, start, end, door1, door2, door3, door4, pin)

        self.assertEqual(response, expected.PutCardResponse)

    def test_put_card_record(self):
        """
        Tests the put-card-record function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = Card(
            123456789,
            datetime.date(2023, 1, 1),
            datetime.date(2025, 12, 31),
            {
                1: 1,
                3: 29,
                4: 1,
            },
            7531,
        )

        response = self.u.put_card_record(controller, card)

        self.assertEqual(response, expected.PutCardRecordResponse)

    def test_put_card_record_invalid_controller_response(self):
        """
        Tests the put-card-record function with an incorrect controller in the response.
        """
        controller = (303986753, DEST_ADDR)
        card = Card(
            123456789,
            datetime.date(2023, 1, 1),
            datetime.date(2025, 12, 31),
            {
                1: 1,
                3: 29,
                4: 1,
            },
            7531,
        )

        with self.assertRaisesRegex(InvalidResponse, r"invalid controller \(405419896\)"):
            self.u.put_card_record(controller, card)

    def test_delete_card(self):
        """
        Tests the delete-card function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        card = CARD
        response = self.u.delete_card(controller, card)

        self.assertEqual(response, expected.DeleteCardResponse)

    def test_delete_all_cards(self):
        """
        Tests the delete-all-cards function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.delete_all_cards(controller)

        self.assertEqual(response, expected.DeleteAllCardsResponse)

    def test_get_event(self):
        """
        Tests the get-event function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = EVENT_INDEX
        response = self.u.get_event(controller, index)

        self.assertEqual(response, expected.GetEventResponse)

    def test_get_event_record(self):
        """
        Tests the get-event-record function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = EVENT_INDEX

        record = self.u.get_event_record(controller, index)

        self.assertEqual(record, expected.GetEventRecord)

    def test_get_event_record_not_found(self):
        """
        Tests the get-event-record function for a non-existent record.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = EVENT_INDEX_NOT_FOUND

        self.assertRaises(EventNotFound, self.u.get_event_record, controller, index)

    def test_get_event_record_overwritten(self):
        """
        Tests the get-event-record function for a record that has been overwritten.
        """
        controller = (201020304, DEST_ADDR)
        index = EVENT_INDEX_OVERWRITTEN

        self.assertRaises(EventOverwritten, self.u.get_event_record, controller, index)

    def test_get_event_record_invalid_controller_response(self):
        """
        Tests the get-event-record function with an incorrect controller in the response.
        """
        controller = (303986753, DEST_ADDR)
        index = EVENT_INDEX

        with self.assertRaisesRegex(InvalidResponse, r"invalid controller \(405419896\)"):
            self.u.get_event_record(controller, index)

    def test_get_event_index(self):
        """
        Tests the get-event-index function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.get_event_index(controller)

        self.assertEqual(response, expected.GetEventIndexResponse)

    def test_set_event_index(self):
        """
        Tests the set-event-index function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        index = EVENT_INDEX
        response = self.u.set_event_index(controller, index)

        self.assertEqual(response, expected.SetEventIndexResponse)

    def test_record_special_events(self):
        """
        Tests the record-special-events function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        enabled = True
        response = self.u.record_special_events(controller, enabled)

        self.assertEqual(response, expected.RecordSpecialEventsResponse)

    def test_get_time_profile(self):
        """
        Tests the get-time-profile function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        profile = TIME_PROFILE

        response = self.u.get_time_profile(controller, profile)

        self.assertEqual(response, expected.GetTimeProfileResponse)

    def test_get_time_profile_record(self):
        """
        Tests the get-time-profile-record function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR)
        profile = TIME_PROFILE

        record = self.u.get_time_profile_record(controller, profile)

        self.assertEqual(record, expected.GetTimeProfileRecord)

    def test_get_time_profile_record_not_found(self):
        """
        Tests the get-time-profile-record function with a non-existent record.
        """
        controller = (CONTROLLER, DEST_ADDR)
        profile = TIME_PROFILE_NOT_FOUND

        with self.assertRaisesRegex(TimeProfileNotFound, r"time profile 92 not found"):
            self.u.get_time_profile_record(controller, profile)

    def test_set_time_profile(self):
        """
        Tests the set-time-profile function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        profile_id = TIME_PROFILE
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 12, 31)
        weekdays = {
            "monday": True,
            "tuesday": False,
            "wednesday": True,
            "thursday": False,
            "friday": True,
            "saturday": False,
            "sunday": False,
        }
        segments = {
            1: (datetime.time(8, 30), datetime.time(11, 45)),
            2: (datetime.time(13, 15), datetime.time(17, 25)),
            3: (None, None),
        }
        linked_profile_id = 3

        response = self.u.set_time_profile(
            controller,
            profile_id,
            start_date,
            end_date,
            weekdays["monday"],
            weekdays["tuesday"],
            weekdays["wednesday"],
            weekdays["thursday"],
            weekdays["friday"],
            weekdays["saturday"],
            weekdays["sunday"],
            segments[1][0],
            segments[1][1],
            segments[2][0],
            segments[2][1],
            segments[3][0],
            segments[3][1],
            linked_profile_id,
        )

        self.assertEqual(response, expected.SetTimeProfileResponse)

    def test_set_time_profile_record(self):
        """
        Tests the set-time-profile-record function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR)
        profile = TimeProfile(
            id=TIME_PROFILE,
            start_date=datetime.date(2021, 1, 1),
            end_date=datetime.date(2021, 12, 31),
            weekdays=Weekdays(
                monday=True,
                wednesday=True,
                friday=True,
            ),
            segments={
                1: TimeSegment(datetime.time(8, 30), datetime.time(11, 45)),
                2: TimeSegment(datetime.time(13, 15), datetime.time(17, 25)),
            },
            linked_profile=3,
        )

        response = self.u.set_time_profile_record(controller, profile)

        self.assertEqual(response, expected.SetTimeProfileRecordResponse)

    def test_delete_all_time_profiles(self):
        """
        Tests the delete-all-time-profiles function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.delete_all_time_profiles(controller)

        self.assertEqual(response, expected.DeleteAllTimeProfilesResponse)

    def test_add_task(self):
        """
        Tests the add-task function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 12, 31)
        weekdays = {
            "monday": True,
            "tuesday": False,
            "wednesday": True,
            "thursday": False,
            "friday": True,
            "saturday": False,
            "sunday": False,
        }
        start_time = datetime.time(8, 30)
        door = 3
        task_type = 4
        more_cards = 17

        response = self.u.add_task(
            controller,
            start_date,
            end_date,
            weekdays["monday"],
            weekdays["tuesday"],
            weekdays["wednesday"],
            weekdays["thursday"],
            weekdays["friday"],
            weekdays["saturday"],
            weekdays["sunday"],
            start_time,
            door,
            task_type,
            more_cards,
        )

        self.assertEqual(response, expected.AddTaskResponse)

    def test_add_task_record(self):
        """
        Tests the add-task-record function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR)
        task = Task(
            task=4,
            door=3,
            start_date=datetime.date(2021, 1, 1),
            end_date=datetime.date(2021, 12, 31),
            weekdays=Weekdays(
                monday=True,
                wednesday=True,
                friday=True,
            ),
            start_time=datetime.time(8, 30),
            more_cards=17,
        )

        response = self.u.add_task_record(controller, task)

        self.assertEqual(response, expected.AddTaskRecordResponse)

    def test_refresh_tasklist(self):
        """
        Tests the refresh-tasklist function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.refresh_tasklist(controller)

        self.assertEqual(response, expected.RefreshTaskListResponse)

    def test_clear_tasklist(self):
        """
        Tests the clear-tasklist function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.clear_tasklist(controller)

        self.assertEqual(response, expected.ClearTaskListResponse)

    def test_set_pc_control(self):
        """
        Tests the set-pc-control function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        enable = True
        response = self.u.set_pc_control(controller, enable)

        self.assertEqual(response, expected.SetPCControlResponse)

    def test_set_interlock(self):
        """
        Tests the set-interlock function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        interlock = 8

        response = self.u.set_interlock(controller, interlock)

        self.assertEqual(response, expected.SetInterlockResponse)

    def test_activate_keypads(self):
        """
        Tests the activate-keypads function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        reader1 = True
        reader2 = True
        reader3 = False
        reader4 = True

        response = self.u.activate_keypads(controller, reader1, reader2, reader3, reader4)

        self.assertEqual(response, expected.ActivateKeypadsResponse)

    def test_set_door_passcodes(self):
        """
        Tests the set-door-passcodes function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        door = 3
        passcode1 = 12345
        passcode2 = 0
        passcode3 = 999999
        passcode4 = 54321

        response = self.u.set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4)

        self.assertEqual(response, expected.SetDoorPasscodesResponse)

    def test_get_antipassback(self):
        """
        Tests the get_antipassback function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.get_antipassback(controller)

        self.assertEqual(response, expected.GetAntiPassbackResponse)

    def test_set_antipassback(self):
        """
        Tests the set_antipassback function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        antipassback = 2
        response = self.u.set_antipassback(controller, antipassback)

        self.assertEqual(response, expected.SetAntiPassbackResponse)

    def test_restore_default_parameters(self):
        """
        Tests the restore-default-parameters function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR)
        response = self.u.restore_default_parameters(controller)

        self.assertEqual(response, expected.RestoreDefaultParametersResponse)
