# FOR TESTING LOCALLY

import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.append(os.path.join(root, 'src'))

import ipaddress
import datetime

from uhppoted import uhppote
from pprint import pprint

CONTROLLER = 405419896
DOOR = 3
MODE = 2
DELAY = 10
CARD = 8165538
CARD_INDEX = 3
EVENT_INDEX = 37
TIME_PROFILE_ID = 29

ADDRESS = ipaddress.IPv4Address('192.168.1.100')
NETMASK = ipaddress.IPv4Address('255.255.255.0')
GATEWAY = ipaddress.IPv4Address('192.168.1.1')
LISTENER = (ipaddress.IPv4Address('192.168.1.100'), 60001)


def commands():
    return {
        'get-all-controllers': get_all_controllers,
        'get-controller': get_controller,
        'set-ip': set_ip,
        'get-time': get_time,
        'set-time': set_time,
        'get-listener': get_listener,
        'set-listener': set_listener,
        'get-door-control': get_door_control,
        'set-door-control': set_door_control,
        'get-status': get_status,
        'open-door': open_door,
        'get-cards': get_cards,
        'get-card': get_card,
        'get-card-by-index': get_card_by_index,
        'put-card': put_card,
        'delete-card': delete_card,
        'delete-all-cards': delete_all_cards,
        'get-event': get_event,
        'get-event-index': get_event_index,
        'set-event-index': set_event_index,
        'record-special-events': record_special_events,
        'get-time-profile': get_time_profile,
        'set-time-profile': set_time_profile,
        'delete-all-time-profiles': delete_all_time_profiles,
        'add-task': add_task,
        'refresh-tasklist': refresh_tasklist,
        'clear-tasklist': clear_tasklist,
        'set-pc-control': set_pc_control,
        'set-interlock': set_interlock,
        'activate-keypads': activate_keypads,
        'set-door-passcodes': set_door_passcodes,
        'restore-default-parameters': restore_default_parameters,
        'listen': listen,
    }


def exec(f, args):
    bind = args.bind
    broadcast = args.broadcast
    listen = args.listen
    debug = args.debug

    u = uhppote.Uhppote(bind, broadcast, listen, debug)
    response = f(u, args)

    if response != None:
        if type(response).__name__ == 'list':
            for v in response:
                pprint(v.__dict__, indent=2, width=1, sort_dicts=False)
        elif type(response).__name__ == 'bool':
            pprint(response, indent=2, width=1, sort_dicts=False)
        else:
            pprint(response.__dict__, indent=2, width=1, sort_dicts=False)


def get_all_controllers(u, args):
    timeout = args.timeout

    return u.get_all_controllers(timeout=timeout)


def get_controller(u, args):
    controller = CONTROLLER
    dest = args.destination
    timeout = args.timeout

    return u.get_controller(controller, dest_addr=dest, timeout=timeout)


def set_ip(u, args):
    controller = CONTROLLER
    address = ADDRESS
    netmask = NETMASK
    gateway = GATEWAY

    return u.set_ip(controller, address, netmask, gateway)


def get_time(u, args):
    controller = CONTROLLER

    return u.get_time(controller)


def set_time(u, args):
    controller = CONTROLLER
    now = datetime.datetime.now()

    return u.set_time(controller, now)


def get_listener(u, args):
    controller = CONTROLLER

    return u.get_listener(controller)


def set_listener(u, args):
    controller = CONTROLLER
    (address, port) = LISTENER

    return u.set_listener(controller, address, port)


def get_door_control(u, args):
    controller = CONTROLLER
    door = DOOR

    return u.get_door_control(controller, door)


def set_door_control(u, args):
    controller = CONTROLLER
    door = DOOR
    mode = MODE
    delay = DELAY

    return u.set_door_control(controller, door, mode, delay)


def get_status(u, args):
    controller = CONTROLLER

    return u.get_status(controller)


def open_door(u, args):
    controller = CONTROLLER
    door = DOOR

    return u.open_door(controller, door)


def get_cards(u, args):
    controller = CONTROLLER

    return u.get_cards(controller)


def get_card(u, args):
    controller = CONTROLLER
    card = CARD

    response = u.get_card(controller, card)
    if response.card_number == 0:
        raise ValueError(f'card {card} not found')

    return response


def get_card_by_index(u, args):
    controller = CONTROLLER
    index = CARD_INDEX

    response = u.get_card_by_index(controller, index)
    if response.card_number == 0:
        raise ValueError(f'card @ index {index} not found')
    elif response.card_number == 0xffffffff:
        raise ValueError(f'card @ index {index} deleted')

    return response


