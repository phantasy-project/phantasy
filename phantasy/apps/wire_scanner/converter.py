#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Reading PM data file (.dat), convert to .json file.
"""

import json
import os
import logging
import sys
from argparse import ArgumentParser

_LOGGER = logging.getLogger("PM Data Converter")
#_LOGGER.addHandler(logging.StreamHandler())

FORK_MAPPING = {
    'DRV': 'fork',
    'DRV1': 'fork1',
    'DRV2': 'fork2'
}

KEY_MAPPING = {
    'PPOT': 'ppot_raw',
    'PPOT1': 'ppot_val1',
    'BC1': 'signal1',
    'PPOT2': 'ppot_val2',
    'BC2': 'signal2',
    'PPOT3': 'ppot_val3',
    'BC3': 'signal3',
    'OFST1': 'offset1',
    'OFST2': 'offset2',
    'OFST3': 'offset3'
}


parser = ArgumentParser(prog=os.path.basename(sys.argv[0]),
            description="Convert old PM data file into JSON formatted file.")
parser.add_argument("datfilepath", help="path of the old PM data file (.dat)")
parser.add_argument("jsonfilepath", help="path of the output JSON file")
parser.add_argument("-v", dest="verbosity", action='store_true',
        help="print out verbose message")

print_help = parser.print_help

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    args = parser.parse_args(sys.argv[1:])

    if args.verbosity:
        logging.getLogger().setLevel(logging.DEBUG)

    ifile, ofile = args.datfilepath, args.jsonfilepath
    if not os.path.isfile(ifile):
        print("Invalid input file path")
        print_help()
        sys.exit(1)

    data_dict = {}

    _LOGGER.debug("Reading data from {}...".format(ifile))
    with open(ifile, 'r') as f:
        for line in f:
            row = line.split()
            pv_name = row[0]
            ts = ' '.join(row[1:3])
            if 'OFST' not in pv_name:
                val = [float(x) for x in row[4:] if x != '0']
            else:
                val = float(row[3])
            row_dict = {'timestamp': ts, 'value': val, 'pv': pv_name}

            f, k = pv_name.split(':')[-1].split('_')
            fork_name = FORK_MAPPING.get(f)
            key_name = KEY_MAPPING.get(k)

            if fork_name not in data_dict:
                data_dict.setdefault(fork_name, {})
            data_dict[fork_name].update({key_name: row_dict})
            _LOGGER.debug("Processing line starts with {}...".format(pv_name))

    _LOGGER.debug("Saving data into {}...".format(ofile))
    with open(ofile, 'w') as f:
        json.dump({'data': data_dict}, f, indent=2, sort_keys=True)

    return 0


if __name__ == '__main__':
    main()
