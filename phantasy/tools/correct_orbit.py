#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" quickly correct orbit

Tong Zhang <zhangt@frib.msu.edu>
2016-11-18 16:51:00 PM EST
"""

import argparse
import sys
import os


parser = argparse.ArgumentParser(
        description="Correct beam orbit in a pretty easy way",
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('latfile', nargs='?',
        help='path of FLAME lattice file')
parser.add_argument('--x', dest='x', nargs='?', const='x', default=None, 
        help='correct x only')
parser.add_argument('--y', dest='y', nargs='?', const='y', default=None,
        help='correct y only')
parser.add_argument('--pseudo_all', dest='pseudo_all', nargs='?', const=True, default=False,
        help='select all elements as monitors')
parser.add_argument('--echo', dest='echo', nargs='?', const=True, default=False,
        help='if print output information during correction')
parser.add_argument('--iternum', dest='iternum', nargs='?', type=int, default=10,
        help='maximum iteration number')
parser.add_argument('--outfile', dest='outfile', nargs='?', 
        default=sys.stdout, help='output lattice file (default: stdout)')

parser.epilog= \
"""
Examples:
> {n} test.lat --iternum 20 # define iteration number
> {n} test.lat --x # correct only x
> {n} test.lat --echo # print optimization output
> {n} test.lat --pseudo_all  # take all element as BPMs
> {n} test.lat --outfile # correct x and y, and print new lattice
> {n} test.lat --outfile new.lat # correct x and y, and save lattice to new.lat
""".format(n=os.path.basename(sys.argv[0]))

def main():
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(sys.argv[1:])

    if args.latfile is None:
        parser.print_help()
        sys.exit(1)

    import traceback
    import genopt

    iternum = 10 if args.iternum is None else args.iternum
    outfile = sys.stdout if args.outfile is None else args.outfile

    try:
        oc = genopt.DakotaOC(lat_file=args.latfile)
        bpms = oc.get_elem_by_type('bpm')
        oc.set_bpms(bpm=bpms, pseudo_all=args.pseudo_all)

        if args.x is not None and args.y is None:
            hcors = oc.get_all_cors(type='h')
            oc.set_cors(hcor=hcors)
            oc.ref_flag = 'xy'
        elif args.x is None and args.y is not None:
            vcors = oc.get_all_cors(type='v')
            oc.set_cors(vcor=vcors)
            oc.ref_flag = 'xy'
        else:
            hcors = oc.get_all_cors(type='h')
            vcors = oc.get_all_cors(type='v')
            oc.set_cors(hcor=hcors, vcor=vcors)
            oc.ref_flag = 'xy'
        oc.simple_run(mpi=True, iternum=iternum, echo=args.echo)
        oc.get_opt_latfile(outfile)
    except:
        traceback.print_exc()
        sys.exit(1)
      
    return 0
