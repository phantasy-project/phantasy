# encoding: UTF-8

"""Library for generating IMPACT lattice file (test.in) from Accelerator Design Description."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import os.path, logging, json, sys

from datetime import datetime

from .. import cfg

from ..layout.accel import Element, DriftElement, ValveElement, PortElement
from ..layout.accel import SeqElement, CavityElement, SolCorrElement, ChgStripElement
from ..layout.accel import CorrElement, BendElement, QuadElement, HexElement
from ..layout.accel import BCMElement, PMElement, BLElement, BLMElement, BPMElement


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

# Constants used for IMPACT header parameters

INTEGRATOR_LINEAR = 1

INTEGRATOR_LORENTZ = 2

OUTPUT_MODE_NONE = 0

OUTPUT_MODE_STD = 1

OUTPUT_MODE_DIAG = 3

OUTPUT_MODE_END = 5

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


_LOGGER = logging.getLogger(__name__)


def build_lattice(accel, settings=None, start=None, end=None,  template=False):
    """Convenience method for building the IMPACT lattice."""

    lattice_factory = LatticeFactory(accel)

    if settings != None:
        lattice_factory.settings = settings

    if start != None:
        lattice_factory.start = start

    if end != None:
        lattice_factory.end = end

    if template == True:
        lattice_factory.template = template

    return lattice_factory.build()


class LatticeFactory(object):
    """LatticeFactory class builds an IMPACT lattice
       object from an Accelerator Design Description.
    """

    def __init__(self, accel):
        self.accel = accel
        self.nstates = None
        self.nparticles = None
        self.nprocessors = None
        self.integrator = None
        self.ndimensions = None
        self.errorStudy = None
        self.meshMode = None
        self.meshSize = None
        self.pipeSize = None
        self.periodSize = None
        self.outputMode = None
        self.inputMode = None
        self.current = None
        self.charge = None
        self.distSigma = None
        self.distLambda = None
        self.distMu = None
        self.mismatch = None
        self.emismatch = None
        self.offset = None
        self.eoffset = None
        self.settings = None
        self.start = None
        self.end = None
        self.template = False


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
        if (start != None) and not isinstance(start, basestring):
            raise TypeError("LatticeFactory: 'start' property must be type string or None")
        self._start = start


    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end != None) and not isinstance(end, basestring):
            raise TypeError("LatticeFactory: 'end' property must be type string or None")
        self._end = end


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if (settings != None) and not isinstance(settings, (dict)):
            raise TypeError("LatticeFactory: 'settings' property must be type string or None")
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
        if cfg.config.has_option(dtype, CONFIG_IMPACT_TYPE, False):
            return cfg.config.getint(dtype, CONFIG_IMPACT_TYPE, False)

        return default


    def _get_config_integrator_input_id(self, dtype, integrator):
        if (integrator == INTEGRATOR_LINEAR):
            if cfg.config.has_option(dtype, CONFIG_IMPACT_LINEAR_INPUT_ID, False):
                return cfg.config.getint(dtype, CONFIG_IMPACT_LINEAR_INPUT_ID, False)

        if (integrator == INTEGRATOR_LORENTZ):
            if cfg.config.has_option(dtype, CONFIG_IMPACT_LORENTZ_INPUT_ID, False):
                return cfg.config.getint(dtype, CONFIG_IMPACT_LORENTZ_INPUT_ID, False)

        return None


    def _get_config_t7data_input_id(self, dtype):
        if cfg.config.has_option(dtype, CONFIG_IMPACT_T7DATA_INPUT_ID, False):
            return cfg.config.getint(dtype, CONFIG_IMPACT_T7DATA_INPUT_ID, False)

        return None


    def _get_config_strip_input_id(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_IMPACT_STRIP_INPUT_ID, False):
            return cfg.config.getint(elem.name, CONFIG_IMPACT_STRIP_INPUT_ID, False)

        if cfg.config.has_option(elem.dtype, CONFIG_IMPACT_STRIP_INPUT_ID, False):
            return cfg.config.getint(elem.dtype, CONFIG_IMPACT_STRIP_INPUT_ID, False)

        return None


    def _get_config_nstates(self):
        if cfg.config.has_default(CONFIG_IMPACT_NSTATES):
            nstates = cfg.config.getint_default(CONFIG_IMPACT_NSTATES)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_NSTATES, nstates)
            return nstates

        return _DEFAULT_NSTATES


    def _get_config_nparticles(self):
        if cfg.config.has_default(CONFIG_IMPACT_NPARTICLES):
            nparticles = cfg.config.get_default(CONFIG_IMPACT_NPARTICLES)
            splitNParticles = nparticles.split()
            if len(splitNParticles) > 1:
                nparticles = []
                for m in splitNParticles:
                    nparticles.append(float(m))
            else:
                nparticles = float(splitNParticles[0])
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_NPARTICLES, nparticles)
            return nparticles

        return _DEFAULT_NPARTICLES


    def _get_config_nprocessors(self):
        if cfg.config.has_default(CONFIG_IMPACT_NPROCESSORS):
            nprocessors = cfg.config.getint_default(CONFIG_IMPACT_NPROCESSORS)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_NPROCESSORS, nprocessors)
            return nprocessors

        return _DEFAULT_NPROCESSORS


    def _get_config_integrator(self):
        if cfg.config.has_default(CONFIG_IMPACT_INTEGRATOR):
            integrator = cfg.config.getint_default(CONFIG_IMPACT_INTEGRATOR)
            if integrator in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
                return integrator

        return _DEFAULT_INTEGRATOR


    def _get_config_ndimensions(self):
        if cfg.config.has_default(CONFIG_IMPACT_NDIMENSIONS):
            ndimensions = cfg.config.getint_default(CONFIG_IMPACT_NDIMENSIONS)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_NDIMENSIONS, ndimensions)
            return ndimensions

        return _DEFAULT_NDIMENSIONS

    def _get_config_error_study(self):
        if cfg.config.has_default(CONFIG_IMPACT_ERROR_STUDY):
            errorStudy =  cfg.config.getint_default(CONFIG_IMPACT_ERROR_STUDY)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_ERROR_STUDY, errorStudy)
            return errorStudy

        return _DEFAULT_ERROR_STUDY


    def _get_config_mesh_mode(self):
        if cfg.config.has_default(CONFIG_IMPACT_MESH_MODE):
            meshMode = cfg.config.getint_default(CONFIG_IMPACT_MESH_MODE)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_MESH_MODE, meshMode)
            return meshMode

        return _DEFAULT_MESH_MODE


    def _get_config_mesh_size(self):
        if cfg.config.has_default(CONFIG_IMPACT_MESH_SIZE):
            meshSize = cfg.config.get_default(CONFIG_IMPACT_MESH_SIZE)
            splitMeshSize = meshSize.split()
            if len(splitMeshSize) > 1:
                meshSize = []
                for m in splitMeshSize:
                    meshSize.append(float(m))
            else:
                meshSize = float(splitMeshSize[0])
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_MESH_SIZE, meshSize)
            return meshSize

        return _DEFAULT_MESH_SIZE


    def _get_config_pipe_size(self):
        if cfg.config.has_default(CONFIG_IMPACT_PIPE_SIZE):
            pipeSize = cfg.config.get_default(CONFIG_IMPACT_PIPE_SIZE)
            splitPipeSize = pipeSize.split()
            if len(splitPipeSize) > 1:
                pipeSize = []
                for m in splitPipeSize:
                    pipeSize.append(float(m))
            else:
                pipeSize = float(splitPipeSize[0])
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_PIPE_SIZE, pipeSize)
            return pipeSize

        return _DEFAULT_PIPE_SIZE


    def _get_config_period_size(self):
        if cfg.config.has_default(CONFIG_IMPACT_PERIOD_SIZE):
            periodSize = cfg.config.getfloat_default(CONFIG_IMPACT_PERIOD_SIZE)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_PERIOD_SIZE, periodSize)
            return periodSize

        return _DEFAULT_PERIOD_SIZE


    def _get_config_output_mode(self):
        if cfg.config.has_default(CONFIG_IMPACT_OUTPUT_MODE):
            outputMode = cfg.config.getint_default(CONFIG_IMPACT_OUTPUT_MODE)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_OUTPUT_MODE, outputMode)
            return outputMode

        return _DEFAULT_OUTPUT_MODE


    def _get_config_input_mode(self):
        if cfg.config.has_default(CONFIG_IMPACT_INPUT_MODE):
            inputMode = cfg.config.getint_default(CONFIG_IMPACT_INPUT_MODE)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_INPUT_MODE, inputMode)
            return inputMode

        return _DEFAULT_INPUT_MODE


    def _get_config_current(self):
        if cfg.config.has_default(CONFIG_IMPACT_CURRENT):
            current = cfg.config.get_default(CONFIG_IMPACT_CURRENT)
            splitCurrent = current.split()
            if len(splitCurrent) > 1:
                current = []
                for m in splitCurrent:
                    current.append(float(m))
            else:
                current = float(splitCurrent[0])
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_CURRENT, current)
            return current

        return _DEFAULT_CURRENT


    def _get_config_charge(self):
        if cfg.config.has_default(CONFIG_IMPACT_CHARGE):
            charge = cfg.config.get_default(CONFIG_IMPACT_CHARGE)
            splitCharge = charge.split()
            if len(splitCharge) > 1:
                charge = []
                for m in splitCharge:
                    charge.append(float(m))
            else:
                charge = float(splitCharge[0])
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_CHARGE, charge)
            return charge

        return _DEFAULT_CHARGE


    def _get_config_dist_sigma(self):
        if cfg.config.has_default(CONFIG_IMPACT_DIST_SIGMA):
            sigma = cfg.config.getarray_default(CONFIG_IMPACT_DIST_SIGMA, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_DIST_SIGMA, sigma)
            return sigma

        return _DEFAULT_DIST_SIGMA


    def _get_config_dist_lambda(self):
        if cfg.config.has_default(CONFIG_IMPACT_DIST_LAMBDA):
            lambda_ = cfg.config.getarray_default(CONFIG_IMPACT_DIST_LAMBDA, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_DIST_LAMBDA, lambda_)
            return lambda_

        return _DEFAULT_DIST_LAMBDA


    def _get_config_dist_mu(self):
        if cfg.config.has_default(CONFIG_IMPACT_DIST_MU):
            mu = cfg.config.getarray_default(CONFIG_IMPACT_DIST_MU, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_DIST_MU, mu)
            return mu

        return _DEFAULT_DIST_MU


    def _get_config_dist_mismatch(self):
        if cfg.config.has_default(CONFIG_IMPACT_MISMATCH):
            value = cfg.config.getarray_default(CONFIG_IMPACT_MISMATCH, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_MISMATCH, value)
            return value

        return _DEFAULT_MISMATCH


    def _get_config_dist_emismatch(self):
        if cfg.config.has_default(CONFIG_IMPACT_EMISMATCH):
            value = cfg.config.getarray_default(CONFIG_IMPACT_EMISMATCH, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_EMISMATCH, value)
            return value

        return _DEFAULT_EMISMATCH


    def _get_config_dist_offset(self):
        if cfg.config.has_default(CONFIG_IMPACT_OFFSET):
            value = cfg.config.getarray_default(CONFIG_IMPACT_OFFSET, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_OFFSET, value)
            return value

        return _DEFAULT_OFFSET


    def _get_config_dist_eoffset(self):
        if cfg.config.has_default(CONFIG_IMPACT_EOFFSET):
            value = cfg.config.getarray_default(CONFIG_IMPACT_EOFFSET, conv=float)
            _LOGGER.info("LatticeFactory: %s found in configuration: %s", CONFIG_IMPACT_EOFFSET, value)
            return value

        return _DEFAULT_EOFFSET


    def _get_config_settings(self):
        if cfg.config.has_default("settings_file"):
            stgpath = cfg.config.get_default("settings_file")
            if not os.path.isabs(stgpath) and (cfg.config_path != None):
                stgpath = os.path.abspath(os.path.join(os.path.dirname(cfg.config_path), stgpath))
            with open(stgpath, "r") as stgfile:
                return json.load(stgfile)

        return None


    def _get_config_steps(self, dtype=None):
        if (dtype == None) and cfg.config.has_default(CONFIG_IMPACT_STEPS):
            return cfg.config.getint_default(CONFIG_IMPACT_STEPS)

        if (dtype != None) and cfg.config.has_option(dtype, CONFIG_IMPACT_STEPS):
            return cfg.config.getint(dtype, CONFIG_IMPACT_STEPS)

        return _DEFAULT_STEPS


    def _get_config_mapsteps(self, dtype=None):
        if (dtype == None) and cfg.config.has_default(CONFIG_IMPACT_MAPSTEPS):
            return cfg.config.getint_default(CONFIG_IMPACT_MAPSTEPS)

        if (dtype != None) and cfg.config.has_option(dtype, CONFIG_IMPACT_MAPSTEPS):
            return cfg.config.getint(dtype, CONFIG_IMPACT_MAPSTEPS)

        return _DEFAULT_MAPSTEPS



    def build(self):

        settings = None
        if self.template == False:
            settings = self.settings
            if settings == None:
                settings = self._get_config_settings()

        integrator = self.integrator
        if integrator == None:
            integrator = self._get_config_integrator()

        lattice = Lattice(integrator)

        if self.nstates != None:
            lattice.nstates = self.nstates
        else:
            lattice.nstates = self._get_config_nstates()

        if self.nparticles != None:
            lattice.nparticles = self.nparticles
        else:
            lattice.nparticles = self._get_config_nparticles()

        if self.nprocessors != None:
            lattice.nprocessors = self.nprocessors
        else:
            lattice.nprocessors = self._get_config_nprocessors()

        if self.ndimensions != None:
            lattice.ndimensions = self.ndimensions
        else:
            lattice.ndimensions = self._get_config_ndimensions()

        if self.errorStudy != None:
            lattice.errorStudy = self.errorStudy
        else:
            lattice.errorStudy = self._get_config_error_study()

        if self.meshMode != None:
            lattice.meshMode = self.meshMode
        else:
            lattice.meshMode = self._get_config_mesh_mode()

        if  self.meshSize != None:
            lattice.meshSize = self.meshSize
        else:
            lattice.meshSize = self._get_config_mesh_size()

        if self.pipeSize != None:
            lattice.pipeSize = self.pipeSize
        else:
            lattice.pipeSize = self._get_config_pipe_size()

        if self.periodSize != None:
            lattice.periodSize = self.periodSize
        else:
            lattice.periodSize = self._get_config_period_size()

        if self.outputMode != None:
            lattice.outputMode = self.outputMode
        else:
            lattice.outputMode = self._get_config_output_mode()

        if self.inputMode != None:
            lattice.inputMode = self.inputMode
        else:
            lattice.inputMode = self._get_config_input_mode()

        if self.current != None:
            lattice.current = self.current
        else:
            lattice.current = self._get_config_current()

        if self.charge != None:
            lattice.charge = self.charge
        else:
            lattice.charge = self._get_config_charge()

        if self.distSigma != None:
            lattice.distSigma = self.distSigma
        else:
            lattice.distSigma = self._get_config_dist_sigma()

        if self.distLambda != None:
            lattice.distLambda = self.distLambda
        else:
            lattice.distLambda = self._get_config_dist_lambda()

        if self.distMu != None:
            lattice.distMu = self.distMu
        else:
            lattice.distMu = self._get_config_dist_mu()

        if self.mismatch != None:
            lattice.mismatch = self.mismatch
        else:
            lattice.mismatch = self._get_config_dist_mismatch()

        if self.emismatch != None:
            lattice.emismatch = self.emismatch
        else:
            lattice.emismatch = self._get_config_dist_emismatch()

        if self.offset != None:
            lattice.offset = self.offset
        else:
            lattice.offset = self._get_config_dist_offset()

        if self.eoffset != None:
            lattice.eoffset = self.eoffset
        else:
            lattice.eoffset = self._get_config_dist_eoffset()


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
                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, ValveElement):
                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="VALVE")

            elif isinstance(elem, PortElement):
                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="PORT")

            elif isinstance(elem, CavityElement):
                phase = 0.0
                if settings != None:
                    if elem.channels.phase_cset in settings:
                        phase = settings[elem.channels.phase_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.phase_cset, elem.name))

                amplitude = 0.0
                if settings != None:
                    if elem.channels.amplitude_cset in settings:
                        amplitude = settings[elem.channels.amplitude_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.amplitude_cset, elem.name))

                itype = self._get_config_type(elem.dtype, 103)
                if itype == 103:
                    input_id = self._get_config_integrator_input_id(elem.dtype, integrator)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                    lattice.addProperty("AMP", "V")
                    lattice.addProperty("PHA", "deg")

                    lattice.append("{length} {steps} {mapsteps} {itype} {properties[AMP]} "+str(elem.frequency)+" {properties[PHA]} "+str(input_id)+" {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=103, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="CAV",
                                    properties={ "AMP":amplitude, "PHA":phase })
                elif itype == 110:
                    input_id = self._get_config_t7data_input_id(elem.dtype)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                    lattice.addProperty("AMP", "V")
                    lattice.addProperty("PHA", "deg")

                    lattice.append("{length} {steps} {mapsteps} {itype} {properties[AMP]} "+str(elem.frequency)+" {properties[PHA]} "+str(input_id)+" {radius} {radius} 0 0 0 0 0 1 2",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=110, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="CAV",
                                    properties={ "AMP":amplitude, "PHA":phase })

                else:
                    raise RuntimeError("LatticeFactory: IMPACT element type for '{}' not supported: {}".format(elem.name, itype))

            elif isinstance(elem, SolCorrElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                hkick = 0.0
                if settings != None:
                    if elem.channels.hkick_cset in settings:
                        hkick = settings[elem.channels.hkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.hkick_cset, elem.name))

                vkick = 0.0
                if settings != None:
                    if elem.channels.vkick_cset in settings:
                        vkick = settings[elem.channels.vkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.vkick_cset, elem.name))


                lattice.addProperty("B", "T")

                lattice.append("{length} {steps} {mapsteps} {itype} {properties[B]} 0 {radius}",
                                    length=elem.length/2.0, steps=steps/2, mapsteps=mapsteps, itype=3, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name=elem.name, etype="SOL", properties={ "B":field })

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 {properties[ANG]} 0.0 0.0 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem), etype="HCOR", properties={ "ANG":hkick })

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 0.0 0.0 {properties[ANG]} 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem), etype="VCOR", properties={ "ANG":vkick })

                lattice.append("{length} {steps} {mapsteps} {itype} {properties[B]} 0 {radius}",
                                    length=elem.length/2.0, steps=steps/2, mapsteps=mapsteps, itype=3, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="SOL", properties={ "B":field })


            elif isinstance(elem, QuadElement):
                gradient = 0.0
                if settings != None:
                    if elem.channels.gradient_cset in settings:
                        gradient = settings[elem.channels.gradient_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' not found for element: {}".format(elem.channels.gradient_cset, elem.name))

                lattice.addProperty("GRAD", "T/m")

                lattice.append("{length} {steps} {mapsteps} {itype} {properties[GRAD]} 0 {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=1, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="QUAD", properties={ "GRAD":gradient })


            elif isinstance(elem, CorrElement):
                hkick = 0.0
                if settings != None:
                    if elem.channels.hkick_cset in settings:
                        hkick = settings[elem.channels.hkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.hkick_cset, elem.name))

                vkick = 0.0
                if settings != None:
                    if elem.channels.vkick_cset in settings:
                        vkick = settings[elem.channels.vkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.vkick_cset, elem.name))

                lattice.addProperty("ANG", "rad")

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 {properties[ANG]} 0.0 0.0 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem), etype="HCOR", properties={ "ANG":hkick })

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 0.0 0.0 {properties[ANG]} 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem), etype="VCOR", properties={ "ANG":vkick })

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")


            elif isinstance(elem, HexElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                ## IMPACT element 5 is not currently document. Below is provided for reference.
                ## L, ss, ms, 5, Gq(T/m), Gs(T/m^2),Go(T/m^3),Gd(T/m^4),Gdd(T/m^5),G14,G16,R
                #lattice.append("{length} {steps} {mapsteps} {itype} 0.0 {properties[B]} 0.0 0.0 0.0 0.0 0.0 {radius}",
                #                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=5, radius=elem.apertureX/2.0,
                #                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="SEXT", properties={ "B":field })

                if field != 0.0:
                    _LOGGER.warning("LatticeFactory: Hexapole magnet element support not implemented. Ignoring field: %s T/m^2", field)

                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, BendElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                if steps < 3:
                    raise RuntimeError("LatticeFactory: '{}' number of steps must be greater than 2.".format(elem.name))

                lattice.addProperty("B", "T")

                lattice.append("{length} {steps} {mapsteps} {itype} "+str(elem.angle/steps)+" {properties[B]} 400 {radius} "+str(elem.entrAngle)+" "+str(elem.exitAngle)+" 0.0 0.0 0.0",
                                    length=elem.length/steps, steps=1, mapsteps=mapsteps, itype=4, radius=elem.apertureX/2.0,
                                    position=elem.z-(elem.length/2.0)+(elem.length/steps)-poffset,
                                    name=elem.name, etype="BEND", properties={ "B":field })

                for i in xrange(2, steps):
                    lattice.append("{length} {steps} {mapsteps} {itype} "+str(elem.angle/steps)+" {properties[B]} 500 {radius} 0.0 0.0 0.0 0.0 0.0",
                                    length=elem.length/steps, steps=1, mapsteps=mapsteps, itype=4, radius=elem.apertureX/2.0,
                                    position=elem.z-(elem.length/2.0)+i*(elem.length/steps)-poffset,
                                    name=elem.name, etype="BEND", properties={ "B":field })

                lattice.append("{length} {steps} {mapsteps} {itype} "+str(elem.angle/steps)+" {properties[B]} 600 {radius} "+str(elem.entrAngle)+" "+str(elem.exitAngle)+" 0.0 0.0 0.0",
                                    length=elem.length/steps, steps=1, mapsteps=mapsteps, itype=4, radius=elem.apertureX/2.0,
                                    position=elem.z-(elem.length/2.0)+(elem.length/steps)-poffset,
                                    name=elem.name, etype="BEND", properties={ "B":field })

            elif isinstance(elem, (ChgStripElement)):
                input_id = self._get_config_strip_input_id(elem)
                if input_id == None:
                    raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                lattice.append("{length} 0 "+str(input_id)+" {itype} 0 0", length=0.0, itype=-11, position=elem.z-poffset, name=elem.name, etype="STRIP")

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, (BPMElement, PMElement)):
                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                if isinstance(elem, BPMElement):
                    etype = "BPM"
                else:
                    etype = "PM"

                lattice.append("0 0 0 {itype}", length=0.0, itype=-28, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name=elem.name, etype=etype)

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            else:
                raise Exception("Unsupport ADD element: {}".format(elem))

        return lattice



class Lattice(object):
    """Describes the IMPACT lattice (test.in) including header and elements.

    :params integrator: integrator type (Linear Map or Lorentz)
    """
    def __init__(self, integrator):
        if integrator not in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
            raise ValueError("Lattice: 'integrator' property must be a supported integer value")
        self._integrator = integrator

        self.comment = None
        self.nstates = _DEFAULT_NSTATES
        self.nparticles = _DEFAULT_NPARTICLES
        self.nprocessors = _DEFAULT_NPROCESSORS
        self.outputMode = _DEFAULT_OUTPUT_MODE
        self.ndimensions = _DEFAULT_NDIMENSIONS
        self.errorStudy = _DEFAULT_ERROR_STUDY
        self._meshSize = _DEFAULT_MESH_SIZE
        self._meshMode = _DEFAULT_MESH_MODE
        self._pipeSize = _DEFAULT_PIPE_SIZE
        self._periodSize = _DEFAULT_PERIOD_SIZE
        self._current = _DEFAULT_CURRENT
        self._charge = _DEFAULT_CHARGE
        self.distSigma = _DEFAULT_DIST_SIGMA
        self.distLambda = _DEFAULT_DIST_LAMBDA
        self.distMu = _DEFAULT_DIST_MU
        self.mismatch = _DEFAULT_MISMATCH
        self.emismatch = _DEFAULT_EMISMATCH
        self.offset = _DEFAULT_OFFSET
        self.eoffset = _DEFAULT_EOFFSET
        self.elements = []
        self.properties = []



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
            raise TypeError("Lattice: 'nparticles' must be integer or list")


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
        if not isinstance(meshSize, (list,tuple)):
            raise TypeError("Lattice: 'meshSize' property must be list or tuple")
        if len(meshSize) != 3:
            raise ValueError("Lattice: 'meshSize' property must have length 3")
        for m in meshSize:
            if not isinstance(m, (int,float)):
                raise TypeError("Lattice: 'meshSize' property must be list of numbers")
        self._meshSize = [ int(meshSize[0]), int(meshSize[1]), int(meshSize[2]) ]


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
            self._pipeSize = [ pipeSize, pipeSize ]
        elif isinstance(pipeSize, (list,tuple)):
            if len(pipeSize) != 2:
                raise ValueError("Lattice: 'pipeSize' property must have length 2")
            for p in pipeSize:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'pipeSize' must be a list of numbers")
            self._pipeSize = [ float(pipeSize[0]), float(pipeSize[1]) ]


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
        if outputMode not in [ OUTPUT_MODE_NONE, OUTPUT_MODE_STD, OUTPUT_MODE_DIAG, OUTPUT_MODE_END ]:
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
            for p in distSigma:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'distSigma' must be a list of numbers")
            self._distSigma = [ float(distSigma[0]), float(distSigma[1]), float(distSigma[2]) ]
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
            for p in distLambda:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'distLambda' must be a list of numbers")
            self._distLambda = [ float(distLambda[0]), float(distLambda[1]), float(distLambda[2]) ]
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
            for p in distMu:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'distMu' must be a list of numbers")
            self._distMu = [ float(distMu[0]), float(distMu[1]), float(distMu[2]) ]
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
            for p in mismatch:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'mismatch' must be a list of numbers")
            self._mismatch = [ float(mismatch[0]), float(mismatch[1]), float(mismatch[2]) ]
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
            for p in emismatch:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'emismatch' must be a list of numbers")
            self._emismatch = [ float(emismatch[0]), float(emismatch[1]), float(emismatch[2]) ]
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
            for p in offset:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'offset' must be a list of numbers")
            self._offset = [ float(offset[0]), float(offset[1]), float(offset[2]) ]
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
            for p in eoffset:
                if not isinstance(p, (int,float)):
                    raise TypeError("Lattice: 'eoffset' must be a list of numbers")
            self._eoffset = [ float(eoffset[0]), float(eoffset[1]), float(eoffset[2]) ]
        else:
            raise TypeError("Lattice: 'eoffset' must be number or list")


    def append(self, elemformat, length=0.0, steps=0, mapsteps=0, itype=0, radius=0.0, position=0.0, name=None, etype=None, properties={}):
        self.elements.append(LatticeElement(elemformat, length, steps, mapsteps, itype, radius, position, name, etype, properties))


    def addProperty(self, name, units):
        for prop in self.properties:
            if prop.name == name:
                if prop.units == units:
                    return # Proprty has already added, and it has the same units so nothing needed to be done.
                else:
                    raise RuntimeError("Lattice: Error adding property: '{}': Units not match: '{}' vs '{}'".format(name, units, prop.units))

        self.properties.append(LatticeProperty(name, units))


    def write(self, file=sys.stdout):
        """Write the IMPACT lattice file (test.in) to the specified file object.

        :param file: file-like object to write lattice (test.in)
        """

        def write_list(f, a):
            first = True
            for i in a:
                if first:
                    first = False
                else:
                    file.write(" ")
                file.write(f.format(i))
            file.write("\r\n")

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


        file.write("!! Generated by PhysUtil - {}\r\n".format(datetime.now()))

        if self.comment != None:
            file.write("!! {}\r\n".format(self.comment))

        file.write("{lat.nprocessors} 1\r\n".format(lat=self))
        file.write("{lat.ndimensions} {nparticles} {lat._integrator} {lat.errorStudy} {lat.outputMode}\r\n".format(lat=self, nparticles=nparticles))
        file.write("{lat.meshSize[0]} {lat.meshSize[1]} {lat.meshSize[2]} {lat.meshMode} {lat.pipeSize[0]} {lat.pipeSize[1]} {lat.periodSize}\r\n".format(lat=self))
        file.write("{lat.inputMode} 0 0 {lat.nstates}\r\n".format(lat=self))

        write_list("{}", ncsparticles)
        write_list("{}", current)
        write_list("{}", charge)

        file.write("{lat.distSigma[0]} {lat.distLambda[0]} {lat.distMu[0]} {lat.mismatch[0]} {lat.emismatch[0]} {lat.offset[0]} {lat.eoffset[0]}\r\n".format(lat=self))
        file.write("{lat.distSigma[1]} {lat.distLambda[1]} {lat.distMu[1]} {lat.mismatch[1]} {lat.emismatch[1]} {lat.offset[1]} {lat.eoffset[1]}\r\n".format(lat=self))
        file.write("{lat.distSigma[2]} {lat.distLambda[2]} {lat.distMu[2]} {lat.mismatch[2]} {lat.emismatch[2]} {lat.offset[2]} {lat.eoffset[2]}\r\n".format(lat=self))

        file.write("0.0 0.5e6 931.49432e6 0.1386554621848 80.50e6 0.0 99.9\r\n")

        # TODO: Option to compact lattice by merging drifts, etc.

        for elem in self.elements:
            file.write(str(elem))
            file.write(" /\r\n")



class LatticeElement(object):
    """Describes an IMPACT lattice element (a row in the test.in file).

    :param elemformat: a python format string
    :param length: element length
    :param steps: number of simulation steps
    :param mapsteps: number of sumulation map steps
    :param itype: the IMPACT numeric element type
    :param radius: element radius
    :param position: element position
    :param name: element name
    :param etype: element type
    :param properties: element property values
    """

    def __init__(self, elemformat, length=0.0, steps=4, mapsteps=20, itype=0, radius=0.0, position=0.0, name=None, etype=None, properties={}):
        self.elemformat = elemformat
        self.length = length
        self.steps = steps
        self.mapsteps = mapsteps
        self.itype = itype
        self.position = position
        self.radius = radius
        self.name = name
        self.etype = etype
        self.properties = properties


    def __str__(self):
        return self.elemformat.format(length=self.length, steps=self.steps, mapsteps=self.mapsteps,
                                        itype=self.itype, radius=self.radius, position=self.position, properties=self.properties)




class LatticeProperty(object):
    """Describes a property of a lattice elements such as field or angle.

    :param name: the property name
    :param units: the physical units
    """
    def __init__(self, name, units):
        self.name = name
        self.units = units


    def __str__(self):
        return "{{ name='{prop.name}', units='{prop.units}' }}".format(prop=self)

