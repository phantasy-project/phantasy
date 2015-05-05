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
    return ResultFactory(directory).build()


class ResultFactory(object):
    """A factory to get simulation results from IMPACT working directory.
    """

    def __init__(self, directory=None):
        """Initialize class, give IMPACT working directory.

        :param directory: IMPACT working directory (default is current directory)
        """
        self.directory = directory

    def build(self, **kwargs):
        """ Build result from impact simulation.
        It needs IMPACT fort file, fort.18, fort.24, fort.25, and fort.26

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
            # Y0, Y0', Yrms, Y'rms, Ey, Alpha y, Beta y
            fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 7, 5, 6))
            # Z0, Z0', Zrms, Z'rms, Ez, Alpha Z, Beta z
            fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 7, 5, 6))
        elif _IMPACT in ["LBL", "LBNL"]:
            # z, phase (rad), energy (MeV), gamma, beta
            fort18 = np.loadtxt(fort18path, usecols=(0, 1, 3, 2, 4))
            # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
            fort24 = np.loadtxt(fort24path, usecols=(1, 3, 2, 4, 6, 5))
            # Y0, Y0', Yrms, Y'rms, Ey, Alpha y, Beta y
            fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 6, 5))
            # Z0, Z0', Zrms, Z'rms, Ez, Alpha Z, Beta z
            fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 6, 5))

        else:
            raise RuntimeError("Unknown IMPACT version. Cannot parse results.")

        if not _keep:
            shutil.rmtree(wkdir)
        
        return Result(fort18, fort24, fort25, fort26)
    
    def update(self, **kwargs):
        """ Build result from impact simulation.
        It needs IMPACT fort file, fort.18, fort.24, fort.25, and fort.26

        :param fort18:  impact energy file name
        :param fort24:  impact horizontal file name
        :param fort25:  impact vertical file name
        :param fort26:  impact longitudinal file name
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
            # Y0, Y0', Yrms, Y'rms, Ey, Alpha y, Beta y
            fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 7, 5, 6))
            # Z0, Z0', Zrms, Z'rms, Ez, Alpha Z, Beta z
            fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 7, 5, 6))
        elif _IMPACT in ["LBL", "LBNL"]:
            # z, phase (rad), energy (MeV), gamma, beta
            fort18 = np.loadtxt(fort18path, usecols=(0, 1, 3, 2, 4))
            # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
            fort24 = np.loadtxt(fort24path, usecols=(1, 3, 2, 4, 6, 5))
            # Y0, Y0', Yrms, Y'rms, Ey, Alpha y, Beta y
            fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 6, 5))
            # Z0, Z0', Zrms, Z'rms, Ez, Alpha Z, Beta z
            fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 6, 5))

        else:
            raise RuntimeError("Unknown IMPACT version. Cannot parse results.")

        if not _keep:
            shutil.rmtree(wkdir)

        self.result = Result(fort18, fort24, fort25, fort26)

