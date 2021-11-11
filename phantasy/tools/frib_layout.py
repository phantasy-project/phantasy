# encoding: UTF-8

"""
Implement phytool command 'frib-layout'.

Convert [FRIB] Expanded Lattice File (XLF) to general layout data file.

:author: Dylan Maxwell <maxwelld@frib.msu.edu>
:date: 2015-06-09
"""
import logging
import os.path
import sys
import traceback
from argparse import ArgumentParser

from phantasy.facility.frib.layout import fribxlf
from phantasy.library.parser import Configuration

parser = ArgumentParser(prog=os.path.basename(sys.argv[0]) + " frib-layout",
                        description="Generate accelerator layout file from Expanded Lattice File (XLF).")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("layoutPath", nargs="?", help="path to output layout file")

print_help = parser.print_help


def main():
    """
    Entry point for command 'frib-layout'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.cfgpath is not None:
        try:
            config = Configuration(args.cfgpath)
        except FileNotFoundError:
            if args.verbosity > 0:
                traceback.print_exc()
            print("Error: configuration file not found: {}".format(args.cfgpath), file=sys.stderr)
            return 1

    else:
        config = Configuration()

    if (args.layoutPath is not None) and os.path.exists(args.layoutPath):
        print("Destination file already exists: {}".format(args.layoutPath), file=sys.stderr)
        return 1

    try:
        layout = fribxlf.build_layout(xlfpath=args.xlfpath, config=config)
    except Exception as e:
        if args.verbosity > 0:
            traceback.print_exc()
        print("Error reading XLF layout:", e, file=sys.stderr)
        return 1

    try:
        if args.layoutPath is not None:
            with open(args.layoutPath, "w") as stream:
                layout.write(stream, start=args.start, end=args.end)
        else:
            layout.write(sys.stdout, start=args.start, end=args.end)
    except Exception as e:
        if args.verbosity > 0:
            traceback.print_exc()
        print("Error writing accelerator layout:", e, file=sys.stderr)
        return 1

    return 0
