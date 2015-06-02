# encoding: UTF-8

"""
Implement phylib command 'impact-lattice'.
"""

from __future__ import print_function

import sys, os.path, logging, traceback

from collections import OrderedDict

from argparse import ArgumentParser

from .. import phylib
phylib.AUTO_CONFIG=False

from ..phylib import cfg

from ..phylib.settings import Settings

from ..phylib.lattice import impact

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
parser.add_argument("--latdata", help="path of file to write lattice data")
parser.add_argument("--template", action="store_true", help="ignore settings and generate template")
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

    if (args.latdata != None) and os.path.exists(args.latdata):
        print("Destination file already exists: {}".format(args.latdata), file=sys.stderr)
        return 1

    try:
        accel = fribxlf.build_accel(xlfpath=args.xlfpath, machine=args.mach)
    except Exception as e:
        print("Error building accelerator:", e, file=sys.stderr)
        return 1


    if (args.stgpath == None) or (args.template == True):
        settings = None
    else:
        try:
            with open(args.stgpath, "r") as fp:
                settings = Settings()
                settings.readfp(fp)
        except Exception as e:
            print("Error reading settings:", e, file=sys.stderr)
            return 1


    try:
        lat = impact.build_lattice(accel, settings=settings, start=args.start, end=args.end, template=args.template)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building lattice:", e, file=sys.stderr)
        return 1


    if args.chanmap != None:
        with open(args.chanmap, "w") as fp:
            _write_channel_map(accel, lat, fp)

    if args.latdata != None:
        with open(args.latdata, "w") as fp:
            _write_lattice_data(lat, fp)

    if args.latpath != None:
        name, _ = os.path.splitext(args.latpath)
        maps = name + ".map"
        with open(args.latpath, "w") as fp, open(maps, "w") as fmp:
            lat.write(fp, fmp)
    else:
        lat.write(sys.stdout)

    return 0


def _write_channel_map(accel, lat, fio):
    """Write the channel to IMPACT output map to file in CSV format:

       PV,elemIndex,elemPosition,elemLength,machine,elemName,elemHandle,elemField,elemType
       V_1:LS1_CA01:CAV1_D1127:PHA_CSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,setpoint,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:PHA_RSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,readset,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:PHA_RD,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,readback,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:AMPL_CSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,setpoint,AMP,CAV
       [...]
    """

    chanstore = OrderedDict()
    for elem in accel:
        chanstore.update(elem.chanstore)


    props = [ "machine", "elemName", "elemHandle", "elemField", "elemType" ]

    fio.write("PV,elemIndex,elemPosition,elemLength")
    for p in props:
        fio.write(","+p)
    fio.write("\r\n")

    for idx in xrange(len(lat.elements)):
        elem = lat.elements[idx]
        for chan, data in chanstore.iteritems():
            if elem.name == data['elemName']:
                fio.write(chan+","+str(idx+1)+","+str(elem.position)+","+str(elem.length))
                for p in props:
                    fio.write(","+data[p])
                fio.write("\r\n")


def _write_lattice_data(lat, fio):
    """Write the element data to space delimited format for use with Lattice Service.

    ElementName  ElementType  L  s  AMP PHA B GRAD ANG
                              m  m   V  deg T T/m  rad
    ---------------------------------------------
    DRIFT  VALVE  0.072  0.072  0.0  0.0  0.0  0.0  0.0
    DRIFT  DRIFT  0.1350635  0.19094025  0.0  0.0  0.0  0.0  0.0
    LS1_CA01:CAV1_D1127  CAV  0.24  0.4470635  0.64  -6.524  0.0  0.0  0.0
    DRIFT  DRIFT  0.06426334  0.52745009  0.0  0.0  0.0  0.0  0.0
    LS1_CA01:BPM_D1129  BPM  0.0  0.51132684  0.0  0.0  0.0  0.0  0.0
    [...]
    """
    fio.write("ElementName  ElementType  L  s")
    for prop in lat.properties:
        fio.write(" ")
        fio.write(prop.name)
    fio.write("\r\n")

    fio.write("                          m  m")
    for prop in lat.properties:
        fio.write(" ")
        fio.write(prop.units)
    fio.write("\r\n")

    fio.write("---------------------------------------------\r\n")

    for elem in lat.elements:
        fio.write(elem.name)
        fio.write("  ")
        fio.write(str(elem.etype))
        fio.write("  ")
        fio.write(str(elem.length))
        fio.write("  ")
        fio.write(str(elem.position))
        for prop in lat.properties:
            fio.write("  ")
            if prop.name in elem.properties:
                fio.write(str(elem.properties[prop.name]))
            else:
                fio.write("NONE")
        fio.write("\r\n")

