# encoding: UTF-8

"""
Implement phylib command 'impact-vastart'.
"""

from __future__ import print_function

import sys, os.path, json, logging

from argparse import ArgumentParser

from .. import phylib
phylib.AUTO_CONFIG=False

from ..phylib import cfg

from ..machine.frib.layout import fribxlf

from ..machine.frib.virtaccel import impact

parser = ArgumentParser(description="Start the virtual accelerator using IMPACT simulation")


parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--stg", dest="stgpath", help="path to device settings file (.json)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--mach", help="name of machine (used to indicate VA)")
parser.add_argument("--data", dest="datapath", help="path to directory with IMPACT data")
parser.add_argument("--work", dest="workpath", help="path to directory for executing IMPACT")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-vastart'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    if args.cfgpath != None:
        try:
            cfg.load(args.cfgpath)
        except:
            print("Error: configuration file not found: {}".format(args.cfgpath), file=sys.stderr)
            return 1

    elif not cfg.load(cfg.DEFAULT_LOCATIONS):
        print("Warning: no default configuration found: {}".format(cfg.DEFAULT_LOCATIONS), file=sys.stderr)


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
            print("Error reading settings file:", e, file=sys.stderr)
            return 1


    try:
        va = impact.build(accel, settings=settings, machine=args.mach, start=args.start,
                             end=args.end, data_dir=args.datapath, work_dir=args.workpath)
    except Exception as e:
        print("Error building virtual accelerator:", e, file=sys.stderr)
        return 1


    try:
        va.start(True)
    except Exception as e:
        print("Error starting virtual accelerator:", e, file=sys.stderr)
        return 1


    try:
        va.wait()
    except Exception as e:
        print("Error executing virtual accelerator:", e, file=sys.stderr)
        return 1


    return 0

