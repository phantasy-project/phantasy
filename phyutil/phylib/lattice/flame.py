# encoding: UTF-8

"""
Utility for generating a FLAME lattice from accelerator layout.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import logging
import os.path
from collections import OrderedDict

import numpy
from flame import GLPSPrinter

from phyutil.phylib.cfg import Configuration
from phyutil.phylib.layout.accel import Element
from phyutil.phylib.layout.accel import DriftElement
from phyutil.phylib.layout.accel import ValveElement
from phyutil.phylib.layout.accel import CavityElement
from phyutil.phylib.layout.accel import BLMElement
from phyutil.phylib.layout.accel import BLElement
from phyutil.phylib.layout.accel import BCMElement
from phyutil.phylib.layout.accel import BPMElement
from phyutil.phylib.layout.accel import PMElement
from phyutil.phylib.layout.accel import SolCorElement
from phyutil.phylib.layout.accel import PortElement
from phyutil.phylib.layout.accel import CorElement
from phyutil.phylib.layout.accel import BendElement
from phyutil.phylib.layout.accel import QuadElement
from phyutil.phylib.layout.accel import StripElement
from phyutil.phylib.layout.accel import SextElement



CONFIG_FLAME_SIM_TYPE = "flame_sim_type"

CONFIG_FLAME_CAV_TYPE = "flame_cav_type"

CONFIG_FLAME_DATA_DIR = "flame_data_dir"

CONFIG_FLAME_MPOLE_LEVEL = "flame_mpole_level"

CONFIG_FLAME_HDIPOLE_FIT_MODE = "flame_hdipole_fit_mode"

CONFIG_FLAME_PARTICLE_MASS = "flame_particle_mass"

CONFIG_FLAME_INITIAL_ENERGY = "flame_initial_energy"

CONFIG_FLAME_CHARGE = "flame_charge"

CONFIG_FLAME_COUNT = "flame_count"

CONFIG_FLAME_STRIPPER_CHARGE = "flame_stripper_charge"

CONFIG_FLAME_STRIPPER_COUNT = "flame_stripper_count"

CONFIG_FLAME_INITIAL_POSITION_FILE = "flame_initial_position_file"

CONFIG_FLAME_INITIAL_ENVELOPE_FILE = "flame_initial_envelope_file"

CONFIG_FLAME_SPLIT = "flame_split"

# Constants used for IMPACT header parameters

SIM_TYPE_MOMENT_MATRIX = "MomentMatrix"

MPOLE_LEVEL_FOCUS_DEFOCUS = 0

MPOLE_LEVEL_DIPOLE = 1

MPOLE_LEVEL_QUADRUPOLE = 2


HDIPOLE_FIT_MODE_BEAM_ENERGY = 1

# Default values for IMPACT lattice generation

_DEFAULT_SIM_TYPE = SIM_TYPE_MOMENT_MATRIX

_DEFAULT_MPOLE_LEVEL = MPOLE_LEVEL_QUADRUPOLE

_DEFAULT_HDIPOLE_FIT_MODE = HDIPOLE_FIT_MODE_BEAM_ENERGY

_DEFAULT_CHARGE = 0.138655462

_DEFAULT_COUNT = 1.0

_DEFAULT_PARTICLE_MASS = 931.49432e6

_DEFAULT_INITIAL_ENERGY = 0.0

_DEFAULT_INITIAL_POSITION = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
]

_DEFAULT_INITIAL_ENVELOPE = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
]

_DEFAULT_DATA_DIR = "data"

_DEFAULT_SPLIT = 1

_LOGGER = logging.getLogger(__name__)


def build_lattice(accel, **kwargs):
    lattice_factory = FlameLatticeFactory(accel, **kwargs)

    return lattice_factory.build()



class BaseLatticeFactory(object):
    """
    """
    def __init__(self):
        pass

    def _get_config_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.get_default(option)
            _LOGGER.debug("BaseLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return value
        return defvalue


    def _get_config_int_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.getint_default(option)
            _LOGGER.debug("BaseLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return value
        return defvalue


    def _get_config_float_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.getfloat_default(option)
            _LOGGER.debug("BaseLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return value
        return defvalue

    def _get_config_array_default(self, option, defvalue, conv=None, unpack=True):
        if self.config.has_default(option):
            value = self.config.getarray_default(option, conv=conv)
            if unpack and (len(value) == 1):
                value = value[0]
            _LOGGER.debug("BaseLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return value
        return defvalue

    def _get_config_abspath_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.getabspath_default(option)
            _LOGGER.debug("BaseLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return value
        return defvalue


    def _get_config(self, section, option, defvalue):
        if self.config.has_option(section, option):
            value = self.config.get(section, option)
            _LOGGER.debug("BaseLatticeFactory: [{}] '{}' found in configuration: {}".format(section, option, value))
            return value
        return defvalue


    def _get_config_array(self, section, option, defvalue, conv=None, unpack=True):
        if self.config.has_option(section, option):
            value = self.config.getarray(section, option, conv=conv)
            if unpack and (len(value) == 1):
                value = value[0]
            _LOGGER.debug("BaseLatticeFactory: [{}] '{}' found in configuration: {}".format(section, option, value))
            return value
        return defvalue


    def build(self):
        raise NotImplemented()



class FlameLatticeFactory(BaseLatticeFactory):
    """FlameLatticeFactory class builds a FLAME Lattice object
      from an Accelerator Design Description.

      :param accel: accelerator layout
      :param config: configuration options
      :param settings: accelerator settings
    """
    def __init__(self, accel, **kwargs):
        self._accel = accel

        if kwargs.get("config", None) is not None:
            self.config = kwargs.get("config")
        else:
            self.config = Configuration()

        if kwargs.get("settings", None) is not None:
            self.settings = kwargs.get("settings")
        else:
            self.settings = self._get_config_settings()


        self.simType = kwargs.get("simType", None)
        self.dataDir = kwargs.get("dataDir", None)
        self.count = kwargs.get("count", None)
        self.charge = kwargs.get("charge", None)
        self.mpoleLevel = kwargs.get("mpoleLevel", None)
        self.hdipoleFitMode = kwargs.get("hdipoleFitMode", None)
        self.particleMass = kwargs.get("particleMass", None)
        self.initialEnergy = kwargs.get("initialEnergy", None)
        self.initialPosition = kwargs.get("initialPosition", None)
        self.initialEnvelope = kwargs.get("initialEnvelope", None)
        self.start = kwargs.get("start", None)
        self.end = kwargs.get("end", None)
        self.template = kwargs.get("template", False)


    def _get_config_stripper_charge(self, dtype):
        option = CONFIG_FLAME_STRIPPER_CHARGE
        if self.config.has_option(dtype, option):
            value = self.config.getarray


    def _get_config_data_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.getabspath_default(option)
            _LOGGER.debug("FlameLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return numpy.loadtxt(value)
        return defvalue


    # COMMON
    def _get_config_settings(self):
        if self.config.has_default("settings_file"):
            stgpath = self.config.getabspath_default("settings_file")
            with open(stgpath, "r") as stgfile:
                settings = Settings()
                settings.readfp(stgfile)
                return settings
        return None


    def _get_config_split(self, dtype=None):
        option = CONFIG_FLAME_SPLIT
        if (dtype is None) and self.config.has_default(option):
            value = self.config.getint_default(option)
            _LOGGER.debug("FlameLatticeFactory: '{}' found in configuration: {}".format(option, value))
            return value
        elif (dtype is not None) and self.config.has_option(dtype, option):
            value = self.config.getint(dtype, option)
            _LOGGER.debug("LatticeFactory: [{}] {} found in configuration: {}".format(dtype, option, value))
            return value
        return _DEFAULT_SPLIT


    def build(self):

        settings = None
        if not self.template:
            settings = self.settings

        lattice = FlameLattice()

        if self.simType is not None:
            lattice.simType = self.simType
        else:
            lattice.simType = self._get_config_default(CONFIG_FLAME_SIM_TYPE, _DEFAULT_SIM_TYPE)

        if self.dataDir is not None:
            lattice.dataDir = self.dataDir
        else:
            lattice.dataDir = self._get_config_abspath_default(CONFIG_FLAME_DATA_DIR, _DEFAULT_DATA_DIR)

        if self.mpoleLevel is not None:
            lattice.mpoleLevel = self.mpoleLevel
        else:
            lattice.mpoleLevel = self._get_config_int_default(CONFIG_FLAME_MPOLE_LEVEL, _DEFAULT_MPOLE_LEVEL)

        if self.hdipoleFitMode is not None:
            lattice.hdipoleFitMode = self.hdipoleFitMode
        else:
            lattice.hdipoleFitMode = self._get_config_int_default(CONFIG_FLAME_HDIPOLE_FIT_MODE, _DEFAULT_HDIPOLE_FIT_MODE)

        if self.particleMass is not None:
            lattice.particleMass = self.particleMass
        else:
            lattice.particleMass = self._get_config_float_default(CONFIG_FLAME_PARTICLE_MASS, _DEFAULT_PARTICLE_MASS)

        if self.initialEnergy is not None:
            lattice.initialEnergy = self.initialEnergy
        else:
            lattice.initialEnergy = self._get_config_float_default(CONFIG_FLAME_INITIAL_ENERGY, _DEFAULT_INITIAL_ENERGY)

        if self.count is not None:
            lattice.count = self.count
        else:
            lattice.count = self._get_config_float_default(CONFIG_FLAME_COUNT, _DEFAULT_COUNT)

        if self.charge is not None:
            lattice.charge = self.charge
        else:
            lattice.charge =  self._get_config_float_default(CONFIG_FLAME_CHARGE, _DEFAULT_CHARGE)

        if self.initialPosition is not None:
            lattice.initialPosition = self.initialPosition
        else:
            lattice.initialPosition = self._get_config_data_default(CONFIG_FLAME_INITIAL_POSITION_FILE, _DEFAULT_INITIAL_POSITION)

        if self.initialEnvelope is not None:
            lattice.initialEnvelope = self.initialEnvelope
        else:
            lattice.initialEnvelope = self._get_config_data_default(CONFIG_FLAME_INITIAL_ENVELOPE_FILE, _DEFAULT_INITIAL_ENVELOPE)

        ndrift = [ 0 ]
        def nextDrift():
            ndrift[0] += 1
            return "DRIFT_" + str(ndrift[0])

        for elem in self._accel.iter(self.start, self.end):

            if isinstance(elem, DriftElement):
                lattice.append(nextDrift(), "drift",
                               ('L',elem.length), ('aper',elem.aperture/2.0))

            elif isinstance(elem, (ValveElement, PortElement)):
                lattice.append(elem.name, "drift",
                               ('L',elem.length), ('aper',elem.aperture/2.0),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, BPMElement):
                if elem.length != 0.0:
                    lattice.append(nextDrift(), "drift", ('L',elem.length/2.0), ('aper',elem.aperture/2.0))

                lattice.append(elem.name, "bpm", name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(nextDrift(), "drift", ('L',elem.length/2.0), ('aper',elem.aperture/2.0))

            elif isinstance(elem, (PMElement, BLMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append(elem.name, "drift", ('L',elem.length), ('aper',elem.aperture/2.0))

            elif isinstance(elem, CavityElement):
                phase = 0.0
                if settings != None:
                    try:
                        phase = settings[elem.name][elem.fields.phase]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.phase, elem.name))

                amplitude = 0.0
                if settings != None:
                    try:
                        amplitude = settings[elem.name][elem.fields.amplitude]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.amplitude, elem.name))

                frequency = 0.0
                if settings != None:
                    try:
                        frequency = settings[elem.name][elem.fields.frequency]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.frequency, elem.name))

                cavType = self._get_config(elem.dtype, CONFIG_FLAME_CAV_TYPE, None)
                if cavType is None:
                    raise RuntimeError("FlameLatticeFactory: Cavity type not found: {}", elem.dtype)

                lattice.append(elem.name, "rfcavity",
                               ('cavtype',cavType), ('f',frequency),
                               ('phi',phase), ('scl_fac',amplitude),
                               ('L',elem.length), ('aper',elem.aperture/2.0),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, SolCorElement):
                field = 0.0
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                hkick = 0.0
                if settings != None:
                    try:
                        hkick = settings[elem.h.name][elem.h.fields.angle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.h.fields.angle, elem.name))

                vkick = 0.0
                if settings != None:
                    try:
                        vkick = settings[elem.v.name][elem.v.fields.angle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.v.fields.angle, elem.name))

                #error = self._get_error(elem)

                lattice.append(elem.name + "_1", "solenoid", ('L',elem.length/2.0),
                               ('aper',elem.aperture/2.0), ('B',field),
                               name=elem.name, etype="SOL")

                lattice.append(elem.h.name, "orbtrim", ('theta_x',hkick),
                               name=elem.h.name, etype=elem.h.ETYPE)

                lattice.append(elem.v.name, "orbtrim", ('theta_y',vkick),
                               name=elem.v.name, etype=elem.v.ETYPE)

                lattice.append(elem.name + "_2", "solenoid", ('L',elem.length/2.0),
                               ('aper',elem.aperture/2.0), ('B',field),
                               name=elem.name, etype="SOL")

            elif isinstance(elem, QuadElement):
                gradient = 0.0
                if settings != None:
                    try:
                        gradient = settings[elem.name][elem.fields.gradient]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.gradient, elem.name))

                #error = self._get_error(elem)

                lattice.append(elem.name, "quadrupole", ('L',elem.length),
                               ('aper',elem.aperture/2.0), ('B2',gradient),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, SextElement):
                field = 0.0
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                if field != 0.0:
                    _LOGGER.warning("FlameLatticeFactory: Hexapole magnet element support not implemented. Ignoring field: %s T/m^2", field)

                lattice.append(elem.name, "drift", ('L',elem.length), ('aper',elem.aperture/2.0))

            elif isinstance(elem, CorElement):
                hkick = 0.0
                if settings != None:
                    try:
                        hkick = settings[elem.h.name][elem.h.fields.angle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.h.fields.angle, elem.name))

                vkick = 0.0
                if settings != None:
                    try:
                        vkick = settings[elem.v.name][elem.v.fields.angle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.v.fields.angle, elem.name))

                if elem.length != 0.0:
                    lattice.append(nextDrift(), "drift",
                                   ('L',elem.length/2.0),
                                   ('aper',elem.apertureX/2.0))

                lattice.append(elem.h.name, "orbtrim", ('theta_x',hkick),
                               name=elem.h.name, etype=elem.h.ETYPE)

                lattice.append(elem.v.name, "orbtrim", ('theta_y',vkick),
                               name=elem.v.name, etype=elem.v.ETYPE)

                if elem.length != 0.0:
                    lattice.append(nextDrift(), "drift",
                                   ('L',elem.length/2.0),
                                   ('aper',elem.apertureX/2.0))

            elif isinstance(elem, BendElement):
                field = 0.0
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                angle = 0.0
                if settings != None:
                    try:
                        angle = settings[elem.name][elem.fields.angle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.angle, elem.name))

                entrAngle = 0.0
                if settings != None:
                    try:
                        entrAngle = settings[elem.name][elem.fields.entrAngle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.entrAngle, elem.name))

                exitAngle = 0.0
                if settings != None:
                    try:
                        exitAngle = settings[elem.name][elem.fields.exitAngle]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.exitAngle, elem.name))

                split = self._get_config_split(elem.dtype)

                if split < 3:
                    raise RuntimeError("FlameLatticeFactory: '{}' split must be greater than 3.".format(elem.name))

                lattice.append(elem.name + "_1", "sbend", ('L',elem.length/split),
                               ('aper',elem.aperture/2.0), ('phi',angle/split),
                               ('phi1',entrAngle), ('phi2',exitAngle), ('bg',field),
                               name=elem.name, etype=elem.ETYPE)

                for i in xrange(2, split):
                    lattice.append(elem.name + "_" + str(i), "sbend", ('L',elem.length/split),
                                   ('aper',elem.aperture/2.0), ('phi',angle/split),
                                   ('phi1',0.0), ('phi2',0.0), ('bg',field),
                                   name=elem.name, etype=elem.ETYPE)

                lattice.append(elem.name + "_" + str(split), "sbend", ('L',elem.length/split),
                               ('aper',elem.aperture/2.0), ('phi',angle/split),
                               ('phi1',entrAngle), ('phi2',exitAngle), ('bg',field),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, StripElement):
                stripper_charge = self._get_config_array(elem.name, CONFIG_FLAME_STRIPPER_CHARGE, None, conv=float)
                if stripper_charge is None:
                    raise RuntimeError("FlameLatticeFactory: Stripper charge not found: {}".format(elem.name))
                stripper_charge = numpy.array(stripper_charge)

                stripper_count = self._get_config_array(elem.name, CONFIG_FLAME_STRIPPER_COUNT, None, conv=float)
                if stripper_count is None:
                    raise RuntimeError("FlameLatticeFactory: Stripper count not found: {}".format(elem.name))
                stripper_count = numpy.array(stripper_count)

                if elem.length != 0.0:
                    lattice.append(nextDrift(), "drift",
                                   ('L',elem.length/2.0),
                                   ('aper',elem.aperture/2.0))

                lattice.append(elem.name, "stripper",
                               ('IonChargeStates',stripper_charge),
                               ('NCharge',stripper_count),
                               name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(nextDrift(), "drift",
                                   ('L',elem.length/2.0),
                                   ('aper',elem.aperture/2.0))

            else:
                raise Exception("Unsupported accelerator element: {}".format(elem))

        return lattice


class FlameLattice(object):

    def __init__(self):
        self.elements = []
        self.variables = OrderedDict()
        self.simType = _DEFAULT_SIM_TYPE
        self.mpoleLevel = _DEFAULT_MPOLE_LEVEL
        self.hdipoleFitMode = _DEFAULT_HDIPOLE_FIT_MODE
        self.particleMass = _DEFAULT_PARTICLE_MASS
        self.initialEnergy = _DEFAULT_INITIAL_ENERGY
        self.charge = _DEFAULT_CHARGE
        self.count = _DEFAULT_COUNT
        self.initialPosition = _DEFAULT_INITIAL_POSITION
        self.initialEvelope = _DEFAULT_INITIAL_ENVELOPE
        self.dataDir = os.path.abspath(_DEFAULT_DATA_DIR)
        self.append('S', "source", ('vector_variable',"P"), ('matrix_variable',"S"))


    @property
    def simType(self):
        return self.variables['sim_type']

    @simType.setter
    def simType(self, simType):
        if simType not in [ SIM_TYPE_MOMENT_MATRIX ]:
            raise ValueError("FlameLattice: 'simType' property must be supported value")
        self.variables['sim_type'] = simType

    @property
    def dataDir(self):
        return self.variables['Eng_Data_Dir']

    @dataDir.setter
    def dataDir(self, dataDir):
        if not isinstance(dataDir, (basestring, unicode)):
            raise ValueError("FlameLattice: 'dataDir' property must be a string")
        self.variables['Eng_Data_Dir'] = dataDir


    @property
    def mpoleLevel(self):
        return self.variables['MpoleLevel']

    @mpoleLevel.setter
    def mpoleLevel(self, mpoleLevel):
        if mpoleLevel not in [MPOLE_LEVEL_FOCUS_DEFOCUS,
                              MPOLE_LEVEL_DIPOLE,
                              MPOLE_LEVEL_QUADRUPOLE]:
            raise ValueError("FlameLattice: 'mpoleLevel' property must be supported value")
        self.variables['MpoleLevel'] = mpoleLevel


    @property
    def hdipoleFitMode(self):
        return self.variables['HdipoleFitMode']

    @hdipoleFitMode.setter
    def hdipoleFitMode(self, hdipoleFitMode):
        if hdipoleFitMode not in [HDIPOLE_FIT_MODE_BEAM_ENERGY]:
            raise ValueError("FlameLattice: 'hdipoleFitMode' property must be supported value")
        self.variables['HdipoleFitMode'] = hdipoleFitMode


    @property
    def charge(self):
        return self.variables['IonChargeStates']

    @charge.setter
    def charge(self, charge):
        if isinstance(charge, (int, float)):
            self.variables['IonChargeStates'] = numpy.array([float(charge)])
        elif isinstance(charge, (list,tuple)):
            v = []
            for c in charge:
                if not isinstance(c, (int,float)):
                    raise TypeError("FlameLattice: 'charge' must be a list of numbers")
                v.append(float(c))
            self.variables['IonChargeStates'] = numpy.array(v)
        elif isinstance(charge, numpy.ndarray):
            self.variables['IonChargeStates'] = numpy.array(charge)
        else:
            raise TypeError("FlameLattice: 'charge' must be a number or list of numbers")


    @property
    def count(self):
        return self.variables['NCharge']

    @count.setter
    def count(self, count):
        if isinstance(count, (int,float)):
            self.variables['NCharge'] = numpy.array([float(count)])
        elif isinstance(count, (list,tuple)):
            v = []
            for c in count:
                if not isinstance(c, (int,float)):
                    raise TypeError("FlameLattice: 'count' must be a list of numbers")
                v.append(float(c))
            self.variables['NCharge'] = numpy.array(v)
        elif isinstance(count, numpy.ndarray):
            self.variables['NCharge'] = numpy.array(count)
        else:
            raise TypeError("FlameLattice: 'count' must be a number or list of numbers")


    @property
    def initialPosition(self):
        keys = []
        for k in self.variables.keys():
            if re.match("P(\\d+)$", k):
                keys.append(k)
        keys.sort()
        position = numpy.empty((len(keys),7))
        for i, k in enumerate(keys):
            position[i] = self.variables[k]
        return position

    @initialPosition.setter
    def initialPosition(self, initialPosition):
        def replace_variable(position):
            for k in self.variables.keys():
                if re.match("P(\\d+)$", k):
                    del self.variables[k]
            for i in range(0, position.shape[0]):
                self.variables['P'+str(i)] = position[i]
        if isinstance(initialPosition, (list,tuple)):
            try:
                position = numpy.array(initialPosition).reshape((-1, 7))
            except:
                raise ValueError("FlameLattice: 'initialPosition' must have shape (x, 7)")
            replace_variable(position)
        elif isinstance(initialPosition, numpy.ndarray):
            try:
                position = initialPosition.reshape((-1, 7))
            except:
                raise ValueError("FlameLattice: 'initialPosition' must have shape (x, 7)")
            replace_variable(position)
        else:
            raise TypeError("FlameLattice: 'initialPosition' must be a list of numbers")


    @property
    def initialEnvelope(self):
        keys = []
        for k in self.variables.keys():
            if re.match("S(\\d+)$", k):
                keys.append(k)
        keys.sort()
        position = numpy.empty((len(keys), 7, 7))
        for i, k in enumerate(keys):
            position[i] = self.variables[k]
        return position

    @initialEnvelope.setter
    def initialEnvelope(self, initialEnvelope):
        def replace_variable(position):
            for k in self.variables.keys():
                if re.match("S(\\d+)$", k):
                    del self.variables[k]
            for i in range(0, position.shape[0]):
                self.variables['S'+str(i)] = position[i]
        if isinstance(initialEnvelope, (list,tuple)):
            try:
                position = numpy.array(initialEnvelope).reshape((-1, 7, 7))
            except:
                raise ValueError("FlameLattice: 'initialEnvelope' must have shape (x, 7, 7)")
            replace_variable(position)
        elif isinstance(initialEnvelope, numpy.ndarray):
            try:
                position = initialEnvelope.reshape((-1, 7, 7))
            except:
                raise ValueError("FlameLattice: 'initialEnvelope' must have shape (x, 7, 7)")
            replace_variable(position)
        else:
            raise TypeError("FlameLattice: 'initialEnvelope' must be a list of numbers")


    @property
    def initialEnergy(self):
        return self.variables['IonEk']

    @initialEnergy.setter
    def initialEnergy(self, initialEnergy):
        if not isinstance(initialEnergy, (int,float)):
            raise TypeError("FlameLattice: 'initialEnergy' must be a number")
        self.variables['IonEk'] = float(initialEnergy)


    @property
    def particleMass(self):
        return self.variables['IonEs']

    @particleMass.setter
    def particleMass(self, particleMass):
        if not isinstance(particleMass, (int,float)):
            raise TypeError("FlameLattice: 'particleMass' must be a number")
        self.variables['IonEs'] = float(particleMass)


    def append(self, fname, ftype, *args, **kwargs):
        self.elements.append((fname, ftype, OrderedDict(args), OrderedDict(kwargs)))


    def conf(self):
        c = OrderedDict(self.variables)
        c['elements'] = []
        for elem in self.elements:
            e = OrderedDict()
            e['name'] = elem[0]
            e['type'] = elem[1]
            e.update(elem[2])
            c['elements'].append(e)
        return c


    def write(self, fp):
        fp.write(GLPSPrinter(self.conf()))
