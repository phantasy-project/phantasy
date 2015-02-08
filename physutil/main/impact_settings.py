# encoding: UTF-8

"""
Implement physutil command 'impact-settings'.
"""

from __future__ import print_function

import sys, json

from argparse import ArgumentParser

#from physutil import frib

from physutil import cfg, layout, lattice

#from physutil.lattice import 


parser = ArgumentParser(description="Generate settings file from IMPACT input file.")
parser.add_argument("--xlf", dest="xlfpath", required=True)
parser.add_argument("--cfg", dest="cfgpath", required=True)
parser.add_argument("--start")
parser.add_argument("--end")
parser.add_argument("latpath")
parser.add_argument("setpath")


help = parser.print_help


def main():
    """
    Entry point for command 'impact-settings'.
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
        accel = layout.fribxlf.build_accel(args.xlfpath, config)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    settings = lattice.impact.build_settings(accel, args.latpath, start=args.start, end=args.end)

    with open(args.setpath, "w") as fp:
        json.dump(settings, fp, indent=2)
    
    return 0
