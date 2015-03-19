# encoding: UTF-8

"""
Implement phylib command 'impact-vastart'.
"""

from __future__ import print_function

import sys, os.path
import json
from argparse import ArgumentParser

import cothread

from ..phylib import cfg

from ..machine.frib.layout import fribxlf
from ..machine.frib.virtaccel import impact

parser = ArgumentParser(description="Start the virtual accelerator using IMPACT")
parser.add_argument("--xlf", dest="xlfpath", required=True)
parser.add_argument("--cfg", dest="cfgpath", required=True)
parser.add_argument("--stg", dest="stgpath", required=True)
parser.add_argument("--data", dest="datapath", required=True)
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

    #try:
        accel = fribxlf.build_accel(args.xlfpath, config, prefix=prefix)
    #except Exception as e:
    #    print(e, file=sys.stderr)
    #    return 1

    impact.start(accel, config=config, settings=settings, data_dir=os.path.abspath(args.datapath))
    cothread.WaitForQuit()
    impact.stop()
    
    return 0
