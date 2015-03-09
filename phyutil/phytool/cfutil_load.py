# encoding: UTF-8

"""
Implement phylib command 'cfutil-load'.
"""

from __future__ import print_function

import sys
from argparse import ArgumentParser

from ..phylib import cfg

from ..phylib.channelfinder import cfutil

from ..machine.frib.layout import fribxlf




parser = ArgumentParser(description="Load channel data into Channel Finder")
parser.add_argument("--xlf", dest="xlfpath", required=True, help="Path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--cfg", dest="cfgpath", required=True, help="Path to configuration file (.json)")
parser.add_argument("--start", help="Element name to start lattice generation")
parser.add_argument("--end", help="Element name to end lattice generation")
parser.add_argument("--mach", help="Specify machine version id")
parser.add_argument("--user", help="Specify CF username")
parser.add_argument("--pass", dest="passwd", help="Specify CF password")
parser.add_argument("cfurl", help="Channel finder root URL")

help = parser.print_help


def main():
    """
    Entry point for command 'cfutil-load'.
    """
    args = parser.parse_args(sys.argv[2:])

    try:
        with open(args.cfgpath, "r") as fp:
            config = cfg.Configuration()
            config.readfp(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    if args.mach != None:
        prefix = args.mach+":"
    else:
        prefix = ""

    try:
        accel = fribxlf.build_accel(args.xlfpath, config, prefix=prefix)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    if args.mach != None:
        machine=args.mach
    else:
        machine=""

    cfutil.load(accel, args.cfurl, username=args.user, password=args.passwd,
                start=args.start, end=args.end, machine=machine)

    return 0

