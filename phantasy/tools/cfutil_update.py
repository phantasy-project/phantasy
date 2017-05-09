#!/usr/bin/python

"""Update PV data in Channel Finder Service, with input channels file.

.. Tong Zhang <zhangt@frib.msu.edu>
.. 2017-02-16 13:46:58 EST
"""

import argparse
import sys
import os
import getpass

from channelfinder import ChannelFinderClient
from phantasy.library.pv import DataSource
from phantasy.library.channelfinder import write_cfs

try:
    r_input = raw_input
except NameError:
    r_input = input

parser = argparse.ArgumentParser(
    prog=os.path.basename(sys.argv[0]) + " cfutil-update",
    description="Update Channel Finder service with given channels file",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('channelsfile', nargs='?',
                    help='path of channels file (csv, SQLite)')
parser.add_argument('--op', dest='op', nargs='?', const='add', default='add',
                    help="operation applied onto channel finder service, 'add' (default) or 'del'")
parser.add_argument('--url', dest='url',
                    help='URL of channel finder service, https://127.0.0.1:8181/ChannelFinder by default')
parser.add_argument('--user', dest='username',
                    help='username of channel finder service')
parser.add_argument('--pass', dest='password',
                    help='password of username')

print_help = parser.print_help


def main():
    if len(sys.argv) < 2:
        parser.print_help()
        return 1

    args = parser.parse_args(sys.argv[2:])

    if args.channelsfile is None:
        parser.print_help()
        return 1

    if args.channelsfile is None:
        parser.print_help()
        return 1

    try:
        if args.url is None:
            cfc = ChannelFinderClient()
            args.url = "https://127.0.0.1:8181/ChannelFinder"
        else:
            if args.username is None:
                args.username = r_input("Enter username: ")
            if args.password is None:
                args.password = getpass.getpass("Enter password: ")
            cfc = ChannelFinderClient(args.url, args.username, args.password)
    except:
        print("Cannot connect to channelfinder service.")
        return 1

    ds = DataSource(source=args.channelsfile)
    pv_data = ds.get_data()
    if args.op == 'del':
        try:
            [cfc.delete(channelName=pv['name']) for pv in pv_data]
        except:
            print("Channels deleting ERROR, probably channel(s) does not exist.")
    else:  # args.op == 'add'
        if args.username is None:
            write_cfs(pv_data, args.url, force=True)
        else:
            write_cfs(pv_data, args.url,
                      username=args.username, password=args.password)
    return 0
