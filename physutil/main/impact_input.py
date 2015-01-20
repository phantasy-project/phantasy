# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser

from physutil import frib


parser = ArgumentParser(description="Generate input files for IMPACT simulation.")
parser.add_argument("--xlf", required=True)


help = parser.print_help


def main():
    """
    Entry point for command 'impact-input'.
    """
    args = parser.parse_args(sys.argv[2:])

    #try:
    accel = frib.read_xlf(args.xlf)
    #except Exception as e:
    #    print(e, file=sys.stderr)
    #    return 1

    for elm in accel:
        print(elm)

    return 0
