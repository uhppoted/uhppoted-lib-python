"""
CLI command implementation.
"""

import os
import ipaddress
import datetime
import pprint
import sys
import pathlib

from collections import namedtuple

if os.environ["UHPPOTED_ENV"] == "DEV":
    root = pathlib.Path(__file__).resolve().parents[2]
    sys.path.append(os.path.join(root, "src"))

# pylint: disable=import-error, wrong-import-position
import cli_args as Args
from uhppoted import uhppote
from uhppoted import structs

DOOR = 3
MODE = 2
DELAY = 10
EVENT_INDEX = 37
TIME_PROFILE_ID = 29
AUTO_SEND = 15
ANTIPASSBACK = 2

ADDRESS = ipaddress.IPv4Address("192.168.1.125")
NETMASK = ipaddress.IPv4Address("255.255.255.0")
GATEWAY = ipaddress.IPv4Address("192.168.1.1")
LISTENER = (ipaddress.IPv4Address("192.168.1.125"), 60001)

Command = namedtuple("Command", ["f", "args"])


# fmt: off
def commands():
    """
    Returns a dict that maps a CLI command to the implementation function and command line args.
    """
    return {
        "get-all-controllers":        Command(get_all_controllers,        []),
        "get-controller":             Command(get_controller,             [Args.controller]),
        "set-ip":                     Command(set_ip,                     [Args.controller]),
        "get-time":                   Command(get_time,                   [Args.controller]),
        "set-time":                   Command(set_time,                   [Args.controller]),
        "get-listener":               Command(get_listener,               [Args.controller]),
        "set-listener":               Command(set_listener,               [Args.controller]),
        "get-door-control":           Command(get_door_control,           [Args.controller]),
        "set-door-control":           Command(set_door_control,           [Args.controller]),
        "get-status":                 Command(get_status,                 [Args.controller]),
        "get-status-record":          Command(get_status_record,          [Args.controller]),
        "open-door":                  Command(open_door,                  [Args.controller]),
        "get-cards":                  Command(get_cards,                  [Args.controller]),
        "get-card":                   Command(get_card,                   [Args.controller, Args.card]),
        "get-card-record":            Command(get_card_record,            [Args.controller, Args.card]),
        "get-card-by-index":          Command(get_card_by_index,          [Args.controller, Args.index]),
        "get-card-record-by-index":   Command(get_card_record_by_index,   [Args.controller, Args.index]),
        "put-card":                   Command(put_card,                   [Args.controller, Args.card]),
        "put-card-record":            Command(put_card_record,            [Args.controller, Args.card]),
        "delete-card":                Command(delete_card,                [Args.controller, Args.card]),
        "delete-all-cards":           Command(delete_all_cards,           [Args.controller]),
        "get-event":                  Command(get_event,                  [Args.controller, Args.index]),
        "get-event-record":           Command(get_event_record,           [Args.controller, Args.index]),
        "get-event-index":            Command(get_event_index,            [Args.controller]),
        "set-event-index":            Command(set_event_index,            [Args.controller]),
        "record-special-events":      Command(record_special_events,      [Args.controller]),
        "get-time-profile":           Command(get_time_profile,           [Args.controller, Args.profile]),
        "get-time-profile-record":    Command(get_time_profile_record,    [Args.controller, Args.profile]),
        "set-time-profile":           Command(set_time_profile,           [Args.controller, Args.profile]),
        "set-time-profile-record":    Command(set_time_profile_record,    [Args.controller, Args.profile]),
        "clear-time-profiles":        Command(clear_time_profiles,        [Args.controller]),
        "add-task":                   Command(add_task,                   [Args.controller]),
        "add-task-record":            Command(add_task_record,            [Args.controller]),
        "refresh-tasklist":           Command(refresh_tasklist,           [Args.controller]),
        "clear-tasklist":             Command(clear_tasklist,             [Args.controller]),
        "set-pc-control":             Command(set_pc_control,             [Args.controller]),
        "set-interlock":              Command(set_interlock,              [Args.controller]),
        "activate-keypads":           Command(activate_keypads,           [Args.controller]),
        "set-door-passcodes":         Command(set_door_passcodes,         [Args.controller, Args.door, Args.passcodes]),
        "set-door-passcodes-record":  Command(set_door_passcodes_record,  [Args.controller, Args.door, Args.passcodes]),
        "get-antipassback":           Command(get_antipassback,           [Args.controller]),
        "set-antipassback":           Command(set_antipassback,           [Args.controller, Args.antipassback]),
        "restore-default-parameters": Command(restore_default_parameters, [Args.controller]),
        "listen":                     Command(listen, []),
    }
