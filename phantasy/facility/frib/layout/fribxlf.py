# -*- coding: utf-8 -*-
"""Library for reading FRIB Expanded Lattice File (*.xlsx) and generating Accelerator Design Description."""

import logging
import os.path
import re
import xlrd
from collections import OrderedDict

from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import FoilElement
from phantasy.library.layout import NDElement
from phantasy.library.layout import ICElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import ColumnElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import EBendElement
from phantasy.library.layout import EMSElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import ElectrodeElement
from phantasy.library.layout import FCElement
from phantasy.library.layout import HCorElement
from phantasy.library.layout import MarkerElement
from phantasy.library.layout import Layout
from phantasy.library.layout import HMRElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SeqElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import OctElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import VCorElement
from phantasy.library.layout import VDElement
from phantasy.library.layout import SDElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import SlitElement
from phantasy.library.layout import ChopperElement
from phantasy.library.layout import AttenuatorElement
from phantasy.library.layout import DumpElement
from phantasy.library.layout import ApertureElement
from phantasy.library.layout import CollimatorElement
from phantasy.library.layout import RotElement
from phantasy.library.layout import WedgeElement
from phantasy.library.layout import ELDElement
from phantasy.library.layout import TargetElement
from phantasy.library.parser import Configuration

NON_DRIFT_ELEMENTS = (
        BCMElement, BLElement, BLMElement, BPMElement, BendElement,
        CavityElement, ColumnElement, CorElement, HCorElement, VCorElement,
        EBendElement, EMSElement,
        EQuadElement, ElectrodeElement, FCElement, HCorElement, PMElement,
        PortElement, QuadElement, SextElement, SolElement, SolCorElement,
        StripElement, VCorElement, VDElement, ValveElement, SlitElement,
        ChopperElement, AttenuatorElement, DumpElement, ApertureElement,
        HMRElement, CollimatorElement, NDElement, ICElement, RotElement,
        SDElement, MarkerElement, OctElement, WedgeElement, ELDElement,
        TargetElement, FoilElement,
)

# constants for parsing xlsx file
# skip line whose system field startswith any one of the words defined by SYSTEM_SKIP_WORDS
SYSTEM_SKIP_WORDS = ( "dump", "SEGMENT", "LINAC", "Target",
                      "beta=0.085 QWR cryomodules START",
                      "D-station start", "D-station end",
                      'First beam dump line starts in "V" column',
                      'Second beam dump line starts in "V" column',
                      'Third beam dump line starts in "V" column',
                      'Fourth beam dump line starts in "V" column',
                      "location of temporary carbon foil without Li module: PM2225 to foil is 1.356008 m",
                      "END", "LEBT",
                      )
# skip line whose device field in one of the tuple defined by DEVICE_SKIP_WORDS
DEVICE_SKIP_WORDS = ( "end", "start", "END", )

# skip line whose name field is any one of the words defined by NAME_SKIP_WORDS
NAME_SKIP_WORDS = ("FE_MEBT:PM_D1053",
                   "DANS:TL_D1439", # ReA
                   "DATP:TL_D1460", # ReA
                   "DJNS:TL_D1465", # ReA
                   "REA_ISRC2:FIL_D0849", # ReA
                   "REA_ISRC2:AND_D0849", # ReA
                   "REA_ISRC2:EXT_D0849", # ReA
                   "REA_BTS02:EIN_D0850", # ReA
                   "REA_ISRC1:FIL_D0946", # ReA
                   "REA_ISRC1:AND_D0946", # ReA
                   "REA_ISRC1:EXT_D0946", # ReA
                   "REA_ISRC1:DCV1_D0947", # ReA
                   "REA_ISRC1:DCV2_D0947", # ReA
                   "REA_ISRC1:WF_D0948", # ReA
                   "REA_ISRC1:HVP_D0951", # ReA
)

