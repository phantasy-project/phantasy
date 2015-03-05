# encoding: UTF-8

"""
Implement phylib command 'cfutil-load'.
"""

from __future__ import print_function

import sys
from argparse import ArgumentParser

from phylib import cfg

from machine.frib import layout
from machine.frib.utils import cfutil


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

    try:
        accel = layout.fribxlf.build_accel(args.xlfpath, config, prefix=args.mach+":")
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    cfutil.load(accel, args.cfurl, username=args.user, password=args.passwd,
                start=args.start, end=args.end, machine=args.mach)

    return 0

