# encoding: UTF-8

"""
Implement phylib command line application.
"""

from __future__ import print_function

import sys

from utils import impact_settings, impact_model, impact_vastart, impact_lattice, cfutil_load


__USAGE__ = """usage: phylib <command> [<args>]

The support commands are:
   cfutil-load      load channel data into Channel Finder
   impact-lattice   generate IMPACT lattice file (test.in)
   impact-vastart   start IMPACT virtual accelerator
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
        import utils.impact_lattice
        return impact_lattice.main()

    elif cmd == "impact-settings":
        from utils import impact_settings

        return impact_settings.main()

    elif cmd == "impact-vastart":
        import utils.impact_vastart
        return impact_vastart.main()

    elif cmd == "impact-model":
        import utils.impact_model
        return impact_model.main()

    elif cmd == "cfutil-load":
        import utils.cfutil_load
        return cfutil_load.main()

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
        print("See 'phylib help <command>' for more information on a specific command.", file=sys.stderr)
        return 1

    cmd = sys.argv[2].strip().lower()

    if cmd == "impact-lattice":
        import utils.impact_lattice
        impact_input.help()

    elif cmd == "impact-settings":
        import utils.impact_settings
        impact_settings.help()

    elif cmd == "impact-vastart":
        import utils.impact_vastart
        impact_vastart.help()

    elif cmd == "impact-model":
        import utils.impact_model
        impact_model.help()

    elif cmd == "cfutil-load":
        import utils.cfutil_load
        cfutil_load.help()

    else:
        print("No help available for command: {}".format(cmd), file=sys.stderr)

    return 1
