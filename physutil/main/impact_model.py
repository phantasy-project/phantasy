# encoding: UTF-8

"""
Implement physutil command 'impact-model'.
"""

from __future__ import print_function

import sys, json, numpy

from argparse import ArgumentParser

from physutil import cfg, layout, lattice, model


parser = ArgumentParser(description="Run IMPACT model and produce results")
parser.add_argument("--xlf", dest="xlfpath", required=True, help="Path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--cfg", dest="cfgpath", required=True, help="Path to physutil configuration file (.json)")
parser.add_argument("--settings", required=True, help="Path to device settings file (.json)")


help = parser.print_help


def main():
    """
    Entry point for command 'impact-run'.
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

    #accel.write()

    try:
        with open(args.settings, "r") as fp:
            settings = json.load(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    try:
        lat = lattice.impact.build_lattice(accel, config, settings, start="LS1", end=None)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    result = model.impact.build_result(lat, config)

    orbit = result.get_orbit("XY")

    for idx in xrange(orbit.shape[0]):
        sys.stdout.write("{}, {}, {}\r\n".format(orbit[idx,0], orbit[idx,1], orbit[idx,2]))

    return 0
