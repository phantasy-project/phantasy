# encoding: UTF-8

"""Library for IMPACT related lattice/model function."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import sys, os.path, tempfile, logging, subprocess, shutil

from ..lattice.impact import Lattice

from .. import cfg

import numpy as np

from ..common import DataError

# configuration options

CONFIG_IMPACT_EXE_FILE = "impact_exe_file"

CONFIG_IMPACT_DATA_DIR = "impact_data_dir"

# default values

_DEFAULT_IMPACT_EXE = "impact"

_TEMP_DIRECTORY_SUFFIX = "_impact"

# global logger instance

_LOGGER = logging.getLogger(__name__)


def run(lattice, **kwargs):
    """Convenience method to build result with specified configuration.

    :param lattice: IMPACT Lattice object
    :param config: machine configuration
    :param settings: dictionary of machine settings
    :param data_dir: path of directory containing IMPACT data files
    :param work_dir: path of directory for execution of IMPACT
    :return: Result instance
    """
    result_factory = ResultFactory(lattice, **kwargs)

    return result_factory.build()


class ResultFactory(object):
    """A factory to run IMPACT and get the resulting model."""

    def __init__(self, lattice, **kwargs):
        """Initialzie the with the required IMPACT lattice.

        :param lattice: IMPACT Lattice object
        :param config: machine configuration
        :param settings: dictionary of machine settings
        :param data_dir: path of directory containing IMPACT data files
        :param work_dir: path of directory for execution of IMPACT
        """
        self.lattice = lattice
        
        if "config" in kwargs:
            self.config = kwargs.get("config")
        else:
            self.cofig = cfg.config
        
        self.data_dir = kwargs.get("data_dir", None)
        self.work_dir = kwargs.get("work_dir", None)


    @property
    def lattice(self):
        return self._lattice

    @lattice.setter
    def lattice(self, lattice):
        if not isinstance(lattice, Lattice):
            raise TypeError("ResultFactory: 'lattice' property much be type Lattice")
        self._lattice = lattice


    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if (data_dir != None) and not isinstance(data_dir, basestring):
            raise TypeError("ResultFactory: 'data_dir' property much be type string or None")
        self._data_dir = data_dir


    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir != None) and not isinstance(work_dir, basestring):
            raise TypeError("ResultFactory: 'work_dir' property much be type string or None")
        self._work_dir = work_dir


    def _get_config_impact_exe(self):
        if cfg.config.has_default(CONFIG_IMPACT_EXE_FILE):
            impact_exe = cfg.config.get_default(CONFIG_IMPACT_EXE_FILE)
            if not os.path.isabs(impact_exe) and impact_exe.startswith(".") and (cfg.config_path != None):
                impact_exe = os.path.abspath(os.path.join(os.path.dirname(cfg.config_path), impact_exe))
            return impact_exe

        return _DEFAULT_IMPACT_EXE

    def build(self):
        """Prepare working directory, execute IMPACT and read the resulting model.
        """

        data_dir = self.data_dir
        if (data_dir == None) and cfg.config.has_default(CONFIG_IMPACT_DATA_DIR):
            data_dir = cfg.config.get_default(CONFIG_IMPACT_DATA_DIR)

        if data_dir == None:
            raise RuntimeError("ResultFactory: No data directory provided, check the configuration")

        work_dir = self.work_dir

        impact_exe = self._get_config_impact_exe()

        if not os.path.isdir(data_dir):
            raise RuntimeError("ResultFactory: Data directory not found: {}".format(data_dir))

        if (work_dir != None) and os.path.exists(work_dir):
            raise RuntimeError("ResultFactory: Working directory already exists: {}".format(work_dir))

        if work_dir != None:
            os.makedirs(work_dir)
            rm_work_dir = False
        else:
            work_dir = tempfile.mkdtemp(_TEMP_DIRECTORY_SUFFIX)
            rm_work_dir = True

        _LOGGER.info("ResultFactory: Working directory: %s", work_dir)

        if os.path.isabs(data_dir):
            abs_data_dir = data_dir
        else:
            abs_data_dir = os.path.abspath(data_dir)

        for datafile in os.listdir(abs_data_dir):
            srcpath = os.path.join(abs_data_dir, datafile)
            destpath = os.path.join(work_dir, datafile)
            if os.path.isfile(os.path.join(abs_data_dir, datafile)):
                os.symlink(srcpath, destpath)
                _LOGGER.debug("ResultFactory: Link data file %s to %s", srcpath, destpath)

        try:
            with open(os.path.join(work_dir, "test.in"), "w") as fp:
                self._lattice.write(fp)
        except:
            self._remove_work_dir(work_dir, rm_work_dir)
            raise

        try:
            subprocess.check_output(["mpirun", "-np", str(self.lattice.nprocessors), impact_exe],
                                           cwd=work_dir, stderr=subprocess.STDOUT)
        except Exception as e:
            if isinstance(e, subprocess.CalledProcessError):
                sys.stderr.write(e.output)
            self._remove_work_dir(work_dir, rm_work_dir)
            raise

        try:
            return build_result(impact="FRIB", directory=work_dir, keep=True)
        finally:
            self._remove_work_dir(work_dir, rm_work_dir)



    @staticmethod
    def _remove_work_dir(work_dir, rm_work_dir):
        """Cleanup the working directory.
        """
        if rm_work_dir:
            _LOGGER.debug("ResultFactory: Cleanup: remove work directory")
            shutil.rmtree(work_dir)



def build_result(impact="FRIB", directory=None, keep=True):
    """Convenience method to build IMPACT model result.
    """
    model = Result(impact, directory)
    model.updateResult(keep=keep)
    return model

class Result(object):

    def __init__(self, impact="FRIB", directory=None):
        """

        :return:
        """
        self.impact = impact
        self.directory = directory
        self.totalelements = None

    def updateResult(self, **kwargs):
        """ Build result from impact simulation.
        It needs IMPACT fort file, fort.18, fort.24, fort.25, and fort.26

        :param IMPACT:  IMPACT-Z version, either "FRIB" or "LBL". "FRIB" by default.
        :param fort18:  impact energy file name, numpy N x 5 array
        :param fort24:  impact horizontal file name, numpy N x 7 array, or N x 6 for LBL version (no TWISS beta)
        :param fort25:  impact vertical file name, numpy N x 7 array, or N x 6 for LBL version (no TWISS beta)
        :param fort26:  impact longitudinal file name, numpy N x 7 array, or N x 6 for LBL version (no TWISS beta)
        :param keep:    keep simulation results, True by default.
        :return:
        """

        if self.directory != None:
            wkdir = self.directory
        else:
            wkdir = os.getcwd()

        _fort18 = kwargs.get("fort18", "fort.18")
        _fort24 = kwargs.get("fort24", "fort.24")
        _fort25 = kwargs.get("fort25", "fort.25")
        _fort26 = kwargs.get("fort26", "fort.26")
        _keep = kwargs.get("keep", True)

        fort18path = os.path.join(wkdir, _fort18)
        if not os.path.isfile(fort18path):
            raise RuntimeError("Result: IMPACT output not found: {}".format(fort18path))

        fort24path = os.path.join(wkdir, _fort24)
        if not os.path.isfile(fort24path):
            raise RuntimeError("Result: IMPACT output not found: {}".format(fort24path))

        fort25path = os.path.join(wkdir, _fort25)
        if not os.path.isfile(fort25path):
            raise RuntimeError("Result: IMPACT output not found: {}".format(fort25path))

        fort26path = os.path.join(wkdir, _fort26)
        if not os.path.isfile(fort25path):
            raise RuntimeError("Result: IMPACT output not found: {}".format(fort25path))

        # read data in if all data files are in place
        if self.impact == "FRIB":
            # z, phase (rad), energy (MeV), gamma, beta
            self._fort18 = np.loadtxt(fort18path, usecols=(0, 1, 3, 2, 4))
            # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
            self._fort24 = np.loadtxt(fort24path, usecols=(1, 3, 2, 4, 7, 5, 6))
            # Y0, Y0', Yrms, Y'rms, Ey, Alpha y, Beta y
            self._fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 7, 5, 6))
            # Z0, Z0', Zrms, Z'rms, Ez, Alpha Z, Beta z
            self._fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 7, 5, 6))
        elif self.impact in ["LBL", "LBNL"]:
            # z, phase (rad), energy (MeV), gamma, beta
            self._fort18 = np.loadtxt(fort18path, usecols=(0, 1, 3, 2, 4))
            # X0, X0', Xrms, X'rms, Ex, Alpha x, Beta x
            self._fort24 = np.loadtxt(fort24path, usecols=(1, 3, 2, 4, 6, 5))
            # Y0, Y0', Yrms, Y'rms, Ey, Alpha y, Beta y
            self._fort25 = np.loadtxt(fort25path, usecols=(1, 3, 2, 4, 6, 5))
            # Z0, Z0', Zrms, Z'rms, Ez, Alpha Z, Beta z
            self._fort26 = np.loadtxt(fort26path, usecols=(1, 3, 2, 4, 6, 5))
        else:
            raise RuntimeError("Unknown IMPACT version. Cannot parse results.")

        if not _keep:
            shutil.rmtree(wkdir)
        self.totalelements = len(self._fort18[:, 0])
        
    def __checkElements(self, elemIdx):
        """Check whether required element index is over the range.
        
        :param elemIdx: element index
        
        :raise: RuntimeError
        """
        maxindex = elemIdx
        if isinstance(elemIdx, (list, tuple)):
            maxindex = max(elemIdx)
        if maxindex > self.totalelements:
            raise RuntimeError("Required element index {0} over maximum {1}.".format(elemIdx, self.totalelements))

    def getSPosition(self, elemIdx=None):
        """Get element s position at the end if elemIdx is given, or list of s position for all totalelements
        
        :param elemIdx: index number of given element
        
        :return: s position or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 0]
        else:
            self.__checkElements(elemIdx)
            if isinstance(elemIdx, (list, tuple)):
                res = []
                for idx, val in enumerate(self._fort18[:, 0]):
                    if idx in elemIdx:
                        res.append(val)
                return np.array(res)
            else:
                return self._fort18[:, 0][elemIdx]

    def getAbsPhase(self, elemIdx=None):
        """Get accumulated beam phase in radian at the end if elemIdx is given, 
        or a list for all totalelements
        
        :param elemIdx: index number of given element
        
        :return: accumulated beam phase or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 1]
        else:
            self.__checkElements(elemIdx)
            if isinstance(elemIdx, (list, tuple)):
                res = []
                for idx, val in enumerate(self._fort18[:, 1]):
                    if idx in elemIdx:
                        res.append(val)
                return np.array(res)
            else:
                return self._fort18[:, 1][elemIdx]

    def getEnergy(self, elemIdx=None):
        """Get beam energy in MeV/u at the end if elemIdx is given, 
        or a list for all totalelements
        
        :param elemIdx: index number of given element
        
        :return: beam energy or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 2]
        else:
            self.__checkElements(elemIdx)
            if isinstance(elemIdx, (list, tuple)):
                res = []
                for idx, val in enumerate(self._fort18[:, 2]):
                    if idx in elemIdx:
                        res.append(val)
                return np.array(res)
            else:
                return self._fort18[:, 2][elemIdx]
    
    def getBeta(self, elemIdx=None):
        """Get beam beta (v/c) at the end if elemIdx is given, or a list for all elements
        
        :param elemIdx: index number of given element
        
        :return: beta or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 4]
        else:
            self.__checkElements(elemIdx)
            if isinstance(elemIdx, (list, tuple)):
                res = []
                for idx, val in enumerate(self._fort18[:, 4]):
                    if idx in elemIdx:
                        res.append(val)
                return np.array(res)
            else:
                return self._fort18[:, 4][elemIdx]
    
    def getGamma(self, elemIdx=None):
        """Get beam gamma at the end if elemIdx is given, or a list for all elements
        
        :param elemIdx: index number of given element
        
        :return: beta*gamma or list
        :raise: RuntimeError
        """
        
        if elemIdx is None:
            return self._fort18[:, 3]
        else:
            self.__checkElements(elemIdx)
            if isinstance(elemIdx, (list, tuple)):
                res = []
                for idx, val in enumerate(self._fort18[:, 3]):
                    if idx in elemIdx:
                        res.append(val)
                return np.array(res)
            else:
                return self._fort18[:, 3][elemIdx]
    
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
            if isinstance(elemIdx, (list, tuple)):
                res = []
                for idx, val in enumerate(data):
                    if idx in elemIdx:
                        res.append(val)
                res2=[]
                if data2 is not None:
                    for idx, val in enumerate(data2):
                        if idx in elemIdx:
                            res2.append(val)
                    return [np.array(res), np.array[res2]]

                return np.array(res)
            else:
                if data2 is None:
                    result = data[:, col][elemIdx]
                else:
                    result = [data[:, col][elemIdx], data2[:, col][elemIdx]]
        return result


    def getOrbit(self, plane="X", elemIdx=None):
        """Get beam position at the end of an element if elemIdx is given, or beam orbit at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam position at given location, or at all totalelements
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
        """Get beam twiss alpha parameters at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss alpha at given location, or at all totalelements
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
        """Get beam twiss beta parameters at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss beta at given location, or at all totalelements
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
        
    def getBeamRms(self, plane="X", elemIdx=None):
        """Get beam RMS parameters at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss beta at given location, or at all totalelements
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
        at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all totalelements
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
        at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all totalelements
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
        at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all totalelements
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
