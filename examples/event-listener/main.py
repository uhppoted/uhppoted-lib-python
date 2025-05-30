"""
Implements an event listener that pushes received events on to a queue for processing separately.
"""

import ipaddress
import os
import pathlib
import pprint
import queue
import sys
import threading
import time

if os.environ.get("UHPPOTED_ENV", "") == "DEV":
    root = pathlib.Path(__file__).resolve().parents[2]
    sys.path.append(os.path.join(root, "src"))

# pylint: disable=import-error, wrong-import-position
from uhppoted import uhppote

QUEUE_SIZE = 8


def main():
    """
    Sets the access controller(s) event listener address:port and then listens for received events on a thread.
    """
    controller = 405419896  # controller serial number
    host_addr = ipaddress.IPv4Address("192.168.1.100")  # IPv4 address of host machine
    host_port = 60001  # port on which to listen for events

    bind_addr = "0.0.0.0"  # either INADDR_ANY (0.0.0.0) or the host IPv4 address
    broadcast_addr = (
        "255.255.255.255:60000"  # either the broadcast address for INADDR_ANY or the host IP broadcast address
    )
    listen_addr = f"0.0.0.0:{host_port}"  # either INADDR_ANY (0.0.0.0) or the host IP IPv4 address
    debug = False

    try:
        # base configuration for UHPPOTE driver
        u = uhppote.Uhppote(bind_addr, broadcast_addr, listen_addr, debug)

        # set the IPv4 address and UDP port to which the controller should send events
        set_listener(u, controller, host_addr, host_port)

        # enable door open/close/unlock events
        record_special_events(u, controller)

        # initialise work queue
        q = queue.Queue()

        # start processing thread
        t = threading.Thread(target=process_events, name="processing", args=[q])
        t.daemon = True
        t.start()

        # listen for incoming controller events
        listen(u, q)

    except Exception as x:  # pylint: disable=broad-exception-caught
        print()
        print(f"*** ERROR  {x}")
        print()


def set_listener(u, controller, address, port):
    """
    Sets  the controller event listen IPv4 address and auto-send interval using the
    'set_listener' API function.
    """
    u.set_listener(controller, address, port)


def record_special_events(u, controller):
    """
    Enables/disables door open, door close and door unlock events using the 'record_special_events'
    API function.
    """
    u.record_special_events(controller, True)


def listen(u, q):
    """
    Listens for controller generated events the 'listen' API function.
    """
    print("INFO   listening for events")
    u.listen(lambda e: on_event(e, q))


def on_event(event, q):
    """
    Pushes received events on to the processing queue.
    """
    if event is not None:
        print(f"DEBUG  event queue: {q.qsize()} entries")
        if q.qsize() < QUEUE_SIZE:
            q.put(event)
        else:
            print(f"WARN   *** event queue full - discarding event {event.event_index}")


def process_events(q):
    """
    Removes events from the queue for processing.
    """
    while True:
        event = q.get()
        process_event(event)


def process_event(event):
    """
    Example event processing - pretty prints event.
    """
    print(f"INFO   processing event {event.event_index}")
    pprint.pprint(event.__dict__, indent=2, width=1)
    time.sleep(5)  # simulate time consuming event processing


if __name__ == "__main__":
    main()
