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

from phantasy.library.parser import Configuration
from phantasy.library.layout import DriftElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BCMElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import EBendElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import FCElement
from phantasy.library.layout import VDElement
from phantasy.library.layout import EMSElement
from phantasy.library.layout import ElectrodeElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import ApertureElement
from phantasy.library.layout import AttenuatorElement
from phantasy.library.layout import SlitElement
from phantasy.library.layout import DumpElement
from phantasy.library.layout import ChopperElement
from phantasy.library.settings import Settings

try:
    basestring
except NameError:
    basestring = str

CONFIG_FLAME_SIM_TYPE = "flame_sim_type"
CONFIG_FLAME_CAV_TYPE = "flame_cav_type"
CONFIG_FLAME_CAV_CONF = "flame_cav_conf"
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
CONFIG_FLAME_EQUAD_RADIUS = "flame_radius"
CONFIG_FLAME_EBEND_PHI = "flame_phi"
CONFIG_FLAME_EBEND_FRINGEX = 'flame_fringe_x'
CONFIG_FLAME_EBEND_FRINGEY = 'flame_fringe_y'
CONFIG_FLAME_EBEND_VERBOOL = 'flame_ver'
CONFIG_FLAME_EBEND_SPHERBOOL = 'flame_spher'
CONFIG_FLAME_EBEND_ASYMFAC = 'flame_asym_fac'
CONFIG_FLAME_BEND_FOCUSING = 'focusing_component'
# Corrector:
# flag to indicate if using kick ([T.m]) ("tm_kick") or theta ([rad]) ("rad_kick")
CONFIG_FLAME_COR_GAUGE = "flame_cor_gauge"

# drift mask: bool
CONFIG_DRIFT_MASK = "drift_mask"

# Sextupole
CONFIG_FLAME_SEXT_STEP = 'step'
CONFIG_FLAME_SEXT_DSTKICK = 'dstkick'
DEFAULT_FLAME_SEXT_STEP = 10
DEFAULT_FLAME_SEXT_DSTKICK = 1

# Position type for PM
CONFIG_PM_ANGLE = 'pm_angle'
DEFAULT_PM_ANGLE = "-45"

# Constants used for IMPACT header parameters

