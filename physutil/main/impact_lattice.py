# encoding: UTF-8

"""
Implement physutil command 'impact-lattice'.
"""

from __future__ import print_function

import sys, json

from argparse import ArgumentParser

from physutil.config import Configuration

from physutil import frib

from physutil import impact

#from physutil.impact import lattice


parser = ArgumentParser(description="Generate IMPACT lattice file (test.in).")
parser.add_argument("--xlf", dest="xlfpath", required=True, help="Path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--config", dest="confpath", required=True, help="Path to configuration file (.json)")
parser.add_argument("--settings", required=True, help="Path to device settings file (.json)")
parser.add_argument("--fort-map", help="Path to output result data mapping file")
parser.add_argument("--start", help="Element name to start lattice generation")
parser.add_argument("--end", help="Element name to end lattice generation")
parser.add_argument("-f", help="Force overwrite of existing files")
parser.add_argument("latpath", default="test.in", help="Path to output IMPACT lattice file (default: test.in)")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-lattice'.
    """
    args = parser.parse_args(sys.argv[2:])

    try:
        with open(args.confpath, "r") as fp:
            config = Configuration()
            config.readfp(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    #try:
    accel = frib.build_accel(args.xlfpath, config)
    #except Exception as e:
    #    print(e, file=sys.stderr)
    #    return 1

    #accel.print_details()

    try:
        with open(args.settings, "r") as fp:
            settings = json.load(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    #try:
    lat = impact.build_lattice(accel, config, settings)
    #except Exception as e:
    #    print(e, file=sys.stderr)
    #    return 1

    lat.write()


    return 0