class Result(object):

    def __init__(self, fort18, fort24, fort25, fort26, impact="LBL"):
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
        self.elements = len(self._fort18[:, 0])
        
        self.impact = impact

    def __checkElements(self, elemIdx):
        """Check whether required element index is over the range.
        
        :param elemIdx: element index
        
        :raise: RuntimeError
        """
        if elemIdx > self.elements:
            raise RuntimeError("Required element index {0} over maximum {1}.".format(elemIdx, self.elements))

    def getSPosition(self, elemIdx=None):
        """Get element s position at the end if elemIdx is given, or list of s position for all elements
        
        :param elemIdx: index number of given element
        
        :return: s position or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 0]
        else:
            self.__checkElements(elemIdx)
        return self._fort18[:, 0][elemIdx]

    def getAbsPhase(self, elemIdx=None):
        """Get accumulated beam phase in radian at the end if elemIdx is given, 
        or a list for all elements
        
        :param elemIdx: index number of given element
        
        :return: accumulated beam phase or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 1]
        else:
            self.__checkElements(elemIdx)
        return self._fort18[:, 1][elemIdx]

    def getEnergy(self, elemIdx=None):
        """Get beam energy in MeV/u at the end if elemIdx is given, 
        or a list for all elements
        
        :param elemIdx: index number of given element
        
        :return: beam energy or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 2]
        else:
            self.__checkElements(elemIdx)
        return self._fort18[:, 2][elemIdx]
    
    def getBetaGamma(self, elemIdx=None):
        """Get beam beta*gamma at the end if elemIdx is given, or a list for all elements
        
        :param elemIdx: index number of given element
        
        :return: beta*gamma or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 3]*self._fort18[:, 4]
        else:
            self.__checkElements(elemIdx)
        return self._fort18[:, 3][elemIdx]*self._fort18[:, 4][elemIdx]
    
    def __getData(self, data, data2=None, elemIdx=None, col=0):
        """Common interface to get simulation data.
        
        :param elemIdx: element index
        :param data:    first data set
        :param data2:   2nd data set 
        :param col:     column in data/data2
        
        :return: value at given location if elemIdx is `None`, or 1D array if data2 is `None`, otherwise 2D array
        
        :raise: RuntimeError  
        """
        result = None
        if elemIdx is None:
            if data2 is None:
                result = data[:, col]
            else:
                result = np.empty((data.shape[0], 2))
                result[:, 0] = data[:, col]
                result[:, 1] = data2[:, col]
        else:
            self.__checkElements(elemIdx)
            if data2 is None:
                result = data[:, col][elemIdx]
            else:
                result = [data[:, col][elemIdx], data2[:, col][elemIdx]]
        return result

    def getOrbit(self, plane="X", elemIdx=None):
        """Get beam position at the end of an element if elemIdx is given, or beam orbit at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam position at given location, or at all elements
        """
        if plane.upper() == "X":
            return self.__getData(self._fort24, elemIdx=elemIdx, col=0)
        elif plane.upper() == "Y":
            return self.__getData(self._fort25, elemIdx=elemIdx, col=0)
        elif plane.upper() == "XY":
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=0)
        else:
            raise RuntimeError("Result: Unknown plane for beam orbit on: {}".format(plane))

    def getTwissAlpha(self, plane="X", elemIdx=None):
        """Get beam twiss alpha parameters at the end of an element if elemIdx is given, or at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss alpha at given location, or at all elements
        """
        if plane.upper() == "X":
            return self.__getData(self._fort24, elemIdx=elemIdx, col=5)
        elif plane.upper() == "Y":
            return self.__getData(self._fort25, elemIdx=elemIdx, col=5)
        elif plane.upper() == "Z":
            return self.__getData(self._fort26, elemIdx=elemIdx, col=5)
        elif plane.upper() == "XY":
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=5)
        else:
            raise RuntimeError("Result: Unknown plane for beam twiss alpha on: {}".format(plane))

    def getTwissBeta(self, plane="X", elemIdx=None):
        """Get beam twiss beta parameters at the end of an element if elemIdx is given, or at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss beta at given location, or at all elements
        """
        if plane.upper() == "X":
            if self._fort24.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            return self.__getData(self._fort24, elemIdx=elemIdx, col=6)
        elif plane.upper() == "Y":
            if self._fort25.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            return self.__getData(self._fort25, elemIdx=elemIdx, col=6)
        elif plane.upper() == "Z":
            if self._fort26.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            return self.__getData(self._fort26, elemIdx=elemIdx, col=6)
        elif plane.upper() == "XY":
            if self._fort24.shape()[1] < 7 or self._fort25.shape()[1] < 7:
                raise DataError("No Twiss Beta available")
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=6)
        else:
            raise RuntimeError("Result: Unknown plane for beam twiss beta on: {}".format(plane))
        
    def geBeamRms(self, plane="X", elemIdx=None):
        """Get beam RMS parameters at the end of an element if elemIdx is given, or at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss beta at given location, or at all elements
        """
        if plane.upper() == "X":
            return self.__getData(self._fort24, elemIdx=elemIdx, col=2)
        elif plane.upper() == "Y":
            return self.__getData(self._fort25, elemIdx=elemIdx, col=2)
        elif plane.upper() == "Z":
            return self.__getData(self._fort26, elemIdx=elemIdx, col=2)
        elif plane.upper() == "XY":
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=2)
        else:
            raise RuntimeError("Result: Unknown plane for beam RMS on: {}".format(plane))

    def getEmittance(self, plane="X", elemIdx=None):
        """Get beam normalized emittance (m-rad for transverse and degree-MeV for longitudinal)
        at the end of an element if elemIdx is given, or at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all elements
        """
        if plane.upper() == "X":
            return self.__getData(self._fort24, elemIdx=elemIdx, col=4)
        elif plane.upper() == "Y":
            return self.__getData(self._fort25, elemIdx=elemIdx, col=4)
        elif plane.upper() == "Z":
            return self.__getData(self._fort26, elemIdx=elemIdx, col=4)
        elif plane.upper() == "XY":
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=4)
        else:
            raise RuntimeError("Result: Unknown plane for beam RMS on: {}".format(plane))
    
    def getBeamMomentumCentroid(self, plane="X", elemIdx=None):
        """Get beam centroid momentum (radian for transverse and MeV for longitudinal)
        at the end of an element if elemIdx is given, or at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all elements
        """
        if plane.upper() == "X":
            return self.__getData(self._fort24, elemIdx=elemIdx, col=1)
        elif plane.upper() == "Y":
            return self.__getData(self._fort25, elemIdx=elemIdx, col=1)
        elif plane.upper() == "Z":
            return self.__getData(self._fort26, elemIdx=elemIdx, col=1)
        elif plane.upper() == "XY":
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=1)
        else:
            raise RuntimeError("Result: Unknown plane for beam RMS on: {}".format(plane))
        
    def getMomentumRms(self, plane="X", elemIdx=None):
        """Get beam RMS momentum (radian for transverse and MeV for longitudinal)
        at the end of an element if elemIdx is given, or at all elements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all elements
        """
        if plane.upper() == "X":
            return self.__getData(self._fort24, elemIdx=elemIdx, col=3)
        elif plane.upper() == "Y":
            return self.__getData(self._fort25, elemIdx=elemIdx, col=3)
        elif plane.upper() == "Z":
            return self.__getData(self._fort26, elemIdx=elemIdx, col=3)
        elif plane.upper() == "XY":
            return self.__getData(self._fort24, data2=self._fort25, elemIdx=elemIdx, col=3)
        else:
            raise RuntimeError("Result: Unknown plane for beam RMS on: {}".format(plane))

def build_lattice(directory=None):
    """Convenience method to build IMPACT lattice.
    """
    return LatticeFactory(directory).build()


class LatticeFactory(object):
    """A factory to create lattice input file in working directory for IMPACT.
    """

    def __init__(self, lattice, directory=None):
        """Initialize class, give IMPACT working directory.

        :param directory: IMPACT working directory (default is current directory)
        """
        self.directory = directory


    def build(self, **kwargs):
        """ Build IMPACT input lattice deck.

        :param IMPACT:  IMPACT-Z version, either "FRIB" or "LBL". "FRIB" by default.
        :return:
        """

        if self.directory != None:
            wkdir = self.directory
        else:
            wkdir = os.getcwd()

        _IMPACT = kwargs.get("IMPACT", "FRIB")
        return Lattice()

class Lattice(object):
    pass
