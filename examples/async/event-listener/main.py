"""
Implements an async event listener that pushes received events on to a queue for processing separately.
"""

import argparse
import asyncio
import ipaddress
import pprint
import signal

from uhppoted import uhppote_async as uhppote

QUEUE_SIZE = 8


async def main():
    """
    Sets the access controller(s) event listener address:port and then listens for received events on a thread.
    """
    controllers = [405419896, 303986753, 201020304]  # controller serial numbers
    host_addr = "192.168.1.100"  # IPv4 address of host machine
    host_port = 60001  # port on which to listen for events

    bind_addr = "0.0.0.0"  # INADDR_ANY (0.0.0.0) or the host IPv4 address
    broadcast_addr = "255.255.255.255:60000"  # broadcast address for INADDR_ANY or the host IP broadcast address
    listen_addr = f"0.0.0.0:{host_port}"  # INADDR_ANY (0.0.0.0) or the host IP IPv4 address

    parser = argparse.ArgumentParser(description="Queued event listener example")
    parser.add_argument(
        "--bind",
        type=str,
        default=bind_addr,
        help="IPv4 bind address for host machine (e.g. 192.168.1.125). Defaults to 0.0.0.0",
    )
    parser.add_argument(
        "--broadcast",
        type=str,
        default=broadcast_addr,
        help="IPv4 broadcast address for host machine (e.g. 192.168.1.255). Defaults to 255.255.255.255",
    )
    parser.add_argument(
        "--listen",
        type=str,
        default=listen_addr,
        help="IPv4 listen address:port for host machine (e.g. 192.168.1.125:60001). Defaults to 0.0.0.0:60001",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=f"{host_addr}:{host_port}",
        help="IPv4 address for controller event listener (e.g. 192.168.1.125:60001)",
    )
    parser.add_argument("--debug", action="store_true", help="enables debugging messages")

    args = parser.parse_args()

    try:
        # base configuration for UHPPOTE driver
        u = uhppote.UhppoteAsync(args.bind, args.broadcast, args.listen, args.debug)

        # # set the IPv4 address and UDP port to which the controller should send events
        tasks = [asyncio.create_task(set_listener(u, controller, args.host)) for controller in controllers]

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


async def set_listener(u, controller, addr_port):
    """
    Sets  the controller event listen IPv4 address and auto-send interval using the
    'set_listener' API function.
    """
    addr, port = addr_port.split(":")

    return await u.set_listener(controller, ipaddress.IPv4Address(addr), int(port))


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
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, close.set)

    await u.listen(lambda e: on_event(e, q), on_error=on_error, close=close)


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


def on_error(error):
    """
    Prints a warning message for the error.
    """
    if error is not None:
        print(f"WARN   {error}", flush=True)


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
