#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate template maching configuration file.
"""
import os
import sys
import logging
from argparse import ArgumentParser

from phantasy.facility.frib import generate_inifile


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" gen-mconfig",
                        description="Generate machine configuration files.")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0,
        help="set the amount of output")
parser.add_argument("filename", nargs="?", help="name or path of configuration file")

print_help = parser.print_help


def main():
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)

    mpath = args.filename
    if os.path.exists(mpath):
        print("Destination file already exists: {}".format(mpath), file=sys.stderr)
        return 1

    with open(mpath, 'w') as f:
        generate_inifile(out=f)

    return 0
