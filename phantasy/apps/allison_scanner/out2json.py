#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Standardise raw output into JSON file.

Tong Zhang <zhangt@frib.msu.edu>
2019-04-18 04:44:48 PM EDT
"""

import json
from collections import OrderedDict

import numpy as np


def out2json(outfile, jsonfile=None):
    if jsonfile is None:
        fn, _ = outfile.rsplit('.', 1)
        jsonfile = '{}.json'.format(fn)

    r = []
    data = np.loadtxt(outfile)
    xoy = {0: 'x', 1: 'y'}[data[0]]
    pos_begin, pos_end, pos_step = data[1:4]
    volt_begin, volt_end, volt_step = data[4:7]
    pos_size = int((pos_end - pos_begin) / pos_step) + 1
    volt_size = int((volt_end - volt_begin) / volt_step) + 1

    data1 = data[7:].reshape(volt_size, pos_size)

    r.append(('xoy', xoy))
    r.append(('position', {'begin': pos_begin, 'end': pos_end, 'step': pos_step}))
    r.append(('voltage', {'begin': volt_begin, 'end': volt_end, 'step': volt_step}))
    r.append(('data', {'shape': (volt_size, pos_size), 'array': data1.tolist()}))

    with open(jsonfile, 'w') as fp:
        json.dump(OrderedDict(r), fp, indent=2)


def main():
    from argparse import ArgumentParser
    import os
    import sys

    parser = ArgumentParser(prog=os.path.basename(sys.argv[0]),
                            description="Convert old raw data file of Allison-Scanner measurment into JSON format.")
    parser.add_argument("outfilepath", help="path of the old raw data file (.out)")
    parser.add_argument("--json", dest="jsonfilepath", help="path of the output JSON file")
    print_help = parser.print_help

    if len(sys.argv) < 1:
        print_help()
        sys.exit(1)

    args = parser.parse_args(sys.argv[1:])

    outfile = args.outfilepath
    jsonfile = args.jsonfilepath

    out2json(outfile, jsonfile)
