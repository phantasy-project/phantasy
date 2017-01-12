# encoding: UTF-8

"""
Implement phytool command 'cfutil-export'.
"""

from __future__ import print_function

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


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" cfutil-export",
                        description="Export channel data (.csv, .sqlite) to \
                        file (.csv, .sqlite, .json) or \
                        Channel Finder Service (CFS)")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0,
        help="set the amount of output")
parser.add_argument("--from", dest='from_path',
        help="path to input file (.csv, .sqlite) as channel data source")
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

    channel_source = args.from_path
    if not os.path.isfile(channel_source):
        print("Cannot find channel data source: ", args.from_path, file=sys.stderr)
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
                args.username = raw_input("Enter username: ")

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


def _export_to_sqlite(channels, path):
    write_db(channels, path, overwrite=True)


def _export_to_csv(channels, path):
    write_tb(channels, path, overwrite=True)


def _export_to_json(channels, path):
    write_json(channels, path, overwrite=True)


def _export_to_cfweb(channels, uri, username, password):
    write_cfs(channels, uri, username=username, password=password, force=True)
    """
    # Channel data with the following structure:
    #
    # {
    #    "CH:NAME1": {
    #           "properties":{
    #                 "system":"SEG1",
    #                 "device":"DEV1"
    #            },
    #            "tags":[
    #                "phyutil.sys.LS1",
    #                "phyutil.sub.CA01"
    #            ]
    #    },
    #    "CH:NAME2: {
    #            "properties":{
    #                 "system":"SEG1",
    #                 "device":"DEV2"
    #            }
    #            "tags":[
    #                "phyutil.sys.LS1",
    #                "phyutil.sub.BTS"
    #            ]
    #    }
    # }
    #
    client = ChannelFinderClient(BaseURL=uri, username=username, password=password)

    data = []
    existing_tags = []
    existing_properties = []
    for name, properties, tags in channels:
        c = {'name':name, 'owner':username, 'properties':[], 'tags':[]}

        for tname in tags:
             t = {'name':tname, 'owner':username}
             if tname not in existing_tags:
                 if not client.findTag(tname):
                     client.set(tag=t)
                     _LOGGER.debug("Tag created in Channel Finder: %s", tname)
                 else:
                     _LOGGER.debug("Tag exists in Channel Finder: %s", tname)
                 existing_tags.append(tname)
             _LOGGER.debug("Add tag '%s' to channel: %s", tname, name)
             c['tags'].append(t)

        for pname, pvalue in properties.iteritems():
             p = {'name':pname, 'owner':username}
             if pname not in existing_properties:
                 if not client.findProperty(pname):
                     client.set(property=p)
                     _LOGGER.debug("Property created in Channel Finder: %s", pname)
                 else:
                     _LOGGER.debug("Property exists in Channel Finder: %s", pname)
                 existing_properties.append(pname)
             p['value'] = pvalue
             _LOGGER.debug("Add property '%s' with value '%s' to channel: %s", pname, pvalue, name)
             c['properties'].append(p)

        data.append(c)

    client.set(channels=data)
    """

