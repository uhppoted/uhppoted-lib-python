"""
CLI command arguments.
"""

from collections import namedtuple

Arg = namedtuple("Arg", ["arg", "type", "help"])

controller = Arg("--controller", int, "controller serial number, e.g. 405419896")
listener = Arg("--listener", str, "event listener host address:port, e.g. 192.168.1.100:60001")
card = Arg("--card", int, "card number, e.g. 10058400")
index = Arg("--index", int, "card index, e.g. 17")
antipassback = Arg("--antipassback", str, "disabled, (1:2);(3:4), (1,3):(2,4), 1:(2,3) or 1:(2,3,4)")
profile = Arg("--profile", int, "time profile ID, e.g. 29")
