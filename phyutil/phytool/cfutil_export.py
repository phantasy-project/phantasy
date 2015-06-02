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

from ..phylib import cfg

from ..machine.frib.layout import fribxlf


_LOGGER = logging.getLogger(__name__)


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" cfutil-export",
                        description="Export channel data to file or Channel Finder Service")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--stg", dest="stgpath", help="path to device settings file (.json)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--mach", help="name of machine (used to indicate VA)")
parser.add_argument("--user", dest="username", help="specify ChannelFinder username")
parser.add_argument("--pass", dest="password", help="specify ChannelFinder password")
parser.add_argument("cfurl", help="path to file (.csv, .json) or Channel Finder Service URL")

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


    if args.cfgpath != None:
        try:
            cfg.load(args.cfgpath)
        except:
            print("Error: configuration file not found: {}".format(args.cfgpath), file=sys.stderr)
            return 1

    elif not cfg.load(cfg.DEFAULT_LOCATIONS):
        print("Warning: no default configuration found: {}".format(cfg.DEFAULT_LOCATIONS), file=sys.stderr)


    cfurl = urlparse(args.cfurl, "file")
    if cfurl.scheme == "file":
        (_, ext) = os.path.splitext(cfurl.path)
        if ext in [ ".csv", ".json" ]:
            if os.path.exists(cfurl.path):
                print("Destination file already exists: {}".format(args.cfurl), file=sys.stderr)
                return 1
        else:
            print("Destination file format not supported: {}".format(args.cfurl), file=sys.stderr)
            return 1

    elif cfurl.scheme in [ "http", "https" ]:
        # TODO: check if server is available?
        pass

    else:
        print("Destination URL not supported: {}".format(args.cfurl), file=sys.stderr)
        return 1


    try:
        accel = fribxlf.build_accel(xlfpath=args.xlfpath, machine=args.mach)
    except Exception as e:
        print("Error building accelerator:", e, file=sys.stderr)
        return 1


    if cfurl.scheme == "file":
        if ext == ".csv":
            try:
                _export_to_csv(accel, cfurl.path, args.start, args.end)
            except Exception as e:
                print("Error exporting to CSV:", e, file=sys.stderr)
                return 1

        if ext == ".json":
            try:
                _export_to_json(accel, cfurl.path, args.start, args.end)
            except Exception as e:
                print("Error exporting to JSON:", e, file=sys.stderr)
                return 1

    elif cfurl.scheme in [ "http", "https" ]:
        try:
            if args.username == None:
                args.username = raw_input("Enter username: ")

            if args.password == None:
                args.password = getpass.getpass("Enter password: ")

            _export_to_cfweb(accel, args.cfurl, args.username, args.password, args.start, args.end)
        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Error exporting to ChannelFinder:", e, file=sys.stderr)
            return 1

    return 0


def _export_to_csv(accel, path, start, end):
    properties = None
    with open(path, "w") as fp:
        for elem in accel.iter(start, end):
            for chan, data in elem.chanstore.iteritems():
                if properties == None:
                    # write the header
                    properties = data.keys()
                    fp.write("channel")
                    for p in properties:
                        fp.write(",")
                        fp.write(str(p))
                    fp.write("\r\n")
                # write the data
                fp.write(str(chan))
                for p in properties:
                    fp.write(",")
                    fp.write(str(data[p]))
                fp.write("\r\n")


def _export_to_json(accel, path, start, end):
    channels = OrderedDict()
    with open(path, "w") as fp:
        for elem in accel.iter(start, end):
            for chan, data in elem.chanstore.iteritems():
                channels[chan] = data

        json.dump(channels, fp, indent=4)


def _export_to_cfweb(accel, uri, username, password, start, end):
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
    for elem in accel.iter(start, end):
        for chan, data in elem.chanstore.iteritems():
            for prop, value in data.iteritems():
                if prop not in properties:
                    properties[prop] = {}

                v = str(value)
                if v not in properties[prop]:
                    properties[prop][v] = set()

                properties[prop][v].add(chan)
                channelnames.add(chan)

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

