# encoding: UTF-8

"""
Implement phylib command 'impact-lattice'.
"""

from __future__ import print_function

import sys, os.path, logging, json

from argparse import ArgumentParser

from .. import phylib
phylib.AUTO_CONFIG=False

from ..phylib import cfg

from ..machine.frib.lattice import impact

from ..machine.frib.layout import fribxlf


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" impact-lattice",
                        description="Generate IMPACT lattice file (test.in).")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--stg", dest="stgpath", help="path to device settings file (.json)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--mach", help="name of machine (used to indicate VA)")
parser.add_argument("--chanmap", help="path of file to write channel map")
parser.add_argument("latpath", nargs="?", help="path to output IMPACT lattice file (test.in)")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-lattice'.
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


    if (args.latpath != None) and os.path.exists(args.latpath):
        print("Destination file already exists: {}".format(args.latpath), file=sys.stderr)
        return 1


    if (args.chanmap != None) and os.path.exists(args.chanmap):
        print("Destination file already exists: {}".format(args.chanmap), file=sys.stderr)
        return 1


    try:
        accel = fribxlf.build_accel(xlfpath=args.xlfpath, machine=args.mach)
    except Exception as e:
        print("Error building accelerator:", e, file=sys.stderr)
        return 1


    if args.stgpath == None:
        settings = None
    else:
        try:
            with open(args.stgpath, "r") as fp:
                settings = json.load(fp)
        except Exception as e:
            print(e, file=sys.stderr)
            return 1


    try:
        lat = impact.build_lattice(accel, settings=settings, start=args.start, end=args.end)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    if args.chanmap != None:
        with open(args.chanmap, "w") as fp:
            _write_channel_map(accel, lat, fp)


    if args.latpath != None:
        with open(args.latpath, "w") as fp:
            lat.write(file=fp)
    else:
        lat.write(file=sys.stdout)

    return 0


def _write_channel_map(accel, lat, file):
    """Write the channel to IMPACT output map to file in CSV format:

       PV,elemIndex,elemPosition,elemLength,machine,elemName,elemHandle,elemField,elemType
       V_1:LS1_CA01:CAV1_D1127:PHA_CSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,setpoint,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:PHA_RSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,readset,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:PHA_RD,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,readback,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:AMPL_CSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,setpoint,AMP,CAV
       [...]
    """
    props = [ "machine", "elemName", "elemHandle", "elemField", "elemType" ]

    file.write("PV,elemIndex,elemPosition,elemLength")
    for p in props:
        file.write(","+p)
    file.write("\r\n")

    for chanmap in lat.chanmap:
        for chan in chanmap[4]:
            data = accel.channels[chan]
            file.write(chan+","+str(chanmap[0]+1)+","+str(chanmap[2])+","+str(chanmap[3]))
            for p in props:
                if p == "elemName" and 'SOL' in data[p] and data['elemType'] in ['DCH', 'DCV']:
                    file.write(","+str(data[p].replace('SOL', data['elemType'])))
                else:
                    file.write(","+str(data[p]))
            file.write("\r\n")

