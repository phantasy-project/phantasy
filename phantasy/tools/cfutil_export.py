#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implement phytool command 'cfutil-export'.
"""
import getpass
import logging
import os.path
import sys
import traceback
from argparse import ArgumentParser
from urllib.parse import urlparse

from phantasy.library.channelfinder import write_cfs
from phantasy.library.channelfinder import write_db
from phantasy.library.channelfinder import write_json
from phantasy.library.channelfinder import write_tb
from phantasy.library.pv import DataSource

_LOGGER = logging.getLogger(__name__)

parser = ArgumentParser(prog=os.path.basename(sys.argv[0]) + " cfutil-export",
                        description="Export channel data (.csv, .sqlite, CFS) to \
                        file (.csv, .sqlite, .json) or \
                        Channel Finder Service (CFS)")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0,
                    help="set the amount of output")
parser.add_argument("--from", dest='from_path',
                    help="path to input file (.csv, .sqlite, CFS) as channel data source")
parser.add_argument("--to", dest='to_path',
                    help="path to output file (.csv, .sqlite, .json) or CFS URL")
parser.add_argument("--user", dest="username", help="specify CFS username")
parser.add_argument("--pass", dest="password", help="specify CFS password")

print_help = parser.print_help


def main():
    """
    Entry point for command 'cfutil-export'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)

    channel_source = urlparse(args.from_path, "file")
    if channel_source.scheme == "file":
        sourcepath = channel_source.path
        if not os.path.isfile(channel_source.path):
            print("Cannot find channel data source: ", args.from_path, file=sys.stderr)
            return 1
    elif channel_source.scheme in ["http", "https"]:
        sourcepath = args.from_path
        if args.username is None:
            args.username = input("Enter username: ")
        if args.password is None:
            args.password = getpass.getpass("Enter password: ")
    else:
        print("Unknown source.".format(args.from_path), file=sys.stderr)
        return 1

    try:
        ds = DataSource(source=sourcepath, username=args.username, password=args.password)
        channels = ds.get_data()
    except Exception as e:
        print("Failed to get data from channel source:", e, file=sys.stderr)
        return 1

    cfsurl = urlparse(args.to_path, "file")
    if cfsurl.scheme == "file":
        (_, ext) = os.path.splitext(cfsurl.path)
        if ext in [".csv", ".sqlite", ".json"]:
            if os.path.exists(cfsurl.path):
                print("Destination file already exists: {}".format(args.to_path), file=sys.stderr)
                return 1
        else:
            print("Destination file format not supported: {}".format(args.to_path), file=sys.stderr)
            return 1

    elif cfsurl.scheme in ["http", "https"]:
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

    elif cfsurl.scheme in ["http", "https"]:
        # CFS
        try:
            if args.username is None:
                args.username = input("Enter username: ")

            if args.password is None:
                args.password = getpass.getpass("Enter password: ")

            # Channel Finder Client does not
            # like trailing slashes in the URL.
            if args.to_path.endswith("/"):
                uri = args.to_path[:-1]
            else:
                uri = args.to_path

            _export_to_cfweb(channels, uri, args.username, args.password)
        except Exception as e:
            if args.verbosity > 0:
                traceback.print_exc()
            print("Failed export to Channel Finder Service: ", e, file=sys.stderr)
            return 1

    return 0


def _export_to_sqlite(channels, path):
    write_db(channels, path, overwrite=True)


def _export_to_csv(channels, path):
    write_tb(channels, path, overwrite=True)


def _export_to_json(channels, path):
    write_json(channels, path, overwrite=True)


def _export_to_cfweb(channels, uri, username, password):
    write_cfs(channels, uri, username=username, password=password, force=True)