# element name as drift
ELEMENT_NAME_STRING_AS_DRIFT = [
    "coil-out", "coil-out (assumed)", "coil out", "coil out + leads",
    "collimation flange", "collimation flange moved??",
    "collimation flange removed",
    "BPM-box", "diagnostic box", "vacuum box", "box",
    "box+tube", "mhb box", "4 way cross", "6 way cross",
    "artemis_b extraction/puller", "artemis_b extraction wall",
    "extraction mounting plate", "extraction box",
    "gap (puller & extraction hole)", "gap (puller main & bias)",
    "puller tube", "8 mm extraction hole",
    "artemis_b extraction conical wall",
    "RFQ end wall", "RFQ inn-wall (match point)", "RFQ inn-wall",
    "motor shield", "mirror shield", "mirror", "target collimator",
    "a cross will be added",
    "4-way cross with bellow", "SEE D4 dipole-17.5deg",
    "6-way cross #1 first half", "6-way cross #1 second half",
    "6-way cross #2 first half", "6-way cross #2 second half",
    "4-way cross first half", "4-way cross second half",

# ReA
    "BOB1", "BOB2", "BOB3", "BOB4",
    "BOX1", "BOX2", "BOX3", "BOX4",
    "BOX5", "BOX6", "BOX7", "BOX8",
    "BOX9", "BOX10", "BOX11", "Box 13",
    "Box 14", "Box 15", "Box 16", "Box 17",
    "Box 18", "Box 19", "Box 20", "Box 21", "Box 22",
    "RFQ entrance=100m by definition",
    "ORIGIN POINT",
    "6-Way Cross (temporary)",
# ES
    "space for post-target shield",
    "space for vacuum separation valve",
    "front shield for WIQ2",
    "Entrance Point of dipole at D1064",
    "Exit Point of dipole at D1064",
    "placeholder for anticipated complimentary diagnostics",
    "fragment catchers (entrance plane)",
    "fragment catchers (center plane of movable fragment catchers)",
    "fragment catchers (exit plane of movable fragment catchers)",
    "Entrance Point of dipole at D1108",
    "Exit Point of dipole at D1108",
    "space for WIQ6",
    "space for vacuum separation (gate valve)",
    "image plane",
    "vessel wall (check exact dimensions)",
    "Entrance Point of dipole at D1246",
    "Exit Point of dipole at D1246",
    "Entrance Point of dipole at D1402",
    "Exit Point of dipole at D1402",
    "Center of doublet at D1433",
    "Center of doublet at D1449",
    "upstream insulating flange",
    "downstream insulating flange",
    "was gate valve, moved away",
    "Entrance Point of dipole at D1513",
    "Exit Point of dipole at D1513",
    "Entrance Point of dipole at D1608",
    "Exit Point of dipole at D1608",
    "wedge (and viewer) upstream part",
    "Diagnostics Box DB0",
    "Diagnostics Box DB1",
    "Diagnostics Box DB2",
    "Diagnostics Box DB3",
    "Diagnostics Box DB4",
    "Diagnostics Box DB5",
    "wedge (and viewer) downstream part",
    "Entrance Point of dipole at D1712",
    "Exit Point of dipole at D1712",
    "Entrance Point of dipole at D1807",
    "Exit Point of dipole at D1807",
    "diagnostics box entrance wall",
]

# device alias for target: TargetElement
DEVICE_ALIAS_PTA = ( "PTA",
                     "CHIP", # FSEE beamline
)

# device alias for energy loss detector: ELDElement
DEVICE_ALIAS_ELD = ( "ELD", )

# device alias for wedge: WedgeElement
DEVICE_ALIAS_WEDGE = ( "WED", )

# device alias for valve: ValveElement
DEVICE_ALIAS_VALVE = ( "GV", "FVS", "FAV", "FV", "FAVS",
                       "BGV", "RV", "VV", "TGV", ) # ReA
# device alias for cavity: CavityElement
DEVICE_ALIAS_CAV = ( "CAV1", "CAV2", "CAV3", "CAV4",
                     "CAV5", "CAV6", "CAV7", "CAV8", "CAV", )
# device alias for solenoid: SolElement
DEVICE_ALIAS_SOLR = ( "SOLR", )
# device alias for solenoid w/ hcor&vcor: SolCorElement
DEVICE_ALIAS_SOL = ( "SOL1", "SOL2", "SOL3", "SOLS",
                     "SOL", ) # ReA
# device alias for BPM
DEVICE_ALIAS_BPM = ( "BPM", )
# device alias for PM
DEVICE_ALIAS_PM = ( "PM", "PM1", )
# device alias for BL (measure beam length)
DEVICE_ALIAS_BL = ( "BL", "LPM", )
# device alias for BLM (measure beam loss)
DEVICE_ALIAS_BLM = ( "BLM", )
# device alias for FOIL
DEVICE_ALIAS_FOIL = ( "FOIL", )
# device alias for ND
DEVICE_ALIAS_ND = ( "ND", )
# device alias for IC
DEVICE_ALIAS_IC = ( "IC", )
# device alias for BCM (measure beam current)
DEVICE_ALIAS_BCM = ( "BCM", )
# device alias for EMS (emittance scanner)
DEVICE_ALIAS_EMS = ( "EMS", )
# device alias for faraday cup
DEVICE_ALIAS_FC = ( "FC", "FFC",
                    "FCS",  # ReA
)
# device alias for silicon detector
DEVICE_ALIAS_SD = (
    "FSD",  # ReA, decay counter, temporarily here
    "MCPV", # ReA, (MCPV) Multichannel plate temporarily here
    "TID",  # ReA, Timing detector, temporarily here
)
# device alias for viewer
DEVICE_ALIAS_VD = ( "VD",
                    "SiD",  # SiD is silicon detector, temporarily put it here
                    "SiD1", "SiD2", # FSEE beamline
                    "CAM",  # ReA
)
# device alias for pump, port, etc.
DEVICE_ALIAS_PORT = ( "PORT", "TMP", "NEGP", "IP", "CP",
                      "CCG",  # CCG is cold cathod gauge, temporarily put it here
                      "FE",   # ReA, flow meter, temporarily here
                      "TSH", "TSH1", "TSH2", "TS", # ReA, temperature switch, temporarily here
                      "FPG", "PG",  # ReA, vacuum, temporarily here
                      "LT", # ReA, light, temporarily here
                      "PSD",  # ReA, power supply dipole?
)
# device alias for correctors, comes with H&V pair.
DEVICE_ALIAS_COR = ( "DC", "DC0", "CH", "DCHV", )
# device alias for HCOR
DEVICE_ALIAS_HCOR = ( "DCHE", "DCH", "PSC2", ) # ReA
# device alias for VCOR
DEVICE_ALIAS_VCOR = ( "DCVE", "DCV", "PSC1", ) # ReA
# device alias for dipole, bend
DEVICE_ALIAS_BEND = ( "DH",
                      "DV", ) # ReA
