"""
Implements an async event listener that pushes received events on to a queue for processing separately.
"""

import asyncio
import ipaddress
import os
import pathlib
import pprint
import signal
import sys

from contextlib import suppress

if os.environ.get("UHPPOTED_ENV", "") == "DEV":
    root = pathlib.Path(__file__).resolve().parents[3]
    sys.path.append(os.path.join(root, "src"))

# pylint: disable=import-error, wrong-import-position
from uhppoted import uhppote_async as uhppote

QUEUE_SIZE = 8


async def main():
    """
    Sets the access controller(s) event listener address:port and then listens for received events on a thread.
    """
    controllers = [405419896, 303986753, 201020304]  # controller serial numbers
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
        u = uhppote.UhppoteAsync(bind_addr, broadcast_addr, listen_addr, debug)

        # # set the IPv4 address and UDP port to which the controller should send events
        tasks = [asyncio.create_task(set_listener(u, controller, host_addr, host_port)) for controller in controllers]

        await asyncio.gather(*tasks)

        # enable door open/close/unlock events
        tasks = [asyncio.create_task(record_special_events(u, controller)) for controller in controllers]

        await asyncio.gather(*tasks)

        # initialise work queue
        q = asyncio.Queue()

        # create event processing task
        asyncio.create_task(process_events(q))

        # listen for incoming controller events
        await listen(u, q)

    except Exception as x:  # pylint: disable=broad-exception-caught
        print()
        print(f"*** ERROR  {x}")
        print()


async def set_listener(u, controller, address, port):
    """
    Sets  the controller event listen IPv4 address and auto-send interval using the
    'set_listener' API function.
    """
    return await u.set_listener(controller, address, port)


async def record_special_events(u, controller):
    """
    Enables/disables door open, door close and door unlock events using the 'record_special_events'
    API function.
    """
    return await u.record_special_events(controller, True)


async def listen(u, q):
    """
    Listens for controller generated events the 'listen' API function.
    """
    print("INFO   listening for events")

    close = asyncio.Event()
    #   task = asyncio.create_task(u.listen(lambda e: on_event(e, q)))
    task = asyncio.create_task(u.listen(lambda e: on_event_async(e, q)))

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, close.set)

    try:
        await close.wait()
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    return None


def on_event(event, q):
    """
    Pushes received events on to the processing queue 'synchronously'.
    """
    if event is not None:
        print(f"DEBUG  event queue: {q.qsize()} entries")
        if q.qsize() < QUEUE_SIZE:
            asyncio.create_task(q.put(event))
        else:
            print(f"WARN   *** event queue full - discarding event {event.event_index}")


async def on_event_async(event, q):
    """
    Pushes received events on to the processing queue 'asynchronously'.
    """
    if event is not None:
        print(f"DEBUG  event queue: {q.qsize()} entries")
        if q.qsize() < QUEUE_SIZE:
            await q.put(event)
        else:
            print(f"WARN   *** event queue full - discarding event {event.event_index}")


async def process_events(q):
    """
    Removes events from the queue for processing.
    """
    while True:
        event = await q.get()
        await process_event(event)


async def process_event(event):
    """
    Example event processing - pretty prints event.
    """
    print(f"INFO   processing event {event.event_index}")
    pprint.pprint(event.__dict__, indent=2, width=1)
    await asyncio.sleep(5)  # simulate time consuming event processing


if __name__ == "__main__":
    asyncio.run(main())
