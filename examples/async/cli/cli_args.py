"""
CLI command arguments.
"""

import argparse

from collections import namedtuple

Arg = namedtuple("Arg", ["arg", "type", "help"])

controller = Arg("--controller", int, "controller serial number, e.g. 405419896")
card = Arg("--card", int, "card number, e.g. 10058400")
index = Arg("--index", int, "card index, e.g. 17")
antipassback = Arg("--antipassback", str, "disabled, (1:2);(3:4), (1,3):(2,4), 1:(2,3) or 1:(2,3,4)")


class CommandFormatter(argparse.HelpFormatter):
    def _format_actions(self, actions):
        parts = super()._format_actions(actions)
        if self._current_action and isinstance(self._current_action, argparse._SubParsersAction):
            parts = parts.replace(", ", "\n  ")
        return parts
