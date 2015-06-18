# encoding: UTF-8

"""
Implement phylib command 'cfutil-export'.
"""

from __future__ import print_function

import sys, os.path, logging, json, traceback, getpass
from urlparse import urlparse
from argparse import ArgumentParser
from collections import OrderedDict

from channelfinder import ChannelFinderClient
from channelfinder.CFDataTypes import Property, Channel

from ..phylib.common.csv_utils import read_csv

from ..phylib.chanfinder import importCfLocalData

_LOGGER = logging.getLogger(__name__)


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" cfutil-export",
                        description="Export channel data to file or Channel Finder Service")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--user", dest="username", help="specify ChannelFinder username")
parser.add_argument("--pass", dest="password", help="specify ChannelFinder password")
parser.add_argument("--cfstag", help="tag to query for channels")
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

            _export_to_cfweb(channels, args.cfsurl, args.username, args.password)
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
    # Improve performance by reducing the number
    # of HTTP server requests by restructuring
    # the channel data from channel oriented:
    #
    # {
    #    "CH:NAME1": {
    #         "system":"SEG1",
    #         "device":"DEV1"
    #    },
    #    "CH:NAME2: {
    #         "system":"SEG1",
    #         "device":"DEV2"
    #    }
    # }
    #
    # To property oriented:
    #
    # {
    #    "system" : {
    #        "SEG1": [ "CH:NAME1", "CH:NAME2" ]
    #    },
    #    "device" : {
    #        "DEV1" : [ "CH:NAME1" ],
    #        "DEV2" : [ "CH:NAME2" ]
    #    }
    # }
    #
    properties = {}
    channelnames = set()
    for name, props, _ in channels:
        for prop, value in props:
            if prop not in properties:
                properties[prop] = {}
            v = str(value)

            if v not in properties[prop]:
                properties[prop][v] = set()

            properties[prop][v].add(name)
            channelnames.add(name)

    client = ChannelFinderClient(BaseURL=uri, username=username, password=password)

    channels = []
    for cname in channelnames:
        c = Channel(cname, username)
        channels.append(c)
        _LOGGER.debug("Export to Channel Finder: Set channel: %s", _Chan(c))
    client.set(channels=channels)
    _LOGGER.info("Export to ChannelFinder: Set channels: %s", len(channels))

    for prop, values in properties.iteritems():
        p = Property(prop, username)
        client.set(property=p)
        _LOGGER.info("Export to ChannelFinder: Set property: %s", _Prop(p))
        for propvalue, channelnames in values.iteritems():
            p.Value = propvalue
            client.update(property=p, channelNames=channelnames)
            _LOGGER.debug("Export to ChannelFinder: Update property: %s, for channels: %s", _Prop(p), len(channelnames))


class _Prop(object):
    """Provides pretty printing for CF Property object."""
    def __init__(self, prop):
        self._prop = prop

    def __str__(self):
        return "{{ name:'{prop.Name}', value='{prop.Value}', owner='{prop.Owner}' }}".format(prop=self._prop)


class _Chan(object):
    """Provides pretty printing for CF Channel object."""
    def __init__(self, chan):
        self._chan = chan

    def __str__(self):
        return "{{ name='{chan.Name}', owner='{chan.Owner}' }}".format(chan=self._chan)

