# encoding: UTF-8

"""Library for executing IMPACT and reading the resulting model."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

import sys, os.path, tempfile, logging, subprocess, shutil

from ....phylib.lattice.impact import Lattice

from ....phylib import cfg

from ....phylib.model.impact import ResultFactory as ImpactResultFactory

# configuration options

CONFIG_IMPACT_EXE_FILE = "impact_exe_file"

CONFIG_IMPACT_DATA_DIR = "impact_data_dir"

# default values

_DEFAULT_IMPACT_EXE = "impact"

_TEMP_DIRECTORY_SUFFIX = "_impact"

# global logger instance

_LOGGER = logging.getLogger(__name__)


def build_result(lattice, data_dir=None, work_dir=None):
    """Convenience method to build result with specified configuration.

    :param settings: dictionary of machine settings
    :param data_dir: path of directory containing IMPACT data files
    :param work_dir: path of directory for execution of IMPACT
    :return: Result instance
    """
    result_factory = ResultFactory(lattice)

    if data_dir != None:
        result_factory.data_dir = data_dir

    if work_dir != None:
        result_factory.work_dir = work_dir

    return result_factory.build()


class ResultFactory(object):
    """A factory to run IMPACT and get the resulting model."""

    def __init__(self, lattice):
        """Initialzie the with the required IMPACT lattice.

        :param lattice: IMPACT lattice object
        """
        self.lattice = lattice
        self.data_dir = None
        self.work_dir = None

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
            return ImpactResultFactory(work_dir).build(IMPACT="FRIB", keep=True)
        finally:
            self._remove_work_dir(work_dir, rm_work_dir)



    @staticmethod
    def _remove_work_dir(work_dir, rm_work_dir):
        """Cleanup the working directory.
        """
        if rm_work_dir:
            _LOGGER.debug("ResultFactory: Cleanup: remove work directory")
            shutil.rmtree(work_dir)

