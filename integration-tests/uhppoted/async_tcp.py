# pylint: disable=too-many-public-methods

"""
UHPPOTE UDP async function tests.

End-to-end tests for the uhppote functions over a connected UDP socket.
"""

import unittest
import socket
import threading
import time
import datetime

from ipaddress import IPv4Address

# pylint: disable=import-error
from uhppoted import uhppote_async as uhppote
from uhppoted.net import dump

# pylint: disable=relative-beyond-top-level
from .stub import messages
from . import expected  # pylint: disable=no-name-in-module

DEST_ADDR = "127.0.0.1:12345"
CONTROLLER = 405419896
CARD = 8165538
CARD_INDEX = 2
EVENT_INDEX = 29
TIME_PROFILE = 29


def handle(sock, bind, debug):
    """
    Replies to received TCP packets with the matching response.
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(bind)
    sock.listen(1)

    # pylint: disable=too-many-nested-blocks
    try:
        while True:
            (connection, _) = sock.accept()
            try:
                connection.settimeout(0.5)
                message = connection.recv(1024)

                if len(message) == 64:
                    if debug:
                        dump(message)
                    for m in messages():
                        if bytes(m["request"]) == message:
                            connection.sendall(bytes(m["response"]))
                            break

            except Exception as exc:  # pylint: disable=broad-exception-caught
                print("WARN", exc)
            finally:
                connection.close()
    except Exception:  # pylint: disable=broad-exception-caught
        pass


class TestAsyncUDP(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for the TCP async transport.
    """

    @classmethod
    def setUpClass(cls):
        bind = "0.0.0.0"
        broadcast = "255.255.255.255:60000"
        listen = "0.0.0.0:60001"
        debug = False

        cls.u = uhppote.UhppoteAsync(bind, broadcast, listen, debug)
        cls._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        cls._thread = threading.Thread(target=handle, args=(cls._sock, ("", 12345), False))

        cls._thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls._sock.close()
        cls._sock = None

    async def test_get_controller(self):
        """
        Tests the get-controller function with a valid dest_addr.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.get_controller(controller)

        self.assertEqual(response, expected.GetControllerResponse)

    async def test_set_ip(self):
        """
        Tests the set-ip function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        address = IPv4Address("192.168.1.100")
        netmask = IPv4Address("255.255.255.0")
        gateway = IPv4Address("192.168.1.1")

        response = await self.u.set_ip(controller, address, netmask, gateway)

        self.assertEqual(response, expected.SetIPResponse)

    async def test_get_time(self):
        """
        Tests the get-time function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.get_time(controller)

        self.assertEqual(response, expected.GetTimeResponse)

    async def test_set_time(self):
        """
        Tests the set-time function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        now = datetime.datetime(2021, 5, 28, 14, 56, 14)
        response = await self.u.set_time(controller, now)

        self.assertEqual(response, expected.SetTimeResponse)

    async def test_get_status(self):
        """
        Tests the get-status function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.get_status(controller)

        self.assertEqual(response, expected.GetStatusResponse)

    async def test_get_listener(self):
        """
        Tests the get-listener function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.get_listener(controller)

        self.assertEqual(response, expected.GetListenerResponse)

    async def test_set_listener(self):
        """
        Tests the set-listener function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        address = IPv4Address("192.168.1.100")
        port = 60001
        interval = 15
        response = await self.u.set_listener(controller, address, port, interval)

        self.assertEqual(response, expected.SetListenerResponse)

    async def test_set_listener_without_interval(self):
        """
        Tests the set-listener function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        address = IPv4Address("192.168.1.100")
        port = 60001

        response = await self.u.set_listener(controller, address, port)
        self.assertEqual(response, expected.SetListenerResponse)

    async def test_get_door_control(self):
        """
        Tests the get-door-control function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3
        response = await self.u.get_door_control(controller, door)

        self.assertEqual(response, expected.GetDoorControlResponse)

    async def test_set_door_control(self):
        """
        Tests the set-door-control function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3
        delay = 4
        mode = 2

        response = await self.u.set_door_control(controller, door, mode, delay)

        self.assertEqual(response, expected.SetDoorControlResponse)

    async def test_open_door(self):
        """
        Tests the open-door function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3
        response = await self.u.open_door(controller, door)

        self.assertEqual(response, expected.OpenDoorResponse)

    async def test_get_cards(self):
        """
        Tests the get-cards function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.get_cards(controller)

        self.assertEqual(response, expected.GetCardsResponse)

    async def test_get_card(self):
        """
        Tests the get-card function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = CARD
        response = await self.u.get_card(controller, card)

        self.assertEqual(response, expected.GetCardResponse)

    async def test_get_card_by_index(self):
        """
        Tests the get-card-by-index function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = CARD_INDEX
        response = await self.u.get_card_by_index(controller, index)

        self.assertEqual(response, expected.GetCardByIndexResponse)

    async def test_put_card(self):
        """
        Tests the put-card function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = 123456789
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2025, 12, 31)
        door1 = 1
        door2 = 0
        door3 = 29
        door4 = 1
        pin = 7531

        response = await self.u.put_card(controller, card, start_date, end_date, door1, door2, door3, door4, pin)

        self.assertEqual(response, expected.PutCardResponse)

    async def test_delete_card(self):
        """
        Tests the delete-card function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = CARD
        response = await self.u.delete_card(controller, card)

        self.assertEqual(response, expected.DeleteCardResponse)

    async def test_delete_all_cards(self):
        """
        Tests the delete-all-cards function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.delete_all_cards(controller)

        self.assertEqual(response, expected.DeleteAllCardsResponse)

    async def test_get_event(self):
        """
        Tests the get-event function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = EVENT_INDEX
        response = await self.u.get_event(controller, index)

        self.assertEqual(response, expected.GetEventResponse)

    async def test_get_event_index(self):
        """
        Tests the get-event-index function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.get_event_index(controller)

        self.assertEqual(response, expected.GetEventIndexResponse)

    async def test_set_event_index(self):
        """
        Tests the set-event-index function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = EVENT_INDEX
        response = await self.u.set_event_index(controller, index)

        self.assertEqual(response, expected.SetEventIndexResponse)

    async def test_record_special_events(self):
        """
        Tests the record-special-events function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        enabled = True
        response = await self.u.record_special_events(controller, enabled)

        self.assertEqual(response, expected.RecordSpecialEventsResponse)

    async def test_get_time_profile(self):
        """
        Tests the get-time-profile function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        profile = TIME_PROFILE
        response = await self.u.get_time_profile(controller, profile)

        self.assertEqual(response, expected.GetTimeProfileResponse)

    async def test_set_time_profile(self):
        """
        Tests the set-time-profile function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
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

        response = await self.u.set_time_profile(
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

    async def test_delete_all_time_profiles(self):
        """
        Tests the delete-all-time-profiles function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.delete_all_time_profiles(controller)

        self.assertEqual(response, expected.DeleteAllTimeProfilesResponse)

    async def test_add_task(self):
        """
        Tests the add-task function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
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

        response = await self.u.add_task(
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

    async def test_refresh_tasklist(self):
        """
        Tests the refresh-tasklist function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.refresh_tasklist(controller)

        self.assertEqual(response, expected.RefreshTaskListResponse)

    async def test_clear_tasklist(self):
        """
        Tests the clear-tasklist function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.clear_tasklist(controller)

        self.assertEqual(response, expected.ClearTaskListResponse)

    async def test_set_pc_control(self):
        """
        Tests the set-pc-control function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        enable = True
        response = await self.u.set_pc_control(controller, enable)

        self.assertEqual(response, expected.SetPCControlResponse)

    async def test_set_interlock(self):
        """
        Tests the set-interlock function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        interlock = 8
        response = await self.u.set_interlock(controller, interlock)

        self.assertEqual(response, expected.SetInterlockResponse)

    async def test_activate_keypads(self):
        """
        Tests the activate-keypads function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        reader1 = True
        reader2 = True
        reader3 = False
        reader4 = True

        response = await self.u.activate_keypads(controller, reader1, reader2, reader3, reader4)

        self.assertEqual(response, expected.ActivateKeypadsResponse)

    async def test_set_door_passcodes(self):
        """
        Tests the set-door-passcodes function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3
        passcode1 = 12345
        passcode2 = 0
        passcode3 = 999999
        passcode4 = 54321

        response = await self.u.set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4)

        self.assertEqual(response, expected.SetDoorPasscodesResponse)

    async def test_get_antipassback(self):
        """
        Tests the get_antipassback function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        response = await self.u.get_antipassback(controller)

        self.assertEqual(response, expected.GetAntiPassbackResponse)

    async def test_set_antipassback(self):
        """
        Tests the set_antipassback function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        antipassback = 2

        response = await self.u.set_antipassback(controller, antipassback)

        self.assertEqual(response, expected.SetAntiPassbackResponse)

    async def test_restore_default_parameters(self):
        """
        Tests the restore-default-parameters function with defaults.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        response = await self.u.restore_default_parameters(controller)

        self.assertEqual(response, expected.RestoreDefaultParametersResponse)
