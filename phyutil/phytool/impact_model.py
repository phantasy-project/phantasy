# encoding: UTF-8

"""
Implement phylib command 'impact-model'.
"""

from __future__ import print_function

import os, sys, logging, traceback

from argparse import ArgumentParser

import matplotlib.pyplot as plt

from .. import phylib
phylib.AUTO_CONFIG=False

from ..phylib import cfg

from ..machine.frib.layout import fribxlf

from ..machine.frib.lattice import impact as impact_lattice

from ..machine.frib.model import impact as impact_model


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" impact-model",
                        description="Run IMPACT model and produce results")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--cfg", dest="cfgpath", help="path to alternate configuration file (.cfg)")
parser.add_argument("--xlf", dest="xlfpath", help="path to FRIB Expanded Lattice File (.xlsx)")
parser.add_argument("--stg", dest="stgpath", help="path to device settings file (.json)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--mach", help="name of machine (used to indicate VA)")
parser.add_argument("--data", dest="datapath", help="path to directory with IMPACT data")
parser.add_argument("--work", dest="workpath", help="path to directory for executing IMPACT")
parser.add_argument("--plot", action="store_true", help="generate a plot of the model")
parser.add_argument("resultpath", nargs='?', help="path to write resulting model data")

help = parser.print_help


def main():
    """
    Entry point for command 'impact-model'.
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


    if (args.resultpath != None) and os.path.exists(args.resultpath):
        print("Error: destination result path already exists:", args.resultpath, file=sys.stderr)
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
            print("Error reading settings file:", e, file=sys.stderr)
            return 1


    try:
        lattice = impact_lattice.build_lattice(accel, settings=settings, start=args.start, end=args.end)
    except Exception as e:
        print("Error building lattice:", e, file=sys.stderr)
        return 1

    try:
        result = impact_model.build_result(lattice, data_dir=args.datapath, work_dir=args.workpath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building result:", e, file=sys.stderr)
        return 1

    energy = result.get_energy()

    xorbit = result.get_orbit("X")
    yorbit = result.get_orbit("Y")

    xrms = result.get_beam_rms("X")
    yrms = result.get_beam_rms("Y")
    zrms = result.get_beam_rms("Z")

    xemit = result.get_beam_emittance("X")
    yemit = result.get_beam_emittance("Y")
    zemit = result.get_beam_emittance("Z")

    if args.plot:
        try:
            plt.subplot(221)
            plt.title("Beam Orbit")
            plt.plot(xorbit[:,0], xorbit[:,1], 'r-', label="X")
            plt.plot(yorbit[:,0], yorbit[:,1], 'b-', label="Y")
            plt.xlabel("S [m]")
            plt.ylabel("Beam Position [m]")
            plt.legend()
            plt.grid()

            plt.subplot(222)
            plt.title("Beam RMS")
            plt.plot(xrms[:,0], xrms[:,1], 'r-', label="X")
            plt.plot(yrms[:,0], yrms[:,1], 'b-', label="Y")
            #plt.plot(zrms[:,0], zrms[:,1], 'g-', label="Z")
            plt.xlabel("S [m]")
            plt.ylabel("Beam RMS [m]")
            plt.legend()
            plt.grid()

            plt.subplot(223)
            plt.title("Beam Energy")
            plt.plot(energy[:,0], energy[:,1], 'r-')
            plt.xlabel("S [m]")
            plt.ylabel("Beam Energy [MeV]")
            plt.grid()

            plt.subplot(224)
            plt.title("Beam Emittance")
            plt.plot(xemit[:,0], xemit[:,1], 'r-', label="X")
            plt.plot(yemit[:,0], yemit[:,1], 'b-', label="Y")
            #plt.plot(zemit[:,0], zemit[:,1], 'g-', label="Z")
            plt.xlabel("S [m]")
            plt.ylabel("Beam Emittance [m-rad]")
            plt.legend()
            plt.grid()

            if args.resultpath == None:
                plt.show()
            else:
                plt.savefig(args.resultpath)

        except Exception as e:
            print("Error generating plot: ", e, file=sys.stderr)

    else:
        try:
            if args.resultpath == None:
                csvfile = sys.stdout
            else:
                csvfile = open(args.resultpath, "w")
            csvfile.write("S,X,Y,XRMS,YRMS,ZRMS,Energy,XEmit,YEmit,ZEmit\r\n")
            for idx in xrange(xorbit.shape[0]):
                csvfile.write("{},{},{},{},{},{},{},{},{},{}\r\n".format(xorbit[idx,0], xorbit[idx,1], yorbit[idx,1],
                                                             xrms[idx,1], yrms[idx,1], zrms[idx,1], energy[idx,1],
                                                             xemit[idx,1], yemit[idx,1], zemit[idx,1]))
        except Exception as e:
            print("Error writing CSV result: ", e, file=sys.stderr)

        finally:
            if csvfile != sys.stdout: csvfile.close()


    return 0
