# encoding: UTF-8

"""
Implement phylib command 'impact-lattice'.
"""

from __future__ import print_function

import sys, os.path, json

from argparse import ArgumentParser

from .. import phylib
phylib.AUTO_CONFIG=False

from ..phylib import cfg

from ..machine.frib.lattice import impact

from ..machine.frib.layout import fribxlf


parser = ArgumentParser(description="Generate IMPACT lattice file (test.in).")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--stg", dest="stgpath", help="path to device settings file (.json)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--mach", help="name of machine (used to indicate VA)")
parser.add_argument("latpath", nargs="?", help="path to output IMPACT lattice file (test.in)")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-lattice'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.cfgpath != None:
        try:
            cfg.load(args.cfgpath)
        except:
            print("Error: configuration file not found: {}".format(args.cfgpath), file=sys.stderr)
            return 1
    
    elif not cfg.load(cfg.DEFAULT_LOCATIONS):
        print("Warning: no default configuration found: {}".format(cfg.DEFAULT_LOCATIONS), file=sys.stderr)


    if (args.latpath != None) and os.path.exists(args.latpath):
        print("Destination file already exists: {}".format(args.latpath), file=sys.stderr)
        return 1


    try:
        accel = fribxlf.build_accel(xlfpath=args.xlfpath, machine=args.mach)
    except Exception as e:
        print("Error building accelerator:", e, file=sys.stderr)
        return 1


    if args.stgpath == None:
        settings = None
    else:
        try:
            with open(args.stgpath, "r") as fp:
                settings = json.load(fp)
        except Exception as e:
            print(e, file=sys.stderr)
            return 1


    try:
        lat = impact.build_lattice(accel, settings=settings, start=args.start, end=args.end)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    if args.latpath != None:
        with open(args.latpath, "w") as fp:
            lat.write(file=fp)
    else:
        lat.write(file=sys.stdout)

    return 0
