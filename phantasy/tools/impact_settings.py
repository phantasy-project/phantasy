# encoding: UTF-8

"""
Implement phytool command 'impact-settings'.
"""
import os.path
import sys
import json
import logging
import traceback
from argparse import ArgumentParser

from phantasy.library.settings import build_impact_settings
from .common import loadMachineConfig
from .common import loadLayout


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" impact-settings",
                        description="Extract device settings from IMPACT input file based on accelerator layout.")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--mach", dest="machine", help="name of machine or path of machine directory")
parser.add_argument("--subm", dest="submach", help="name of segment")
parser.add_argument("--layout", dest="layoutpath", help="path of accelerator layout file")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("latticepath", help="path to input IMPACT lattice file (test.in)")
parser.add_argument("settingspath", nargs='?', help="path of output file with JSON format")

print_help = parser.print_help


def main():
    """
    Entry point for command 'impact-settings'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    try:
        mconfig, submach = loadMachineConfig(args.machine, args.submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading machine configuration:", e, file=sys.stderr)
        return 1


    try:
        layout = loadLayout(args.layoutpath, mconfig, submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading layout:", e, file=sys.stderr)
        return 1


    try:
        settings = build_impact_settings(layout, args.latticepath, start=args.start, end=args.end)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building settings:", e, file=sys.stderr)
        return 1


    try:
        if args.settingspath is not None:
            with open(args.settingspath, "w") as fp:
                json.dump(settings, fp, indent=2)
        else:
            json.dump(settings, sys.stdout, indent=2)
    except Exception as e:
        print("Error writing settings:", e, file=sys.stderr)
        return 1

    return 0