# device alias for quad
DEVICE_ALIAS_QUAD = ( "QH", "QV", "Q",
                      "PSQ", # ReA
)
# device alias for rotation elements (virtual)
DEVICE_ALIAS_ROT = ( "ROT", ) # ReA
# device alias for sextupole
DEVICE_ALIAS_SEXT = ( "S", )
# device alias for octopole
DEVICE_ALIAS_OCT = ( "OCT", "O" )
# device alias for electrode
DEVICE_ALIAS_ELC = ( "ELC1", "ELC2", "ELC3", "ELC0", "ELCT",)
# device alias for acc column
DEVICE_ALIAS_ACC = ( "ACC", )
# device alias for ES bend
DEVICE_ALIAS_EBEND = ( "DVE",
                       "DHE", ) # ReA
# device alias for ES quad
DEVICE_ALIAS_EQUAD = ( "QHE", "QVE",
                       "QE", ) # ReA
# device alias for slit
DEVICE_ALIAS_SLIT = ( "SLH", "SLT",
                      "SLHGAP", "SLHCEN", "DD", "SLV", # ReA
                      "SLB", "SLL", "SLR", # ReA
)
# device alias for chopper
DEVICE_ALIAS_CHP = ( "CHP", )
# device alias for aperture
DEVICE_ALIAS_AP = ( "AP", )
# device alias for attenuator
DEVICE_ALIAS_ATT = ( "ATT",
                     "ATP", ) # ReA
# device alias for dump
DEVICE_ALIAS_DUMP = ( "dump", "DUMP", "BD", )
# device alias for halo ring
DEVICE_ALIAS_HMR = ( "HMR", )
# device alias for collimation flange
DEVICE_ALIAS_CLLM = ( "CLLM", )

# configuration options

CONFIG_MACHINE = "machine"
CONFIG_LENGTH = "length"
CONFIG_APERTURE = "aperture"
CONFIG_APERTURE_X = "aperture_x"
CONFIG_APERTURE_Y = "aperture_y"

# XLF parameters

XLF_SECTION_NAME = "LatticeFile"

CONFIG_XLF_DIAMETER = "xlf_diameter"
CONFIG_XLF_DATA_FILE = "xlf_data_file"

CONFIG_LAYOUT_SHEET_NAME = "layout_sheet_name"
CONFIG_LAYOUT_SHEET_START = "layout_sheet_start"
CONFIG_LAYOUT_SYSTEM_IDX = "layout_system_idx"
CONFIG_LAYOUT_SUBSYSTEM_IDX = "layout_subsystem_idx"
CONFIG_LAYOUT_DEVICE_IDX = "layout_device_idx"
CONFIG_LAYOUT_POSITION_IDX = "layout_position_idx"
CONFIG_LAYOUT_NAME_IDX = "layout_name_idx"
CONFIG_LAYOUT_DEVICE_TYPE_IDX = "layout_device_type_idx"
CONFIG_LAYOUT_ELEMENT_NAME_IDX = "layout_element_name_idx"
CONFIG_LAYOUT_DIAMETER_IDX = "layout_diameter_idx"
CONFIG_LAYOUT_EFFECTIVE_LENGTH_IDX = "layout_effective_length_idx"
CONFIG_LAYOUT_CENTER_POSITION_IDX = "layout_center_position_idx"

_XLF_LAYOUT_SHEET_NAME_DEFAULT = "LatticeLayout"
_XLF_LAYOUT_SHEET_START_DEFAULT = 8
_XLF_LAYOUT_SYSTEM_IDX_DEFAULT = 0
_XLF_LAYOUT_SUBSYSTEM_IDX_DEFAULT = 1
_XLF_LAYOUT_DEVICE_IDX_DEFAULT = 2
_XLF_LAYOUT_POSITION_IDX_DEFAULT = 3
_XLF_LAYOUT_NAME_IDX_DEFAULT = 4
_XLF_LAYOUT_DEVICE_TYPE_IDX_DEFAULT = 5
_XLF_LAYOUT_ELEMENT_NAME_IDX_DEFAULT = 6
_XLF_LAYOUT_DIAMETER_IDX_DEFAULT = 7
_XLF_LAYOUT_EFFECTIVE_LENGTH_IDX_DEFAULT = 10
_XLF_LAYOUT_CENTER_POSITION_IDX_DEFAULT = 14

_LOGGER = logging.getLogger(__name__)

# format D.* to D####
FMT_INST = "D{:04d}"


