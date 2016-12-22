# encoding: UTF-8

"""
command line application.
"""

from __future__ import print_function

import sys

__USAGE__ = """usage: phytool <command> [<args>]

The support commands are:
   flame-vastart    start FLAME virtual accelerator
   flame-lattice    generate FLAME lattice file
   flame-settings   read settings from FLAME lattice file (test.lat)
   impact-vastart   start IMPACT virtual accelerator
   impact-lattice   generate IMPACT lattice file (test.in)
   impact-settings  read settings from IMPACT lattice file (test.in)
   import-model     run IMPACT model and produce results
   frib-layout      generate layout file from FRIB Expanded Lattice File (XLF)
   frib-channels    generate a channels data file with FRIB naming conventions
   cfutil-export    export channel data to file or Channel Finder Service
   help             show help information for a specified topic
"""


def main():
    """Entry point of command line application."""

    if len(sys.argv) < 2:
        print(__USAGE__, file=sys.stderr)
        return 1

    cmd = sys.argv[1].strip().lower()

    if cmd == "impact-lattice":
        from . import impact_lattice
        return impact_lattice.main()

    elif cmd == "flame-lattice":
        from . import flame_lattice
        return flame_lattice.main()

    elif cmd == "flame-settings":
        from . import flame_settings
        return flame_settings.main()

    elif cmd == "flame-vastart":
        from . import flame_vastart
        return flame_vastart.main()

    elif cmd == "impact-settings":
        from . import impact_settings
        return impact_settings.main()

    elif cmd == "impact-vastart":
        from . import impact_vastart
        return impact_vastart.main()

    elif cmd == "impact-model":
        from . import impact_model
        return impact_model.main()

    elif cmd == "cfutil-export":
        from . import cfutil_export
        return cfutil_export.main()

    elif cmd == "frib-layout":
        from . import frib_layout
        return frib_layout.main()

    elif cmd == "frib-channels":
        from . import frib_channels
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
        print("See 'phytool <command> --help' for more information on a specific command.", file=sys.stderr)
        return 1

    cmd = sys.argv[2].strip().lower()

    if cmd == "impact-lattice":
        from . import impact_lattice
        impact_lattice.print_help()

    elif cmd == "impact-settings":
        from . import impact_settings
        impact_settings.print_help()

    elif cmd == "impact-vastart":
        from . import impact_vastart
        impact_vastart.print_help()

    elif cmd == "impact-model":
        from . import impact_model
        impact_model.print_help()

    elif cmd == "flame-settings":
        from . import flame_settings
        flame_settings.print_help()

    elif cmd == "cfutil-export":
        from . import cfutil_export
        cfutil_export.print_help()

    elif cmd == "frib-layout":
        from . import frib_layout
        frib_layout.print_help()

    elif cmd == "frib-channels":
        from . import frib_channels
        frib_channels.print_help()

    else:
        print("No help available for command: {}".format(cmd), file=sys.stderr)

    return 1
