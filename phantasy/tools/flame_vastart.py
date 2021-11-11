# encoding: UTF-8

"""
Implement phytool command 'flame-vastart'.
"""
import sys
import os
import logging
import traceback
from argparse import ArgumentParser

from .common import loadLayout
from .common import loadSettings
from .common import loadChannels
from .common import loadLatticeConfig
from .common import loadMachineConfig

from phantasy.facility.frib.virtaccel import build_flame_virtaccel

def set_ca_local():
    os.environ['EPICS_CAS_ADDR_LIST'] = '127.0.0.1'
    os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'
    os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'NO'

parser = ArgumentParser(prog=os.path.basename(sys.argv[0]) + " flame-vastart",
                        description="Start the virtual accelerator using FLAME simulation")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("-l", dest="localonly", nargs='?', type=int, const=1, default=0, help="run IOC localhost only")
parser.add_argument("--mach", dest="machine", help="name of machine or path of machine directory")
parser.add_argument("--subm", dest="submach", help="name of segment")
parser.add_argument("--layout", dest="layoutpath", help="path of accelerator layout file (.csv)")
parser.add_argument("--settings", dest="settingspath", help="path to accelerator settings file (.json)")
parser.add_argument("--config", dest="configpath", help="path to accelerator configuration file (.ini)")
parser.add_argument("--cfsurl", help="url of channel finder service or local sqlite file")
parser.add_argument("--cfstag", help="tag to query for channels")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--data", dest="datapath", help="path to directory with FLAME data")
parser.add_argument("--work", dest="workpath", help="path to directory for executing FLAME")
parser.add_argument("--pv-prefix", dest="pvprefix", help="string prefix to each PV name")
parser.add_argument("--pv-suffix", dest="pvsuffix", default='', help="string suffix only to noise/mps/status PVs")
parser.add_argument("--noise", dest="noise", type=float, default=0.001, help="noise level of device readback")
parser.add_argument("--rep-rate", dest="reprate", type=float, default=1.0, help="repetition rate of virtual accelerator")

print_help = parser.print_help


def main():
    """
    Entry point for command 'flame-vastart'.
    """
    args = parser.parse_args(sys.argv[2:])

    if len(sys.argv) == 2:
        print_help()

    if args.localonly == 1:
        set_ca_local()

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        mconfig, submach = loadMachineConfig(args.machine, args.submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error readings machine configuration:", e, file=sys.stderr)
        return 1

    try:
        layout = loadLayout(args.layoutpath, mconfig, submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading layout:", e, file=sys.stderr)
        return 1

    try:
        settings = loadSettings(args.settingspath, mconfig, submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading settings:", e, file=sys.stderr)
        return 1

    try:
        config = loadLatticeConfig(args.configpath, mconfig, submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading configuration:", e, file=sys.stderr)
        return 1

    channels = loadChannels(args.cfsurl, None, mconfig, submach)

    try:
        va = build_flame_virtaccel(layout, config=config, channels=channels, settings=settings,
                                   start=args.start, end=args.end, data_dir=args.datapath, work_dir=args.workpath,
                                   machine=args.pvprefix, pv_suffix=args.pvsuffix, noise=args.noise,
                                   rate=args.reprate)
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
