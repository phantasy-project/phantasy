# encoding: UTF-8

"""
Implement phytool command 'impact-lattice'.
"""
import sys
import os.path
import logging
import traceback
from collections import OrderedDict
from argparse import ArgumentParser

from phantasy.library.lattice import build_impact_lattice

from .common import loadMachineConfig
from .common import loadLatticeConfig
from .common import loadLayout
from .common import loadSettings
from .common import loadChannels


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" impact-lattice",
                        description="Generate IMPACT lattice file (test.in).")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--mach", dest="machine", help="name of machine or path of machine directory")
parser.add_argument("--subm", dest="submach", help="name of segment")
parser.add_argument("--layout", dest="layoutpath", help="path of accelerator layout file (.csv)")
parser.add_argument("--settings", dest="settingspath", help="path to accelerator settings file (.json)")
parser.add_argument("--config", dest="configpath", help="path to accelerator configuration file (.ini)")
parser.add_argument("--cfsurl", help="url of channel finder service or local sqlite file")
parser.add_argument("--cfstag", help="tag to query for channels")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--chanmap", help="path of file to write channel map")
parser.add_argument("--latdata", help="path of file to write lattice data")
parser.add_argument("--template", action="store_true", help="ignore settings and generate template")
parser.add_argument("--with-elem-data", action="store_true", help="lattice with element data as comments")
parser.add_argument("latticepath", nargs="?", help="path to output IMPACT lattice file (test.in)")

print_help = parser.print_help


def main():
    """
    Entry point for command 'impact-lattice'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    if (args.latticepath != None) and os.path.exists(args.latticepath):
        print("Destination file already exists: {}".format(args.latticepath), file=sys.stderr)
        return 1

    if (args.chanmap != None) and os.path.exists(args.chanmap):
        print("Destination file already exists: {}".format(args.chanmap), file=sys.stderr)
        return 1

    if (args.latdata != None) and os.path.exists(args.latdata):
        print("Destination file already exists: {}".format(args.latdata), file=sys.stderr)
        return 1


    try:
        mconfig, submach = loadMachineConfig(args.machine, args.submach)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error loading machine configuration:", e, file=sys.stderr)
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
        print("Error loading lattice configuration:", e, file=sys.stderr)
        return 1


    try:
        lat = build_impact_lattice(layout, config=config, settings=settings,
                                   start=args.start, end=args.end, template=args.template)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building lattice:", e, file=sys.stderr)
        return 1


    if args.chanmap != None:
        try:
            channels = loadChannels(args.cfsurl, args.cfstag, mconfig, submach)
        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Error loading channels:", e, file=sys.stderr)
            return 1

        with open(args.chanmap, "w") as fp:
            _write_channel_map(layout, lat, channels, fp)

    if args.latdata != None:
        with open(args.latdata, "w") as fp:
            _write_lattice_data(lat, fp)

    if args.latticepath != None:
        name, _ = os.path.splitext(args.latticepath)
        maps = name + ".map"
        with open(args.latticepath, "w") as fp, open(maps, "w") as fmp:
            lat.write(fp, fmp, withElemData=args.with_elem_data)
    else:
        lat.write(sys.stdout, withElemData=args.with_elem_data)

    return 0


def _write_channel_map(accel, lat, channels, stream):
    """Write the channel to IMPACT output map to file in CSV format:

       PV,elemIndex,elemPosition,elemLength,machine,elemName,elemHandle,elemField,elemType
       V_1:LS1_CA01:CAV1_D1127:PHA_CSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,setpoint,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:PHA_RSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,readset,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:PHA_RD,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,readback,PHA,CAV
       V_1:LS1_CA01:CAV1_D1127:AMPL_CSET,3,0.4470635,0.24,V_1,LS1_CA01:CAV1_D1127,setpoint,AMP,CAV
       [...]
    """


    props = [ "machine", "elemName", "elemHandle", "elemField", "elemType" ]

    stream.write("PV,elemIndex,elemPosition,elemLength")
    for p in props:
        stream.write(","+p)
    stream.write("\r\n")

    for idx in range(len(lat.elements)):
        elem = lat.elements[idx]
        for chan, data, _ in channels:
            if elem.name == data['elemName']:
                stream.write(chan+","+str(idx+1)+","+str(elem.position)+","+str(elem.length))
                for p in props:
                    stream.write(","+data[p])
                stream.write("\r\n")


def _write_lattice_data(lat, stream):
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
    fields = OrderedDict()
    for elem in lat.elements:
        for field in elem.fields:
            fields[field.name] = field.unit

    stream.write("ElementName  ElementType  L  s")
    for fname in fields.keys():
        stream.write(" ")
        stream.write(fname)
    stream.write("\r\n")

    stream.write("                          m  m")
    for funit in fields.values():
        stream.write(" ")
        stream.write(funit)
    stream.write("\r\n")

    stream.write("---------------------------------------------\r\n")
    for elem in lat.elements:
        stream.write(str(elem.name))
        stream.write("  ")
        stream.write(str(elem.etype))
        stream.write("  ")
        stream.write(str(float(elem.length)))
        stream.write("  ")
        stream.write(str(float(elem.position)))
        for fname in fields.keys():
            stream.write("  ")
            try:
                stream.write(str(elem.getfield(fname)))
            except:
                stream.write("NONE")
        stream.write("\r\n")