def put_card(u, args):
    controller = CONTROLLER
    card = CARD
    start = datetime.datetime.strptime("2022-01-01", '%Y-%m-%d').date()
    end = datetime.datetime.strptime("2022-12-31", '%Y-%m-%d').date()

    return u.put_card(controller, card, start, end, 0, 1, 29, 0, 7531)


def delete_card(u, args):
    controller = CONTROLLER
    card = CARD

    return u.delete_card(controller, card)


def delete_all_cards(u, args):
    controller = CONTROLLER

    return u.delete_all_cards(controller)


def get_event(u, args):
    controller = CONTROLLER
    index = EVENT_INDEX

    response = u.get_event(controller, index)
    if response.event_type == 0xff:
        raise ValueError(f'event @ index {index} overwritten')
    elif response.index == 0:
        raise ValueError(f'event @ index {index} not found')

    return response


def get_event_index(u, args):
    controller = CONTROLLER

    return u.get_event_index(controller)


def set_event_index(u, args):
    controller = CONTROLLER
    index = EVENT_INDEX

    return u.set_event_index(controller, index)


def record_special_events(u, args):
    controller = CONTROLLER
    enabled = True

    return u.record_special_events(controller, enabled)


def get_time_profile(u, args):
    controller = CONTROLLER
    profile_id = TIME_PROFILE_ID

    response = u.get_time_profile(controller, profile_id)
    if response.profile_id == 0:
        raise ValueError(f'time profile {profile_id} not defined')

    return response


def set_time_profile(u, args):
    controller = CONTROLLER
    profile_id = TIME_PROFILE_ID
    start = datetime.datetime.strptime("2022-01-01", '%Y-%m-%d').date()
    end = datetime.datetime.strptime("2022-12-31", '%Y-%m-%d').date()
    monday = True
    tuesday = False
    wednesday = True
    thursday = True
    friday = False
    saturday = False
    sunday = True
    segment1start = datetime.datetime.strptime("08:15", '%H:%M').time()
    segment1end = datetime.datetime.strptime("11:45", '%H:%M').time()
    segment2start = datetime.datetime.strptime("12:45", '%H:%M').time()
    segment2end = datetime.datetime.strptime("17:15", '%H:%M').time()
    segment3start = datetime.datetime.strptime("19:30", '%H:%M').time()
    segment3end = datetime.datetime.strptime("22:00", '%H:%M').time()
    linked_profile_ID = 23

    return u.set_time_profile(controller, profile_id, start, end, monday, tuesday, wednesday, thursday, friday,
                              saturday, sunday, segment1start, segment1end, segment2start, segment2end, segment3start,
                              segment3end, linked_profile_ID)


def delete_all_time_profiles(u, args):
    return u.delete_all_time_profiles(CONTROLLER)


def add_task(u, args):
    controller = CONTROLLER
    start_date = datetime.datetime.strptime("2022-01-01", '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime("2022-12-31", '%Y-%m-%d').date()
    monday = True
    tuesday = False
    wednesday = True
    thursday = True
    friday = False
    saturday = False
    sunday = True
    start_time = datetime.datetime.strptime("08:15", '%H:%M').time()
    door = DOOR
    task_type = 2
    more_cards = 0

    return u.add_task(controller, start_date, end_date, monday, tuesday, wednesday, thursday, friday, saturday, sunday,
                      start_time, door, task_type, more_cards)


def refresh_tasklist(u, args):
    controller = CONTROLLER

    return u.refresh_tasklist(controller)


def clear_tasklist(u, args):
    controller = CONTROLLER

    return u.clear_tasklist(controller)


def set_pc_control(u, args):
    controller = CONTROLLER
    enabled = True

    return u.set_pc_control(controller, enabled)


def set_interlock(u, args):
    controller = CONTROLLER
    interlock = 3

    return u.set_interlock(controller, interlock)


def activate_keypads(u, args):
    controller = CONTROLLER
    reader1 = True
    reader2 = True
    reader3 = False
    reader4 = True

    return u.activate_keypads(controller, reader1, reader2, reader3, reader4)


def set_door_passcodes(u, args):
    controller = CONTROLLER
    door = DOOR
    passcode1 = 12345
    passcode2 = 0
    passcode3 = 999999
    passcode4 = 54321

    return u.set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4)


def restore_default_parameters(u, args):
    controller = CONTROLLER

    return u.restore_default_parameters(controller)


def listen(u, args):
    return u.listen(onEvent)


def onEvent(event):
    if event != None:
        pprint(event.__dict__, indent=2, width=1)
