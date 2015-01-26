# encoding: UTF-8

"""
Implement physutil command 'impact-settings'.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser

from physutil import frib

from physutil.impact import settings


parser = ArgumentParser(description="Generate settings file from IMPACT input file.")
parser.add_argument("--xlf", required=True)
parser.add_argument("--cdf", required=True)
parser.add_argument("--testin", required=True)


help = parser.print_help


def main():
    """
    Entry point for command 'impact-settings'.
    """
    args = parser.parse_args(sys.argv[2:])

    #try:
    add = frib.read_xlf(args.xlf, args.cdf)
    
    #except Exception as e:
    #    print(e, file=sys.stderr)
    #    return 1

    #for elm in accel:
    #    print(elm)

    settings.write_settings(add, args.testin)



    return 0