# fmt: on


def execute(cmd, args):
    """
    Executes the function corresponding to a CLI command and pretty prints the response (if any).
    """
    bind_addr = args.bind
    broadcast_addr = args.broadcast
    listen_addr = args.listen
    debug = args.debug

    dest = args.destination
    timeout = args.timeout
    protocol = "udp"

    if args.udp:
        protocol = "udp"
    elif args.tcp:
        protocol = "tcp"

    u = uhppote.Uhppote(bind_addr, broadcast_addr, listen_addr, debug)
    response = cmd.f(u, dest, timeout, args, protocol=protocol)

    if response is not None:
        if type(response).__name__ == "list":
            for v in response:
                pprint.pprint(v.__dict__, indent=2, width=1, sort_dicts=False)
        elif type(response).__name__ == "bool":
            pprint.pprint(response, indent=2, width=1, sort_dicts=False)
        else:
            pprint.pprint(response.__dict__, indent=2, width=1, sort_dicts=False)


def get_all_controllers(u, dest, timeout, args, protocol="udp"):  # pylint: disable=unused-argument
    """
    Retrieves a list of found controllers using 'get_all_controllers' API function.
    """
    return u.get_all_controllers(timeout=timeout)


def get_controller(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the information for a controller using the 'get_controller' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_controller(controller, timeout=timeout)


def set_ip(u, dest, timeout, args, protocol="udp"):
    """
    Sets the controller IPv4 network address, subnet mask and gateway using the 'set_ip' API function.
    """
    controller = (args.controller, dest, protocol)
    address = ADDRESS
    netmask = NETMASK
    gateway = GATEWAY

    return u.set_ip(controller, address, netmask, gateway, timeout=timeout)


def get_time(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves a controller current date/time using the 'get_time' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_time(controller, timeout=timeout)


def set_time(u, dest, timeout, args, protocol="udp"):
    """
    Sets the controller date/time using the 'set_time' API function.
    """
    controller = (args.controller, dest, protocol)
    now = datetime.datetime.now()

    return u.set_time(controller, now, timeout=timeout)


def get_listener(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves a controller event listener IPv4 address and auto-send interval using
    the 'get_listener' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_listener(controller, timeout=timeout)


def set_listener(u, dest, timeout, args, protocol="udp"):
    """
    Sets  the controller event listen IPv4 address and auto-send interval using the
    'set_listener' API function.
    """
    controller = (args.controller, dest, protocol)
    (address, port) = LISTENER
    interval = AUTO_SEND

    return u.set_listener(controller, address, port, interval, timeout=timeout)


def get_door_control(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the unlock delay and control mode for a door using the 'get_door' API function.
    """
    controller = (args.controller, dest, protocol)
    door = DOOR

    return u.get_door_control(controller, door, timeout=timeout)


def set_door_control(u, dest, timeout, args, protocol="udp"):
    """
    Sets the unlock delay and control mode for a door using by the 'set_door' API function.
    """
    controller = (args.controller, dest, protocol)
    door = DOOR
    mode = MODE
    delay = DELAY

    return u.set_door_control(controller, door, mode, delay, timeout=timeout)


def get_status(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the controller current state using the 'get_status' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_status(controller, timeout=timeout)


def get_status_record(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the controller current state using the 'get_status' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_status_record(controller, timeout=timeout)


def open_door(u, dest, timeout, args, protocol="udp"):
    """
    Unlocks a door using the 'open_door' API function.
    """
    controller = (args.controller, dest, protocol)
    door = DOOR

    return u.open_door(controller, door, timeout=timeout)


def get_cards(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the number of cards stored in a controller usingt the 'get_cards' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_cards(controller, timeout=timeout)


def get_card(u, dest, timeout, args, protocol="udp"):
    """
    Returns the information for an access card from a controller by card number, using the
    'get_card' API function.
    """
    controller = (args.controller, dest, protocol)
    card = args.card

    response = u.get_card(controller, card, timeout=timeout)
    if response.card == 0:
        raise ValueError(f"card {card} not found")

    return response


def get_card_record(u, dest, timeout, args, protocol="udp"):
    """
    Returns the card record for an access card from a controller by card number, using the
    'get_card_record' API function.
    """
    controller = (args.controller, dest, protocol)
    card = args.card

    record = u.get_card_record(controller, card, timeout=timeout)
    if record and record.card == 0:
        raise ValueError(f"card {card} not found")

    return record


def get_card_by_index(u, dest, timeout, args, protocol="udp"):
    """
    Returns the information for an access card from a controller by record index, using the
    'get_card_by_index' API function.
    """
    controller = (args.controller, dest, protocol)
    index = args.index

    response = u.get_card_by_index(controller, index, timeout=timeout)

    if response.card_number == 0:
        raise ValueError(f"card @ index {index} not found")

    if response.card_number == 0xFFFFFFFF:
        raise ValueError(f"card @ index {index} deleted")

    return response


def get_card_record_by_index(u, dest, timeout, args, protocol="udp"):
    """
    Returns the card record for an access card from a controller by record index, using the
    'get_card_record_by_index' API function.
    """
    controller = (args.controller, dest, protocol)
    index = args.index

    record = u.get_card_record_by_index(controller, index, timeout=timeout)

    if record and record.card == 0:
        raise ValueError(f"card @ index {index} not found")

    if record and record.card == 0xFFFFFFFF:
        raise ValueError(f"card @ index {index} deleted")

    return record


def put_card(u, dest, timeout, args, protocol="udp"):  # pylint: disable=unused-argument
    """
    Adds or updates the information for an access card on a controller using the 'put_card' API function.
    """
    controller = (args.controller, dest, protocol)
    card = args.card
    start = datetime.datetime.strptime("2024-01-01", "%Y-%m-%d").date()
    end = datetime.datetime.strptime("2024-12-31", "%Y-%m-%d").date()
    door1 = 0  # no access
    door2 = 1  # 24/7 access
    door3 = 29  # time_profile
    door4 = 0  # no access
    pin = 7531

    return u.put_card(controller, card, start, end, door1, door2, door3, door4, pin, timeout=timeout)


def put_card_record(u, dest, timeout, args, protocol="udp"):  # pylint: disable=unused-argument
    """
    Adds or updates the information for an access card on a controller using the 'put_card_record' API function.
    """
    controller = (args.controller, dest, protocol)
    card = structs.Card(
        args.card,
        datetime.datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        datetime.datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
        {
            1: 0,  # no access
            2: 1,  # 24/7 access
            3: 29,  # time profile #29
            4: 0,  # no access
        },
        7531,
    )

    return u.put_card_record(controller, card, timeout=timeout)


def delete_card(u, dest, timeout, args, protocol="udp"):
    """
    Deletes an access card from a controller using the 'delete_card' API function.
    """
    controller = (args.controller, dest, protocol)
    card = args.card

    return u.delete_card(controller, card, timeout=timeout)


def delete_all_cards(u, dest, timeout, args, protocol="udp"):
    """
    Deletes all access cards from a controller using the 'delete_all_cards' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.delete_all_cards(controller, timeout=timeout)


def get_event(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the information for an event from a controller using the 'get_event' API function.
    """
    controller = (args.controller, dest, protocol)
    index = args.index

    response = u.get_event(controller, index, timeout=timeout)

    if response.event_type == 0xFF:
        raise ValueError(f"event @ index {index} overwritten")

    if response.index == 0:
        raise ValueError(f"event @ index {index} not found")

    return response


def get_event_record(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the information for an event from a controller using the 'get_event' API function.
    """
    controller = (args.controller, dest, protocol)
    index = args.index

    return u.get_event(controller, index, timeout=timeout)


def get_event_index(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the current 'user event index' from a controller using the 'get_event_index' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_event_index(controller, timeout=timeout)


def set_event_index(u, dest, timeout, args, protocol="udp"):
    """
    Sets the current 'user event index' on a controller using the 'set_event_index' API function.
    """
    controller = (args.controller, dest, protocol)
    index = EVENT_INDEX

    return u.set_event_index(controller, index, timeout=timeout)


def record_special_events(u, dest, timeout, args, protocol="udp"):
    """
    Enables/disables door open, door close and door unlock events using the 'record_special_events'
    API function.
    """
    controller = (args.controller, dest, protocol)
    enabled = True

    return u.record_special_events(controller, enabled, timeout=timeout)


def get_time_profile(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves a time profile from a controller using the 'get_time_profile' API function.
    """
    controller = (args.controller, dest, protocol)
    profile_id = args.profile
    response = u.get_time_profile(controller, profile_id, timeout=timeout)

    if response.profile_id == 0:
        raise ValueError(f"time profile {profile_id} not defined")

    return response


def get_time_profile_record(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves a time profile rom a controller using the 'get_time_profile_record' API function.
    """
    controller = (args.controller, dest, protocol)
    profile_id = args.profile
    record = u.get_time_profile_record(controller, profile_id, timeout=timeout)

    return record


def set_time_profile(u, dest, timeout, args, protocol="udp"):
    """
    Adds or updates a time profile on a controller using the 'set_time_profile' API function.
    """
    controller = (args.controller, dest, protocol)
    profile_id = args.profile
    start = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
    end = datetime.datetime.strptime("2022-12-31", "%Y-%m-%d").date()
    weekdays = {
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": True,
        "friday": False,
        "saturday": False,
        "sunday": True,
    }
    segments = {
        "1": (datetime.datetime.strptime("08:15", "%H:%M").time(), datetime.datetime.strptime("11:45", "%H:%M").time()),
        "2": (datetime.datetime.strptime("12:45", "%H:%M").time(), datetime.datetime.strptime("17:15", "%H:%M").time()),
        "3": (datetime.datetime.strptime("19:30", "%H:%M").time(), datetime.datetime.strptime("22:00", "%H:%M").time()),
    }
    linked_profile_id = 23

    return u.set_time_profile(
        controller,
        profile_id,
        start,
        end,
        weekdays.get("monday", False),
        weekdays.get("tuesday", False),
        weekdays.get("wednesday", False),
        weekdays.get("thursday", False),
        weekdays.get("friday", False),
        weekdays.get("saturday", False),
        weekdays.get("sunday", False),
        segments["1"][0],
        segments["1"][1],
        segments["2"][0],
        segments["2"][1],
        segments["3"][0],
        segments["3"][1],
        linked_profile_id,
        timeout=timeout,
    )


def set_time_profile_record(u, dest, timeout, args, protocol="udp"):
    """
    Adds or updates a time profile on a controller using the 'set_time_profile_record' API function.
    """
    controller = (args.controller, dest, protocol)
    profile = structs.TimeProfile(
        id=args.profile,
        start_date=datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
        end_date=datetime.datetime.strptime("2022-12-31", "%Y-%m-%d").date(),
        weekdays=structs.Weekdays(
            monday=True,
            wednesday=True,
            thursday=True,
            sunday=True,
        ),
        segments={
            1: structs.TimeSegment(datetime.time(8, 15), datetime.time(11, 45)),
            2: structs.TimeSegment(datetime.time(12, 45), datetime.time(17, 15)),
            3: structs.TimeSegment(datetime.time(19, 30), datetime.time(22, 0)),
        },
        linked_profile=23,
    )

    return u.set_time_profile_record(controller, profile, timeout=timeout)


def clear_time_profiles(u, dest, timeout, args, protocol="udp"):
    """
    Deletes all time profiles from a controller using the 'clear_time_profiles' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.delete_all_time_profiles(controller, timeout=timeout)


def add_task(u, dest, timeout, args, protocol="udp"):
    """
    Adds a scheduled task to a controller using the 'add_task' API function.
    """
    controller = (args.controller, dest, protocol)
    start_date = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime("2022-12-31", "%Y-%m-%d").date()
    weekdays = {
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": True,
        "friday": False,
        "saturday": False,
        "sunday": True,
    }
    start_time = datetime.datetime.strptime("08:15", "%H:%M").time()
    door = DOOR
    task_type = 2
    more_cards = 0

    return u.add_task(
        controller,
        start_date,
        end_date,
        weekdays.get("monday", False),
        weekdays.get("tuesday", False),
        weekdays.get("wednesday", False),
        weekdays.get("thursday", False),
        weekdays.get("friday", False),
        weekdays.get("saturday", False),
        weekdays.get("sunday", False),
        start_time,
        door,
        task_type,
        more_cards,
        timeout=timeout,
    )


def add_task_record(u, dest, timeout, args, protocol="udp"):
    """
    Adds a scheduled task to a controller using the 'add_task_record' API function.
    """
    controller = (args.controller, dest, protocol)
    task = structs.Task(
        task=2,
        door=DOOR,
        start_date=datetime.date(2025, 1, 1),
        end_date=datetime.date(2025, 12, 31),
        weekdays=structs.Weekdays(
            monday=True,
            wednesday=True,
            thursday=True,
            sunday=True,
        ),
        start_time=datetime.time(8, 15),
        more_cards=0,
    )

    return u.add_task_record(controller, task, timeout=timeout)


def refresh_tasklist(u, dest, timeout, args, protocol="udp"):
    """
    Schedules tasks added using 'add_task' for execution using the 'refresh_tasklist' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.refresh_tasklist(controller, timeout=timeout)


def clear_tasklist(u, dest, timeout, args, protocol="udp"):
    """
    Clears the scheduled tasklist from a controller using the 'clear_tasklist' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.clear_tasklist(controller, timeout=timeout)


def set_pc_control(u, dest, timeout, args, protocol="udp"):
    """
    Enables remote access control using the 'set_pc_control' API function.
    """
    controller = (args.controller, dest, protocol)
    enabled = True

    return u.set_pc_control(controller, enabled, timeout=timeout)


def set_interlock(u, dest, timeout, args, protocol="udp"):
    """
    Sets the door interlock mode for a controller using the 'set_interlock' API function.
    """
    controller = (args.controller, dest, protocol)
    interlock = 3

    return u.set_interlock(controller, interlock, timeout=timeout)


def activate_keypads(u, dest, timeout, args, protocol="udp"):
    """
    Enables/disables reader keypads on a controller using the 'activate_keypads' API function.
    """
    controller = (args.controller, dest, protocol)
    reader1 = True
    reader2 = True
    reader3 = False
    reader4 = True

    return u.activate_keypads(controller, reader1, reader2, reader3, reader4, timeout=timeout)


def set_door_passcodes(u, dest, timeout, args, protocol="udp"):
    """
    Sets the supervisor passcodes for a door using the 'set_door_passcodes' API function.
    """
    controller = (args.controller, dest, protocol)
    door = args.door
    passcode1 = 0
    passcode2 = 0
    passcode3 = 0
    passcode4 = 0

    if len(args.passcodes) > 0:
        passcode1 = args.passcodes[0]

    if len(args.passcodes) > 1:
        passcode2 = args.passcodes[1]

    if len(args.passcodes) > 2:
        passcode3 = args.passcodes[2]

    if len(args.passcodes) > 3:
        passcode4 = args.passcodes[3]

    return u.set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4, timeout=timeout)


def set_door_passcodes_record(u, dest, timeout, args, protocol="udp"):
    """
    Sets the supervisor passcodes for a door using the 'set_door_passcodes_record' API function.
    """
    controller = (args.controller, dest, protocol)
    door = args.door
    passcodes = args.passcodes

    return u.set_door_passcodes_record(controller, door, passcodes, timeout=timeout)


def get_antipassback(u, dest, timeout, args, protocol="udp"):
    """
    Retrieves the anti-passback mode from a controller using the 'get_antipassback' API function.
    """
    controller = (args.controller, dest, protocol)

    return u.get_antipassback(controller, timeout=timeout)


def set_antipassback(u, dest, timeout, args, protocol="udp"):
    """
    Sets the anti-passback mode for a controller using the 'set_antipassback' API function.
    """
    controller = (args.controller, dest, protocol)
    antipassback = ANTIPASSBACK

    return u.set_antipassback(controller, antipassback, timeout=timeout)


def restore_default_parameters(u, dest, timeout, args, protocol="udp"):
    """
    Resets the controller configuration to the manufacturer defaults using the 'restore_default_parameters'
    API function.
    """
    controller = (args.controller, dest, protocol)

    return u.restore_default_parameters(controller, timeout=timeout)


def listen(u, dest, timeout, args, protocol="udp"):  # pylint: disable=unused-argument
    """
    Listens for controller generated events the 'listen' API function.
    """
    return u.listen(on_event)


def on_event(event):
    """
    Pretty prints an event received via the 'listen' API function.
    """
    if event is not None:
        pprint.pprint(event.__dict__, indent=2, width=1)
