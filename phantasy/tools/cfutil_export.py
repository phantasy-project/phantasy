# encoding: UTF-8

"""
Implement phytool command 'cfutil-export'.
"""

from __future__ import print_function

import sys, os.path, logging, json, traceback, getpass
from urlparse import urlparse
from argparse import ArgumentParser
from collections import OrderedDict

from channelfinder import ChannelFinderClient

from ..library.misc import read_csv
from ..library.channelfinder import importCfLocalData

_LOGGER = logging.getLogger(__name__)


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" cfutil-export",
                        description="Export channel data to file or Channel Finder Service")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--user", dest="username", help="specify ChannelFinder username")
parser.add_argument("--pass", dest="password", help="specify ChannelFinder password")
parser.add_argument("channelsPath", help="path to input file (.csv)")
parser.add_argument("cfsurl", help="path to output file (.csv, .sqlite) or Channel Finder Service URL")

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

    if not os.path.isfile(args.channelsPath):
        print("Error channel CSV file not found:", args.channelsPath, file=sys.stderr)
        return 1

    try:
        channels = read_csv(args.channelsPath)
    except Exception as e:
        print("Error reading channels from CSV file:", e, file=sys.stderr)
        return 1


    cfsurl = urlparse(args.cfsurl, "file")
    if cfsurl.scheme == "file":
        (_, ext) = os.path.splitext(cfsurl.path)
        if ext in [ ".sqlite", ".json" ]:
            if os.path.exists(cfsurl.path):
                print("Destination file already exists: {}".format(args.cfsurl), file=sys.stderr)
                return 1
        else:
            print("Destination file format not supported: {}".format(args.cfsurl), file=sys.stderr)
            return 1

    elif cfsurl.scheme in [ "http", "https" ]:
        # TODO: check if server is available?
        pass

    else:
        print("Destination URL not supported: {}".format(args.cfsurl), file=sys.stderr)
        return 1


    if cfsurl.scheme == "file":
        if ext == ".sqlite":
            try:
                _export_to_sqlite(channels, cfsurl.path)
            except Exception as e:
                print("Error exporting to CSV:", e, file=sys.stderr)
                return 1

        if ext == ".json":
            try:
                _export_to_json(channels, cfsurl.path)
            except Exception as e:
                print("Error exporting to JSON:", e, file=sys.stderr)
                return 1

    elif cfsurl.scheme in [ "http", "https" ]:
        try:
            if args.username == None:
                args.username = raw_input("Enter username: ")

            if args.password == None:
                args.password = getpass.getpass("Enter password: ")

            # Channel Finder Client does not
            # like trailing slashes in the URL.
            if args.cfsurl.endswith("/"):
                uri = args.cfsurl[:-1]
            else:
                uri = args.cfsurl

            _export_to_cfweb(channels, uri, args.username, args.password)
        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Error exporting to ChannelFinder:", e, file=sys.stderr)
            return 1

    return 0


def _export_to_sqlite(channels, path):
    importCfLocalData(channels, path, overwrite=True)


def _export_to_json(channels, path):
    chandict = OrderedDict()
    with open(path, "w") as fp:
        for name, props, tags in channels:
            data = OrderedDict(props)
            data["tags"] = ";".join(tags)
            chandict[name] = data

        json.dump(chandict, fp, indent=4)


def _export_to_cfweb(channels, uri, username, password):
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

