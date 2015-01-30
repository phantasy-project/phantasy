# encoding: UTF-8

"""
Implement physutil command line application.
"""

from __future__ import print_function

import sys



__USAGE__ = """usage: physutil <command> [<args>]

The support commands are:
   impact-lattice   generate IMPACT lattice file (test.in)
   impact-settings  read settings from IMPACT lattice file (test.in)
   help             show help information for a specified topic
"""


def main():
    """Entry point of command line application."""

    if len(sys.argv) < 2:
        print(__USAGE__, file=sys.stderr)
        return 1

    cmd = sys.argv[1].strip().lower()

    if cmd == "impact-lattice":
        import impact_lattice
        return impact_lattice.main()

    if cmd == "impact-settings":
        import impact_settings
        return impact_settings.main()

    elif cmd == "help":
        return help()

    else:
        print(__USAGE__, file=sys.stderr)
        print("Unrecognized command: {}".format(cmd), file=sys.stderr)
        return 1


def help():
    """Display help information for the specified topic."""

    if len(sys.argv) < 3:
        print(__USAGE__, file=sys.stderr)
        print("See 'physutil help <command>' for more information on a specific command.", file=sys.stderr)
        return 1

    cmd = sys.argv[2].strip().lower()

    if cmd == "impact-lattice":
        import impact_lattice
        impact_input.help()

    elif cmd == "impact-settings":
        import impact_settings
        impact_settings.help()

    else:
        print("No help available for command: {}".format(cmd), file=sys.stderr)

    return 1
