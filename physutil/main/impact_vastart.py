# encoding: UTF-8

"""
Implement physutil command 'impact-vastart'.
"""

from __future__ import print_function

import sys, json

from argparse import ArgumentParser

#from physutil import frib

from physutil import cfg, layout, impact

#from physutil.lattice import 


parser = ArgumentParser(description="Start the virtual accelerator using IMPACT")
parser.add_argument("--xlf", dest="xlfpath", required=True)
parser.add_argument("--cfg", dest="cfgpath", required=True)
parser.add_argument("--stg", dest="stgpath", required=True)
parser.add_argument("--start")
parser.add_argument("--end")


help = parser.print_help


def main():
    """
    Entry point for command 'impact-vastart'.
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
        with open(args.stgpath, "r") as fp:
            settings = json.load(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1   

    try:
        accel = layout.fribxlf.build_accel(args.xlfpath, config, prefix="D_M:")
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    impact.va.start(accel, config=config, settings=settings)
        
    return 0
