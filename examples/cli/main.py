#!python3

"""
Implements a simple CLI to demonstrate the basic usage of the uhppoted-lib-python API.
"""

import argparse
import sys
import traceback

from commands import commands
from commands import execute


def parse_args():
    """
    Initialises arg_parse with the general and command specific options.
    """
    parser = argparse.ArgumentParser(description="uhppoted-lib-python example", usage=usage())

    parser.add_argument(
        "--bind",
        type=str,
        default="0.0.0.0",
        help="UDP IPv4 bind address. Defaults to 0.0.0.0:0",
    )

    parser.add_argument(
        "--broadcast",
        type=str,
        default="255.255.255.255:60000",
        help="UDP IPv4 broadcast address. Defaults to 255.255.255.255:60000",
    )

    parser.add_argument(
        "--listen",
        type=str,
        default="0.0.0.0:60001",
        help="UDP IPv4 event listener bind address. Defaults to 0.0.0.0:60001",
    )

    parser.add_argument(
        "--debug",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="displays sent and received packets",
    )

    parser.add_argument(
        "--destination",
        "-d",
        type=str,
        default=None,
        help="(optional) controller IPv4 address:port. Defaults to broadcast address.",
    )

    parser.add_argument(
        "--timeout",
        "-t",
        type=float,
        default=2.5,
        help="(optional) operation timeout (in seconds). Defaults to 2.5.",
    )

    parser.add_argument(
        "--udp",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="use UDP protocol",
    )
    parser.add_argument(
        "--tcp",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="use TCP protocol",
    )

    # ... command specific args
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    for c, v in commands().items():
        subparser = subparsers.add_parser(f"{c}")
        for arg in v.args:
            subparser.add_argument(arg.arg, type=arg.type, help=arg.help)

    return parser.parse_args()


def main():
    """
    Parses the command line and executes the requested command.
    """
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    args = parse_args()
    cmd = args.command
    debug = args.debug

    if cmd is None:
        print(usage())
        sys.exit(1)

    if args.udp and args.tcp:
        print()
        print("*** ERROR  conflicting UDP/TCP flags - choose one or the other (default is UDP)")
        print()
        sys.exit(1)

    if cmd in commands():
        try:
            execute(commands()[cmd], args)
        except Exception as x:  # pylint: disable=broad-exception-caught
            print()
            print(f"*** ERROR  {cmd}: {x}")
            print()
            if debug:
                print(traceback.format_exc())

            sys.exit(1)
    else:
        print()
        print(f"  ERROR: invalid command ({cmd})")
        print()


def usage() -> str:
    """
    Returns the usage description for the CLI as a string.
    """
    lines = []
    lines.append("")
    lines.append("  Usage: python3 main.py <options> <command> <args>")
    lines.append("")
    lines.append("  Supported commands:")

    for cmd in sorted(commands().keys()):
        lines.append(f"    {cmd}")

    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
