# -*- coding: utf-8 -*-
"""Generate settings (json) from .snp file (exported from Save&Restore app)
"""

from argparse import ArgumentParser
import os
import sys
import json

from phantasy import generate_settings
from phantasy import MachinePortal
from phantasy import set_loglevel
from phantasy import disable_warnings


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" snapshot-settings",
                        description="Generate lattice settings from snapshot file.")
parser.add_argument("snpfile", nargs="?",
                    help="path for snapshot file exported from Save&Restore app")
parser.add_argument("jsonfile", nargs="?",
                    help="path of output json data with lattice settings")
parser.add_argument("-v", dest="verbosity", nargs="?", type=int, const=1, default=0,
                    help="set the amount of output")
parser.add_argument("--mach", dest="machine",
                    help="name of machine or path of machine directory")
parser.add_argument("--latname", dest="latname",
                    help="name of lattice (segment) of machine")

print_help = parser.print_help

def main():
    args = parser.parse_args(sys.argv[2:])

    mach = args.machine
    if mach is None:
        print("Machine (--mach) not found.")
        print_help()
        return 1

    if args.verbosity == 0:
        disable_warnings(50)
    elif args.verbosity == 1:
        set_loglevel('info')
    elif args.verbosity > 1:
        set_loglevel('debug')

    snpfile = args.snpfile

    if args.latname is None:
        mp = MachinePortal(machine=mach)
    else:
        mp = MachinePortal(machine=mach, segment=args.latname)

    lattice = mp.work_lattice_conf
    settings = generate_settings(snpfile, lattice)
    with open(args.jsonfile, 'wb') as f:
        json.dump(settings, f, indent=2)

    return 0