# pylint: disable=too-many-public-methods

"""
UHPPOTE function tests.

End-to-end tests for the uhppote TCP transport function timeout.
"""

import unittest
import socket
import threading
import time
import datetime

from ipaddress import IPv4Address

# pylint: disable=import-error
from uhppoted import uhppote
from uhppoted.net import dump

# pylint: disable=relative-beyond-top-level
from .stub import messages

DEST_ADDR = "127.0.0.1:12345"
TIMEOUT = 0.25
CONTROLLER = 405419896
CARD = 8165538
CARD_INDEX = 2
EVENT_INDEX = 29
TIME_PROFILE = 29


def handle(sock, bind, debug):
    """
    Replies to received TCP packets with the matching response after 0.5s delay.
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
                            time.sleep(0.5)
                            connection.sendall(bytes(m["response"]))
                            break

            except Exception as exc:  # pylint: disable=broad-exception-caught
                print("WARN", exc)
            finally:
                connection.close()
    except Exception:  # pylint: disable=broad-exception-caught
        pass


class TestTCPWithTimeout(unittest.TestCase):
    """
    Test suite for the TCP transport timeout handling.
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

    def test_get_controller(self):
        """
        Tests the get-controller function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_controller(controller)
        self.assertRaises(socket.timeout, self.u.get_controller, controller, timeout=TIMEOUT)

    def test_set_ip(self):
        """
        Tests the set-ip function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        address = IPv4Address("192.168.1.100")
        netmask = IPv4Address("255.255.255.0")
        gateway = IPv4Address("192.168.1.1")

        self.u.set_ip(controller, address, netmask, gateway, timeout=TIMEOUT)

    def test_get_time(self):
        """
        Tests the get-time function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_time(controller)
        self.assertRaises(socket.timeout, self.u.get_time, controller, timeout=TIMEOUT)

    def test_set_time(self):
        """
        Tests the set-time function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        now = datetime.datetime(2021, 5, 28, 14, 56, 14)

        self.u.set_time(controller, now)
        self.assertRaises(socket.timeout, self.u.set_time, controller, now, timeout=TIMEOUT)

    def test_get_status(self):
        """
        Tests the get-status function  with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_status(controller)
        self.assertRaises(socket.timeout, self.u.get_status, controller, timeout=TIMEOUT)

    def test_get_listener(self):
        """
        Tests the get-listener function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_listener(controller)
        self.assertRaises(socket.timeout, self.u.get_listener, controller, timeout=TIMEOUT)

    def test_set_listener(self):
        """
        Tests the set-listener function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        address = IPv4Address("192.168.1.100")
        port = 60001
        interval = 15

        self.u.set_listener(controller, address, port, interval)
        self.assertRaises(socket.timeout, self.u.set_listener, controller, address, port, timeout=TIMEOUT)

    def test_get_door_control(self):
        """
        Tests the get-door-control function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3

        self.u.get_door_control(controller, door)
        self.assertRaises(socket.timeout, self.u.get_door_control, controller, door, timeout=TIMEOUT)

    def test_set_door_control(self):
        """
        Tests the set-door-control function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3
        delay = 4
        mode = 2

        self.u.set_door_control(controller, door, mode, delay)

        self.assertRaises(socket.timeout, self.u.set_door_control, controller, door, mode, delay, timeout=TIMEOUT)

    def test_open_door(self):
        """
        Tests the open-door function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3

        self.u.open_door(controller, door)
        self.assertRaises(socket.timeout, self.u.open_door, controller, door, timeout=TIMEOUT)

    def test_get_cards(self):
        """
        Tests the get-cards function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_cards(controller)
        self.assertRaises(socket.timeout, self.u.get_cards, controller, timeout=TIMEOUT)

    def test_get_card(self):
        """
        Tests the get-card function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = CARD

        self.u.get_card(controller, card)
        self.assertRaises(socket.timeout, self.u.get_card, controller, card, timeout=TIMEOUT)

    def test_get_card_record(self):
        """
        Tests the get-card-record function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = CARD

        self.u.get_card_record(controller, card)
        self.assertRaises(socket.timeout, self.u.get_card_record, controller, card, timeout=TIMEOUT)

    def test_get_card_by_index(self):
        """
        Tests the get-card-by-index function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = CARD_INDEX

        self.u.get_card_by_index(controller, index)
        self.assertRaises(socket.timeout, self.u.get_card_by_index, controller, index, timeout=TIMEOUT)

    def test_get_card_record_by_index(self):
        """
        Tests the get-card-by-index function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = CARD_INDEX

        self.u.get_card_record_by_index(controller, index)
        self.assertRaises(socket.timeout, self.u.get_card_record_by_index, controller, index, timeout=TIMEOUT)

    def test_put_card(self):
        """
        Tests the put-card function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = 123456789
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2025, 12, 31)
        door1 = 1
        door2 = 0
        door3 = 29
        door4 = 1
        pin = 7531

        self.u.put_card(controller, card, start, end, door1, door2, door3, door4, pin)

        self.assertRaises(
            socket.timeout,
            self.u.put_card,
            controller,
            card,
            start,
            end,
            door1,
            door2,
            door3,
            door4,
            pin,
            timeout=TIMEOUT,
        )

    def test_delete_card(self):
        """
        Tests the delete-card function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        card = CARD

        self.u.delete_card(controller, card)
        self.assertRaises(socket.timeout, self.u.delete_card, controller, card, timeout=TIMEOUT)

    def test_delete_all_cards(self):
        """
        Tests the delete-all-cards function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.delete_all_cards(controller)
        self.assertRaises(socket.timeout, self.u.delete_all_cards, controller, timeout=TIMEOUT)

    def test_get_event(self):
        """
        Tests the get-event function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = EVENT_INDEX

        self.u.get_event(controller, index)
        self.assertRaises(socket.timeout, self.u.get_event, controller, index, timeout=TIMEOUT)

    def test_get_event_index(self):
        """
        Tests the get-event-index function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_event_index(controller)
        self.assertRaises(socket.timeout, self.u.get_event_index, controller, timeout=TIMEOUT)

    def test_set_event_index(self):
        """
        Tests the set-event-index function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        index = EVENT_INDEX

        self.u.set_event_index(controller, index)
        self.assertRaises(socket.timeout, self.u.set_event_index, controller, index, timeout=TIMEOUT)

    def test_record_special_events(self):
        """
        Tests the record-special-events function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        enabled = True

        self.u.record_special_events(controller, enabled)
        self.assertRaises(socket.timeout, self.u.record_special_events, controller, enabled, timeout=TIMEOUT)

    def test_get_time_profile(self):
        """
        Tests the get-time-profile function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        profile = TIME_PROFILE

        self.u.get_time_profile(controller, profile)
        self.assertRaises(socket.timeout, self.u.get_time_profile, controller, profile, timeout=TIMEOUT)

    def test_set_time_profile(self):
        """
        Tests the set-time-profile function with a timeout
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

        self.u.set_time_profile(
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

        self.assertRaises(
            socket.timeout,
            self.u.set_time_profile,
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
            timeout=TIMEOUT,
        )

    def test_delete_all_time_profiles(self):
        """
        Tests the delete-all-time-profiles function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.delete_all_time_profiles(controller)
        self.assertRaises(socket.timeout, self.u.delete_all_time_profiles, controller, timeout=TIMEOUT)

    def test_add_task(self):
        """
        Tests the add-task function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
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

        self.u.add_task(
            controller,
            start_date,
            end_date,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            start_time,
            door,
            task_type,
            more_cards,
        )

        self.assertRaises(
            socket.timeout,
            self.u.add_task,
            controller,
            start_date,
            end_date,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            start_time,
            door,
            task_type,
            more_cards,
            timeout=TIMEOUT,
        )

    def test_refresh_tasklist(self):
        """
        Tests the refresh-tasklist function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.refresh_tasklist(controller)
        self.assertRaises(socket.timeout, self.u.refresh_tasklist, controller, timeout=TIMEOUT)

    def test_clear_tasklist(self):
        """
        Tests the clear-tasklist function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.clear_tasklist(controller)
        self.assertRaises(socket.timeout, self.u.clear_tasklist, controller, timeout=TIMEOUT)

    def test_set_pc_control(self):
        """
        Tests the set-pc-control function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        enable = True

        self.u.set_pc_control(controller, enable)
        self.assertRaises(socket.timeout, self.u.set_pc_control, controller, enable, timeout=TIMEOUT)

    def test_set_interlock(self):
        """
        Tests the set-interlock function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        interlock = 8

        self.u.set_interlock(controller, interlock)
        self.assertRaises(socket.timeout, self.u.set_interlock, controller, interlock, timeout=TIMEOUT)

    def test_activate_keypads(self):
        """
        Tests the activate-keypads function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        reader1 = True
        reader2 = True
        reader3 = False
        reader4 = True

        self.u.activate_keypads(controller, reader1, reader2, reader3, reader4)

        self.assertRaises(
            socket.timeout, self.u.activate_keypads, controller, reader1, reader2, reader3, reader4, timeout=TIMEOUT
        )

    def test_set_door_passcodes(self):
        """
        Tests the set-door-passcodes function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        door = 3
        passcode1 = 12345
        passcode2 = 0
        passcode3 = 999999
        passcode4 = 54321

        self.u.set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4)

        self.assertRaises(
            socket.timeout,
            self.u.set_door_passcodes,
            controller,
            door,
            passcode1,
            passcode2,
            passcode3,
            passcode4,
            timeout=TIMEOUT,
        )

    def test_get_antipassback(self):
        """
        Tests the get_antipassback function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.get_antipassback(controller)
        self.assertRaises(socket.timeout, self.u.get_antipassback, controller, timeout=TIMEOUT)

    def test_set_antipassback(self):
        """
        Tests the set_antipassback function with a timeout.
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")
        antipassback = 2

        self.u.get_antipassback(controller, antipassback)
        self.assertRaises(socket.timeout, self.u.set_antipassback, controller, antipassback, timeout=TIMEOUT)

    def test_restore_default_parameters(self):
        """
        Tests the restore-default-parameters function with a timeout
        """
        controller = (CONTROLLER, DEST_ADDR, "tcp")

        self.u.restore_default_parameters(controller)
        self.assertRaises(socket.timeout, self.u.restore_default_parameters, controller, timeout=TIMEOUT)
