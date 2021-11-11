# encoding: UTF-8

"""
Implement phytool command 'impact-model'.
"""
import os
import sys
import logging
import traceback
import shutil

from argparse import ArgumentParser

import matplotlib.pyplot as plt

from phantasy.library.lattice.impact import OUTPUT_MODE_END
from phantasy.library.lattice.impact import build_lattice
from phantasy.library.lattice.impact import run_lattice
from phantasy.library.model.impact import build_result

from .common import loadMachineConfig
from .common import loadLatticeConfig
from .common import loadLayout
from .common import loadSettings


parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" impact-model",
                        description="Run IMPACT model and produce results")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
parser.add_argument("--mach", dest="machine", help="name of machine or path of machine directory")
parser.add_argument("--subm", dest="submach", help="name of segment")
parser.add_argument("--layout", dest="layoutpath", help="path of accelerator layout file (.csv)")
parser.add_argument("--settings", dest="settingspath", help="path to accelerator settings file (.json)")
parser.add_argument("--config", dest="configpath", help="path to accelerator configuration file (.ini)")
parser.add_argument("--start", help="name of accelerator element to start processing")
parser.add_argument("--end", help="name of accelerator element to end processing")
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

    def rm_temp_dir(path):
        if args.workpath == None:
            shutil.rmtree(path)

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    if (args.resultpath != None) and os.path.exists(args.resultpath):
        print("Error: destination result path already exists:", args.resultpath, file=sys.stderr)
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
        print("Error loading configuration:", e, file=sys.stderr)
        return 1


    try:
        lattice = build_lattice(layout, config=config, settings=settings, start=args.start, end=args.end)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building lattice:", e, file=sys.stderr)
        return 1

    lattice.outputMode = OUTPUT_MODE_END

    try:
        result_dir = run_lattice(lattice, config=config, data_dir=args.datapath, work_dir=args.workpath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error running lattice:", e, file=sys.stderr)
        return 1

    try:
        result = build_result(impact="FRIB", directory=result_dir, keep=True)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building result:", e, file=sys.stderr)
        rm_temp_dir(result_dir)
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
            csvfile.write("#  i  name   s   energy   codx   cody  rmsx  rmsy  alphax alphay emittancex emittancey emittancez TM\r\n")
            csvfile.write("#           [m]   [eV]     [m]    [m]   [m]   [m]                                                   \r\n")

            for idx in range(len(lattice.elements)):
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
                csvfile.write(str(xrms[idx]))
                csvfile.write("  ")
                csvfile.write(str(yrms[idx]))
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

    rm_temp_dir(result_dir)

    return 0
