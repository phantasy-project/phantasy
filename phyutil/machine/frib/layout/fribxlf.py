# encoding: UTF-8

"""Library for reading FRIB Expanded Lattice File (*.xlsx) and generating Accelerator Design Description."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

import os.path, re, logging, xlrd

from collections import OrderedDict

from ....phylib import cfg

from ....phylib.layout.accel import *


# configuration options

CONFIG_XLF_DIAMETER = "xlf_diameter"

CONFIG_XLF_DATA_FILE = "xlf_data_file"


# XLF parameters

_XLF_LAYOUT_SHEET_NAME = "LatticeLayout"

_XLF_LAYOUT_SHEET_START = 8

_XLF_LAYOUT_SYSTEM_IDX = 0

_XLF_LAYOUT_SUBSYSTEM_IDX = 1

_XLF_LAYOUT_DEVICE_IDX = 2

_XLF_LAYOUT_POSITION_IDX = 3

_XLF_LAYOUT_NAME_IDX = 4

_XLF_LAYOUT_DEVICE_TYPE_IDX = 5

_XLF_LAYOUT_ELEMENT_NAME_IDX = 6

_XLF_LAYOUT_DIAMETER_IDX = 7

_XLF_LAYOUT_EFFECTIVE_LENGTH_IDX = 10

_XLF_LAYOUT_CENTER_POSITION_IDX = 14


_LOGGER = logging.getLogger(__name__)



def build_accel(xlfpath=None, machine=None):
    """
    Convenience method for building ADD from Expanded Lattice File.
    """

    accel_factory = AccelFactory()

    if xlfpath != None:
        accel_factory.xlfpath = xlfpath

    if machine != None:
        accel_factory.machine = machine

    return accel_factory.build()


class AccelFactory(object):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.
    """
    def __init__(self):
        self.xlfpath = None
        self.machine = None
        self.diameter = None


    @property
    def xlfpath(self):
        return self._xlfpath

    @xlfpath.setter
    def xlfpath(self, xlfpath):
        if (xlfpath != None) and not isinstance(xlfpath, basestring):
            raise TypeError("AccelFactory: 'xlfpath' property must be type a string or None")
        self._xlfpath = xlfpath


    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, machine):
        if (machine != None) and not isinstance(machine, basestring):
            raise TypeError("AccelFactory: 'machine' property much be type string or None")
        self._machine = machine


    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter):
        if (diameter != None) and not isinstance(diameter, (int, float)):
            raise TypeError("AccelFactory: 'diameter' property must be type a number or None")
        self._diameter = diameter


    def _get_config_beta(self, dtype):
        return cfg.config.getfloat(dtype, CONFIG_CAV_BETA)

    def _has_config_beta(self, dtype):
        return cfg.config.has_option(dtype, CONFIG_CAV_BETA)


    def _get_config_voltage(self, dtype):
        return cfg.config.getfloat(dtype, CONFIG_CAV_VOLTAGE)

    def _has_config_voltage(self, dtype):
        return cfg.config.has_option(dtype, CONFIG_CAV_VOLTAGE)


    def _get_config_frequency(self, dtype):
        return cfg.config.getfloat(dtype, CONFIG_CAV_FREQUENCY)

    def _has_config_frequency(self, dtype):
        return cfg.config.has_option(dtype, CONFIG_CAV_FREQUENCY)


    def _get_config_bend_angle(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_BEND_ANGLE, False):
            return cfg.config.getfloat(elem.name, CONFIG_BEND_ANGLE, False)
        else:
            return cfg.config.getfloat(elem.dtype, CONFIG_BEND_ANGLE, False)

    def _has_config_bend_angle(self, elem):
        return cfg.config.has_option(elem.name, CONFIG_BEND_ANGLE, False) \
                or cfg.config.has_option(elem.dtype, CONFIG_BEND_ANGLE, False)


    def _get_config_bend_entr_angle(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_BEND_ENTR_ANGLE, False):
            return cfg.config.getfloat(elem.name, CONFIG_BEND_ENTR_ANGLE, False)
        else:
            return cfg.config.getfloat(elem.dtype, CONFIG_BEND_ENTR_ANGLE, False)

    def _has_config_bend_entr_angle(self, elem):
        return cfg.config.has_option(elem.name, CONFIG_BEND_ENTR_ANGLE, False) \
                or cfg.config.has_option(elem.dtype, CONFIG_BEND_ENTR_ANGLE, False)


    def _get_config_bend_exit_angle(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_BEND_EXIT_ANGLE, False):
            return cfg.config.getfloat(elem.name, CONFIG_BEND_EXIT_ANGLE, False)
        else:
            return cfg.config.getfloat(elem.dtype, CONFIG_BEND_EXIT_ANGLE, False)

    def _has_config_bend_exit_angle(self, elem):
        return cfg.config.has_option(elem.name, CONFIG_BEND_EXIT_ANGLE, False) \
                or cfg.config.has_option(elem.dtype, CONFIG_BEND_EXIT_ANGLE, False)


    def _get_config_length(self, dtype):
        return cfg.config.getfloat(dtype, CONFIG_LENGTH, False)

    def _has_config_length(self, dtype):
        return cfg.config.has_option(dtype, CONFIG_LENGTH, False)


    def _get_config_aperture(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_APERTURE, False):
            return cfg.config.getfloat(elem.name, CONFIG_APERTURE, False)
        else:
            return cfg.config.getfloat(elem.dtype, CONFIG_APERTURE, False)

    def _has_config_aperture(self, elem):
         return cfg.config.has_option(elem.name, CONFIG_APERTURE, False) \
                or cfg.config.has_option(elem.dtype, CONFIG_APERTURE, False)


    def _get_config_aperture_x(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_APERTURE_X, False):
            return cfg.config.getfloat(elem.name, CONFIG_APERTURE_X, False)
        else:
            return cfg.config.getfloat(elem.dtype, CONFIG_APERTURE_X, False)

    def _has_config_aperture_x(self, elem):
        return cfg.config.has_option(elem.name, CONFIG_APERTURE_X, False) \
                or cfg.config.has_option(elem.dtype, CONFIG_APERTURE_X, False)


    def _get_config_aperture_y(self, elem):
        if cfg.config.has_option(elem.name, CONFIG_APERTURE_Y, False):
            return cfg.config.getfloat(elem.name, CONFIG_APERTURE_Y, False)
        else:
            return cfg.config.getfloat(elem.dtype, CONFIG_APERTURE_Y, False)

    def _has_config_aperture_y(self, elem):
        return cfg.config.has_option(elem.name, CONFIG_APERTURE_Y, False) \
                or cfg.config.has_option(elem.dtype, CONFIG_APERTURE_Y, False)


    def _apply_config(self, elem):
        if self._has_config_aperture(elem):
            elem.aperture = self._get_config_aperture(elem)
            _LOGGER.info("AccelFactory: %s: aperture found in configuration: %s", elem.name, elem.aperture)

        if self._has_config_aperture_x(elem):
            elem.apertureX = self._get_config_aperture_x(elem)
            _LOGGER.info("AccelFactory: %s: aperture X found in configuration: %s", elem.name, elem.apertureX)

        if self._has_config_aperture_y(elem):
            elem.apertureY = self._get_config_aperture_y(elem)
            _LOGGER.info("AccelFactory: %s: aperture Y found in configuration: %s", elem.name, elem.apertureY)



    def build(self):

        xlfpath = self.xlfpath
        if (xlfpath == None) and cfg.config.has_default(CONFIG_XLF_DATA_FILE):
            xlfpath = cfg.config.get_default(CONFIG_XLF_DATA_FILE)
            if not os.path.isabs(xlfpath) and cfg.config_path != None:
                xlfpath = os.path.abspath(os.path.join(os.path.dirname(cfg.config_path), xlfpath))

        if xlfpath == None:
            raise ValueError("AccelFactory: Expanded Lattice File not specified, check the configuration.")

        if not os.path.isfile(xlfpath):
            raise ValueError("AccelFactory: Expanded Lattice File not found: '{}'".format(xlfpath))


        machine = self.machine
        if (machine == None) and cfg.config.has_default(CONFIG_MACHINE):
            machine = cfg.config.get_default(CONFIG_MACHINE)


        diameter = self.diameter
        if (diameter == None) and cfg.config.has_default(CONFIG_XLF_DIAMETER):
            diameter = _parse_diameter(cfg.config.get_default(CONFIG_XLF_DIAMETER))


        chanprefix = ""
        if (machine != None) and (len(machine.strip()) > 0):
            chanprefix = machine.strip()+":"


        wkbk = xlrd.open_workbook(xlfpath)

        if _XLF_LAYOUT_SHEET_NAME not in wkbk.sheet_names():
            raise RuntimeError("AccelFactory: Expanded Lattice File layout not found: '{}'".format(_XLF_LAYOUT_SHEET_NAME))

        layout = wkbk.sheet_by_name(_XLF_LAYOUT_SHEET_NAME)

        # skip front-end, perhaps this should be read too?
        for ridx in xrange(_XLF_LAYOUT_SHEET_START, layout.nrows):
            row = _LayoutRow(layout.row(ridx))
            if row.system == "LS1": break

        accelerator = Accelerator(os.path.splitext(os.path.basename(xlfpath))[0], desc="FRIB Linear Accelerator")

        sequence = None

        subsequence = None

        drift_delta = 0.0

        def get_prev_element(allow_types=(DriftElement,)):
            elements = subsequence.elements
            if len(elements) == 0:
                raise RuntimeError("AccelFactory: previous element not found")
            elif not isinstance(elements[-1], allow_types):
                raise RuntimeError("AccelFactory: previous element type invalid")
            return elements[-1]

        for ridx in xrange(ridx, layout.nrows):
            row = _LayoutRow(layout.row(ridx))

            # skip rows without length
            if row.eff_length == None:
                continue

            # clear lines with comments
            if row.system != None:
                for prefix in [  "dump", "SEGMENT", "LINAC", "Target" ]:
                    if row.system.startswith(prefix):
                        row.system = None
                        break

            # apply default values
            if row.diameter == None:
                if (subsequence != None) and (len(subsequence.elements) > 0):
                    # diameter from the aperture of the previous element
                    row.diameter = [subsequence.elements[-1].apertureX * 1000.0,
                                       subsequence.elements[-1].apertureY * 1000.0]
                elif diameter != None:
                    # diameter from the configuration default
                    row.diameter = diameter
                else:
                    raise RuntimeError("AccelFactory: Layout data missing diameter (row:{}): {}".format(ridx+1,row))

            # unit conversion
            row.diameter[0] *= 0.001
            row.diameter[1] *= 0.001


            if sequence == None:
                if row.system != None:
                    sequence = SeqElement(row.system)
                    accelerator.append(sequence)
                else:
                    raise RuntimeError("AccelFactory: Initial layout data must specifiy system (row:{}): {}".format(ridx+1,row))

            elif (row.system != None) and (row.system != sequence.name):
                sequence = SeqElement(row.system)
                accelerator.append(sequence)
                subsequence = None

            if subsequence == None:
                if row.subsystem != None:
                    subsequence = SeqElement(row.subsystem)
                    sequence.append(subsequence)
                else:
                    raise RuntimeError("AccelFactory: Initial layout data must specify subsystem (row:{}): {}".format(ridx+1,row))

            elif (row.subsystem != None) and (row.subsystem != subsequence.name):
                subsequence = SeqElement(row.subsystem)
                sequence.append(subsequence)


            try:
                if row.device != None:

                    if (drift_delta != 0.0) and (row.eff_length != 0.0):
                        # these 'named' elements do not support non-zero drift delta
                        raise RuntimeError("Unsupported drift delta on element: {}".format(row.element_name))

                    elif row.device in [ "GV", "FVS", "FAV"  ]:
                        subsequence.append(ValveElement(row.center_position, row.eff_length, row.diameter, row.name,
                                            desc=row.element_name, system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "CAV1", "CAV2", "CAV3", "CAV4", "CAV5", "CAV6", "CAV7", "CAV8" ]:
                        m = re.match("(b\\d{2}) cavity", row.element_name)
                        if not m:
                            raise RuntimeError("Unrecognized element name for cavity: '{}'".format(row.element_name))

                        dtype = "CAV_{}".format(m.group(1).upper())
                        inst = "D{:d}".format(int(row.position))

                        elem = CavityElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype, inst=inst)

                        if self._has_config_length(dtype):
                            drift_delta = (elem.length - self._get_config_length(dtype)) / 2.0
                            get_prev_element().length += drift_delta
                            get_prev_element().z += drift_delta
                            elem.length -= drift_delta * 2.0

                        if self._has_config_beta(dtype):
                            elem.beta = self._get_config_beta(dtype)
                        else:
                            raise RuntimeError("Cavity parameter 'beta' not found")

                        if self._has_config_voltage(dtype):
                            elem.voltage = self._get_config_voltage(dtype)
                        else:
                            raise RuntimeError("Cavity parameter 'voltage' not found")

                        if self._has_config_frequency(dtype):
                            elem.frequency = self._get_config_frequency(dtype)
                        else:
                            raise RuntimeError("Cavity parameter 'frequency' not found")

                        elem.channels.phase_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_CSET".format(chanprefix, elem=elem)
                        elem.channels.phase_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_RSET".format(chanprefix, elem=elem)
                        elem.channels.phase_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_RD".format(chanprefix, elem=elem)
                        elem.channels.amplitude_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:AMPL_CSET".format(chanprefix, elem=elem)
                        elem.channels.amplitude_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:AMPL_RSET".format(chanprefix, elem=elem)
                        elem.channels.amplitude_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:AMPL_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.phase_cset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "setpoint", "PHA", "CAV")
                        accelerator.channels[elem.channels.phase_rset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readset", "PHA", "CAV")
                        accelerator.channels[elem.channels.phase_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "PHA", "CAV")
                        accelerator.channels[elem.channels.amplitude_cset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "setpoint", "AMP", "CAV")
                        accelerator.channels[elem.channels.amplitude_rset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readset", "AMP", "CAV")
                        accelerator.channels[elem.channels.amplitude_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "AMP", "CAV")

                        subsequence.append(elem)

                    elif row.device in [ "SOL1", "SOL2", "SOL3" ]:
                        dtype = "SOL_{}".format(row.device_type)
                        inst = "D{:d}".format(int(row.position))

                        elem = SolCorrElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype, inst=inst)

                        if self._has_config_length(dtype):
                            drift_delta = (elem.length - self._get_config_length(dtype)) / 2.0
                            get_prev_element().length += drift_delta
                            get_prev_element().z += drift_delta
                            elem.length -= drift_delta * 2.0

                        elem.channels.field_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_CSET".format(chanprefix, elem=elem)
                        elem.channels.field_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RSET".format(chanprefix, elem=elem)
                        elem.channels.field_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RD".format(chanprefix, elem=elem)
                        elem.channels.hkick_cset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_CSET".format(chanprefix, elem=elem)
                        elem.channels.hkick_rset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RSET".format(chanprefix, elem=elem)
                        elem.channels.hkick_read = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RD".format(chanprefix, elem=elem)
                        elem.channels.vkick_cset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_CSET".format(chanprefix, elem=elem)
                        elem.channels.vkick_rset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RSET".format(chanprefix, elem=elem)
                        elem.channels.vkick_read = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.field_cset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "setpoint", "B", "SOL")
                        accelerator.channels[elem.channels.field_rset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readset", "B", "SOL")
                        accelerator.channels[elem.channels.field_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "B", "SOL")
                        accelerator.channels[elem.channels.hkick_cset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCH", elem.z, "setpoint", "ANG", "HCOR")
                        accelerator.channels[elem.channels.hkick_rset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCH", elem.z, "readset", "ANG", "HCOR")
                        accelerator.channels[elem.channels.hkick_read] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCH", elem.z, "readback", "ANG", "HCOR")
                        accelerator.channels[elem.channels.vkick_cset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCV", elem.z, "setpoint", "ANG", "VCOR")
                        accelerator.channels[elem.channels.vkick_rset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCV", elem.z, "readset", "ANG", "VCOR")
                        accelerator.channels[elem.channels.vkick_read] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCV", elem.z, "readback", "ANG", "VCOR")

                        subsequence.append(elem)

                    elif row.device in [ "BPM" ]:

                        inst = "D{:d}".format(int(row.position))

                        elem = BPMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        elem.channels.hposition_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:X_RD".format(chanprefix, elem=elem)
                        elem.channels.vposition_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:Y_RD".format(chanprefix, elem=elem)
                        elem.channels.phase_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.hposition_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "X", elem.device)
                        accelerator.channels[elem.channels.vposition_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "Y", elem.device)
                        accelerator.channels[elem.channels.phase_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "PHA", elem.device)

                        subsequence.append(elem)

                    elif row.device in [ "PM" ]:

                        inst = "D{:d}".format(int(row.position))

                        elem = PMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                           system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        elem.channels.hposition_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:X_RD".format(chanprefix, elem=elem)
                        elem.channels.vposition_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:Y_RD".format(chanprefix, elem=elem)
                        elem.channels.hsize_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:XRMS_RD".format(chanprefix, elem=elem)
                        elem.channels.vsize_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:YRMS_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.hposition_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "X", elem.device)
                        accelerator.channels[elem.channels.vposition_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "Y", elem.device)
                        accelerator.channels[elem.channels.hsize_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "XRMS", elem.device)
                        accelerator.channels[elem.channels.vsize_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "YRMS", elem.device)

                        subsequence.append(elem)

                    elif row.device in [ "BL" ]:
                        subsequence.append(BLElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "BLM" ]:
                        subsequence.append(BLMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "BCM" ]:
                        subsequence.append(BCMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PORT" ]:
                        dtype = "" if row.device_type == None else row.device_type
                        subsystem = "" if row.subsystem == None else row.subsystem
                        subsequence.append(PortElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                                system=row.system, subsystem=subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "DC", "DC0", "CH" ]:

                        inst = "D{:d}".format(int(row.position))

                        elem = CorrElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        elem.channels.hkick_cset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_CSET".format(chanprefix, elem=elem)
                        elem.channels.hkick_rset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RSET".format(chanprefix, elem=elem)
                        elem.channels.hkick_read = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RD".format(chanprefix, elem=elem)
                        elem.channels.vkick_cset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_CSET".format(chanprefix, elem=elem)
                        elem.channels.vkick_rset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RSET".format(chanprefix, elem=elem)
                        elem.channels.vkick_read = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.hkick_cset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCH", elem.z, "setpoint", "ANG", "HCOR")
                        accelerator.channels[elem.channels.hkick_rset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCH", elem.z, "readset", "ANG", "HCOR")
                        accelerator.channels[elem.channels.hkick_read] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCH", elem.z, "readback", "ANG", "HCOR")
                        accelerator.channels[elem.channels.vkick_cset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCV", elem.z, "setpoint", "ANG", "VCOR")
                        accelerator.channels[elem.channels.vkick_rset] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCV", elem.z, "readset", "ANG", "VCOR")
                        accelerator.channels[elem.channels.vkick_read] = self._channel_data(machine, "{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem),
                                                                                                elem.system, elem.subsystem, "DCV", elem.z, "readback", "ANG", "VCOR")

                        subsequence.append(elem)

                    elif row.device in [ "DH" ]:
                        m = re.match("dipole\\s*\\(?(.*)deg\\)?", row.element_name)
                        if not m:
                            raise RuntimeError("Unrecognized element name for bend magnet: '{}'".format(row.element_name))

                        dtype = "BEND_{}".format(row.device_type)
                        inst = "D{:d}".format(int(row.position))

                        elem = BendElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype, inst=inst)

                        self._apply_config(elem)

                        elem.angle = float(m.group(1))

                        if self._has_config_bend_angle(elem):
                            elem.angle = self._get_config_bend_angle(elem)
                            _LOGGER.info("AccelFactory: %s: angle found in configuration: %s", elem.name, elem.angle)

                        if self._has_config_bend_entr_angle(elem):
                            elem.entrAngle = self._get_config_bend_entr_angle(elem)
                            _LOGGER.info("AccelFactory: %s: entrance angle found in configuration: %s", elem.name, elem.entrAngle)

                        if self._has_config_bend_exit_angle(elem):
                            elem.exitAngle = self._get_config_bend_exit_angle(elem)
                            _LOGGER.info("AccelFactory: %s: exit angle found in configuration: %s", elem.name, elem.exitAngle)

                        elem.channels.field_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_CSET".format(chanprefix, elem=elem)
                        elem.channels.field_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RSET".format(chanprefix, elem=elem)
                        elem.channels.field_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.field_cset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "setpoint", "B", "BEND")
                        accelerator.channels[elem.channels.field_rset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readset", "B", "BEND")
                        accelerator.channels[elem.channels.field_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "B", "BEND")

                        subsequence.append(elem)


                    elif row.device in [ "QH", "QV" ]:

                        dtype = "QUAD_{}".format(row.device_type)
                        inst = "D{:d}".format(int(row.position))

                        elem = QuadElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype, inst=inst)

                        elem.channels.gradient_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:GRAD_CSET".format(chanprefix, elem=elem)
                        elem.channels.gradient_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:GRAD_RSET".format(chanprefix, elem=elem)
                        elem.channels.gradient_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:GRAD_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.gradient_cset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "setpoint", "GRAD", "QUAD")
                        accelerator.channels[elem.channels.gradient_rset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readset", "GRAD", "QUAD")
                        accelerator.channels[elem.channels.gradient_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "GRAD", "QUAD")

                        subsequence.append(elem)

                    elif row.device in [ "S" ]:

                        inst = "D{:d}".format(int(row.position))

                        elem = HexElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                   system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        elem.channels.field_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_CSET".format(chanprefix, elem=elem)
                        elem.channels.field_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RSET".format(chanprefix, elem=elem)
                        elem.channels.field_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RD".format(chanprefix, elem=elem)
                        # channel metadata (for channel finder)
                        accelerator.channels[elem.channels.field_cset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "setpoint", "B", "SEXT")
                        accelerator.channels[elem.channels.field_rset] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readset", "B", "SEXT")
                        accelerator.channels[elem.channels.field_read] = self._channel_data(machine, elem.name, elem.system, elem.subsystem, elem.device, elem.z, "readback", "B", "SEXT")

                        subsequence.append(elem)

                    elif row.device in [ "SLH" ]:
                        # use dift to represent slit for now
                        subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.device in [ "dump" ]:
                        subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.device in [ "STRIP" ]:
                        elem = get_prev_element((ChgStripElement))
                        elem.z = row.center_position
                        elem.name = row.name
                        elem.desc = row.element_name
                        elem.system = row.system
                        elem.subsystem = row.subsystem

                    else:
                        raise Exception("Unsupported layout with device: '{}'".format(row.device))

                elif row.element_name != None:

                    if row.element_name in [ "bellow", "bellows", "bellow+tube", "2 bellows + tube" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            row.center_position -= drift_delta
                            drift_delta = 0.0
                        subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "solenoid-entry", "solenoid-exit" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            row.center_position -= drift_delta
                            drift_delta = 0.0
                        subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "coil-out", "coil-out (assumed)", "coil out", "coil out + leads" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "BPM-box", "diagnostic box", "vacuum box" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name == "stripper module":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        try:
                            get_prev_element((ChgStripElement)).length += row.eff_length
                        except:
                            subsequence.append(ChgStripElement(row.center_position, row.eff_length, row.diameter, "CHARGE STRIPPER", desc=row.element_name))

                    elif row.element_name == "lithium film stripper":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elem = get_prev_element((ChgStripElement))
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
                            row.center_position -= drift_delta
                            drift_delta = 0.0
                    desc = "drift_{}".format(ridx+1) if row.element_name == None else row.element_name
                    subsequence.append(DriftElement(row.center_position, row.eff_length, row.diameter, desc=desc))

            except Exception as e:
                raise RuntimeError("AccelFactory: {}: row {}: {}".format(str(e), ridx+1, row))

        return accelerator

    @staticmethod
    def _channel_data(machine, name, system, subsystem, device, z, handle, field, etype):
        d = OrderedDict()
        d["machine"] = machine
        d["system"] = system
        d["subsystem"] = subsystem
        d["device"] = device
        #d["deviceType"] = elem.dtype
        d["z"] = z
        d["elemName"] = name
        d["elemHandle"] = handle
        d["elemField"] = field
        d["elemType"] = etype
        return d


def _parse_diameter(d):
    s = d.split("x", 2)
    if len(s) == 1:
        try:
            return [float(s[0]), float(s[0])]
        except:
            pass # ignore exception

    elif len(s) == 2:
        try:
            # Note that the Expanded Lattice File specifies
            # the diameter as Height (Y) x Width (X)
            # which means we need to reverse the order.
            return [float(s[1]), float(s[0])]
        except:
            pass # ignore exception

    return None


class _LayoutRow(object):
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
                pass # ignore exception

        elif cell.ctype == xlrd.XL_CELL_NUMBER:
            return cell.value

        return None


    def __init__(self, row):
        self.system = self._cell_to_string(row[_XLF_LAYOUT_SYSTEM_IDX])
        self.subsystem = self._cell_to_string(row[_XLF_LAYOUT_SUBSYSTEM_IDX])
        self.position = self._cell_to_float(row[_XLF_LAYOUT_POSITION_IDX])
        self.name = self._cell_to_string(row[_XLF_LAYOUT_NAME_IDX])
        self.device = self._cell_to_string(row[_XLF_LAYOUT_DEVICE_IDX])
        self.device_type = self._cell_to_string(row[_XLF_LAYOUT_DEVICE_TYPE_IDX])
        self.element_name = self._cell_to_string(row[_XLF_LAYOUT_ELEMENT_NAME_IDX])
        self.diameter = self._cell_to_diameter(row[_XLF_LAYOUT_DIAMETER_IDX])
        self.eff_length = self._cell_to_float(row[_XLF_LAYOUT_EFFECTIVE_LENGTH_IDX])
        self.center_position = self._cell_to_float(row[_XLF_LAYOUT_CENTER_POSITION_IDX])


    def __str__(self):
        return type(self).__name__+str(self.__dict__)
