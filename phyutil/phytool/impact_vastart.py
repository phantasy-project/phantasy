# encoding: UTF-8

"""
Implement phylib command 'impact-vastart'.
"""

from __future__ import print_function

import sys, os.path, re, logging, traceback

from argparse import ArgumentParser

from ..phylib import cfg

from ..phylib.settings import Settings

from ..phylib.layout.layout import build_layout

from ..phylib.chanfinder.chanfinderAgent import ChannelFinderAgent

from ..machine import findMachineConfig

from ..machine.frib.virtaccel.impact import build_virtaccel


_CONFIG_COMMON_SECTION = "COMMON"

_CONFIG_DEFAULT_SUBMACHINE = "default_submachine"

_CONFIG_CONFIG_FILE = "config_file"

_CONFIG_SETTINGS_FILE = "settings_file"

_CONFIG_LAYOUT_FILE = "layout_file"

_CONFIG_CFS_URL = "cfs_url"

_CONFIG_CFS_TAG = "cfs_tag"

_LOGGER = logging.getLogger(__name__)



parser = ArgumentParser(description="Start the virtual accelerator using IMPACT simulation")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--config", dest="configpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--layout", dest="layoutpath", help="")
parser.add_argument("--settings", dest="settingspath", help="path to device settings file (.json)")
parser.add_argument("--cfsurl", help="url of channel finder service or local sqlite file")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--subm", help="name of submachine to load otherwise use configuration")
parser.add_argument("--data", dest="datapath", help="path to directory with IMPACT data")
parser.add_argument("--work", dest="workpath", help="path to directory for executing IMPACT")
parser.add_argument("machine")


print_help = parser.print_help


def main():
    """
    Entry point for command 'impact-vastart'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    try:
        mconfig, _, _ = findMachineConfig(args.machine)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error readings machine configuration:", e, file=sys.stderr)
        return 1


    if args.subm is None:
        if mconfig.has_option(_CONFIG_COMMON_SECTION, _CONFIG_DEFAULT_SUBMACHINE):
            subm = mconfig.get(_CONFIG_COMMON_SECTION, _CONFIG_DEFAULT_SUBMACHINE)
        else:
            print("Error: default submachine not specified", file=sys.stderr)
            return 1
    else:
        subm = args.subm.strip()


    if args.settingspath is None:
        if mconfig.has_option(subm, _CONFIG_SETTINGS_FILE):
            settingsPath = mconfig.getabspath(subm, _CONFIG_SETTINGS_FILE)
        else:
            print("Error: settings file not specified", file=sys.stderr)
            return 1
    else:
        settingsPath = args.settingspath

    try:
        settings = Settings(settingsPath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error readings settings file:", e, file=sys.stderr)
        return 1


    if args.configpath is None:
        if mconfig.has_option(subm, _CONFIG_CONFIG_FILE):
            configPath = mconfig.getabspath(subm, _CONFIG_CONFIG_FILE)
        else:
            print("Error: config file not specified", file=sys.stderr)
            return 1
    else:
        configPath = args.configpath

    try:
        config = cfg.Configuration(configPath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error readings config file:", e, file=sys.stderr)
        return 1


    if args.layoutpath is None:
        if mconfig.has_option(subm, _CONFIG_LAYOUT_FILE):
            layoutPath = mconfig.getabspath(subm, _CONFIG_LAYOUT_FILE)
        else:
            print("Error: layout file not specified", file=sys.stderr)
            return 1
    else:
        layoutPath = args.layoutpath

    try:
        layout = build_layout(layoutPath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error readings layout file:", e, file=sys.stderr)
        return 1


    if args.cfsurl is None:
        if mconfig.has_option(subm, _CONFIG_CFS_URL):
            cfsUrl = mconfig.get(subm, _CONFIG_CFS_URL)
        else:
            print("Error: Channel Finder source not specified", file=sys.stderr)
            return 1
    else:
        cfsUrl = args.cfsurl

    cfa = ChannelFinderAgent()

    if re.match(r"https?://.*", cfsUrl, re.I):
        _LOGGER.info("impact_vastart: using service '%s' for '%s'" % (cfsUrl, subm))
        if mconfig.has_option(subm, _CONFIG_CFS_TAG):
            cfsTag = mconfig.get(subm, _CONFIG_CFS_TAG)
        else:
            cfsTag = "phyutil.sys.%s" % subm
        cfa.downloadCfs(source=cfsUrl, property=[('elemName', '*'),], tagName=cfsTag)
    else:
        cfsPath = mconfig.getabspath(subm, _CONFIG_CFS_URL)
        if os.path.isfile(cfsPath):
            _LOGGER.info("impact_vastart: using SQLite '%s'" % (cfsPath,))
            cfa.downloadCfs(source=cfsPath)
        else:
            print("Error loading channels from source:", cfsUrl, file=sys.stderr)
            return 1


    try:
        va = build_virtaccel(layout, config=config, channels=cfa.results, settings=settings,
                             start=args.start, end=args.end, data_dir=args.datapath, work_dir=args.workpath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building virtual accelerator:", e, file=sys.stderr)
        return 1


    try:
        va.start(True)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error starting virtual accelerator:", e, file=sys.stderr)
        return 1


    try:
        va.wait()
    except KeyboardInterrupt:
        va.stop()
        va.wait()
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error executing virtual accelerator:", e, file=sys.stderr)
        return 1


    return 0

