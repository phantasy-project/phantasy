# encoding: UTF-8

"""Library for IMPACT related lattice/model function."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import os.path, shutil

import numpy as np

from ..common import DataError

def build_result(directory=None):
    """Convenience method to build IMPACT model result.
    """
    result_factory = ResultFactory(directory)

    return result_factory.build()


class ResultFactory(object):
    """A factory to get simulation results from IMPACT working directory.

    """

    def __init__(self, directory=None):
        """Initialize class, give IMPACT working directory.

        :param directory: IMPACT working directory (default is current directory)
        """
        self.directory = directory


    def build(self, runimpact=False, **kwargs):
        """ Build result from impact simulation.
        It needs IMPACT fort file, fort.18, fort.24, fort.25, and fort.26

        :param runimpact: flag to identify whether to execute a new run, False by default.

        :param IMPACT:  IMPACT-Z version, either "FRIB" or "LBL". "FRIB" by default.
        :param fort18:  impact energy file name
        :param fort24:  impact horizontal file name
        :param fort25:  impact vertical file name
        :param fort26:  impact longitudinal file name
        :param keep:    keep simulation results, True by default.
        :return:
        """

        if self.directory != None:
            wkdir = self.directory
        else:
            wkdir = os.getcwd()

        _IMPACT = kwargs.get("IMPACT", "FRIB")
        _fort18 = kwargs.get("fort18", "fort.18")
        _fort24 = kwargs.get("fort24", "fort.24")
        _fort25 = kwargs.get("fort25", "fort.25")
        _fort26 = kwargs.get("fort26", "fort.26")
        _keep = kwargs.get("keep", True)

        if runimpact:
            raise NotImplementedError("ResultFactory: Execution of IMPACT not implemented. See phylib.machine.frib.model.impact.ResultFactory.")


        fort18path = os.path.join(wkdir, _fort18)
        if not os.path.isfile(fort18path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort18path))

        fort24path = os.path.join(wkdir, _fort24)
        if not os.path.isfile(fort24path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort24path))

        fort25path = os.path.join(wkdir, _fort25)
        if not os.path.isfile(fort25path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort25path))

        fort26path = os.path.join(wkdir, _fort26)
        if not os.path.isfile(fort25path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort25path))

        # read data in if all data files are in place
        if _IMPACT == "FRIB":
            # z, phase (rad), energy (MeV), gamma, beta
            fort18 = np.loadtxt(fort18path, usecols=(0, 1, 3, 2, 4))
            # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
            fort24 = np.loadtxt(fort24path, usecols=(1, 3, 2, 4, 7, 5, 6))
            # Y0, Y0', Yrms, Y'rms, Yp, Alpha y, Beta y
            fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 7, 5, 6))
            # Z0, Z0', Zrms, Z'rms, Zp, Alpha Z, Beta z
            fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 7, 5, 6))
        elif _IMPACT in ["LBL", "LBNL"]:
            # z, phase (rad), energy (MeV), gamma, beta
            fort18 = np.loadtxt(fort18path, usecols=(0, 1, 3, 2, 4))
            # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
            fort24 = np.loadtxt(fort24path, usecols=(1, 3, 2, 4, 6, 5))
            # Y0, Y0', Yrms, Y'rms, Yp, Alpha y, Beta y
            fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 6, 5))
            # Z0, Z0', Zrms, Z'rms, Zp, Alpha Z, Beta z
            fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 6, 5))

        else:
            raise RuntimeError("Unknown IMPACT version. Cannot parse results.")

        if not _keep:
            shutil.rmtree(wkdir)

        return Result(fort18, fort24, fort25, fort26)

class Result(object):

    def __init__(self, fort18, fort24, fort25, fort26):
        """

        :param fort18: numpy N x 5 array
        :param fort24: numpy N x 7 array, or N x 6 for LBL version (no TWISS beta)
        :param fort25: numpy N x 7 array, or N x 6 for LBL version (no TWISS beta)
        :param fort26: numpy N x 7 array, or N x 6 for LBL version (no TWISS beta)
        :return:
        """
        # z, phase (rad), energy (MeV), gamma, beta
        self._fort18 = fort18
        # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
        self._fort24 = fort24
        # Y0, Y0', Yrms, Y'rms, Yp, Alpha y, Beta y
        self._fort25 = fort25
        # Z0, Z0', Zrms, Z'rms, Zp, Alpha Z, Beta z
        self._fort26 = fort26

    def get_sposition(self):
        """

        :return: list of s position for each element
        """
        return self._fort18[:, 0]

    def get_orbit(self, plane="X"):
        """Get beam orbit

        :param plane:
        :return:
        """
        if plane.upper() in [ "X"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 0]
        elif plane.upper() in [ "Y"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 0]
        elif plane.upper() in [ "XY"]:
            data = np.empty((self._fort24.shape[0], 3))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 0]
            data[:, 2] = self._fort25[:, 0]
        else:
            raise RuntimeError("Result: Unknown plane to get beam orbit: {}".format(plane))

        return data

    def get_abs_phase(self):
        """Get accumulated beam phase in radian.

        :return:
        """
        return self._fort18[:, [0, 1]]

    def get_energy(self):
        """ Get beam energy in MeV.

        :return:
        """
        return self._fort18[:, [0, 2]]

    def get_twiss_alpha(self, plane="X"):
        """Get beam twiss alpha parameters.

        :return:
        """
        if plane.upper() in [ "X"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 5]
        elif plane.upper() in [ "Y"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 5]
        elif plane.upper() in [ "XY"]:
            data = np.empty((self._fort24.shape[0], 3))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 5]
            data[:, 2] = self._fort25[:, 5]
        elif plane.upper() in [ "Z"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 5]
        else:
            raise RuntimeError("Result: Unknown plane to get Twiss Alpha: {}".format(plane))

        return data



    def get_twiss_beta(self, plane="X"):
        """Get beam twiss beta parameters.

        :return:
        """
        if plane.upper() in [ "X"]:
            if self._fort18.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 6]
        elif plane.upper() in [ "Y"]:
            if self._fort18.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 6]
        elif plane.upper() in [ "XY"]:
            if self._fort18.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            data = np.empty((self._fort24.shape[0], 3))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 6]
            data[:, 2] = self._fort25[:, 6]
        elif plane.upper() in [ "Z"]:
            if self._fort18.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 6]
        else:
            raise RuntimeError("Result: Unknown plane to get Twiss beta: {}".format(plane))

        return data


    def get_beam_rms(self, plane="X"):
        """Get beam RMS size in X, Y, Z, or XY [meter].

        :return:
        """
        if plane.upper() in [ "X"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 2]
        elif plane.upper() in [ "Y"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 2]
        elif plane.upper() in [ "XY"]:
            data = np.empty((self._fort24.shape[0], 3))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 2]
            data[:, 2] = self._fort25[:, 2]
        elif plane.upper() in [ "Z"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort26[:, 2]
        else:
            raise RuntimeError("Result: Unknown plane to get beam RMS size: {}".format(plane))

        return data

    def get_beam_emittance(self, plane="X"):
        """Get beam normalized RMS emittance (m-rad for transverse and degree-MeV for longitudinal).

        :return:
        """
        if plane.upper() in [ "X"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 4]
        elif plane.upper() in [ "Y"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort25[:, 4]
        elif plane.upper() in [ "XY"]:
            data = np.empty((self._fort24.shape[0], 3))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort24[:, 4]
            data[:, 2] = self._fort25[:, 4]
        elif plane.upper() in [ "Z"]:
            data = np.empty((self._fort24.shape[0], 2))
            data[:, 0] = self._fort18[:, 0]
            data[:, 1] = self._fort26[:, 4]
        else:
            raise RuntimeError("Result: Unknown plane to get beam normalized RMS Emittance: {}".format(plane))

        return data