class XlfConfig(object):
    """Configuration for XLF file.
    """
    def __init__(self, config, **kws):
        section = kws.get('section', XLF_SECTION_NAME)
        k = (CONFIG_LAYOUT_SHEET_NAME, CONFIG_LAYOUT_SHEET_START,
             CONFIG_LAYOUT_SYSTEM_IDX, CONFIG_LAYOUT_SUBSYSTEM_IDX,
             CONFIG_LAYOUT_DEVICE_IDX, CONFIG_LAYOUT_POSITION_IDX,
             CONFIG_LAYOUT_NAME_IDX, CONFIG_LAYOUT_DEVICE_TYPE_IDX,
             CONFIG_LAYOUT_ELEMENT_NAME_IDX, CONFIG_LAYOUT_DIAMETER_IDX,
             CONFIG_LAYOUT_EFFECTIVE_LENGTH_IDX, CONFIG_LAYOUT_CENTER_POSITION_IDX)
        v = (_XLF_LAYOUT_SHEET_NAME_DEFAULT, _XLF_LAYOUT_SHEET_START_DEFAULT,
             _XLF_LAYOUT_SYSTEM_IDX_DEFAULT, _XLF_LAYOUT_SUBSYSTEM_IDX_DEFAULT,
             _XLF_LAYOUT_DEVICE_IDX_DEFAULT, _XLF_LAYOUT_POSITION_IDX_DEFAULT,
             _XLF_LAYOUT_NAME_IDX_DEFAULT, _XLF_LAYOUT_DEVICE_TYPE_IDX_DEFAULT,
             _XLF_LAYOUT_ELEMENT_NAME_IDX_DEFAULT, _XLF_LAYOUT_DIAMETER_IDX_DEFAULT,
             _XLF_LAYOUT_EFFECTIVE_LENGTH_IDX_DEFAULT, _XLF_LAYOUT_CENTER_POSITION_IDX_DEFAULT)
        d = dict(zip(k, v))

        for option in k:
            if config.has_option(section, option, False):
                new_value = config.get(section, option)
                try:
                    x = int(new_value)
                except ValueError:
                    x = new_value
                finally:
                    d[option] = x
        self._xlf_layout_sheet_name = d.get(CONFIG_LAYOUT_SHEET_NAME)
        self._xlf_layout_sheet_start = d.get(CONFIG_LAYOUT_SHEET_START)
        self._xlf_layout_system_idx = d.get(CONFIG_LAYOUT_SYSTEM_IDX)
        self._xlf_layout_subsystem_idx = d.get(CONFIG_LAYOUT_SUBSYSTEM_IDX)
        self._xlf_layout_device_idx = d.get(CONFIG_LAYOUT_DEVICE_IDX)
        self._xlf_layout_position_idx = d.get(CONFIG_LAYOUT_POSITION_IDX)
        self._xlf_layout_name_idx = d.get(CONFIG_LAYOUT_NAME_IDX)
        self._xlf_layout_device_type_idx = d.get(CONFIG_LAYOUT_DEVICE_TYPE_IDX)
        self._xlf_layout_element_name_idx = d.get(CONFIG_LAYOUT_ELEMENT_NAME_IDX)
        self._xlf_layout_diameter_idx = d.get(CONFIG_LAYOUT_DIAMETER_IDX)
        self._xlf_layout_effective_length_idx = d.get(CONFIG_LAYOUT_EFFECTIVE_LENGTH_IDX)
        self._xlf_layout_center_position_idx = d.get(CONFIG_LAYOUT_CENTER_POSITION_IDX)
        self._options = d

        if config.has_option(section, 'device_mapping', False):
            # 'device_mapping' is an option name in phantasy.cfg, to change the
            # device name defined by key to the name defined by value.
            self.d_map = _to_dict(config.get(section, 'device_mapping'))
        else:
            self.d_map = {}

    def get_options(self):
        return self._options


def build_accel(xlfpath=None, machine=None):
    """
    Convenience method for building ADD from Expanded Lattice File.
    """

    accel_factory = AccelFactory()

    if xlfpath is not None:
        accel_factory.xlfpath = xlfpath

    if machine is not None:
        accel_factory.machine = machine

    return accel_factory.build()


def build_layout(**kwargs):
    """Convenience method for building layout from Expanded Lattice File.

       :returns: accelerator layout
    """

    accel_factory = AccelFactory(**kwargs)

    return accel_factory.build()


