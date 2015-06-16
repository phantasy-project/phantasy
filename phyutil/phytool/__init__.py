# encoding: UTF-8

"""
Implement phylib command line application.
"""

from __future__ import print_function

import sys

__USAGE__ = """usage: phylib <command> [<args>]

The support commands are:
   cfutil-export    export channel data to file or Channel Finder Service
   impact-lattice   generate IMPACT lattice file (test.in)
   impact-vastart   start IMPACT virtual accelerator
   impact-settings  read settings from IMPACT lattice file (test.in)
   frib-layout      generate layout file from FRIB Expanded Lattice File (XLF)
   frib-channels    generate a channels data file with FRIB naming conventions
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

    elif cmd == "impact-settings":
        import impact_settings
        return impact_settings.main()

    elif cmd == "impact-vastart":
        import impact_vastart
        return impact_vastart.main()

    elif cmd == "impact-model":
        import impact_model
        return impact_model.main()

    elif cmd == "cfutil-export":
        import cfutil_export
        return cfutil_export.main()

    elif cmd == "frib-layout":
        from phyutil.phytool import frib_layout
        return frib_layout.main()

    elif cmd == "frib-channels":
        from phyutil.phytool import frib_channels
        return frib_channels.main()

    elif cmd == "help":
        return print_help()

    else:
        print(__USAGE__, file=sys.stderr)
        print("Unrecognized command: {}".format(cmd), file=sys.stderr)
        return 1


def print_help():
    """Display help information for the specified topic."""

    if len(sys.argv) < 3:
        print(__USAGE__, file=sys.stderr)
        print("See 'phylib help <command>' for more information on a specific command.", file=sys.stderr)
        return 1

    cmd = sys.argv[2].strip().lower()

    if cmd == "impact-lattice":
        import impact_lattice
        impact_lattice.print_help()

    elif cmd == "impact-settings":
        import impact_settings
        impact_settings.print_help()

    elif cmd == "impact-vastart":
        import impact_vastart
        impact_vastart.print_help()

    elif cmd == "impact-model":
        import impact_model
        impact_model.print_help()

    elif cmd == "cfutil-export":
        import cfutil_export
        cfutil_export.print_help()

    elif cmd == "frib-layout":
        from phyutil.phytool import frib_layout
        frib_layout.print_help()

    elif cmd == "frib-channels":
        from phyutil.phytool import frib_channels
        frib_channels.print_help()

    else:
        print("No help available for command: {}".format(cmd), file=sys.stderr)

    return 1
