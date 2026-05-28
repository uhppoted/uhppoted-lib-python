"""
CLI command arguments.
"""

from collections import namedtuple

Arg = namedtuple("Arg", ["arg", "type", "help"])

controller = Arg("--controller", int, "controller serial number, e.g. 405419896")
door = Arg("--door", int, "door ID ([1..4]), e.g. 3")
card = Arg("--card", int, "card number, e.g. 10058400")
index = Arg("--index", int, "card index, e.g. 17")
profile = Arg("--profile", int, "time profile ID, e.g. 29")
passcodes = Arg("--passcodes", "passcodes", "list of door passcodes, e.g. 12345,7531,999999")
antipassback = Arg("--antipassback", str, "disabled, (1:2);(3:4), (1,3):(2,4), 1:(2,3) or 1:(2,3,4)")
firstcard = Arg("--firstcard", str, "08:30,16:45,normally open,firstcard only,[Mon,Tues,Fri]")
