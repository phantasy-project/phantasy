# encoding: UTF-8

#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Library for generating IMPACT lattice file (test.in) from Accelerator Design Description.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

import sys, os.path, logging, subprocess, shutil, tempfile, json, random

from datetime import datetime
from collections import OrderedDict

from phantasy.library.settings import Settings
from phantasy.library.parser import Configuration
from phantasy.library.layout import Element
from phantasy.library.layout import DriftElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import SeqElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import BCMElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import ElectrodeElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import ColumnElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import EBendElement
from phantasy.library.layout import FCElement
from phantasy.library.layout import VDElement
from phantasy.library.layout import EMSElement


CONFIG_IMPACT_NSTATES = "impact_nstates"
CONFIG_IMPACT_NPARTICLES = "impact_nparticles"
CONFIG_IMPACT_NPROCESSORS = "impact_nprocessors"
CONFIG_IMPACT_TYPE = "impact_type"
CONFIG_IMPACT_STEPS = "impact_steps"
CONFIG_IMPACT_MAPSTEPS = "impact_mapsteps"
CONFIG_IMPACT_INTEGRATOR = "impact_integrator"
CONFIG_IMPACT_LINEAR_INPUT_ID = "impact_linear_input_id"
CONFIG_IMPACT_LORENTZ_INPUT_ID = "impact_lorentz_input_id"
CONFIG_IMPACT_T7DATA_INPUT_ID = "impact_t7data_input_id"
CONFIG_IMPACT_STRIP_INPUT_ID = "impact_strip_input_id"
CONFIG_IMPACT_NDIMENSIONS = "impact_ndimensions"
CONFIG_IMPACT_ERROR_STUDY = "impact_error_study"
CONFIG_IMPACT_ERROR_RANDOM = "impact_error_random"
CONFIG_IMPACT_MESH_SIZE = "impact_mesh_size"
CONFIG_IMPACT_MESH_MODE = "impact_mesh_mode"
CONFIG_IMPACT_PIPE_SIZE = "impact_pipe_size"
CONFIG_IMPACT_PERIOD_SIZE = "impact_period_size"
CONFIG_IMPACT_INPUT_MODE = "impact_input_mode"
CONFIG_IMPACT_OUTPUT_MODE = "impact_output_mode"
CONFIG_IMPACT_CURRENT = "impact_current"
CONFIG_IMPACT_CHARGE = "impact_charge"
CONFIG_IMPACT_DIST_SIGMA = "impact_dist_sigma"
CONFIG_IMPACT_DIST_LAMBDA = "impact_dist_lambda"
CONFIG_IMPACT_DIST_MU = "impact_dist_mu"
CONFIG_IMPACT_MISMATCH = "impact_mismatch"
CONFIG_IMPACT_EMISMATCH = "impact_emismatch"
CONFIG_IMPACT_OFFSET = "impact_offset"
CONFIG_IMPACT_EOFFSET = "impact_eoffset"
CONFIG_IMPACT_RESTART = "impact_restart"
CONFIG_IMPACT_SUBCYCLE = "impact_subcycle"
CONFIG_IMPACT_INITIAL_CURRENT = "impact_initial_current"
CONFIG_IMPACT_INITIAL_ENERGY = "impact_initial_energy"
CONFIG_IMPACT_INITIAL_PHASE = "impact_initial_phase"
CONFIG_IMPACT_INITIAL_CHARGE = "impact_initial_charge"
CONFIG_IMPACT_PARTICLE_MASS = "impact_particle_mass"
CONFIG_IMPACT_SCALING_FREQ = "impact_scaling_freq"
CONFIG_IMPACT_BEAM_PERCENT = "impact_beam_percent"

# Constants used for IMPACT header parameters

INTEGRATOR_LINEAR = 1
INTEGRATOR_LORENTZ = 2
OUTPUT_MODE_NONE = 0
OUTPUT_MODE_STD = 1
OUTPUT_MODE_STD99 = 2
OUTPUT_MODE_DIAG = 3
OUTPUT_MODE_DIAG99 = 4
OUTPUT_MODE_END = 5
OUTPUT_MODE_END99 = 6
INPUT_MODE_RECTANGLE_SINGLE = 1
INPUT_MODE_GAUSSIAN_SINGLE = 2
INPUT_MODE_WATERBAG_SINGLE = 3
INPUT_MODE_SEMIGAUSSIAN_SINGLE = 4
INPUT_MODE_KV_UNIFORM_SINGLE = 5
INPUT_MODE_WATERBAG_MULTI = 16
INPUT_MODE_GAUSSIAN_MULTI = 17
INPUT_MODE_EXTERNAL_FILE = 19
NDIMENSIONS_6D = 6
ERROR_STUDY_DISABLED = 0
ERROR_STUDY_ENABLED = 1
MESH_MODE_OPEN_OPEN = 1
MESH_MODE_OPEN_PERIODIC = 2
MESH_MODE_FINITE_OPEN_ROUND = 3
MESH_MODE_FINITE_PERIODIC_ROUND = 4
MESH_MODE_FINITE_OPEN_RECT = 5
MESH_MODE_FINITE_PERIODIC_RECT = 6
RESTART_DISABLED = 0
RESTART_ENABLED = 1
SUBCYCLE_DISABLED = 0
SUBCYCLE_ENABLED = 1

# Default values for IMPACT lattice generation

_DEFAULT_NSTATES = 1
_DEFAULT_NPARTICLES = 1000
_DEFAULT_NPROCESSORS = 1
_DEFAULT_STEPS = 4
_DEFAULT_MAPSTEPS = 20
_DEFAULT_INTEGRATOR = INTEGRATOR_LORENTZ
_DEFAULT_OUTPUT_MODE = OUTPUT_MODE_DIAG
_DEFAULT_INPUT_MODE = INPUT_MODE_WATERBAG_SINGLE
_DEFAULT_NDIMENSIONS = NDIMENSIONS_6D
_DEFAULT_ERROR_STUDY = ERROR_STUDY_DISABLED
_DEFAULT_ERROR_RANDOM = []
_DEFAULT_MESH_SIZE = [ 64, 64, 64 ]
_DEFAULT_MESH_MODE = MESH_MODE_OPEN_OPEN
_DEFAULT_PIPE_SIZE = [ 0.01, 0.01 ]
_DEFAULT_PERIOD_SIZE = 0.1
_DEFAULT_CURRENT = 0.0
_DEFAULT_CHARGE = 1.065836735E-9
_DEFAULT_DIST_SIGMA = [ 1.0, 1.0, 1.0 ]
_DEFAULT_DIST_LAMBDA = [ 1.0, 1.0, 1.0 ]
_DEFAULT_DIST_MU = [ 1.0, 1.0, 1.0 ]
_DEFAULT_MISMATCH = [ 1.0, 1.0, 1.0 ]
_DEFAULT_EMISMATCH = [ 1.0, 1.0, 1.0 ]
_DEFAULT_OFFSET = [ 0.0, 0.0, 0.0]
_DEFAULT_EOFFSET = [ 0.0, 0.0, 0.0 ]
_DEFAULT_RESTART = RESTART_DISABLED
_DEFAULT_SUBCYCLE = SUBCYCLE_DISABLED
_DEFAULT_INITIAL_CURRENT = 0.0
_DEFAULT_INITIAL_ENERGY = 0.0
_DEFAULT_INITIAL_PHASE = 0.0
_DEFAULT_INITIAL_CHARGE = 1.0
_DEFAULT_PARTICLE_MASS = 939.294
_DEFAULT_SCALING_FREQ = 100
_DEFAULT_BEAM_PERCENT = 99.9


_LOGGER = logging.getLogger(__name__)


def build_lattice(accel, **kwargs):
    """Convenience method for building the IMPACT lattice.

    Parameters
    ----------
    accel :
        Accelerator layout.
    config :
        Configuration options.
    settings :
        Accelerator settings.

    Returns
    -------
    ret :
        :class:`Lattice` object.
    """
    lattice_factory = LatticeFactory(accel, **kwargs)
    return lattice_factory.build()


