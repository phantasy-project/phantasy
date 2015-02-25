# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import sys, os, os.path, tempfile, subprocess, shutil, time

import numpy as np


def build_result(lattice, config=None):

    result_factory = ResultFactory(config, lattice)

    return result_factory.build()


class ResultFactory(object):


    def __init__(self, config, lattice):
        self._config = config
        self._lattice = lattice

        self.directory = None


    def _get_config_data_dir(self):
        return self._config.get_default("impact_data_dir")

    def build(self):

        start_time = time.time()

        wkdir = tempfile.mkdtemp("impact")
        #print(wkdir)

        testpath = os.path.join(wkdir, "test.in")

        with open(os.path.join(wkdir, "test.in"), "w") as fp:
            self._lattice.write(fp)


        datadir = self._get_config_data_dir()

        for datafile in os.listdir(datadir):
            if os.path.isfile(os.path.join(datadir, datafile)):
                #print("SymLink {} to {}".format(os.path.join(datadir, datafile), os.path.join(wkdir, datafile)))
                os.symlink(os.path.join(datadir, datafile), os.path.join(wkdir, datafile))

        #print("Preparation time: {}".format(time.time() - start_time), file=sys.stderr)

        with open(os.path.join(wkdir,"impact.log"), "w") as fp:
            rtn = subprocess.call(["mpirun", "-np", str(self._lattice.nprocessors), "impact"], cwd=wkdir, stdout=fp, stderr=subprocess.STDOUT)

        if rtn != 0:
            raise RuntimeError("ResultFactory: IMPACT exited with error: {}".format(rtn))

        fort18path = os.path.join(wkdir, "fort.18")
        if not os.path.isfile(fort18path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort18path))

        fort24path = os.path.join(wkdir, "fort.24")
        if not os.path.isfile(fort24path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort24path))

        fort25path = os.path.join(wkdir, "fort.25")
        if not os.path.isfile(fort25path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort25path))

        fort18 = np.loadtxt(fort18path, usecols=(0, 1))
        fort24 = np.loadtxt(fort24path, usecols=(1, 2))
        fort25 = np.loadtxt(fort25path, usecols=(1, 2))

        shutil.rmtree(wkdir)

        return Result(fort18, fort24, fort25)




class Result(object):

    def __init__(self, fort18, fort24, fort25):
        self._fort18 = fort18
        self._fort24 = fort24
        self._fort25 = fort25


    def get_orbit(self, plane="X"):
        if plane.upper() in [ "X", "H" ]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 0]
        elif plane.upper() in [ "Y", "V" ]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 0]
        elif plane.upper() in [ "XY", "HV" ]:
            data = np.empty((self._fort24.shape[0], 3))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 0]
            data[:, 2] = self._fort25[:, 0]
        else:
            raise RuntimeError("Result: Unknown plane to get beam orbit: {}".format(plane))

        return data
