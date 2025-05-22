"""
UHPPOTE network utility functions.

"""

import struct
import re
import ipaddress

from collections import namedtuple

Controller = namedtuple("Controller", "id address protocol")

READ_TIMEOUT = struct.pack("ll", 5, 0)  # 5 seconds
WRITE_TIMEOUT = struct.pack("ll", 1, 0)  # 1 second
NO_TIMEOUT = struct.pack("ll", 0, 0)  # (infinite)


def resolve(addr):
    """
    Resolves an address:port string into the equivalent ( address, port ) tuple. An addr value
    without a :port suffix defaults to port 60000.

        Parameters:
            addr  (string)  address:port string

        Returns:
            (address, port) as a (string, uint16) tuple
    """
    match = re.match(r"(.*?):([0-9]+)", addr)
    if match:
        return (match.group(1), int(match.group(2)))

    address = ipaddress.IPv4Address(addr)
    return (str(address), 60000)


def timeout_to_seconds(val, defval=2.5):
    """
    Converts a timeout value to seconds, returning the default value if the supplied value
    is None, cannot be converted, or is out of the range [50ms..30s]

        Parameters:
            val    (float)  Timeout in seconds
            defval (float)  Optional default values.

        Returns:
            timeout in seconds as a float
    """
    try:
        if val is not None:
            v = float(f"{val}")
            if 0.05 <= v <= 30:
                return v
    except (ValueError, TypeError):
        pass

    return defval


def disambiguate(v):
    """
    Resolves a controller value that may be a uint32 or a (id,address,protocol) tuple to a
    Controller named tuple.

        Parameters:
            v  (int | tuple | Controller)  Controller serial number, tuple with (id,address,protocol) fields or
                                           Controller named tuple.

        Returns:
            (id, address, protocol) Controller named tuple. address defaults to None and protocol defaults to 'udp'.
    """
    if isinstance(v, int):
        return Controller(v, None, "udp")

    if isinstance(v, tuple):
        controller = v[0]
        address = None
        protocol = "udp"

        if len(v) > 1 and isinstance(v[1], str):
            address = v[1]

        if len(v) > 2 and (v[2] == "tcp" or v[2] == "TCP"):
            protocol = "tcp"

        return Controller(controller, address, protocol)

    return Controller(None, None, "udp")


def dump(packet):
    """
    Prints a packet to the console as a formatted hexadecimal string.

        Parameters:
           packet  (bytearray)  64 byte UDP packet.

        Returns:
            None.
    """
    print("\r")
    for i in range(0, 4):
        offset = i * 16
        u = packet[offset : offset + 8]
        v = packet[offset + 8 : offset + 16]

        p = f"{u[0]:02x} {u[1]:02x} {u[2]:02x} {u[3]:02x} {u[4]:02x} {u[5]:02x} {u[6]:02x} {u[7]:02x}"
        q = f"{v[0]:02x} {v[1]:02x} {v[2]:02x} {v[3]:02x} {v[4]:02x} {v[5]:02x} {v[6]:02x} {v[7]:02x}"

        print(f"   {offset:08x}  {p}  {q}")

    print()