class LatticeFactory(object):
    """LatticeFactory class builds an IMPACT lattice
    object from an Accelerator Design Description.

    :param accel: accelerator layout
    :param config: configuration options
    :param settings: accelerator settings
    """

    def __init__(self, accel, **kwargs):
        self.accel = accel

        if kwargs.get("config", None) is not None:
            self.config = kwargs.get("config")
        else:
            self.config = Configuration()

        if kwargs.get("settings", None) is not None:
            self.settings = kwargs.get("settings")
        else:
            self.settings = self._get_config_settings()

        self.nstates = kwargs.get("nstates", None)
        self.nparticles = kwargs.get("nparticles", None)
        self.nprocessors = kwargs.get("nprocessors", None)
        self.integrator = kwargs.get("integrator", None)
        self.ndimensions = kwargs.get("ndimensions", None)
        self.errorStudy = kwargs.get("errorStudy", None)
        self.errorRandom = kwargs.get("errorRandom", None)
        self.meshMode = kwargs.get("meshMode", None)
        self.meshSize = kwargs.get("meshSize", None)
        self.pipeSize = kwargs.get("pipeSize", None)
        self.periodSize = kwargs.get("periodSize", None)
        self.outputMode = kwargs.get("outputMode", None)
        self.inputMode = kwargs.get("inputMode", None)
        self.current = kwargs.get("current", None)
        self.charge = kwargs.get("charge", None)
        self.distSigma = kwargs.get("distSigma", None)
        self.distLambda = kwargs.get("distLambda", None)
        self.distMu = kwargs.get("distMu", None)
        self.mismatch = kwargs.get("mismatch", None)
        self.emismatch = kwargs.get("emismatch", None)
        self.offset = kwargs.get("offset", None)
        self.eoffset = kwargs.get("eoffset", None)
        self.restart = kwargs.get("restart", None)
        self.subcycle = kwargs.get("subcycle", None)
        self.initialCurrent = kwargs.get("initialCurrent", None)
        self.initialEnergy = kwargs.get("initialEnergy", None)
        self.initialPhase = kwargs.get("initialPhase", None)
        self.initialCharge = kwargs.get("initialCharge", None)
        self.particleMass = kwargs.get("particleMass", None)
        self.scalingFreq = kwargs.get("scalingFreq", None)
        self.beamPercent = kwargs.get("beamPercent", None)
        self.start = kwargs.get("start", None)
        self.end = kwargs.get("end", None)
        self.template = kwargs.get("template", False)
        self._errors = {}


    @property
    def accel(self):
        return self._accel

    @accel.setter
    def accel(self, accel):
        if not isinstance(accel, SeqElement):
            raise TypeError("LatticeFactory: 'accel' property must be type a SeqElement")
        self._accel = accel

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if (start != None) and not isinstance(start, str):
            raise TypeError("LatticeFactory: 'start' property must be type string or None")
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end != None) and not isinstance(end, str):
            raise TypeError("LatticeFactory: 'end' property must be type string or None")
        self._end = end

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not isinstance(config, Configuration):
            raise TypeError("LatticeFactory: 'config' property must be type Configuration")
        self._config = config

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if not isinstance(settings, (dict)):
            raise TypeError("LatticeFactory: 'settings' property must be a dictionary")
        self._settings = settings

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        if not isinstance(template, bool):
            raise TypeError("LatticeFactory: 'template' property must be type bool")
        self._template = template

    def _get_config_type(self, dtype, default):
        if self.config.has_option(dtype, CONFIG_IMPACT_TYPE, False):
            return self.config.getint(dtype, CONFIG_IMPACT_TYPE, False)

        return default

    def _get_config_integrator_input_id(self, dtype, integrator):
        if (integrator == INTEGRATOR_LINEAR):
            if self.config.has_option(dtype, CONFIG_IMPACT_LINEAR_INPUT_ID, False):
                return self.config.getint(dtype, CONFIG_IMPACT_LINEAR_INPUT_ID, False)

        if (integrator == INTEGRATOR_LORENTZ):
            if self.config.has_option(dtype, CONFIG_IMPACT_LORENTZ_INPUT_ID, False):
                return self.config.getint(dtype, CONFIG_IMPACT_LORENTZ_INPUT_ID, False)

        return None

    def _get_config_t7data_input_id(self, dtype):
        if self.config.has_option(dtype, CONFIG_IMPACT_T7DATA_INPUT_ID, False):
            return self.config.getint(dtype, CONFIG_IMPACT_T7DATA_INPUT_ID, False)

        return None

    def _get_config_strip_input_id(self, elem):
        if self.config.has_option(elem.name, CONFIG_IMPACT_STRIP_INPUT_ID, False):
            return self.config.getint(elem.name, CONFIG_IMPACT_STRIP_INPUT_ID, False)

        if self.config.has_option(elem.dtype, CONFIG_IMPACT_STRIP_INPUT_ID, False):
            return self.config.getint(elem.dtype, CONFIG_IMPACT_STRIP_INPUT_ID, False)

        return None

    def _get_config_int_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.getint_default(option)
            _LOGGER.debug("LatticeFactory: %s found in configuration: %s", option, value)
            return value

        return defvalue

    def _get_config_float_default(self, option, defvalue):
        if self.config.has_default(option):
            value = self.config.getfloat_default(option)
            _LOGGER.debug("LatticeFactory: %s found in configuration: %s", option, value)
            return value

        return defvalue

    def _get_config_array_default(self, option, defvalue, conv=None, unpack=True):
        if self.config.has_default(option):
            value = self.config.getarray_default(option, conv=conv)
            if unpack and (len(value) == 1):
                value = value[0]
            _LOGGER.debug("LatticeFactory: %s found in configuration: %s", option, value)
            return value

        return defvalue

    def _get_config_settings(self):
        if self.config.has_default("settings_file"):
            stgpath = self.config.getabspath_default("settings_file")
            with open(stgpath, "r") as stgfile:
                settings = Settings()
                settings.readfp(stgfile)
                return settings

        return None

    def _get_config_steps(self, dtype=None):
        option = CONFIG_IMPACT_STEPS
        if (dtype == None) and self.config.has_default(option):
            value = self.config.getint_default(option)
            _LOGGER.debug("LatticeFactory: %s found in configuration: %s", option, value)
            return value

        if (dtype != None) and self.config.has_option(dtype, option):
            value = self.config.getint(dtype, option)
            _LOGGER.debug("LatticeFactory: [%s] %s found in configuration: %s", dtype, option, value)
            return value

        return _DEFAULT_STEPS

    def _get_config_mapsteps(self, dtype=None):
        option = CONFIG_IMPACT_MAPSTEPS
        if (dtype == None) and self.config.has_default(option):
            value = self.config.getint_default(option)
            _LOGGER.debug("LatticeFactory: %s found in configuration: %s", option, value)
            return value

        if (dtype != None) and self.config.has_option(dtype, option):
            value = self.config.getint(dtype, option)
            _LOGGER.debug("LatticeFactory: [%s] %s found in configuration: %s", dtype, option, value)
            return value

        return _DEFAULT_MAPSTEPS

    def _get_config_error_random(self, dtype=None):
        option = CONFIG_IMPACT_ERROR_RANDOM
        if (dtype == None) and self.config.has_default(option):
            value = self.config.getarray_default(option, conv=float)
            _LOGGER.debug("LatticeFactory: %s found in configuration: %s", option, value)
            return value

        if (dtype != None) and self.config.has_option(dtype, option):
            value = self.config.getarray(dtype, option, conv=float)
            _LOGGER.debug("LatticeFactory: [%s] %s found in configuration: %s", dtype, option, value)
            return value

        return _DEFAULT_ERROR_RANDOM

    def _get_error(self, elem):
        if elem.name in self._errors:
            return self._errors[elem.name]

        error_random = self._get_config_error_random(dtype=elem.dtype)
        if not error_random:
            return []

        error = [ 0.0 ] * 5
        for idx in range(min(len(error), len(error_random))):
            error[idx] = random.uniform(-1*error_random[idx], error_random[idx])

        self._errors[elem.name] = error

        return error

    def build(self):
        settings = None
        if self.template == False:
            settings = self.settings

        integrator = self.integrator
        if integrator == None:
            integrator = self._get_config_int_default(CONFIG_IMPACT_INTEGRATOR, _DEFAULT_INTEGRATOR)

        lattice = Lattice(integrator)

        if self.nstates != None:
            lattice.nstates = self.nstates
        else:
            lattice.nstates = self._get_config_int_default(CONFIG_IMPACT_NSTATES, _DEFAULT_NSTATES)

        if self.nparticles != None:
            lattice.nparticles = self.nparticles
        else:
            lattice.nparticles = self._get_config_array_default(CONFIG_IMPACT_NPARTICLES, _DEFAULT_NPARTICLES, conv=int)

        if self.nprocessors != None:
            lattice.nprocessors = self.nprocessors
        else:
            lattice.nprocessors = self._get_config_int_default(CONFIG_IMPACT_NPROCESSORS, _DEFAULT_NPROCESSORS)

        if self.ndimensions != None:
            lattice.ndimensions = self.ndimensions
        else:
            lattice.ndimensions = self._get_config_int_default(CONFIG_IMPACT_NDIMENSIONS, _DEFAULT_NDIMENSIONS)

        if self.errorStudy != None:
            lattice.errorStudy = self.errorStudy
        else:
            lattice.errorStudy = self._get_config_int_default(CONFIG_IMPACT_ERROR_STUDY, _DEFAULT_ERROR_STUDY)

        if self.meshMode != None:
            lattice.meshMode = self.meshMode
        else:
            lattice.meshMode = self._get_config_int_default(CONFIG_IMPACT_MESH_MODE, _DEFAULT_MESH_MODE)

        if  self.meshSize != None:
            lattice.meshSize = self.meshSize
        else:
            lattice.meshSize = self._get_config_array_default(CONFIG_IMPACT_MESH_SIZE, _DEFAULT_MESH_SIZE, conv=int)

        if self.pipeSize != None:
            lattice.pipeSize = self.pipeSize
        else:
            lattice.pipeSize = self._get_config_array_default(CONFIG_IMPACT_PIPE_SIZE, _DEFAULT_PIPE_SIZE, conv=float)

        if self.periodSize != None:
            lattice.periodSize = self.periodSize
        else:
            lattice.periodSize = self._get_config_float_default(CONFIG_IMPACT_PERIOD_SIZE, _DEFAULT_PERIOD_SIZE)

        if self.outputMode != None:
            lattice.outputMode = self.outputMode
        else:
            lattice.outputMode = self._get_config_int_default(CONFIG_IMPACT_OUTPUT_MODE, _DEFAULT_OUTPUT_MODE)

        if self.inputMode != None:
            lattice.inputMode = self.inputMode
        else:
            lattice.inputMode = self._get_config_int_default(CONFIG_IMPACT_INPUT_MODE, _DEFAULT_INPUT_MODE)

        if self.current != None:
            lattice.current = self.current
        else:
            lattice.current = self._get_config_array_default(CONFIG_IMPACT_CURRENT, _DEFAULT_CURRENT, conv=float)

        if self.charge != None:
            lattice.charge = self.charge
        else:
            lattice.charge = self._get_config_array_default(CONFIG_IMPACT_CHARGE, _DEFAULT_CHARGE, conv=float)

        if self.distSigma != None:
            lattice.distSigma = self.distSigma
        else:
            lattice.distSigma = self._get_config_array_default(CONFIG_IMPACT_DIST_SIGMA, _DEFAULT_DIST_SIGMA, conv=float)

        if self.distLambda != None:
            lattice.distLambda = self.distLambda
        else:
            lattice.distLambda = self._get_config_array_default(CONFIG_IMPACT_DIST_LAMBDA, _DEFAULT_DIST_LAMBDA, conv=float)

        if self.distMu != None:
            lattice.distMu = self.distMu
        else:
            lattice.distMu = self._get_config_array_default(CONFIG_IMPACT_DIST_MU, _DEFAULT_DIST_MU, conv=float)

        if self.mismatch != None:
            lattice.mismatch = self.mismatch
        else:
            lattice.mismatch = self._get_config_array_default(CONFIG_IMPACT_MISMATCH, _DEFAULT_MISMATCH, conv=float)

        if self.emismatch != None:
            lattice.emismatch = self.emismatch
        else:
            lattice.emismatch = self._get_config_array_default(CONFIG_IMPACT_EMISMATCH, _DEFAULT_EMISMATCH, conv=float)

        if self.offset != None:
            lattice.offset = self.offset
        else:
            lattice.offset = self._get_config_array_default(CONFIG_IMPACT_OFFSET, _DEFAULT_OFFSET, conv=float)

        if self.eoffset != None:
            lattice.eoffset = self.eoffset
        else:
            lattice.eoffset = self._get_config_array_default(CONFIG_IMPACT_EOFFSET, _DEFAULT_EOFFSET, conv=float)

        if self.restart != None:
            lattice.restart = self.restart
        else:
            lattice.restart = self._get_config_int_default(CONFIG_IMPACT_RESTART, _DEFAULT_RESTART)

        if self.subcycle != None:
            lattice.subcycle = self.subcycle
        else:
            lattice.subcycle = self._get_config_int_default(CONFIG_IMPACT_SUBCYCLE, _DEFAULT_SUBCYCLE)

        if self.initialCurrent != None:
            lattice.initialCurrent = self.initialCurrent
        else:
            lattice.initialCurrent = self._get_config_float_default(CONFIG_IMPACT_INITIAL_CURRENT, _DEFAULT_INITIAL_CURRENT)

        if self.initialEnergy != None:
            lattice.initialEnergy = self.initialEnergy
        else:
            lattice.initialEnergy = self._get_config_float_default(CONFIG_IMPACT_INITIAL_ENERGY, _DEFAULT_INITIAL_ENERGY)

        if self.initialPhase != None:
            lattice.initialPhase = self.initialPhase
        else:
            lattice.initialPhase = self._get_config_float_default(CONFIG_IMPACT_INITIAL_PHASE, _DEFAULT_INITIAL_PHASE)

        if self.particleMass != None:
            lattice.particleMass = self.particleMass
        else:
            lattice.particleMass = self._get_config_float_default(CONFIG_IMPACT_PARTICLE_MASS, _DEFAULT_PARTICLE_MASS)

        if self.initialCharge != None:
            lattice.initialCharge = self.initialCharge
        else:
            lattice.initialCharge = self._get_config_float_default(CONFIG_IMPACT_INITIAL_CHARGE, _DEFAULT_INITIAL_CHARGE)

        if self.scalingFreq != None:
            lattice.scalingFreq = self.scalingFreq
        else:
            lattice.scalingFreq = self._get_config_float_default(CONFIG_IMPACT_SCALING_FREQ, _DEFAULT_SCALING_FREQ)

        if self.beamPercent != None:
            lattice.beamPercent = self.beamPercent
        else:
            lattice.beamPercent = self._get_config_float_default(CONFIG_IMPACT_BEAM_PERCENT, _DEFAULT_BEAM_PERCENT)

        lattice.comment = "Name: {a.name}, Desc: {a.desc}".format(a=self._accel)

        poffset = None

        for elem in self._accel.iter(self.start, self.end):

            if poffset == None:
                poffset = elem.z - (elem.length/2.0)

            if isinstance(elem, Element):
                steps = self._get_config_steps(elem.dtype)
                mapsteps = self._get_config_mapsteps(elem.dtype)
            else:
                steps = self._get_config_steps()
                mapsteps = self._get_config_mapsteps()

            if isinstance(elem, DriftElement):
                lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                               position=elem.z+(elem.length/2.0)-poffset,
                               name="DRIFT", etype=elem.ETYPE)

            elif isinstance(elem, ValveElement):
                lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                               position=elem.z+(elem.length/2.0)-poffset,
                               name="DRIFT", etype=elem.ETYPE)

            elif isinstance(elem, PortElement):
                lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                               position=elem.z+(elem.length/2.0)-poffset,
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, ColumnElement):
                lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                               position=elem.z+(elem.length/2.0)-poffset,
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, CavityElement):
                phase = 99999
                if settings != None:
                    try:
                        phase = settings[elem.name][elem.fields.phase]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.phase, elem.name))

                amplitude = 99999
                if settings != None:
                    try:
                        amplitude = settings[elem.name][elem.fields.amplitude]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.amplitude, elem.name))

                frequency = 99999
                if settings != None:
                    try:
                        frequency = settings[elem.name][elem.fields.frequency]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.frequency, elem.name))

                error = self._get_error(elem)

                itype = self._get_config_type(elem.dtype, 103)
                if itype == 103:
                    input_id = self._get_config_integrator_input_id(elem.dtype, integrator)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for type '{}' not found".format(elem.dtype))

                    lattice.append(elem.length, steps, mapsteps, 103, amplitude, frequency, phase, input_id, elem.apertureX/2.0, *error,
                                   position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype=elem.ETYPE,
                                   fields=[ (elem.fields.amplitude, "V", 4), (elem.fields.phase, "deg", 6) ])

                elif itype == 110:
                    input_id = self._get_config_t7data_input_id(elem.dtype)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for type '{}' not found".format(elem.dtype))

                    lattice.append(elem.length, steps, mapsteps, 110, amplitude, frequency, phase, input_id, elem.apertureX/2.0, elem.apertureX/2.0, 0, 0, 0, 0, 0, 1, 2, *error,
                                   position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype=elem.ETYPE,
                                   fields=[ (elem.fields.amplitude, "V", 4), (elem.fields.phase, "deg", 6) ])

                else:
                    raise RuntimeError("LatticeFactory: IMPACT element type for '{}' not supported: {}".format(elem.name, itype))


            elif isinstance(elem, SolElement):
                field = 99999
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                error = self._get_error(elem)

                lattice.append(elem.length, steps, mapsteps, 3, field, 0, elem.apertureX/2.0, *error,
                               position=elem.z-poffset, name=elem.name, etype="SOL", #elem.ETYPE
                               fields=[ (elem.fields.field, "T", 4) ])

            elif isinstance(elem, SolCorElement):
                field = 99999
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                hkick = 99999
                if settings != None:
                    try:
                        hkick = settings[elem.h.name][elem.h.fields.angle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.h.fields.angle, elem.name))

                vkick = 99999
                if settings != None:
                    try:
                        vkick = settings[elem.v.name][elem.v.fields.angle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.v.fields.angle, elem.name))

                error = self._get_error(elem)

                lattice.append(elem.length/2.0, int(steps/2), mapsteps, 3, field, 0, elem.apertureX/2.0, *error,
                               position=elem.z-poffset, name=elem.name, etype="SOL", #elem.ETYPE
                               fields=[ (elem.fields.field, "T", 4) ])

                lattice.append(0.0, 0, 0, -21, elem.apertureX/2.0, 0.0, hkick, 0.0, 0.0, 0.0, 0.0,
                                position=elem.h.z-poffset, name=elem.h.name, etype=elem.h.ETYPE,
                                fields=[ (elem.h.fields.angle, "rad", 6) ])

                lattice.append(0.0, 0, 0, -21, elem.apertureX/2.0, 0.0, 0.0, 0.0, vkick, 0.0, 0.0,
                               position=elem.v.z-poffset, name=elem.v.name, etype=elem.v.ETYPE,
                               fields=[ (elem.v.fields.angle, "rad", 8) ])

                lattice.append(elem.length/2.0, int(steps/2), mapsteps, 3, field, 0, elem.apertureX/2.0, *error,
                               position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="SOL", #elem.ETYPE
                               fields=[ (elem.fields.field, "T", 4) ])


            elif isinstance(elem, QuadElement):
                gradient = 99999
                if settings != None:
                    try:
                        gradient = settings[elem.name][elem.fields.gradient]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.gradient, elem.name))

                error = self._get_error(elem)

                lattice.append(elem.length, steps, mapsteps, 1, gradient, 0, elem.apertureX/2.0, *error,
                               position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype=elem.ETYPE,
                               fields=[ (elem.fields.gradient, "T/m", 4) ])


            elif isinstance(elem, CorElement):
                hkick = 99999
                if settings != None:
                    try:
                        hkick = settings[elem.h.name][elem.h.fields.angle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.h.fields.angle, elem.name))

                vkick = 99999
                if settings != None:
                    try:
                        vkick = settings[elem.v.name][elem.v.fields.angle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.v.fields.angle, elem.name))

                if elem.length != 0.0:
                    lattice.append(elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                lattice.append(0.0, 0, 0, -21, elem.apertureX/2.0, 0.0, hkick, 0.0, 0.0, 0.0, 0.0,
                               position=elem.h.z-poffset, name=elem.h.name, etype=elem.h.ETYPE,
                               fields=[ (elem.h.fields.angle, "rad", 6) ])

                lattice.append(0.0, 0, 0, -21, elem.apertureX/2.0, 0.0, 0.0, 0.0, vkick, 0.0, 0.0,
                               position=elem.v.z-poffset, name=elem.v.name, etype=elem.v.ETYPE,
                               fields=[ (elem.v.fields.angle, "rad", 8) ])

                if elem.length != 0.0:
                    lattice.append(elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")


            elif isinstance(elem, SextElement):
                field = 99999
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                ## IMPACT element 5 is not currently document. Below is provided for reference.
                ## L, ss, ms, 5, Gq(T/m), Gs(T/m^2),Go(T/m^3),Gd(T/m^4),Gdd(T/m^5),G14,G16,R
                #lattice.append("{length} {steps} {mapsteps} {itype} 0.0 {properties[B]} 0.0 0.0 0.0 0.0 0.0 {radius}",
                #                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=5, radius=elem.apertureX/2.0,
                #                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="SEXT", properties={ "B":field })

                if field != 0.0:
                    _LOGGER.warning("LatticeFactory: Hexapole magnet element support not implemented. Ignoring field: %s T/m^2", field)

                lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                               position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, BendElement):
                field = 99999
                if settings != None:
                    try:
                        field = settings[elem.name][elem.fields.field]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field, elem.name))

                angle = 99999
                if settings != None:
                    try:
                        angle = settings[elem.name][elem.fields.angle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.angle, elem.name))

                entrAngle = 99999
                if settings != None:
                    try:
                        entrAngle = settings[elem.name][elem.fields.entrAngle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.entrAngle, elem.name))

                exitAngle = 99999
                if settings != None:
                    try:
                        exitAngle = settings[elem.name][elem.fields.exitAngle]
                    except KeyError:
                        raise RuntimeError("LatticeFactory: '{}' setting not found for element: {}".format(elem.fields.exitAngle, elem.name))

                if steps < 3:
                    raise RuntimeError("LatticeFactory: '{}' number of steps must be greater than 2.".format(elem.name))

                lattice.append(elem.length/steps, 1, mapsteps, 4, angle/steps, field, 400, elem.apertureX/2.0, entrAngle, exitAngle, 0.0, 0.0, 0.0,
                               position=elem.z-(elem.length/2.0)+(elem.length/steps)-poffset, name=elem.name, etype=elem.ETYPE,
                               fields=[ (elem.fields.field, "T", 5) ])

                for i in range(2, steps):
                    lattice.append(elem.length/steps, 1, mapsteps, 4, angle/steps, field, 500, elem.apertureX/2.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                   position=elem.z-(elem.length/2.0)+i*(elem.length/steps)-poffset, name=elem.name, etype=elem.ETYPE,
                                   fields=[ (elem.fields.field, "T", 5) ])

                lattice.append(elem.length/steps, 1, mapsteps, 4, angle/steps, field, 600, elem.apertureX/2.0, entrAngle, exitAngle, 0.0, 0.0, 0.0,
                               position=elem.z-(elem.length/2.0)+elem.length-poffset, name=elem.name, etype=elem.ETYPE,
                               fields=[ (elem.fields.field, "T", 5) ])

            elif isinstance(elem, StripElement):
                input_id = self._get_config_strip_input_id(elem)
                if input_id == None:
                    raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                if elem.length != 0.0:
                    lattice.append(elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                lattice.append(0.0, 0, input_id, -11, 0, 0, position=elem.z-poffset, name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, (ElectrodeElement, EBendElement, EQuadElement, FCElement, VDElement, EMSElement)):
                if elem.length != 0.0:
                    lattice.append(elem.length, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype=elem.ETYPE)


            elif isinstance(elem, (BPMElement, PMElement)):
                if elem.length != 0.0:
                    lattice.append(elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                lattice.append(0, 0, 0, -28, position=elem.z-poffset, name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0,
                                   position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            else:
                raise Exception("Unsupport ADD element: {}".format(elem))

        return lattice


def read_lattice(stream):
    '''Read the IMPACT enhanced lattice file (test.in) with element information.

       The file format is generated by Lattice.write(stream, withElemData=True)

      :param stream: file-like input stream
      :returns: Lattice object
    '''
    headers = 1
    element = None
    position = None
    lattice = Lattice()

    for _, line in enumerate(stream):
        if line.startswith("!!["):
            if headers <= 11:
                raise RuntimeError("read_lattice: Element data before end of lattice header")
            if element is not None:
                raise RuntimeError("read_lattice: Element data found, expecting lattice data")
            element = json.loads(line[2:])

        if line.startswith("!"):
            # Ignore other comments
            continue

        # Example IMPACT-Z Lattice (test.in) Header
        # 4 1
        # 6 1000 2 0 1
        # 65 65 129 4 0.14 0.14 0.1025446
        # 3 0 0 1
        # 1000
        # 0.0
        # 1.48852718947e-10
        # 0.0022734189 8.8312578e-05 0.0 1.0 1.0 0.0 0.0
        # 0.0022734189 8.8312578e-05 0.0 1.0 1.0 0.0 0.0
        # 0.076704772 3.4741445e-06 0.0 1.0 1.0 0.0 0.0
        # 0.0 500000.0 931494320.0 0.138655462185 80500000.0 0.0 99.9
        if headers == 1:
            row = line.split()
            if len(row) != 2:
                raise RuntimeError("read_lattice: header line 1: "
                                   "expecting length 2 (found %s)", len(row))
            lattice.nprocessors = int(row[0])
            if int(row[1]) != 1:
                raise RuntimeError("read_lattice: header line 1: "
                                   "expecting parameter 2 with value 1 (found %s)",
                                   row[1])
            headers += 1
            continue

        if headers == 2:
            row = line.split()
            if len(row) != 5:
                raise RuntimeError("read_lattice: header line 2: "
                                   "expecting length 5 (found %s)", len(row))
            lattice.ndimensions = int(row[0])
            lattice.nparticles = int(row[1])
            lattice.integrator = int(row[2])
            lattice.errorStudy = int(row[3])
            lattice.outputMode = int(row[4])
            headers += 1
            continue

        if headers == 3:
            row = line.split()
            if len(row) != 7:
                raise RuntimeError("read_lattice: header line 3: "
                                   "expecting length 7 (found %s)", len(row))
            lattice.meshSize = [ int(row[0]), int(row[1]), int(row[2]) ]
            lattice.meshMode = int(row[3])
            lattice.pipeSize = [ float(row[4]), float(row[5]) ]
            lattice.periodSize = float(row[6])
            headers += 1
            continue

        if headers == 4:
            row = line.split()
            if len(row) != 4:
                raise RuntimeError("read_lattice: header line 4: "
                                   "expecting length 7 (found %s)", len(row))
            lattice.inputMode = int(row[0])
            lattice.restart = int(row[1])
            lattice.subcycle = int(row[2])
            lattice.nstates = int(row[3])
            headers += 1
            continue

        if headers == 5:
            row = line.split()
            if len(row) != lattice.nstates:
                raise RuntimeError("read_lattice: header line 5: "
                                   "expecting length %s (found %s)",
                                   lattice.nstates, len(row))
            if lattice.nstates == 1:
                lattice.nparticles = int(row[0])
            else:
                lattice.nparticles = [ int(n) for n in row ]
            headers += 1
            continue

        if headers == 6:
            row = line.split()
            if len(row) != lattice.nstates:
                raise RuntimeError("read_lattice: header line 6: "
                                   "expecting length %s (found %s)",
                                   lattice.nstates, len(row))
            if lattice.nstates == 1:
                lattice.current = float(row[0])
            else:
                lattice.current = [ float(n) for n in row ]
            headers += 1
            continue

        if headers == 7:
            row = line.split()
            if len(row) != lattice.nstates:
                raise RuntimeError("read_lattice: header line 7: "
                                   "expecting length %s (found %s)",
                                   lattice.nstates, len(row))
            if lattice.nstates == 1:
                lattice.charge = float(row[0])
            else:
                lattice.charge = [ float(n) for n in row ]
            headers += 1
            continue

        if headers == 8:
            row = [ line.split() ]
            if len(row[0]) != 7:
                raise RuntimeError("read_lattice: header line 8: "
                                   "expecting length 7 (found %s)",
                                   len(row[0]))
            headers += 1
            continue

        if headers == 9:
            row.append(line.split())
            if len(row[1]) != 7:
                raise RuntimeError("read_lattice: header line 9: "
                                   "expecting length 7 (found %s)",
                                   len(row[1]))
            headers += 1
            continue

        if headers == 10:
            row.append(line.split())
            if len(row[2]) != 7:
                raise RuntimeError("read_lattice: header line 10: "
                                   "expecting length 7 (found %s)",
                                   len(row[2]))
            lattice.distSigma = [ float(row[0][0]), float(row[1][0]), float(row[2][0]) ]
            lattice.distLambda = [ float(row[0][1]), float(row[1][1]), float(row[2][1]) ]
            lattice.distMu = [ float(row[0][2]), float(row[1][2]), float(row[2][2]) ]
            lattice.mismatch = [ float(row[0][3]), float(row[1][3]), float(row[2][3]) ]
            lattice.emismatch = [ float(row[0][4]), float(row[1][4]), float(row[2][4]) ]
            lattice.offset = [ float(row[0][5]), float(row[1][5]), float(row[2][5]) ]
            lattice.eoffset = [ float(row[0][6]), float(row[1][6]), float(row[2][6]) ]
            headers += 1
            continue

        if headers == 11:
            row = line.split()
            if len(row) != 7:
                raise RuntimeError("read_lattice: header line 11: "
                                   "expecting length 7 (found %s)",
                                   len(row))
            lattice.initialCurrent = float(row[0])
            lattice.initialEnergy = float(row[1])
            lattice.particleMass = float(row[2])
            lattice.initialCharge = float(row[3])
            lattice.scalingFreq = float(row[4])
            lattice.initialPhase = float(row[5])
            lattice.beamPercent = float(row[6])
            headers += 1
            continue

        row = [ float(r) for r in line.split()[:-1] ]

        kwargs = {}

        if element is not None:
            kwargs["name"] = element[0]
            element = None
        else:
            kwargs["name"] = ""

        elem = lattice.append(*row, **kwargs)

        if position is not None:
            position += row[0]
        else:
            position = row[0]

        elem.position = position

        if elem.itype == 0:
            elem.etype = "DRIFT"
        elif elem.itype == 1:
            elem.etype = "QUAD"
            elem.addfield("GRAD", "T/m", 4)
        elif elem.itype == 3:
            elem.etype = "SOL"
            elem.addfield("B", "T", 4)
        elif elem.itype == 4:
            elem.etype = "BEND" # DIPOLE
            elem.addfield("B", "T", 5)
        elif elem.itype == 5:
            # Element 5 is missing from the IMPACT documentation,
            # so the element format is provided below for reference.
            # L, ss, ms, 5, Gq(T/m), Gs(T/m^2),Go(T/m^3),Gd(T/m^4),Gdd(T/m^5),G14,G16,R
            elem.etype = "MULT" # MULTIPOLE
            elem.addfield("GRAD", "T/m", 4)
            elem.addfield("GSEXT", "T/m^2", 5)
            elem.addfield("GOCT", "T/m^3", 6)
        elif elem.itype == 103:
            elem.etype = "CAV"
            elem.addfield("AMP", "V", 4)
            elem.addfield("PHA", "deg", 6)
            lattice.files.add("rfdata{}".format(int(row[7])))
        elif elem.itype == 110:
            elem.etype = "CAV"
            elem.addfield("AMP", "V", 4)
            elem.addfield("PHA", "deg", 6)
            lattice.files.add("1T{}.T7".format(int(row[7])))
        elif elem.itype == -2:
            elem.etype = "MON"
        elif elem.itype == -11:
            elem.etype = "STRIP"
            lattice.files.add("fort.{}".format(int(row[2])))
        elif elem.itype == -13:
            elem.etype = "SLIT"
        elif elem.itype == -21:
            elem.etype = "COR"
            elem.addfield("ANGV", "rad", 4)
            elem.addfield("ANGH", "rad", 6)
        elif elem.itype == -25:
            elem.etype = "COR"
            elem.addfield("ANGV", "rad", 4)
            elem.addfield("ANGH", "rad", 6)
        elif elem.itype == -28:
            elem.etype = "MON"
        else:
            raise RuntimeError("read_lattice: Unsupported IMPACT type: {}".format(elem.itype))

    return lattice


class Lattice(object):
    """Describes the IMPACT lattice (test.in) including header and elements.

    :params integrator: integrator type (Linear Map or Lorentz)
    """
    def __init__(self, integrator=None):
        if integrator is not None:
            self.integrator = integrator
        else:
            self.integrator = _DEFAULT_INTEGRATOR
        self.comment = None
        self.nstates = _DEFAULT_NSTATES
        self.nparticles = _DEFAULT_NPARTICLES
        self.nprocessors = _DEFAULT_NPROCESSORS
        self.outputMode = _DEFAULT_OUTPUT_MODE
        self.ndimensions = _DEFAULT_NDIMENSIONS
        self.errorStudy = _DEFAULT_ERROR_STUDY
        self.meshSize = _DEFAULT_MESH_SIZE
        self.meshMode = _DEFAULT_MESH_MODE
        self.pipeSize = _DEFAULT_PIPE_SIZE
        self.periodSize = _DEFAULT_PERIOD_SIZE
        self.current = _DEFAULT_CURRENT
        self.charge = _DEFAULT_CHARGE
        self.distSigma = _DEFAULT_DIST_SIGMA
        self.distLambda = _DEFAULT_DIST_LAMBDA
        self.distMu = _DEFAULT_DIST_MU
        self.mismatch = _DEFAULT_MISMATCH
        self.emismatch = _DEFAULT_EMISMATCH
        self.offset = _DEFAULT_OFFSET
        self.eoffset = _DEFAULT_EOFFSET
        self.restart = _DEFAULT_RESTART
        self.subcycle = _DEFAULT_SUBCYCLE
        self.initialCurrent = _DEFAULT_INITIAL_CURRENT
        self.initialEnergy = _DEFAULT_INITIAL_ENERGY
        self.initialPhase = _DEFAULT_INITIAL_PHASE
        self.initialCharge = _DEFAULT_INITIAL_CHARGE
        self.particleMass = _DEFAULT_PARTICLE_MASS
        self.scalingFreq = _DEFAULT_SCALING_FREQ
        self.beamPercent = _DEFAULT_BEAM_PERCENT
        self.elements = []
        self.properties = []
        self.files = set()



    @property
    def nstates(self):
        return self._nstates

    @nstates.setter
    def nstates(self, nstates):
        if not isinstance(nstates, (int,float)):
            raise TypeError("LatticeFactory: 'nstates' property must be a number")
        self._nstates = int(nstates)


    @property
    def nparticles(self):
        return self._nparticles

    @nparticles.setter
    def nparticles(self, nparticles):
        if isinstance(nparticles, (int,float)):
            self._nparticles = int(nparticles)
        elif isinstance(nparticles, (list,tuple)):
            self._nparticles = []
            for p in nparticles:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'nparticles' must be a list of numbers")
                self._nparticles.append(int(p))
        else:
            raise TypeError("Lattice: 'nparticles' must be number or list")


    @property
    def nprocessors(self):
        return self._nprocessors

    @nprocessors.setter
    def nprocessors(self, nprocessors):
        if not isinstance(nprocessors, (int,float)):
            raise TypeError("LatticeFactory: 'nprocessors' property must be a number")
        self._nprocessors = int(nprocessors)


    @property
    def ndimensions(self):
        return self._ndimensions

    @ndimensions.setter
    def ndimensions(self, ndimensions):
        if  ndimensions not in [ NDIMENSIONS_6D ]:
            raise ValueError("Lattice: 'ndimensions' property must be a supported integer value")
        self._ndimensions = ndimensions


    @property
    def errorStudy(self):
        return self._errorStudy

    @errorStudy.setter
    def errorStudy(self, errorStudy):
        if errorStudy not in [ ERROR_STUDY_DISABLED, ERROR_STUDY_ENABLED ]:
            raise ValueError("Lattice: 'errorStudy' property must be a supported integer value")
        self._errorStudy = errorStudy


    @property
    def meshSize(self):
        return self._meshSize

    @meshSize.setter
    def meshSize(self, meshSize):
        if isinstance(meshSize, (int,float)):
            self._nparticles = [ int(meshSize) ] * 3
        if isinstance(meshSize, (list,tuple)):
            if len(meshSize) != 3:
                raise ValueError("Lattice: 'meshSize' property must have length 3")
            self._meshSize = []
            for m in meshSize:
                if not isinstance(m, (int,float)):
                    raise TypeError("Lattice: 'meshSize' property must be list of numbers")
                self._meshSize.append(int(m))
        else:
            raise TypeError("Lattice: 'meshSize' property must be number or list")


    @property
    def meshMode(self):
        return self._meshMode

    @meshMode.setter
    def meshMode(self, meshMode):
        if meshMode not in [ MESH_MODE_OPEN_OPEN, MESH_MODE_OPEN_PERIODIC,
                             MESH_MODE_FINITE_OPEN_RECT, MESH_MODE_FINITE_PERIODIC_RECT,
                             MESH_MODE_FINITE_OPEN_ROUND, MESH_MODE_FINITE_PERIODIC_ROUND ]:
            raise ValueError("Lattice: 'meshMode' property must be a supported integer value")
        self._meshMode = meshMode


    @property
    def pipeSize(self):
        return self._pipeSize


    @pipeSize.setter
    def pipeSize(self, pipeSize):
        if isinstance(pipeSize, (int,float)):
            self._pipeSize = [ float(pipeSize) ] * 2
        elif isinstance(pipeSize, (list,tuple)):
            if len(pipeSize) != 2:
                raise ValueError("Lattice: 'pipeSize' property must have length 2")
            self._pipeSize = []
            for p in pipeSize:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'pipeSize' must be a list of numbers")
                self._pipeSize.append(float(p))
        else:
            raise TypeError("Lattice: 'pipeSize' property must be number or list")


    @property
    def periodSize(self):
        return self._periodSize

    @periodSize.setter
    def periodSize(self, periodSize):
        if not isinstance(periodSize, (int,float)):
            raise TypeError("Lattice: 'periodSize' must be a number")
        self._periodSize = periodSize


    @property
    def outputMode(self):
        return self._outputMode

    @outputMode.setter
    def outputMode(self, outputMode):
        if outputMode not in [ OUTPUT_MODE_NONE, OUTPUT_MODE_STD, OUTPUT_MODE_DIAG, OUTPUT_MODE_END,
                                            OUTPUT_MODE_STD99, OUTPUT_MODE_DIAG99, OUTPUT_MODE_END99 ]:
            raise ValueError("Lattice: 'outputMode' property must be a supported integer value")
        self._outputMode = outputMode


    @property
    def inputMode(self):
        return self._inputMode

    @inputMode.setter
    def inputMode(self, inputMode):
        if inputMode not in [ INPUT_MODE_RECTANGLE_SINGLE, INPUT_MODE_GAUSSIAN_SINGLE, INPUT_MODE_WATERBAG_SINGLE,
                              INPUT_MODE_SEMIGAUSSIAN_SINGLE, INPUT_MODE_KV_UNIFORM_SINGLE, INPUT_MODE_EXTERNAL_FILE,
                              INPUT_MODE_GAUSSIAN_MULTI, INPUT_MODE_WATERBAG_MULTI ]:
            raise ValueError("Lattice: 'inputMode' property must be a supported integer value")
        self._inputMode = inputMode


    @property
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, integrator):
        if integrator not in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
            raise ValueError("Lattice: 'integrator' property must be a supported integer value")
        self._integrator = integrator


    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        if isinstance(current, (int,float)):
            self._current = float(current)
        elif isinstance(current, (list,tuple)):
            self._current = []
            for p in current:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'current' must be a list of numbers")
                self._current.append(float(p))
        else:
            raise TypeError("Lattice: 'current' must be number or list")


    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, charge):
        if isinstance(charge, (int,float)):
            self._charge = float(charge)
        elif isinstance(charge, (list,tuple)):
            self._charge = []
            for p in charge:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'charge' must be a list of numbers")
                self._charge.append(float(p))
        else:
            raise TypeError("Lattice: 'charge' must be number or list")


    @property
    def distSigma(self):
        return self._distSigma

    @distSigma.setter
    def distSigma(self, distSigma):
        if isinstance(distSigma, (int,float)):
            self._distSigma = [ float(distSigma) ] * 3
        elif isinstance(distSigma, (list,tuple)):
            if len(distSigma) != 3:
                raise ValueError("Lattice: 'distSigma' property must have length 3")
            self._distSigma = []
            for p in distSigma:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'distSigma' must be a list of numbers")
                self._distSigma.append(float(p))
        else:
            raise TypeError("Lattice: 'distSigma' must be number or list")


    @property
    def distLambda(self):
        return self._distLambda

    @distLambda.setter
    def distLambda(self, distLambda):
        if isinstance(distLambda, (int,float)):
            self._distLambda = [ float(distLambda) ] * 3
        elif isinstance(distLambda, (list,tuple)):
            if len(distLambda) != 3:
                raise ValueError("Lattice: 'distLambda' property must have length 3")
            self._distLambda = []
            for p in distLambda:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'distLambda' must be a list of numbers")
                self._distLambda.append(float(p))
        else:
            raise TypeError("Lattice: 'distLambda' must be number or list")


    @property
    def distMu(self):
        return self._distMu

    @distMu.setter
    def distMu(self, distMu):
        if isinstance(distMu, (int,float)):
            self._distMu = [ float(distMu) ] * 3
        elif isinstance(distMu, (list,tuple)):
            if len(distMu) != 3:
                raise ValueError("Lattice: 'distMu' property must have length 3")
            self._distMu = []
            for p in distMu:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'distMu' must be a list of numbers")
                self._distMu.append(float(p))
        else:
            raise TypeError("Lattice: 'distMu' must be number or list")


    @property
    def mismatch(self):
        return self._mismatch

    @mismatch.setter
    def mismatch(self, mismatch):
        if isinstance(mismatch, (int,float)):
            self._mismatch = [ float(mismatch) ] * 3
        elif isinstance(mismatch, (list,tuple)):
            if len(mismatch) != 3:
                raise ValueError("Lattice: 'mismatch' property must have length 3")
            self._mismatch = []
            for p in mismatch:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'mismatch' must be a list of numbers")
                self._mismatch.append(float(p))
        else:
            raise TypeError("Lattice: 'mismatch' must be number or list")


    @property
    def emismatch(self):
        return self._emismatch

    @emismatch.setter
    def emismatch(self, emismatch):
        if isinstance(emismatch, (int,float)):
            self._emismatch = [ float(emismatch) ] * 3
        elif isinstance(emismatch, (list,tuple)):
            if len(emismatch) != 3:
                raise ValueError("Lattice: 'emismatch' property must have length 3")
            self._emismatch = []
            for p in emismatch:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'emismatch' must be a list of numbers")
                self._emismatch.append(float(p))
        else:
            raise TypeError("Lattice: 'emismatch' must be number or list")


    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if isinstance(offset, (int,float)):
            self._offset = [ float(offset) ] * 3
        elif isinstance(offset, (list,tuple)):
            if len(offset) != 3:
                raise ValueError("Lattice: 'offset' property must have length 3")
            self._offset = []
            for p in offset:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'offset' must be a list of numbers")
                self._offset.append(float(p))
        else:
            raise TypeError("Lattice: 'offset' must be number or list")


    @property
    def eoffset(self):
        return self._eoffset

    @eoffset.setter
    def eoffset(self, eoffset):
        if isinstance(eoffset, (int,float)):
            self._eoffset = [ float(eoffset) ] * 3
        elif isinstance(eoffset, (list,tuple)):
            if len(eoffset) != 3:
                raise ValueError("Lattice: 'eoffset' property must have length 3")
            self._eoffset = []
            for p in eoffset:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'eoffset' must be a list of numbers")
                self._eoffset.append(float(p))
        else:
            raise TypeError("Lattice: 'eoffset' must be number or list")


    @property
    def restart(self):
        return self._restart

    @restart.setter
    def restart(self, restart):
        if restart not in [ RESTART_DISABLED, RESTART_ENABLED ]:
            raise ValueError("Lattice: 'restart' property must be a supported integer value")
        self._restart = restart


    @property
    def subcycle(self):
        return self._subcycle

    @subcycle.setter
    def subcycle(self, subcycle):
        if subcycle not in [ SUBCYCLE_DISABLED, SUBCYCLE_ENABLED ]:
            raise ValueError("Lattice: 'subcycle' property must be a supported integer value")
        self._subcycle = subcycle

    @property
    def initialCurrent(self):
        return self._initialCurrent

    @initialCurrent.setter
    def initialCurrent(self, initialCurrent):
        if not isinstance(initialCurrent, (int,float)):
            raise TypeError("Lattice: 'initialCurrent' must be a number")
        self._initialCurrent = initialCurrent


    @property
    def initialEnergy(self):
        return self._initialEnergy

    @initialEnergy.setter
    def initialEnergy(self, initialEnergy):
        if not isinstance(initialEnergy, (int,float)):
            raise TypeError("Lattice: 'initialEnergy' must be a number")
        self._initialEnergy = initialEnergy


    @property
    def initialPhase(self):
        return self._initialPhase

    @initialPhase.setter
    def initialPhase(self, initialPhase):
        if not isinstance(initialPhase, (int,float)):
            raise TypeError("Lattice: 'initialPhase' must be a number")
        self._initialPhase = initialPhase


    @property
    def particleMass(self):
        return self._particleMass

    @particleMass.setter
    def particleMass(self, particleMass):
        if not isinstance(particleMass, (int,float)):
            raise TypeError("Lattice: 'particleMass' must be a number")
        self._particleMass = particleMass


    @property
    def initialCharge(self):
        return self._initialCharge

    @initialCharge.setter
    def initialCharge(self, initialCharge):
        if not isinstance(initialCharge, (int,float)):
            raise TypeError("Lattice: 'initialCharge' must be a number")
        self._initialCharge = initialCharge


    @property
    def scalingFreq(self):
        return self._scalingFreq

    @scalingFreq.setter
    def scalingFreq(self, scalingFreq):
        if not isinstance(scalingFreq, (int,float)):
            raise TypeError("Lattice: 'scalingFreq' must be a number")
        self._scalingFreq = scalingFreq


    @property
    def beamPercent(self):
        return self._beamPercent

    @beamPercent.setter
    def beamPercent(self, beamPercent):
        if not isinstance(beamPercent, (int,float)):
            raise TypeError("Lattice: 'beamPercent' must be a number")
        self._beamPercent = beamPercent


    def append(self, length, steps, mapsteps, itype, *row, **kwargs):
        """
        Append an element to this lattice. See LatticeElement constructor for details.

        :return: LatticeElement object
        """
        kwargs["fields"] = [ LatticeField(*f) for f in kwargs.get("fields", []) ]
        element = LatticeElement(length, steps, mapsteps, itype, *row, **kwargs)
        self.elements.append(element)
        return element


    def write(self, stream=sys.stdout, mapstream=None, withElemData=False):
        """Write the IMPACT lattice stream (test.in) to the specified stream object.

        :param stream: file-like object to write lattice (test.in)
        :param mapstream: file-like object to write element map (test.map)
        :param withElemData: write element data as comments
        """

        def write_list(f, a):
            first = True
            for i in a:
                if first:
                    first = False
                else:
                    stream.write(" ")
                stream.write(f.format(i))
            stream.write("\r\n")

        if self.nstates == 1:
            if isinstance(self.nparticles, int):
                nparticles = self.nparticles
                ncsparticles = [ self.nparticles ]
            else:
                nparticles = self.nparticles[0]
                ncsparticles = [ self.nparticles[0] ]

            if isinstance(self.current, float):
                current = [ self.current ]
            else:
                current = [ self.current[0] ]

            if isinstance(self.charge, float):
                charge = [ self.charge ]
            else:
                charge = [ self.charge[0] ]

        else:
            if isinstance(self.nparticles, int):
                nparticles = self.nparticles * self.nstates
                ncsparticles = [ self.nparticles ] * self.nstates
            else:
                nparticles = sum(self.nparticles[:self.nstates])
                ncsparticles = list(self.nparticles[:self.nstates])

            if isinstance(self.current, float):
                current = [ self.current ] * self.nstates
            else:
                current = list(self.current[:self.nstates])

            if isinstance(self.charge, float):
                charge = [ self.charge ] * self.nstates
            else:
                charge = list(self.charge[:self.nstates])


        stream.write("!! Generated by PhysUtil - {}\r\n".format(datetime.now()))

        if self.comment != None:
            stream.write("!! {}\r\n".format(self.comment))

        stream.write("{lat.nprocessors} 1\r\n".format(lat=self))
        stream.write("{lat.ndimensions} {nparticles} {lat._integrator} {lat.errorStudy} {lat.outputMode}\r\n".format(lat=self, nparticles=nparticles))
        stream.write("{lat.meshSize[0]} {lat.meshSize[1]} {lat.meshSize[2]} {lat.meshMode} {lat.pipeSize[0]} {lat.pipeSize[1]} {lat.periodSize}\r\n".format(lat=self))
        stream.write("{lat.inputMode} {lat.restart} {lat.subcycle} {lat.nstates}\r\n".format(lat=self))

        write_list("{}", ncsparticles)
        write_list("{}", current)
        write_list("{}", charge)

        stream.write("{lat.distSigma[0]} {lat.distLambda[0]} {lat.distMu[0]} {lat.mismatch[0]} {lat.emismatch[0]} {lat.offset[0]} {lat.eoffset[0]}\r\n".format(lat=self))
        stream.write("{lat.distSigma[1]} {lat.distLambda[1]} {lat.distMu[1]} {lat.mismatch[1]} {lat.emismatch[1]} {lat.offset[1]} {lat.eoffset[1]}\r\n".format(lat=self))
        stream.write("{lat.distSigma[2]} {lat.distLambda[2]} {lat.distMu[2]} {lat.mismatch[2]} {lat.emismatch[2]} {lat.offset[2]} {lat.eoffset[2]}\r\n".format(lat=self))

        stream.write("{lat.initialCurrent} {lat.initialEnergy} {lat.particleMass} {lat.initialCharge} {lat.scalingFreq} {lat.initialPhase} {lat.beamPercent}\r\n".format(lat=self))

        # TODO: Option to compact lattice by merging drifts, etc.

        if self.outputMode in [1, 2]:
            if mapstream is not None:
                # First line of data file is initial
                # values before the first element.
                mapstream.write("NONE 0\r\n")

        for order, elem in enumerate(self.elements, start=1):
            if self.outputMode in [1, 2]:
                loop = elem.steps
                if elem.itype in [ -2, 4 ]:
                    # no output for these elements
                    loop = 0
                elif elem.itype < 0:
                    loop = elem.steps + 1
                if mapstream is not None:
                    for _ in range(loop):
                        mapstream.write("{0} {1}\r\n".format(elem.name, order))
            elif self.outputMode in [3, 4] and elem.itype == -28:
                if mapstream is not None:
                    mapstream.write("{0} {1}\r\n".format(elem.name, order))
            elif self.outputMode in [5, 6]:
                if mapstream is not None:
                    mapstream.write("{0} {1}\r\n".format(elem.name, order))
            elem.write(stream, withElemData)


class LatticeElement(object):
    """Describes an IMPACT lattice element (a row in the test.in file).

    :param length: element length
    :param steps: number of simulation steps
    :param mapsteps: number of sumulation map steps
    :param itype: the IMPACT numeric element type
    :param position: element position
    :param name: element name
    :param etype: element type
    :param fields: element fields
    """
    def __init__(self, length, steps, mapsteps, itype, *data, **kwargs):
        self._data = [ length, int(steps), int(mapsteps), int(itype) ]
        self._data.extend(data)
        self.name = kwargs.get("name", None)
        self.etype = kwargs.get("etype", None)
        self.position = kwargs.get("position", None)
        self.fields = kwargs.get("fields", [])


    @property
    def length(self):
        return self._data[0]

    @length.setter
    def length(self, length):
        self._data[0] = float(length)


    @property
    def steps(self):
        return self._data[1]

    @steps.setter
    def steps(self, steps):
        self.data[1] = int(steps)


    @property
    def itype(self):
        return self._data[3]

    @itype.setter
    def itype(self, itype):
        self._data[3] = int(itype)


    def getfield(self, name):
        for field in self.fields:
            if field.name == name:
                return self._data[field.index]
        raise KeyError("LatticeField with name '{}' not found".format(name))

    def setfield(self, name, value):
        for field in self.fields:
            if field.name == name:
                self._data[field.index] = value
                return
        raise KeyError("LatticeField with name '{}' not found".format(name))

    def addfield(self, name, unit, index):
        for field in self.fields:
            if field.name == name:
                field.unit = unit
                field.index = index
                return
        self.fields.append(LatticeField(name, unit, index))


    def write(self, stream, withElemData=False):
        if withElemData:
            fielddata = OrderedDict()
            for field in self.fields:
                if field.unit is None:
                    fielddata["{f.name}".format(f=field)] = field.index
                else:
                    fielddata["{f.name}[{f.unit}]".format(f=field)] = field.index
            stream.write("!!")
            json.dump([ self.name, self.etype, self.length, self.position, fielddata ], stream)
            stream.write("\r\n")

        stream.write(" ".join([str(x) for x in self._data]))
        stream.write(" /\r\n")


class LatticeField(object):
    """Describes a lattice element field with name, unit and index.

       :param name: field name (ie PHA, AMP)
       :param unit: field unit (ie deg, V)
       :param index: index of field in element data
    """
    def __init__(self, name, unit, index):
        self.name = name
        self.unit = unit
        self.index = index

    def __str__(self):
        return "{{ name={f.name}, unit={f.unit}, index={f.index}".format(f=self)


# configuration options

CONFIG_IMPACT_EXE_FILE = "impact_exe_file"
CONFIG_IMPACT_DATA_DIR = "impact_data_dir"

# default values

_DEFAULT_IMPACT_EXE = "impact"
_TEMP_DIRECTORY_SUFFIX = "_impact"


def run_lattice(lattice, **kwargs):
    """Convenience method to build result with specified configuration.

    :param lattice: IMPACT Lattice object
    :param config: machine configuration
    :param data_dir: path of directory containing IMPACT data files
    :param work_dir: path of directory for execution of IMPACT
    :return: working directory
    """
    lattice_runner = _LatticeRunner(lattice, **kwargs)
    return lattice_runner.run()


class _LatticeRunner(object):
    """A factory to run IMPACT and get the resulting model."""

    def __init__(self, lattice, **kwargs):
        """Initialzie the with the required IMPACT lattice.

        :param lattice: IMPACT Lattice object
        :param config: machine configuration
        :param data_dir: path of directory containing IMPACT data files
        :param work_dir: path of directory for execution of IMPACT
        """
        self.lattice = lattice

        self.config = kwargs.get("config")

        self.data_dir = kwargs.get("data_dir", None)
        self.work_dir = kwargs.get("work_dir", None)

    @property
    def lattice(self):
        return self._lattice

    @lattice.setter
    def lattice(self, lattice):
        if not isinstance(lattice, Lattice):
            raise TypeError("LatticeRunner: 'lattice' property much be type Lattice")
        self._lattice = lattice

    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if (data_dir != None) and not isinstance(data_dir, str):
            raise TypeError("LatticeRunner: 'data_dir' property much be type string or None")
        self._data_dir = data_dir

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir != None) and not isinstance(work_dir, str):
            raise TypeError("LatticeRunner: 'work_dir' property much be type string or None")
        self._work_dir = work_dir

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not isinstance(config, config.Configuration):
            raise TypeError("LatticeRunner: 'config' property must be type Configuration")
        self._config = config

    def _get_config_impact_exe(self):
        if self.config.has_default(CONFIG_IMPACT_EXE_FILE):
            impact_exe = self.config.get_default(CONFIG_IMPACT_EXE_FILE)
            return impact_exe

        return _DEFAULT_IMPACT_EXE

    def run(self):
        """Prepare working directory and execute IMPACT.
        """

        data_dir = self.data_dir
        if (data_dir == None) and self.config.has_default(CONFIG_IMPACT_DATA_DIR):
            data_dir = self.config.getabspath_default(CONFIG_IMPACT_DATA_DIR)

        if data_dir == None:
            raise RuntimeError("LatticeRunner: No data directory provided, check the configuration")

        work_dir = self.work_dir

        impact_exe = self._get_config_impact_exe()

        if not os.path.isdir(data_dir):
            raise RuntimeError("LatticeRunner: Data directory not found: {}".format(data_dir))

        if (work_dir != None) and os.path.isfile(work_dir):
            raise RuntimeError("LatticeRunner: Working directory must be a directory: {}".format(work_dir))

        if work_dir != None:
            if not os.path.exists(work_dir):
                os.makedirs(work_dir)
            rm_work_dir = False
        else:
            work_dir = tempfile.mkdtemp(_TEMP_DIRECTORY_SUFFIX)
            rm_work_dir = True

        _LOGGER.info("LatticeRunner: Working directory: %s", work_dir)

        if os.path.isabs(data_dir):
            abs_data_dir = data_dir
        else:
            abs_data_dir = os.path.abspath(data_dir)

        for datafile in os.listdir(abs_data_dir):
            srcpath = os.path.join(abs_data_dir, datafile)
            destpath = os.path.join(work_dir, datafile)
            if os.path.isfile(os.path.join(abs_data_dir, datafile)):
                if not os.path.exists(destpath):
                    os.symlink(srcpath, destpath)
                    _LOGGER.debug("LatticeRunner: Link data file %s to %s", srcpath, destpath)

        try:
            with open(os.path.join(work_dir, "test.in"), "w") as fp:
                with open(os.path.join(work_dir, "model.map"), "w") as mapfp:
                    self._lattice.write(fp, mapstream=mapfp)
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

        return work_dir

    @staticmethod
    def _remove_work_dir(work_dir, rm_work_dir):
        """Cleanup the working directory.
        """
        if rm_work_dir:
            _LOGGER.debug("LatticeRunner: Cleanup: remove work directory")
            shutil.rmtree(work_dir)

