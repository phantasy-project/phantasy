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

from ..phylib.settings import Settings

from ..phylib.lattice.impact import OUTPUT_MODE_END
from ..phylib.lattice.impact import build_lattice as impact_build_lattice

from ..phylib.model.impact import run_lattice as impact_run_lattice

from ..machine.frib.layout import fribxlf


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

print_help = parser.print_help


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
                settings = Settings()
                settings.readfp(fp)
        except Exception as e:
            print("Error reading settings file:", e, file=sys.stderr)
            return 1


    try:
        lattice = impact_build_lattice(accel, settings=settings, start=args.start, end=args.end)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building lattice:", e, file=sys.stderr)
        return 1

    lattice.outputMode = OUTPUT_MODE_END

    try:
        result = impact_run_lattice(lattice, data_dir=args.datapath, work_dir=args.workpath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building result:", e, file=sys.stderr)
        return 1

    spos = result.getSPosition()

    energy = result.getEnergy()

    xorbit = result.getOrbit("X")
    yorbit = result.getOrbit("Y")

    xrms = result.getBeamRms("X")
    yrms = result.getBeamRms("Y")
    #zrms = result.getBeamRms("Z")

    xalpha = result.getTwissAlpha("X")
    yalpha = result.getTwissAlpha("Y")

    xemit = result.getEmittance("X")
    yemit = result.getEmittance("Y")
    zemit = result.getEmittance("Z")

    if args.plot:
        try:
            plt.figure(figsize=(16,10), dpi=80)
            plt.subplot(221)
            plt.title("Beam Orbit")
            plt.plot(spos, xorbit, 'r-', label="X")
            plt.plot(spos, yorbit, 'b-', label="Y")
            plt.xlabel("S [m]")
            plt.ylabel("Beam Position [m]")
            plt.legend(loc="upper left")
            plt.grid()

            plt.subplot(222)
            plt.title("Beam RMS")
            plt.plot(spos, xrms, 'r-', label="X")
            plt.plot(spos, yrms, 'b-', label="Y")
            #plt.plot(zrms[:,0], zrms[:,1], 'g-', label="Z")
            plt.xlabel("S [m]")
            plt.ylabel("Beam RMS [m]")
            plt.legend(loc="upper left")
            plt.grid()

            plt.subplot(223)
            plt.title("Beam Energy")
            plt.plot(spos, energy, 'r-')
            plt.xlabel("S [m]")
            plt.ylabel("Beam Energy [MeV]")
            plt.grid()

            plt.subplot(224)
            plt.title("Beam Emittance")
            plt.plot(spos, xemit, 'r-', label="X")
            plt.plot(spos, yemit, 'b-', label="Y")
            #plt.plot(zemit[:,0], zemit[:,1], 'g-', label="Z")
            plt.xlabel("S [m]")
            plt.ylabel("Beam Emittance [m-rad]")
            plt.legend(loc="upper left")
            plt.grid()

            if args.resultpath == None:
                plt.show()
            else:
                plt.savefig(args.resultpath)

        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Error generating plot: ", e, file=sys.stderr)

    else:
        try:
            if args.resultpath == None:
                csvfile = sys.stdout
            else:
                csvfile = open(args.resultpath, "w")
            csvfile.write("#  i  name   s   energy   codx   cody  alphax alphay emittancex emittancey emittancez TM\r\n")
            csvfile.write("#           [m]   [eV]     [m]    [m]                                                    \r\n")

            for idx in xrange(len(lattice.elements)):
                csvfile.write(str(idx))
                csvfile.write("  ")
                csvfile.write(lattice.elements[idx].name)
                csvfile.write("  ")
                csvfile.write(str(spos[idx]))
                csvfile.write("  ")
                csvfile.write(str(energy[idx]))
                csvfile.write("  ")
                csvfile.write(str(xorbit[idx]))
                csvfile.write("  ")
                csvfile.write(str(yorbit[idx]))
                csvfile.write("  ")
                csvfile.write(str(xalpha[idx]))
                csvfile.write("  ")
                csvfile.write(str(yalpha[idx]))
                csvfile.write("  ")
                csvfile.write(str(xemit[idx]))
                csvfile.write("  ")
                csvfile.write(str(yemit[idx]))
                csvfile.write("  ")
                csvfile.write(str(zemit[idx]))
                csvfile.write("  ")
                csvfile.write("0.0")
                csvfile.write("\r\n")

        except Exception as e:
            print("Error writing CSV result: ", e, file=sys.stderr)

        finally:
            if csvfile != sys.stdout: csvfile.close()


    return 0
