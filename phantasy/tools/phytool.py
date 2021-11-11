# encoding: UTF-8

"""
command line application.
"""
import sys

__USAGE__ = """Usage: phytool <command> [<args>]

The support commands are:
  flame-vastart     Start FLAME virtual accelerator
  flame-lattice     Generate FLAME lattice file
  flame-settings    Read settings from FLAME lattice file (test.lat)
  impact-vastart    Start IMPACT virtual accelerator
  impact-lattice    Generate IMPACT lattice file (test.in)
  impact-settings   Read settings from IMPACT lattice file (test.in)
  import-model      Run IMPACT model and produce results
  frib-layout       Generate layout file from FRIB Expanded Lattice File (XLF)
  frib-channels     Generate a channels data file with FRIB naming conventions
  cfutil-export     Export channel data to file or Channel Finder Service
  cfutil-update     Update data of channel finder service
  snapshot-settings Generate lattice settings from snapshot file
  gen-mconfig       Generate machine configuration template file
  admin             Admin commands only for development (requires permission)
  help              Show help information for a specified topic
"""
  #cfutil-mark      Mark channel data with more properties and tags

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
    
    elif cmd == "cfutil-mark":
        from . import cfutil_mark
        return cfutil_mark.main()

    elif cmd == "cfutil-update":
        from . import cfutil_update
        return cfutil_update.main()

    elif cmd == "snapshot-settings":
        from . import snapshot_settings
        return snapshot_settings.main()

    elif cmd == "frib-layout":
        from . import frib_layout
        return frib_layout.main()

    elif cmd == "frib-channels":
        from . import frib_channels
        return frib_channels.main()

    elif cmd == "gen-mconfig":
        from . import gen_mconfig
        return gen_mconfig.main()

    elif cmd == "admin":
        from . import _admin
        return _admin.main()

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

    elif cmd == "cfutil-update":
        from . import cfutil_update
        cfutil_update.print_help()

    elif cmd == "snapshot-settings":
        from . import snapshot_settings
        snapshot_settings.print_help()

    elif cmd == "frib-layout":
        from . import frib_layout
        frib_layout.print_help()

    elif cmd == "frib-channels":
        from . import frib_channels
        frib_channels.print_help()

    elif cmd == "gen-mconfig":
        from . import gen_mconfig
        gen_mconfig.print_help()

    elif cmd == "admin":
        from . import _admin
        _admin.print_help()

    else:
        print("No help available for command: {}".format(cmd), file=sys.stderr)

    return 1
