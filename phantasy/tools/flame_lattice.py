# encoding: UTF-8

"""
Implement phytool command 'flame-lattice'.
"""
import os
import sys
import logging
import traceback
from argparse import ArgumentParser

from phantasy.library.lattice import build_flame_lattice
from .common import loadLayout
from .common import loadSettings
from .common import loadLatticeConfig
from .common import loadMachineConfig


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" flame-lattice",
                        description="Generate FLAME lattice file.")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--mach", dest="machine", help="name of machine or path of machine directory")
parser.add_argument("--subm", dest="submach", help="name of segment")
parser.add_argument("--layout", dest="layoutpath", help="path of accelerator layout file (.csv)")
parser.add_argument("--settings", dest="settingspath", help="path to accelerator settings file (.json)")
parser.add_argument("--config", dest="configpath", help="path to accelerator configuration file (.ini)")
#parser.add_argument("--cfsurl", help="url of channel finder service or local sqlite file")
#parser.add_argument("--cfstag", help="tag to query for channels")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
#parser.add_argument("--chanmap", help="path of file to write channel map")
#parser.add_argument("--latdata", help="path of file to write lattice data")
parser.add_argument("--template", action="store_true", help="ignore settings and generate template")
#parser.add_argument("--with-elem-data", action="store_true", help="lattice with element data as comments")
parser.add_argument("latticepath", nargs="?", help="path to output FLAME lattice file")


def main():
    """
    Entry point for command 'flame-lattice'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    if args.latticepath and os.path.exists(args.latticepath):
        print("Destination file already exists: {}".format(args.latticepath), file=sys.stderr)
        return 1

    # if (args.chanmap != None) and os.path.exists(args.chanmap):
    #     print("Destination file already exists: {}".format(args.chanmap), file=sys.stderr)
    #     return 1
    # 
    # if (args.latdata != None) and os.path.exists(args.latdata):
    #     print("Destination file already exists: {}".format(args.latdata), file=sys.stderr)
    #     return 1

    try:
        mconfig, submach = loadMachineConfig(args.machine, args.submach)
        #print(mconfig, submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading machine configuration:", e, file=sys.stderr)
        return 1


    try:
        layout = loadLayout(args.layoutpath, mconfig, submach)
        #print(layout)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading layout:", e, file=sys.stderr)
        return 1


    try:
        settings = loadSettings(args.settingspath, mconfig, submach)
        #print(settings)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading settings:", e, file=sys.stderr)
        return 1


    try:
        config = loadLatticeConfig(args.configpath, mconfig, submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading lattice configuration:", e, file=sys.stderr)
        return 1


    try:    
        lat = build_flame_lattice(layout, config=config, settings=settings,
                    start=args.start, end=args.end, template=args.template)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building lattice:", e, file=sys.stderr)
        return 1


    # if args.chanmap != None:
    #     try:
    #         channels = loadChannels(args.cfsurl, args.cfstag, mconfig, submach)
    #     except Exception as e:
    #         if args.verbosity > 0: traceback.print_exc()
    #         print("Error loading channels:", e, file=sys.stderr)
    #         return 1
    # 
    #     with open(args.chanmap, "w") as fp:
    #         _write_channel_map(layout, lat, channels, fp)
    # 
    # if args.latdata != None:
    #     with open(args.latdata, "w") as fp:
    #         _write_lattice_data(lat, fp)

    if args.latticepath != None:
        name, _ = os.path.splitext(args.latticepath)
        #maps = name + ".map"
        with open(args.latticepath, "w") as fp: #, open(maps, "w") as fmp:
            lat.write(fp)  #, fmp, withElemData=args.with_elem_data)
    else:
        lat.write(sys.stdout)  #, withElemData=args.with_elem_data)
    
    return 0