class AccelFactory(XlfConfig):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.
    """

    def __init__(self, **kwargs):
        if kwargs.get("config", None) is not None:
            self.config = kwargs.get("config")
        else:
            self.config = Configuration()

        XlfConfig.__init__(self, self.config)

        self.xlfpath = kwargs.get("xlfpath", None)
        self.machine = kwargs.get("machine", None)
        self.diameter = kwargs.get("diameter", None)

    @property
    def xlfpath(self):
        return self._xlfpath

    @xlfpath.setter
    def xlfpath(self, xlfpath):
        if (xlfpath is not None) and not isinstance(xlfpath, str):
            raise TypeError("AccelFactory: 'xlfpath' property must be type a string or None")
        self._xlfpath = xlfpath

    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, machine):
        if (machine is not None) and not isinstance(machine, str):
            raise TypeError("AccelFactory: 'machine' property must be type string or None")
        self._machine = machine

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter):
        if (diameter is not None) and not isinstance(diameter, (int, float)):
            raise TypeError("AccelFactory: 'diameter' property must be type a number or None")
        self._diameter = diameter

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not isinstance(config, Configuration):
            raise TypeError("AccelFactory: 'config' property must be type Configuration")
        self._config = config

    def _get_config_length(self, elem):
        if self.config.has_option(elem.name, CONFIG_LENGTH, False):
            return self.config.getfloat(elem.name, CONFIG_LENGTH, False)
        else:
            return self.config.getfloat(elem.dtype, CONFIG_LENGTH, False)

    def _has_config_length(self, elem):
        return self.config.has_option(elem.name, CONFIG_LENGTH, False) \
                or self.config.has_option(elem.dtype, CONFIG_LENGTH, False)

    def _get_config_aperture(self, elem):
        if self.config.has_option(elem.name, CONFIG_APERTURE, False):
            return self.config.getfloat(elem.name, CONFIG_APERTURE, False)
        else:
            return self.config.getfloat(elem.dtype, CONFIG_APERTURE, False)

    def _has_config_aperture(self, elem):
        return self.config.has_option(elem.name, CONFIG_APERTURE, False) \
               or self.config.has_option(elem.dtype, CONFIG_APERTURE, False)

    def _get_config_aperture_x(self, elem):
        if self.config.has_option(elem.name, CONFIG_APERTURE_X, False):
            return self.config.getfloat(elem.name, CONFIG_APERTURE_X, False)
        else:
            return self.config.getfloat(elem.dtype, CONFIG_APERTURE_X, False)

    def _has_config_aperture_x(self, elem):
        return self.config.has_option(elem.name, CONFIG_APERTURE_X, False) \
               or self.config.has_option(elem.dtype, CONFIG_APERTURE_X, False)

    def _get_config_aperture_y(self, elem):
        if self.config.has_option(elem.name, CONFIG_APERTURE_Y, False):
            return self.config.getfloat(elem.name, CONFIG_APERTURE_Y, False)
        else:
            return self.config.getfloat(elem.dtype, CONFIG_APERTURE_Y, False)

    def _has_config_aperture_y(self, elem):
        return self.config.has_option(elem.name, CONFIG_APERTURE_Y, False) \
               or self.config.has_option(elem.dtype, CONFIG_APERTURE_Y, False)

    def apply_config(self, elem, sequence, drift_delta):
        """Apply config to element.

        Parameters
        ----------
        elem :
            Element object.
        sequence :
            SeqElement, elements of SeqElement is a list of SeqElement.
        drift_delta : float
            Input drift_delta.

        Returns
        -------
        r : float
            Updated drfit delta, could be unchanged.
        """
        if self._has_config_aperture(elem):
            elem.aperture = self._get_config_aperture(elem)
            _LOGGER.info("AccelFactory: %s: aperture found in configuration: %s", elem.name, elem.aperture)

        if self._has_config_aperture_x(elem):
            elem.apertureX = self._get_config_aperture_x(elem)
            _LOGGER.info("AccelFactory: %s: aperture X found in configuration: %s", elem.name, elem.apertureX)

        if self._has_config_aperture_y(elem):
            elem.apertureY = self._get_config_aperture_y(elem)
            _LOGGER.info("AccelFactory: %s: aperture Y found in configuration: %s", elem.name, elem.apertureY)

        if self._has_config_length(elem):
            try:
                eff_len = self._get_config_length(elem)
                drift_delta = (elem.length - eff_len) / 2.0
                self.get_prev_element(sequence).length += drift_delta
                self.get_prev_element(sequence).z += drift_delta / 2.0
                elem.length -= drift_delta * 2.0
                _LOGGER.info("AccelFactory: %s: effective length found in configuration: %s", elem.name, elem.dtype)
            except:
                _LOGGER.warning("AccelFactory: %s: effective length configure failed: %s", elem.name, elem.dtype)
                drift_delta = 0.0
        return drift_delta

    def get_prev_element(self, sequence, allow_types=(DriftElement,)):
        # get previous element from sequence
        elements = sequence.elements[-1].elements
        if len(elements) == 0:
            # if not found in subsequence, try searching from the last one
            # note: indexing by -2 since new subsequence is always appended before growing
            return self.get_prev_element(SeqElement(None, elements=sequence.elements[:-1]))
            raise RuntimeError("AccelFactory: previous element not found")
        elif not isinstance(elements[-1], allow_types):
            raise RuntimeError("AccelFactory: previous element type invalid")
        return elements[-1]

    def build(self):
        xlfpath = self.xlfpath
        if (xlfpath is None) and self.config.has_option(XLF_SECTION_NAME, CONFIG_XLF_DATA_FILE):
            xlfpath = self.config.getabspath(XLF_SECTION_NAME, CONFIG_XLF_DATA_FILE)

        if xlfpath is None:
            raise ValueError("AccelFactory: Expanded Lattice File not specified, check the configuration.")

        if not os.path.isfile(xlfpath):
            raise ValueError("AccelFactory: Expanded Lattice File not found: '{}'".format(xlfpath))

        machine = self.machine
        if (machine is None) and self.config.has_default(CONFIG_MACHINE):
            machine = self.config.get_default(CONFIG_MACHINE)

        diameter = self.diameter
        if (diameter is None) and self.config.has_option(XLF_SECTION_NAME, CONFIG_XLF_DIAMETER):
            diameter = _parse_diameter(self.config.get(XLF_SECTION_NAME, CONFIG_XLF_DIAMETER))

        wkbk = xlrd.open_workbook(xlfpath)

        if self._xlf_layout_sheet_name not in wkbk.sheet_names():
            raise RuntimeError(
                "AccelFactory: Expanded Lattice File layout not found: '{}'".format(self._xlf_layout_sheet_name))

        layout = wkbk.sheet_by_name(self._xlf_layout_sheet_name)

        accelerator = Layout(os.path.splitext(os.path.basename(xlfpath))[0], desc="FRIB Linear Accelerator")

        sequence = None
        subsequence = None
        drift_delta = 0.0

        def name_drift():
            try:
                # previous element is not drift
                pre_elem = self.get_prev_element(sequence, NON_DRIFT_ELEMENTS)
                name = "{elem.system}_{elem.subsystem}:{elem.device}_DFT_{elem.inst}".format(elem=pre_elem)
            except:
                # previous element is drift
                pre_elem = self.get_prev_element(sequence)
                r = re.match(r"(.*)_(D.*)_([0-9].*)", pre_elem.name)
                if r is None:
                    # if pre drift name does not ends with '_#', rename it
                    name = '{}_2'.format(pre_elem.name)
                    pre_elem.name = '{}_1'.format(pre_elem.name)
                else:
                    # if pre drift name ends with '_#', inc # to the new drift
                    n, dnum, idx = r.groups()
                    name = "{n}_{d}_{i}".format(n=n, d=dnum, i=int(idx)+1)
            finally:
                return name

        for ridx in range(self._xlf_layout_sheet_start, layout.nrows):
            row = _LayoutRow(layout.row(ridx), self.config)

            # skip rows without length
            if row.eff_length is None:
                continue

            if row.device in DEVICE_SKIP_WORDS:
                continue

            if row.name in NAME_SKIP_WORDS:
                continue

            # clear lines with comments
            if row.system is not None:
                for prefix in SYSTEM_SKIP_WORDS:
                    if row.system.startswith(prefix):
                        row.system = None
                        break

            # apply default values
            if row.diameter is None:
                if (subsequence is not None) and (len(subsequence.elements) > 0):
                    # diameter from the aperture of the previous element
                    row.diameter = [subsequence.elements[-1].apertureX * 1000.0,
                                    subsequence.elements[-1].apertureY * 1000.0]
                elif diameter is not None:
                    # diameter from the configuration default
                    row.diameter = diameter
                else:
                    raise RuntimeError("AccelFactory: Layout data missing diameter (row:{}): {}".format(ridx + 1, row))

            # unit conversion, [mm] -> [m]
            row.diameter[0] *= 0.001
            row.diameter[1] *= 0.001

            if sequence is None:
                if row.system is not None:
                    sequence = SeqElement(row.system)
                    accelerator.append(sequence)
                else:
                    raise RuntimeError(
                        "AccelFactory: Initial layout data must specifiy system (row:{}): {}".format(ridx + 1, row))

            elif (row.system is not None) and (row.system != sequence.name):
                sequence = SeqElement(row.system)
                accelerator.append(sequence)
                subsequence = None

            if subsequence is None:
                if row.subsystem is not None:
                    subsequence = SeqElement(row.subsystem)
                    sequence.append(subsequence)
                else:
                    raise RuntimeError(
                        "AccelFactory: Initial layout data must specify subsystem (row:{}): {}".format(ridx + 1, row))

            elif (row.subsystem is not None) and (row.subsystem != subsequence.name):
                subsequence = SeqElement(row.subsystem)
                sequence.append(subsequence)

            try:
                if row.device is not None:

                    # set dtype with device if not defined.
                    if row.device_type is None:
                        row.device_type = row.device

                    if (drift_delta != 0.0) and (row.eff_length != 0.0):
                        # these 'named' elements do not support non-zero drift delta
                        raise RuntimeError("Unsupported drift delta on element: {}".format(row.element_name))

                    elif row.device in DEVICE_ALIAS_VALVE:
                        inst = FMT_INST.format(int(row.position))
                        elem = ValveElement(row.center_position, row.eff_length, row.diameter, row.name,
                                            desc=row.element_name, system=row.system,
                                            subsystem=row.subsystem, device=row.device, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_CAV:
                        m = re.match("(b\\d{2}) (?:cavity|resonator).*", row.element_name)
                        if m:
                            dtype = "CAV_{}".format(m.group(1).upper())
                        else:
                            dtype = row.element_name
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = CavityElement(row.center_position, row.eff_length, row.diameter, row.name,
                                             desc=row.element_name,
                                             system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype,
                                             inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_SOLR:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "SOL_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = SolElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype,
                                          inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_SOL:
                        ii = row.device[-1]
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "SOL_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = SolCorElement(row.center_position, row.eff_length, row.diameter, row.name,
                                             desc=row.element_name,
                                             system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype,
                                             inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        elem.h = HCorElement(elem.z, 0.0, elem.aperture,
                                             "{elem.system}_{elem.subsystem}:DCH{ii}_{elem.inst}".format(elem=elem, ii=ii),
                                             system=row.system, subsystem=row.subsystem, device="DCH",
                                             dtype=row.device_type, inst=inst)
                        elem.v = VCorElement(elem.z, 0.0, elem.aperture,
                                             "{elem.system}_{elem.subsystem}:DCV{ii}_{elem.inst}".format(elem=elem, ii=ii),
                                             system=row.system, subsystem=row.subsystem, device="DCV",
                                             dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_BPM:
                        inst = FMT_INST.format(int(row.position))
                        elem = BPMElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_PM:
                        inst = FMT_INST.format(int(row.position))
                        elem = PMElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_BL:
                        inst = FMT_INST.format(int(row.position))
                        elem = BLElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_BLM:
                        inst = FMT_INST.format(int(row.position))
                        elem = BLMElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_FOIL:
                        inst = FMT_INST.format(int(row.position))
                        elem = FoilElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_ND:
                        inst = FMT_INST.format(int(row.position))
                        elem = NDElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_IC:
                        inst = FMT_INST.format(int(row.position))
                        elem = ICElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_BCM:
                        inst = FMT_INST.format(int(row.position))
                        elem = BCMElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_EMS:
                        inst = FMT_INST.format(int(row.position))
                        elem = EMSElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_FC:
                        inst = FMT_INST.format(int(row.position))
                        elem = FCElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_HMR:
                        inst = FMT_INST.format(int(row.position))
                        elem = HMRElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_VD:
                        inst = FMT_INST.format(int(row.position))
                        elem = VDElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_SD:
                        inst = FMT_INST.format(int(row.position))
                        elem = SDElement(row.center_position, row.eff_length, row.diameter, row.name,
                                         desc=row.element_name,
                                         system=row.system, subsystem=row.subsystem, device=row.device,
                                         dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_WEDGE:
                        inst = FMT_INST.format(int(row.position))
                        elem = WedgeElement(row.center_position, row.eff_length, row.diameter, row.name,
                                            desc=row.element_name,
                                            system=row.system, subsystem=row.subsystem, device=row.device,
                                            dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_ELD:
                        inst = FMT_INST.format(int(row.position))
                        elem = ELDElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_PORT:
                        dtype = "" if row.device_type is None else row.device_type
                        subsystem = "" if row.subsystem is None else row.subsystem
                        inst = FMT_INST.format(int(row.position))
                        elem = PortElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=subsystem, device=row.device,
                                           dtype=dtype, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_COR:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = CorElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        elem.h = HCorElement(elem.z, 0.0, elem.aperture,
                                             "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                             system=row.system, subsystem=row.subsystem, device="DCH",
                                             dtype=row.device_type, inst=inst)
                        elem.v = VCorElement(elem.z, 0.0, elem.aperture,
                                             "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                             system=row.system, subsystem=row.subsystem, device="DCV",
                                             dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_HCOR:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = HCorElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_VCOR:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = VCorElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_ROT:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = RotElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_BEND:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "BEND_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = BendElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=dtype, inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_QUAD:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "QUAD_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = QuadElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=dtype, inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_SEXT:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "SEXT_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = SextElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=dtype, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_OCT:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "OCT_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = OctElement(row.center_position, row.eff_length, row.diameter, row.name,
                                          desc=row.element_name,
                                          system=row.system, subsystem=row.subsystem, device=row.device,
                                          dtype=dtype, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_ELC:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = ElectrodeElement(row.center_position, row.eff_length, row.diameter, row.name,
                                                desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device,
                                                dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_ACC:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = ColumnElement(row.center_position, row.eff_length, row.diameter, row.name,
                                             desc=row.element_name,
                                             system=row.system, subsystem=row.subsystem, device=row.device,
                                             dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_PTA:
                        row.device = self.d_map.get(row.device, row.device)
                        inst = FMT_INST.format(int(row.position))
                        elem = TargetElement(row.center_position, row.eff_length, row.diameter, row.name,
                                             desc=row.element_name,
                                             system=row.system, subsystem=row.subsystem, device=row.device,
                                             dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_EBEND:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "BEND_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = EBendElement(row.center_position, row.eff_length, row.diameter, row.name,
                                            desc=row.element_name,
                                            system=row.system, subsystem=row.subsystem, device=row.device,
                                            dtype=dtype, inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_EQUAD:
                        row.device = self.d_map.get(row.device, row.device)
                        dtype = "QUAD_{}".format(row.device_type)
                        inst = FMT_INST.format(int(row.position))
                        elem = EQuadElement(row.center_position, row.eff_length, row.diameter, row.name,
                                            desc=row.element_name,
                                            system=row.system, subsystem=row.subsystem, device=row.device,
                                            dtype=dtype, inst=inst)
                        drift_delta = self.apply_config(elem, sequence, drift_delta)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_SLIT:
                        inst = FMT_INST.format(int(row.position))
                        elem = SlitElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_CLLM:
                        inst = FMT_INST.format(int(row.position))
                        elem = CollimatorElement(row.center_position, row.eff_length, row.diameter, row.name,
                                                 desc=row.element_name,
                                                 system=row.system, subsystem=row.subsystem, device=row.device,
                                                 dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_CHP:
                        inst = FMT_INST.format(int(row.position))
                        elem = ChopperElement(row.center_position, row.eff_length, row.diameter, row.name,
                                              desc=row.element_name,
                                              system=row.system, subsystem=row.subsystem, device=row.device,
                                              dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_ATT:
                        inst = FMT_INST.format(int(row.position))
                        elem = AttenuatorElement(row.center_position, row.eff_length, row.diameter, row.name,
                                                 desc=row.element_name,
                                                 system=row.system, subsystem=row.subsystem, device=row.device,
                                                 dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_AP:
                        inst = FMT_INST.format(int(row.position))
                        elem = ApertureElement(row.center_position, row.eff_length, row.diameter, row.name,
                                               desc=row.element_name,
                                               system=row.system, subsystem=row.subsystem, device=row.device,
                                               dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in DEVICE_ALIAS_DUMP:
                        inst = FMT_INST.format(int(row.position))
                        elem = DumpElement(row.center_position, row.eff_length, row.diameter, row.name,
                                           desc=row.element_name,
                                           system=row.system, subsystem=row.subsystem, device=row.device,
                                           dtype=row.device_type, inst=inst)
                        subsequence.append(elem)

                    elif row.device in ["STRIP"]:
                        elem = self.get_prev_element(sequence, (StripElement,))
                        elem.z = row.center_position
                        elem.name = row.name
                        elem.desc = row.element_name
                        elem.system = row.system
                        elem.subsystem = row.subsystem

                    else:
                        raise Exception("Unsupported layout with device: '{}'".format(row.device))

                elif row.element_name is not None:

                    if row.element_name in ("bellow", "bellows", "bellow+tube", "2 bellows + tube", "bellow+box",
                                            "bellow+tube/box", "tube", "reducer flange", "bellow ?", "4 way cross ??",
                                            "BPM bellow", "bellow?", "bellow+tube ??", "6 way cross ??",
                                            "mhb box & bellows",
                                            "solenoid-entry", "solenoid-exit",
                                            "rf coupler",
                                            "2nd chicane not installed initially, replaced by a pipe",
                                            "fast valve sensor will not install",
                                            "no BMP here",
                                            "vacuum box - bellow",
                                            "Li module end flange", "bellow+spool",
                                            ):
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            row.center_position -= drift_delta / 2.0
                            drift_delta = 0.0
                        subsequence.append(
                            DriftElement(row.center_position, row.eff_length, row.diameter, name_drift(), desc=row.element_name))

                    elif row.element_name in ELEMENT_NAME_STRING_AS_DRIFT:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(
                            DriftElement(row.center_position, row.eff_length, row.diameter, name_drift(), desc=row.element_name))

                    elif row.element_name in ("stripper module", "carbon stripper chamber"):
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        try:
                            self.get_prev_element(sequence, (StripElement,)).length += row.eff_length
                        except:
                            subsequence.append(
                                DriftElement(row.center_position, row.eff_length, row.diameter, name_drift(), desc=row.element_name))

                    elif row.element_name == "#stripper":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        try:
                            self.get_prev_element(sequence, (StripElement,)).length += row.eff_length
                        except:
                            subsequence.append(
                                StripElement(row.center_position, row.eff_length, row.diameter, "CHARGE STRIPPER",
                                             desc=row.element_name))

                    elif row.element_name == "lithium film stripper":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elem = self.get_prev_element(sequence, (StripElement,))
                        elem.z = row.center_position
                        elem.name = row.name
                        elem.desc = row.element_name
                        elem.system = row.system
                        elem.subsystem = row.subsystem
                        elem.device = "STRIP"

                    else:
                        raise Exception("Unsupported layout with name: '{}'".format(row.element_name))

                elif row.eff_length != 0.0:
                    if drift_delta != 0.0:
                        row.eff_length += drift_delta
                        row.center_position -= drift_delta / 2.0
                        drift_delta = 0.0
                    desc = "drift_{}".format(ridx + 1) if row.element_name is None else row.element_name
                    subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, name_drift(), desc=desc))

            except Exception as e:
                raise RuntimeError("AccelFactory: {}: row {}: {}".format(str(e), ridx + 1, row))

        return accelerator

    # @staticmethod
    # def _channel_data(machine, name, system, subsystem, device, z, handle, field, etype):
    #     d = OrderedDict()
    #     d["machine"] = machine
    #     d["system"] = system
    #     d["subsystem"] = subsystem
    #     d["device"] = device
    #     # d["deviceType"] = elem.dtype
    #     d["z"] = z
    #     d["elemName"] = name
    #     d["elemHandle"] = handle
    #     d["elemField"] = field
    #     d["elemType"] = etype
    #     return d


def _parse_diameter(d):
    s = d.split("x", 2)
    if len(s) == 1:
        try:
            return [float(s[0]), float(s[0])]
        except:
            pass  # ignore exception

    elif len(s) == 2:
        try:
            # Note that the Expanded Lattice File specifies
            # the diameter as Height (Y) x Width (X)
            # which means we need to reverse the order.
            return [float(s[1]), float(s[0])]
        except:
            pass  # ignore exception

    return None


class _LayoutRow(XlfConfig):
    """
    LayoutRow contains the data from a single row of the layout sheet in the XLF.
    """

    @staticmethod
    def _cell_to_diameter(cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            return _parse_diameter(cell.value.strip())

        elif cell.ctype == xlrd.XL_CELL_NUMBER:
            return [cell.value, cell.value]

        return None

    @staticmethod
    def _cell_to_string(cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            value = cell.value.strip()
            if len(value) > 0:
                return value

        return None

    @staticmethod
    def _cell_to_float(cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            try:
                return float(cell.value)
            except:
                pass  # ignore exception

        elif cell.ctype == xlrd.XL_CELL_NUMBER:
            return cell.value

        return None

    def __init__(self, row, config):
        XlfConfig.__init__(self, config)
        self.system = self._cell_to_string(row[self._xlf_layout_system_idx])
        self.subsystem = self._cell_to_string(row[self._xlf_layout_subsystem_idx])
        self.position = self._cell_to_float(row[self._xlf_layout_position_idx])
        self.name = self._cell_to_string(row[self._xlf_layout_name_idx])
        self.device = self._cell_to_string(row[self._xlf_layout_device_idx])
        self.device_type = self._cell_to_string(row[self._xlf_layout_device_type_idx])
        self.element_name = self._cell_to_string(row[self._xlf_layout_element_name_idx])
        self.diameter = self._cell_to_diameter(row[self._xlf_layout_diameter_idx])
        self.eff_length = self._cell_to_float(row[self._xlf_layout_effective_length_idx])
        self.center_position = self._cell_to_float(row[self._xlf_layout_center_position_idx])

    def __str__(self):
        keys = ('system', 'subsystem', 'position', 'name', 'device', 'device_type',
                'element_name', 'eff_length', 'center_position', 'diameter')
        return type(self).__name__ + str({k:v for k,v in self.__dict__.items() if k in keys})


def _to_dict(s):
    l = s.replace(',',':').split(':')
    k = [s.strip() for s in l[0::2]]
    v = [s.strip() for s in l[1::2]]
    return dict(zip(k,v))
