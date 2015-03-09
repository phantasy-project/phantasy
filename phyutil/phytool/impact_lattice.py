# encoding: UTF-8

"""
Implement phylib command 'impact-lattice'.
"""

from __future__ import print_function

import sys, os.path, json

from argparse import ArgumentParser

from phylib import cfg

from machine.frib import layout, lattice


parser = ArgumentParser(description="Generate IMPACT lattice file (test.in).")
parser.add_argument("--xlf", dest="xlfpath", required=True, help="Path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--cfg", dest="cfgpath", required=True, help="Path to configuration file (.json)")
parser.add_argument("--settings", help="Path to device settings file (.json)")
parser.add_argument("--fort-map", help="Path to output result data mapping file")
parser.add_argument("--start", help="Element name to start lattice generation")
parser.add_argument("--end", help="Element name to end lattice generation")
#parser.add_argument("-f", help="Force overwrite of existing files")
parser.add_argument("latpath", nargs="?", default=None, help="Path to output IMPACT lattice file (default: test.in)")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-lattice'.
    """
    args = parser.parse_args(sys.argv[2:])

    if (args.latpath != None) and os.path.exists(args.latpath):
        print("Destination file already exists: {}".format(args.latpath), file=sys.stderr)
        return 1

    try:
        with open(args.cfgpath, "r") as fp:
            config = cfg.Configuration()
            config.readfp(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    try:
        accel = layout.fribxlf.build_accel(args.xlfpath, config)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    #accel.write()

    if args.settings == None:
        settings = {}
    else:
        try:
            with open(args.settings, "r") as fp:
                settings = json.load(fp)
        except Exception as e:
            print(e, file=sys.stderr)
            return 1


    try:
        lat = lattice.impact.build_lattice(accel, config, settings, start=args.start, end=args.end)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    if args.latpath != None:
        with open(args.latpath, "w") as fp:
            lat.write(file=fp)
    else:
        lat.write(file=sys.stdout)

    return 0
