# encoding: UTF-8

"""
Implement phytool command 'impact-settings'.
"""

from __future__ import print_function

import os.path, sys, json

from argparse import ArgumentParser

from .. import phylib
phylib.AUTO_CONFIG=False

from ..phylib import cfg

from ..machine.frib.settings import impact

from ..machine.frib.layout import fribxlf


parser = ArgumentParser(description="Extract device settings from IMPACT input file based on accelerator layout.")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--mach", help="name of machine (used to indicate VA)")
#parser.add_argument("-v", action="store_true", help="increase verbosity")
parser.add_argument("latpath", help="path to input IMPACT lattive file (test.in)")
parser.add_argument("stgpath", nargs='?', help="path of output file with JSON format")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-settings'.
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


    if (args.stgpath != None) and os.path.exists(args.stgpath):
        print("Error: destination file already exists: {}".format(args.stgpath), file=sys.stderr)
        return 1


    try:
        accel = fribxlf.build_accel(xlfpath=args.xlfpath, machine=args.mach)
    except Exception as e:
        print("Error building accelerator:", e, file=sys.stderr)
        return 1


    try:
        settings = impact.build_settings(accel, args.latpath, start=args.start, end=args.end)
    except Exception as e:
        print("Error building settings:", e, file=sys.stderr)
        return 1

    
    try:
        if args.stgpath != None:
            fp = open(args.stgpath, "w")
        else:
            fp = sys.stdout
    except Exception as e:
        print("Error openning output file:", e, file=sys.stderr)
        return 1    


    try:
        json.dump(settings, fp, indent=2)
    except Exception as e:
        print("Error writing settings:", e, file=sys.stderr)
        return 1
    finally:
        if fp != sys.stdout: fp.close()

    return 0

