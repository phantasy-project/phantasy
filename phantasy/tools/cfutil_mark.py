# encoding: UTF-8

"""
[TODO]
Implement phytool command 'cfutil-mark'.
"""

import sys
import os.path
import logging
import json
import traceback
import getpass

from urlparse import urlparse
from argparse import ArgumentParser
from collections import OrderedDict

from channelfinder import ChannelFinderClient

from phantasy.library.channelfinder import write_db
from phantasy.library.channelfinder import write_tb
from phantasy.library.channelfinder import write_json
from phantasy.library.channelfinder import write_cfs
from phantasy.library.pv import DataSource

_LOGGER = logging.getLogger(__name__)


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" cfutil-mark",
                        description="Mark raw channel data with more \
                                properties/tags, and export into .csv file \
                                for review. For example, \
                                the raw data from channel finder service \
                                (pushed by recsync service) usually only \
                                contain PV name string.")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0,
        help="set the amount of output")
parser.add_argument("--source", dest='source',
        help="Channel data source, path of file (.csv, .sqlite) or URL of Channel finder service")
parser.add_argument("--user", dest="username",
        help="specify CFS username")
parser.add_argument("--pass", dest="password",
        help="specify CFS password")
parser.add_argument("--export", dest='csvfile',
        help="path of .csv output file")

print_help = parser.print_help


def main():
    """
    Entry point for command 'cfutil-mark'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)

    channel_source = args.source
    if not os.path.isfile(channel_source):
        print("Cannot find channel data source: ", args.source, file=sys.stderr)
        return 1

    try:
        ds = DataSource(source=channel_source)
        channels = ds.get_data()
    except Exception as e:
        print("Failed to get data from channel source:", e, file=sys.stderr)
        return 1


    cfsurl = urlparse(args.to_path, "file")
    if cfsurl.scheme == "file":
        (_, ext) = os.path.splitext(cfsurl.path)
        if ext in [ ".csv", ".sqlite", ".json" ]:
            if os.path.exists(cfsurl.path):
                print("Destination file already exists: {}".format(args.to_path), file=sys.stderr)
                return 1
        else:
            print("Destination file format not supported: {}".format(args.to_path), file=sys.stderr)
            return 1

    elif cfsurl.scheme in [ "http", "https" ]:
        # TODO: check if server is available?
        pass

    else:
        print("Destination path not supported: {}".format(args.to_path), file=sys.stderr)
        return 1


    if cfsurl.scheme == "file":
        # local file
        if ext == ".sqlite":
            try:
                _export_to_sqlite(channels, cfsurl.path)
            except Exception as e:
                print("Failed export to SQLite file: ", e, file=sys.stderr)
                return 1

        if ext == ".csv":
            try:
                _export_to_csv(channels, cfsurl.path)
            except Exception as e:
                print("Failed export to CSV file: ", e, file=sys.stderr)
                return 1

        if ext == ".json":
            try:
                _export_to_json(channels, cfsurl.path)
            except Exception as e:
                print("Failed export to JSON file: ", e, file=sys.stderr)
                return 1

    elif cfsurl.scheme in [ "http", "https" ]:
        # CFS
        try:
            if args.username == None:
                args.username = input("Enter username: ")

            if args.password == None:
                args.password = getpass.getpass("Enter password: ")

            # Channel Finder Client does not
            # like trailing slashes in the URL.
            if args.to_path.endswith("/"):
                uri = args.to_path[:-1]
            else:
                uri = args.to_path

            _export_to_cfweb(channels, uri, args.username, args.password)
        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Failed export to Channel Finder Service: ", e, file=sys.stderr)
            return 1

    return 0


def _export_to_csv(channels, path):
    write_tb(channels, path, overwrite=True)

def _export_to_sqlite(channels, path):
    pass

def _export_to_json(channels, path):
    pass

def _export_to_cfweb(channels, path):
    pass
