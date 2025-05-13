#!python3

import argparse
import sys
import traceback

from trace import Trace
from commands import commands
from commands import exec


def parse_args():
    parser = argparse.ArgumentParser(description='uhppoted-lib-python example')

    parser.add_argument('--bind', type=str, default='0.0.0.0', help='UDP IPv4 bind address. Defaults to 0.0.0.0:0')

    parser.add_argument('--broadcast',
                        type=str,
                        default='255.255.255.255:60000',
                        help='UDP IPv4 broadcast address. Defaults to 255.255.255.255:60000')

    parser.add_argument('--listen',
                        type=str,
                        default='0.0.0.0:60001',
                        help='UDP IPv4 event listener bind address. Defaults to 0.0.0.0:60001')

    parser.add_argument('--debug',
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help='displays sent and received packets')

    parser.add_argument('--destination',
                        '-d',
                        type=str,
                        default=None,
                        help='(optional) controller IPv4 address:port. Defaults to broadcast address.')

    parser.add_argument('--timeout',
                        '-t',
                        type=float,
                        default=2.5,
                        help='(optional) operation timeout (in seconds). Defaults to 2.5.')

    parser.add_argument('--udp', action=argparse.BooleanOptionalAction, default=False, help='use UDP protocol')
    parser.add_argument('--tcp', action=argparse.BooleanOptionalAction, default=False, help='use TCP protocol')

    # ... command specific args
    subparsers = parser.add_subparsers(title='subcommands', dest='command')
    parsers = {}

    for c in commands().keys():
        parsers[f'{c}'] = subparsers.add_parser(f'{c}')

    # ... get-controller
    get_controller = parsers['get-controller']
    get_controller.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-ip
    set_ip = parsers['set-ip']
    set_ip.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-status
    get_status = parsers['get-status']
    get_status.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-time
    get_time = parsers['get-time']
    get_time.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-time
    set_time = parsers['set-time']
    set_time.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-listener
    get_listener = parsers['get-listener']
    get_listener.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-listener
    set_listener = parsers['set-listener']
    set_listener.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-door-control
    get_door_control = parsers['get-door-control']
    get_door_control.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-door-control
    set_door_control = parsers['set-door-control']
    set_door_control.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... open-door
    open_door = parsers['open-door']
    open_door.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-cards
    get_cards = parsers['get-cards']
    get_cards.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-card
    get_card = parsers['get-card']
    get_card.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')
    get_card.add_argument('--card', type=int, help='card number, e.g. 10058400')

    # ... get-card-by-index
    get_card_by_index = parsers['get-card-by-index']
    get_card_by_index.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')
    get_card_by_index.add_argument('--index', type=int, help='card index, e.g. 17')

    # ... put-card
    put_card = parsers['put-card']
    put_card.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... delete-card
    delete_card = parsers['delete-card']
    delete_card.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')
    delete_card.add_argument('--card', type=int, help='card number, e.g. 10058400')

    # ... delete-all-cards
    delete_all_cards = parsers['delete-all-cards']
    delete_all_cards.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-event-index
    get_event_index = parsers['get-event-index']
    get_event_index.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-event-index
    set_event_index = parsers['set-event-index']
    set_event_index.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-event
    get_event = parsers['get-event']
    get_event.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... record-special-events
    record_special_events = parsers['record-special-events']
    record_special_events.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-time-profile
    get_time_profile = parsers['get-time-profile']
    get_time_profile.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-time-profile
    set_time_profile = parsers['set-time-profile']
    set_time_profile.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... clear-time-profiles
    clear_time_profiles = parsers['clear-time-profiles']
    clear_time_profiles.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... add-task
    add_task = parsers['add-task']
    add_task.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... refresh-tasklist
    refresh_tasklist = parsers['refresh-tasklist']
    refresh_tasklist.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... clear-tasklist
    clear_tasklist = parsers['clear-tasklist']
    clear_tasklist.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-pc-control
    set_pc_control = parsers['set-pc-control']
    set_pc_control.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-interlock
    set_interlock = parsers['set-interlock']
    set_interlock.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... activate-keypads
    activate_keypads = parsers['activate-keypads']
    activate_keypads.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-door-passcodes
    set_door_passcodes = parsers['set-door-passcodes']
    set_door_passcodes.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... get-antipassback
    get_antipassback = parsers['get-antipassback']
    get_antipassback.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    # ... set-antipassback
    set_antipassback = parsers['set-antipassback']
    set_antipassback.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')
    set_antipassback.add_argument('--antipassback',
                                  type=str,
                                  help='disabled, (1:2);(3:4), (1,3):(2,4), 1:(2,3) or 1:(2,3,4)')

    # ... restore-default-parameters
    restore_default_parameters = parsers['restore-default-parameters']
    restore_default_parameters.add_argument('--controller', type=int, help='controller serial number, e.g. 405419896')

    return parser.parse_args()


def main():
    if len(sys.argv) < 2:
        usage()
        return -1

    args = parse_args()
    cmd = args.command
    debug = args.debug

    if args.udp and args.tcp:
        print()
        print(f'*** ERROR  conflicting UDP/TCP flags - choose one or the other (default is UDP)')
        print()
        sys.exit(1)

    if cmd == 'all':
        for c, fn in commands().items():
            if c != 'listen':
                try:
                    exec(fn, args)
                except Exception as x:
                    print()
                    print(f'*** ERROR  {cmd}: {x}')
                    print()
    elif cmd in commands():
        try:
            exec(commands()[cmd], args)
        except Exception as x:
            print()
            print(f'*** ERROR  {cmd}: {x}')
            print()
            if debug:
                print(traceback.format_exc())

            sys.exit(1)
    else:
        print()
        print(f'  ERROR: invalid command ({cmd})')
        print()


def usage():
    print()
    print('  Usage: python3 main.py <command>')
    print()
    print('  Supported commands:')

    for cmd, _ in commands().items():
        print(f'    {cmd}')

    print()


if __name__ == '__main__':
    main()
