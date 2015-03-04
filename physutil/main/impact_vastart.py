# encoding: UTF-8

"""
Implement physutil command 'impact-vastart'.
"""

from __future__ import print_function

import sys, json, signal, cothread

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
parser.add_argument("--mach")


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

    if args.mach != None:
        prefix = args.mach+":"
    else:
        prefix = ""

    try:
        accel = layout.fribxlf.build_accel(args.xlfpath, config, prefix=prefix)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    impact.va2.start(accel, config=config, settings=settings)
    cothread.WaitForQuit()
    impact.va2.stop()
    
    return 0