SIM_TYPE_MOMENT_MATRIX = "MomentMatrix"
MPOLE_LEVEL_FOCUS_DEFOCUS = 0
MPOLE_LEVEL_DIPOLE = 1
MPOLE_LEVEL_QUADRUPOLE = 2
HDIPOLE_FIT_MODE_BEAM_ENERGY = 1
HDIPOLE_FIT_MODE_NONE = 0

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
    """Build ``FlameLattice`` object.

    Parameters
    ----------
    accel :
        Layout object.

    Keyword Arguments
    -----------------
    config :
        Configuration options.
    settings :
        Accelerator settings.
    start :
        Start element.
    end :
        End element.
    template :
        Template.

    Returns
    -------
    ret :
        Flame lattice object.
    """
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

    Parameters
    ----------
    accel :
        Accelerator layout.

    Keyword Arguments
    -----------------
    config :
        Configuration options.
    settings :
        Accelerator settings.
    start :
        Start element.
    end :
        End element.
    template :
        Template.
    """

    def __init__(self, accel, **kwargs):
        super(FlameLatticeFactory, self).__init__()
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
            lattice.hdipoleFitMode = self._get_config_int_default(CONFIG_FLAME_HDIPOLE_FIT_MODE,
                                                                  _DEFAULT_HDIPOLE_FIT_MODE)

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
            lattice.charge = self._get_config_float_default(CONFIG_FLAME_CHARGE, _DEFAULT_CHARGE)

        if self.initialPosition is not None:
            lattice.initialPosition = self.initialPosition
        else:
            lattice.initialPosition = self._get_config_data_default(CONFIG_FLAME_INITIAL_POSITION_FILE,
                                                                    _DEFAULT_INITIAL_POSITION)

        if self.initialEnvelope is not None:
            lattice.initialEnvelope = self.initialEnvelope
        else:
            lattice.initialEnvelope = self._get_config_data_default(CONFIG_FLAME_INITIAL_ENVELOPE_FILE,
                                                                    _DEFAULT_INITIAL_ENVELOPE)

        for elem in self._accel.iter(self.start, self.end):
            # check drift mask first
            if self._get_config(elem.dtype, CONFIG_DRIFT_MASK, 'False').lower() == 'true':
                elem = DriftElement(elem.z, elem.length, elem.aperture, elem.name)
            #

            if isinstance(elem, DriftElement):
                lattice.append(elem.name, "drift",
                               ('L', elem.length), ('aper', elem.aperture / 2.0))

            elif isinstance(elem, (ValveElement, PortElement)):
                lattice.append(elem.name, "drift",
                               ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, BPMElement):
                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 1), "drift",
                                   ('L', elem.length / 2.0), ('aper', elem.aperture / 2.0))

                lattice.append(elem.name, "bpm", name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 2), "drift",
                                   ('L', elem.length / 2.0), ('aper', elem.aperture / 2.0))

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 1), "drift",
                                   ('L', elem.length / 2.0), ('aper', elem.aperture / 2.0))

                lattice.append(elem.name, "marker", name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 2), "drift",
                                   ('L', elem.length / 2.0), ('aper', elem.aperture / 2.0))

            elif isinstance(elem, PMElement):
                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 1), "drift",
                                   ('L', elem.length / 2.0), ('aper', elem.aperture / 2.0))

                pm_angle = self._get_config(elem.dtype, CONFIG_PM_ANGLE, DEFAULT_PM_ANGLE)
                if pm_angle == '-45':
                    elem.sign = -1.0
                else:
                    elem.sign = 1.0
                lattice.append(elem.name, "marker", name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 2), "drift",
                                   ('L', elem.length / 2.0), ('aper', elem.aperture / 2.0))

            elif isinstance(elem, CavityElement):
                phase = 0.0
                if settings is not None:
                    try:
                        phase = settings[elem.name][elem.fields.phase_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.phase_phy,
                                                                                                 elem.name))

                amplitude = 0.0
                if settings is not None:
                    try:
                        amplitude = settings[elem.name][elem.fields.amplitude_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.amplitude_phy,
                                                                                                 elem.name))

                frequency = 0.0
                if settings is not None:
                    try:
                        frequency = settings[elem.name][elem.fields.frequency]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.frequency,
                                                                                                 elem.name))

                cav_type = self._get_config(elem.dtype, CONFIG_FLAME_CAV_TYPE, None)
                if cav_type is None:
                    raise RuntimeError("FlameLatticeFactory: Cavity type not found: {}".format(elem.dtype))
                elif cav_type == 'Generic':
                    cav_conf = self._get_config(elem.dtype, CONFIG_FLAME_CAV_CONF, None)
                    if cav_conf is None:
                        raise RuntimeError("FlameLatticeFactory: Generic cavity data file not found: {}".format(elem.dtype))
                    lattice.append(elem.name, "rfcavity",
                                   ('cavtype', cav_type), ('f', frequency),
                                   ('phi', phase), ('scl_fac', amplitude),
                                   ('L', elem.length), ('aper', elem.aperture / 2.0),
                                   ('datafile', cav_conf),
                                   name=elem.name, etype=elem.ETYPE)
                else:
                    lattice.append(elem.name, "rfcavity",
                                   ('cavtype', cav_type), ('f', frequency),
                                   ('phi', phase), ('scl_fac', amplitude),
                                   ('L', elem.length), ('aper', elem.aperture / 2.0),
                                   name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, SolCorElement):
                field = 0.0
                if settings is not None:
                    try:
                        field = settings[elem.name][elem.fields.field_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field_phy,
                                                                                                 elem.name))

                hkick = 0.0
                if settings is not None:
                    try:
                        hkick = settings[elem.h.name][elem.h.fields.angle_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.h.fields.angle_phy,
                                                                                                 elem.name))

                vkick = 0.0
                if settings is not None:
                    try:
                        vkick = settings[elem.v.name][elem.v.fields.angle_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.v.fields.angle_phy,
                                                                                                 elem.name))

                # error = self._get_error(elem)

                lattice.append(elem.name + "_1", "solenoid", ('L', elem.length / 2.0),
                               ('aper', elem.aperture / 2.0), ('B', field),
                               name=elem.name, etype="SOL")

                lattice.append(elem.h.name, "orbtrim", ('theta_x', hkick),
                               name=elem.h.name, etype=elem.h.ETYPE)

                lattice.append(elem.v.name, "orbtrim", ('theta_y', vkick),
                               name=elem.v.name, etype=elem.v.ETYPE)

                lattice.append(elem.name + "_2", "solenoid", ('L', elem.length / 2.0),
                               ('aper', elem.aperture / 2.0), ('B', field),
                               name=elem.name, etype="SOL")

            elif isinstance(elem, QuadElement):
                gradient = 0.0
                if settings is not None:
                    try:
                        gradient = settings[elem.name][elem.fields.gradient_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.gradient_phy,
                                                                                                 elem.name))

                # error = self._get_error(elem)

                lattice.append(elem.name, "quadrupole", ('L', elem.length),
                               ('aper', elem.aperture / 2.0), ('B2', gradient),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, SextElement):
                field = 0.0
                if settings is not None:
                    try:
                        field = settings[elem.name][elem.fields.field_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field_phy,
                                                                                                 elem.name))

                step = self._get_config(elem.dtype, CONFIG_FLAME_SEXT_STEP,
                                        DEFAULT_FLAME_SEXT_STEP)
                dstkick = self._get_config(elem.dtype, CONFIG_FLAME_SEXT_DSTKICK,
                                           DEFAULT_FLAME_SEXT_DSTKICK)
                lattice.append(elem.name, "sextupole",
                               ('L', elem.length), ('B3', field),
                               ('dstkick', int(dstkick)), ('step', int(step)),
                               ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, CorElement):
                hkick = 0.0
                if settings is not None:
                    try:
                        hkick = settings[elem.h.name][elem.h.fields.angle_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.h.fields.angle_phy,
                                                                                                 elem.name))

                vkick = 0.0
                if settings is not None:
                    try:
                        vkick = settings[elem.v.name][elem.v.fields.angle_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.v.fields.angle_phy,
                                                                                                 elem.name))

                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 1), "drift",
                                   ('L', elem.length / 2.0),
                                   ('aper', elem.apertureX / 2.0))

                kick_gauge = self._get_config(elem.dtype, CONFIG_FLAME_COR_GAUGE, None)
                if kick_gauge == "tm_kick":
                    lattice.append(elem.h.name, "orbtrim",
                                   ('realpara', 1), ('tm_xkick', hkick),
                                   name=elem.h.name, etype=elem.h.ETYPE)
                    lattice.append(elem.v.name, "orbtrim",
                                   ('realpara', 1), ('tm_ykick', hkick),
                                   name=elem.v.name, etype=elem.v.ETYPE)
                else:
                    lattice.append(elem.h.name, "orbtrim", ('theta_x', hkick),
                                   name=elem.h.name, etype=elem.h.ETYPE)
                    lattice.append(elem.v.name, "orbtrim", ('theta_y', vkick),
                                   name=elem.v.name, etype=elem.v.ETYPE)

                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 2), "drift",
                                   ('L', elem.length / 2.0),
                                   ('aper', elem.apertureX / 2.0))

            elif isinstance(elem, BendElement):
                field = 0.0
                if settings is not None:
                    try:
                        field = settings[elem.name][elem.fields.field_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field_phy,
                                                                                                 elem.name))

                angle = 0.0
                if settings is not None:
                    try:
                        angle = settings[elem.name][elem.fields.angle]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.angle,
                                                                                                 elem.name))

                entr_angle = 0.0
                if settings is not None:
                    try:
                        entr_angle = settings[elem.name][elem.fields.entrAngle]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.entrAngle,
                                                                                                 elem.name))

                exit_angle = 0.0
                if settings is not None:
                    try:
                        exit_angle = settings[elem.name][elem.fields.exitAngle]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.exitAngle,
                                                                                                 elem.name))

                split = self._get_config_split(elem.dtype)

                if split < 3:
                    raise RuntimeError("FlameLatticeFactory: '{}' split must be greater than 3.".format(elem.name))

                focusing_comp = self._get_config(elem.dtype, CONFIG_FLAME_BEND_FOCUSING, None)
                if focusing_comp is not None:
                    _LOGGER.debug("FlameLatticeFactory: focusing component of {} is defined.".format(elem.name))
                    k = float(focusing_comp)

                    lattice.append(elem.name + "_1", "sbend", ('L', elem.length / split),
                                   ('aper', elem.aperture / 2.0), ('phi', angle / split),
                                   ('phi1', entr_angle), ('phi2', 0.0), ('bg', field),
                                   ('K', k),
                                   name=elem.name, etype=elem.ETYPE)

                    for i in range(2, split):
                        lattice.append(elem.name + "_" + str(i), "sbend", ('L', elem.length / split),
                                       ('aper', elem.aperture / 2.0), ('phi', angle / split),
                                       ('phi1', 0.0), ('phi2', 0.0), ('bg', field),
                                       ('K', k),
                                       name=elem.name, etype=elem.ETYPE)

                    lattice.append(elem.name + "_" + str(split), "sbend", ('L', elem.length / split),
                                   ('aper', elem.aperture / 2.0), ('phi', angle / split),
                                   ('phi1', 0.0), ('phi2', exit_angle), ('bg', field),
                                   ('K', k),
                                   name=elem.name, etype=elem.ETYPE)

                else:
                    lattice.append(elem.name + "_1", "sbend", ('L', elem.length / split),
                                   ('aper', elem.aperture / 2.0), ('phi', angle / split),
                                   ('phi1', entr_angle), ('phi2', 0.0), ('bg', field),
                                   name=elem.name, etype=elem.ETYPE)

                    for i in range(2, split):
                        lattice.append(elem.name + "_" + str(i), "sbend", ('L', elem.length / split),
                                       ('aper', elem.aperture / 2.0), ('phi', angle / split),
                                       ('phi1', 0.0), ('phi2', 0.0), ('bg', field),
                                       name=elem.name, etype=elem.ETYPE)

                    lattice.append(elem.name + "_" + str(split), "sbend", ('L', elem.length / split),
                                   ('aper', elem.aperture / 2.0), ('phi', angle / split),
                                   ('phi1', 0.0), ('phi2', exit_angle), ('bg', field),
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
                    lattice.append(_drift_name(elem.name, 1), "drift",
                                   ('L', elem.length / 2.0),
                                   ('aper', elem.aperture / 2.0))

                lattice.append(elem.name, "stripper",
                               ('IonChargeStates', stripper_charge),
                               ('NCharge', stripper_count),
                               name=elem.name, etype=elem.ETYPE)

                if elem.length != 0.0:
                    lattice.append(_drift_name(elem.name, 2), "drift",
                                   ('L', elem.length / 2.0),
                                   ('aper', elem.aperture / 2.0))

            elif isinstance(elem, SolElement):
                field = 0.0
                if settings is not None:
                    try:
                        field = settings[elem.name][elem.fields.field_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field_phy,
                                                                                                 elem.name))

                lattice.append(elem.name, "solenoid", ('L', elem.length),
                               ('aper', elem.aperture / 2.0), ('B', field),
                               name=elem.name, etype='SOL')

            elif isinstance(elem, ElectrodeElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, FCElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, VDElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, EMSElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, ApertureElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, AttenuatorElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, SlitElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, DumpElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)
            elif isinstance(elem, ChopperElement):
                lattice.append(elem.name, "drift", ('L', elem.length), ('aper', elem.aperture / 2.0),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, EBendElement):
                field = 0.0
                if settings is not None:
                    try:
                        field = settings[elem.name][elem.fields.field_phy]
                    except KeyError:
                        raise RuntimeError(
                            "FlameLatticeFactory: '{}' setting not found for element: {}".format(elem.fields.field_phy,
                                                                                                 elem.name))

                phi = self._get_config(elem.dtype, CONFIG_FLAME_EBEND_PHI, None)
                if phi is None:
                    raise RuntimeError("FlameLatticeFactory: EBend 'phi' not found for {}".format(elem.dtype))

                fringe_x = self._get_config(elem.dtype, CONFIG_FLAME_EBEND_FRINGEX, None)
                if fringe_x is None:
                    raise RuntimeError("FlameLatticeFactory: EBend 'fringe_x' not found for {}".format(elem.dtype))

                fringe_y = self._get_config(elem.dtype, CONFIG_FLAME_EBEND_FRINGEY, None)
                if fringe_y is None:
                    raise RuntimeError("FlameLatticeFactory: EBend 'fringe_y' not found for {}".format(elem.dtype))

                ver = self._get_config(elem.dtype, CONFIG_FLAME_EBEND_VERBOOL, None)
                if ver is None:
                    raise RuntimeError("FlameLatticeFactory: EBend 'ver' not found for {}".format(elem.dtype))

                spher = self._get_config(elem.dtype, CONFIG_FLAME_EBEND_SPHERBOOL, None)
                if spher is None:
                    raise RuntimeError("FlameLatticeFactory: EBend 'spher' not found for {}".format(elem.dtype))

                asym_fac = self._get_config(elem.dtype, CONFIG_FLAME_EBEND_ASYMFAC, None)
                if asym_fac is None:
                    raise RuntimeError("FlameLatticeFactory: EBend 'asym_fac' not found for {}".format(elem.dtype))

                lattice.append(elem.name, 'edipole', ('L', elem.length),
                               ('aper', elem.aperture / 2.0), ('phi', float(phi)),
                               ('fringe_x', float(fringe_x)), ('fringe_y', float(fringe_y)),
                               ('ver', int(ver)), ('spher', float(spher)),
                               ('asym_fac', float(asym_fac)), ('beta', field),
                               name=elem.name, etype=elem.ETYPE)

            elif isinstance(elem, EQuadElement):
                gradient = 0.0
                if settings is not None:
                    try:
                        gradient = settings[elem.name][elem.fields.gradient_phy]
                    except KeyError:
                        raise RuntimeError("FlameLatticeFactory: '{}' setting not found for element: {}".format(
                            elem.fields.gradient_phy, elem.name))

                radius = self._get_config(elem.dtype, CONFIG_FLAME_EQUAD_RADIUS, None)
                if radius is None:
                    raise RuntimeError("FlameLatticeFactory: EQuad 'radius' not found for {}".format(elem.dtype))
                lattice.append(elem.name, "equad", ('L', elem.length),
                               ('aper', elem.aperture / 2.0), ('V', gradient),
                               ('radius', float(radius)),
                               name=elem.name, etype=elem.ETYPE)

            else:
                raise Exception("Unsupported accelerator element: {}".format(elem))

        return lattice


def _drift_name(name, did=1):
    """Return equivalent drift section name, before(1) and after(2).
    """
    r = re.match(r"(.*):(.*)_(D.*)", name)
    return '{}:{}_DFT{}_{}'.format(r.group(1), r.group(2), did, r.group(3))


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
        self.append('S', "source", ('vector_variable', "P"), ('matrix_variable', "S"))

    @property
    def simType(self):
        return self.variables['sim_type']

    @simType.setter
    def simType(self, simType):
        if simType not in [SIM_TYPE_MOMENT_MATRIX]:
            raise ValueError("FlameLattice: 'simType' property must be supported value")
        self.variables['sim_type'] = simType

    @property
    def dataDir(self):
        return self.variables['Eng_Data_Dir']

    @dataDir.setter
    def dataDir(self, dataDir):
        if not isinstance(dataDir, basestring):
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
        if hdipoleFitMode not in [HDIPOLE_FIT_MODE_BEAM_ENERGY, HDIPOLE_FIT_MODE_NONE]:
            raise ValueError("FlameLattice: 'hdipoleFitMode' property must be supported value")
        self.variables['HdipoleFitMode'] = hdipoleFitMode

    @property
    def charge(self):
        return self.variables['IonChargeStates']

    @charge.setter
    def charge(self, charge):
        if isinstance(charge, (int, float)):
            self.variables['IonChargeStates'] = numpy.array([float(charge)])
        elif isinstance(charge, (list, tuple)):
            v = []
            for c in charge:
                if not isinstance(c, (int, float)):
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
        if isinstance(count, (int, float)):
            self.variables['NCharge'] = numpy.array([float(count)])
        elif isinstance(count, (list, tuple)):
            v = []
            for c in count:
                if not isinstance(c, (int, float)):
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
        position = numpy.empty((len(keys), 7))
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
                self.variables['P' + str(i)] = position[i]

        if isinstance(initialPosition, (list, tuple)):
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
                self.variables['S' + str(i)] = position[i]

        if isinstance(initialEnvelope, (list, tuple)):
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
        if not isinstance(initialEnergy, (int, float)):
            raise TypeError("FlameLattice: 'initialEnergy' must be a number")
        self.variables['IonEk'] = float(initialEnergy)

    @property
    def particleMass(self):
        return self.variables['IonEs']

    @particleMass.setter
    def particleMass(self, particleMass):
        if not isinstance(particleMass, (int, float)):
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
