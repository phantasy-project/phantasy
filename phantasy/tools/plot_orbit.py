#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" plot orbit from FLAME lattice file

Tong Zhang <zhangt@frib.msu.edu>
2016-11-18 15:19:00 PM EST
"""

import argparse
import sys
import os


parser = argparse.ArgumentParser(
        description="Plot particle orbit from FLAME lattice",
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('latfile', nargs='?',
        help='path of FLAME lattice file')
parser.add_argument('--x', dest='x', nargs='?', const='x', default=None,
        help='plot x orbit only')
parser.add_argument('--y', dest='y', nargs='?', const='y', default=None,
        help='plot y orbit only')
parser.add_argument('--output', dest='output', nargs='?',
        const='figure.png',
        default=None, help='save figure to output file (default: figure.png)')

parser.epilog= \
"""
Examples:
> {n} test.lat # plot both x and y in a pop up window
> {n} test.lat --x # plot only x
> {n} test.lat --y # plot only y
> {n} test.lat --output plot x and y to figure.png
> {n} test.lat --output --x # plot x to figure.png
> {n} test.lat --output test.eps --x # plot x to test.eps
""".format(n=os.path.basename(sys.argv[0]))

def main():
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(sys.argv[1:])

    if args.latfile is None:
        parser.print_help()
        sys.exit(1)


    from flame import Machine
    import traceback
    import logging

    logging.getLogger('flame.machine').disabled = True

    try:
        with open(args.latfile, 'rb') as f:
            m = Machine(f)
        s = m.allocState({})
        m_len = len(m)
        r = m.propagate(s, 0, m_len, range(m_len))
        z = [r[i][1].pos for i in range(m_len)]
        x = [r[i][1].moment0_env[0] for i in range(m_len)]
        y = [r[i][1].moment0_env[2] for i in range(m_len)]
    except:
        traceback.print_exc()
        sys.exit(1)

    import matplotlib.pyplot as plt

    import matplotlib.style as mplstyle
    mplstyle.use('bmh')

    plt.rcParams['font.size'] = 18
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['lines.linewidth'] = 2.0
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['figure.dpi'] = 90

    fig = plt.figure()
    ax = fig.add_subplot(111)
    if args.x is not None:
        line_x, = ax.plot(z, x, 'r-', label='$x$')
    if args.y is not None:
        line_y, = ax.plot(z, y, 'b-', label='$y$')
    if args.x is None and args.y is None:
        line_x, = ax.plot(z, x, 'r-', label='$x$')
        line_y, = ax.plot(z, y, 'b-', label='$y$')

    ax.set_xlabel('$z\,\mathrm{[m]}$')
    ax.set_ylabel('$\mathrm{Centroid\,\mathrm{[mm]}}$')
    ax.set_title(args.latfile, family="monospace")
    ax.legend(loc='best')

    if args.output is not None:
        fig.savefig(args.output)
        print("Generate figure to file: {}.".format(args.output))
    else:
        plt.show()

    return 0
