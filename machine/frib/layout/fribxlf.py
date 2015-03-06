# encoding: UTF-8

"""
Implement phylib command 'impact-input'.
"""

from __future__ import print_function

import os.path, re, xlrd


from phylib import cfg

from phylib.layout import accel


_XLF_LAYOUT_SHEET_START = 8

_XLF_LAYOUT_SHEET_NAME = "LatticeLayout"

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



def build_accel(xlfpath=None, config=None, prefix=""):
    """
    Convenience method for building ADD from Expanded Lattice File.
    """

    # Read in configuration for default location!

    accel_factory = AccelFactory(config)

    accel_factory.xlfpath = xlfpath
    
    accel_factory.prefix = prefix

    return accel_factory.build()


class AccelFactory(object):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.

    :param config: Configuration data
    """
    def __init__(self, config):
        if not isinstance(config, cfg.Configuration):
            raise TypeError("AccelFactory: Configuration data must be specified")
        self._config = config
        self.xlfpath = None
        self.diameter = None


    @property
    def xlfpath(self):
        return self._xlfpath

    @xlfpath.setter
    def xlfpath(self, xlfpath):
        if (xlfpath != None) and not isinstance(xlfpath, str):
            raise TypeError("AccelFactory: 'xlfpath' property must be type a string or None")
        self._xlfpath = xlfpath


    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter):
        if (diameter != None) and not isinstance(cavity_info, (int, float)):
            raise TypeError("AccelFactory: 'diameter' property must be type a number or None")
        self._diameter = diameter


    def _get_config_xlfpath(self):
        if self.xlfpath != None:
            return self.xlfpath
        else:
            return self._config.get(cfg.OPTION_XLF_FILE_PATH)

    def _has_config_xlfpath(self):
        return (self.xlfpath != None) or \
                self._config.has_default(cfg.OPTION_XLF_FILE_PATH)


    def _get_config_diameter(self):
        if self.diameter != None:
            return self.diameter
        else:
            return self._config.getfloat_default(cfg.OPTION_DIAMETER)

    def _has_config_diameter(self):
        return (self.diameter != None) or \
            self._config.has_default(cfg.OPTION_DIAMETER)


    def _get_config_beta(self, dtype):
        return self._config.getfloat(dtype, cfg.OPTION_BETA)

    def _has_config_beta(self, dtype):
        return self._config.has_option(dtype, cfg.OPTION_BETA)


    def _get_config_voltage(self, dtype):
        return self._config.getfloat(dtype, cfg.OPTION_VOLTAGE)

    def _has_config_voltage(self, dtype):
        return self._config.has_option(dtype, cfg.OPTION_VOLTAGE)


    def _get_config_frequency(self, dtype):
        return self._config.getfloat(dtype, cfg.OPTION_FREQUENCY)

    def _has_config_frequency(self, dtype):
        return self._config.has_option(dtype, cfg.OPTION_FREQUENCY)


    def _get_config_length(self, dtype):
        return self._config.getfloat(dtype, cfg.OPTION_LENGTH, False)

    def _has_config_length(self, dtype):
        return self._config.has_option(dtype, cfg.OPTION_LENGTH, False)


    def build(self):
        
        if self.xlfpath != None:
            xlfpath = self.xlfpath
        elif self.has_config_xlfpath():
            xlfpath = self.get_config_xlfpath()
        else:
            raise Exception("AccelFactory: Expanded Lattice File not specified")

        if not os.path.isfile(xlfpath):
            raise Exception("AccelFactory: Expanded Lattice File not found: '{}'".format(self.xlfpath))
  
        wkbk = xlrd.open_workbook(xlfpath)

        if _XLF_LAYOUT_SHEET_NAME not in wkbk.sheet_names():
            raise Exception("AccelFactory: Expanded Lattice File layout not found: '{}'".format(_XLF_LAYOUT_SHEET_NAME))

        layout = wkbk.sheet_by_name(_XLF_LAYOUT_SHEET_NAME)

        # skip front-end, perhaps this should be read too?
        for ridx in xrange(_XLF_LAYOUT_SHEET_START, layout.nrows):
            row = _LayoutRow(layout.row(ridx))
            if row.system == "LS1": break

        accelerator = accel.Accelerator(self.xlfpath)

        sequence = None

        subsequence = None

        drift_delta = 0.0

        def get_prev_element(allow_types=(accel.DriftElement,)):
            elements = subsequence.elements
            if len(elements) == 0:
                raise Exception("AccelFactory: previous element not found")
            elif not isinstance(elements[-1], allow_types):
                raise Exception("AccelFactory: previous element type invalid")
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
                if self._has_config_diameter():
                    row.diameter = self._get_config_diameter()
                else:
                    raise Exception("AccelFactory: Layout data missing diameter (row:{}): {}".format(ridx+1,row))

            # unit conversion
            row.diameter *= 0.001


            if sequence == None:
                if row.system != None:
                    sequence = accel.SeqElement(row.system)
                    accelerator.append(sequence)
                else:
                    raise Exception("AccelFactory: Initial layout data must specifiy system (row:{}): {}".format(ridx+1,row))

            elif (row.system != None) and (row.system != sequence.name):
                sequence = accel.SeqElement(row.system)
                accelerator.append(sequence)
                subsequence = None

            if subsequence == None:
                if row.subsystem != None:
                    subsequence = accel.SeqElement(row.subsystem)
                    sequence.append(subsequence)
                else:
                    raise Exception("AccelFactory: Initial layout data must specify subsystem (row:{}): {}".format(ridx+1,row))

            elif (row.subsystem != None) and (row.subsystem != subsequence.name):
                subsequence = accel.SeqElement(row.subsystem)
                sequence.append(subsequence)


            try:
                if row.device != None:

                    if (drift_delta != 0.0) and (row.eff_length != 0.0):
                        # these 'named' elements do not support non-zero drift delta
                        raise Exception("Unsupported drift delta on element: {}".format(row.element_name))

                    elif row.device in [ "GV", "FVS", "FAV"  ]:
                        subsequence.append(accel.ValveElement(row.center_position, row.eff_length, row.diameter, row.name,
                                            desc=row.element_name, system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "CAV1", "CAV2", "CAV3", "CAV4", "CAV5", "CAV6", "CAV7", "CAV8" ]:
                        m = re.match("(b\\d{2}) cavity", row.element_name)
                        if not m:
                            raise Exception("Unrecognized element name for cavity: '{}'".format(row.element_name))

                        dtype = "CAV_{}".format(m.group(1).upper())
                        inst = "D{:d}".format(int(row.position))

                        elem = accel.CavityElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype, inst=inst)

                        if self._has_config_length(dtype):
                            drift_delta = (elem.length - self._get_config_length(dtype)) / 2.0
                            get_prev_element().length += drift_delta
                            get_prev_element().z += drift_delta
                            elem.length -= drift_delta * 2.0

                        if self._has_config_beta(dtype):
                            elem.beta = self._get_config_beta(dtype)
                        else:
                            raise Exception("Cavity parameter 'beta' not found")

                        if self._has_config_voltage(dtype):
                            elem.voltage = self._get_config_voltage(dtype)
                        else:
                            raise Exception("Cavity parameter 'voltage' not found")
                        
                        if self._has_config_frequency(dtype):
                            elem.frequency = self._get_config_frequency(dtype)
                        else:
                            raise Exception("Cavity parameter 'frequency' not found")

                        elem.channels.phase_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_CSET".format(self.prefix, elem=elem)
                        elem.channels.phase_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_RSET".format(self.prefix, elem=elem)
                        elem.channels.phase_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:PHA_RD".format(self.prefix, elem=elem)
                        elem.channels.amplitude_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:AMPL_CSET".format(self.prefix, elem=elem)
                        elem.channels.amplitude_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:AMPL_RSET".format(self.prefix, elem=elem)
                        elem.channels.amplitude_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:AMPL_RD".format(self.prefix, elem=elem)

                        subsequence.append(elem)

                    elif row.device in [ "SOL1", "SOL2", "SOL3" ]:
                        dtype = "SOL_{}".format(row.device_type)
                        inst = "D{:d}".format(int(row.position))

                        elem = accel.SolCorrElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype, inst=inst)

                        if self._has_config_length(dtype):
                            drift_delta = (elem.length - self._get_config_length(dtype)) / 2.0
                            get_prev_element().length += drift_delta
                            get_prev_element().z += drift_delta
                            elem.length -= drift_delta * 2.0

                        elem.channels.field_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_CSET".format(self.prefix, elem=elem)
                        elem.channels.field_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RSET".format(self.prefix, elem=elem)
                        elem.channels.field_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:B_RD".format(self.prefix, elem=elem)
                        elem.channels.hkick_cset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_CSET".format(self.prefix, elem=elem)
                        elem.channels.hkick_rset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RSET".format(self.prefix, elem=elem)
                        elem.channels.hkick_read = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RD".format(self.prefix, elem=elem)
                        elem.channels.vkick_cset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_CSET".format(self.prefix, elem=elem)
                        elem.channels.vkick_rset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RSET".format(self.prefix, elem=elem)
                        elem.channels.vkick_read = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RD".format(self.prefix, elem=elem)

                        subsequence.append(elem)

                    elif row.device in [ "BLM" ]:
                        subsequence.append(accel.BLMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "BPM" ]:
                    
                        inst = "D{:d}".format(int(row.position))
                    
                        elem = accel.BPMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)
                
                        elem.channels.hposition_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:POSH_RD".format(self.prefix, elem=elem)
                        elem.channels.vposition_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:POSV_RD".format(self.prefix, elem=elem)

                        subsequence.append(elem)

                    elif row.device in [ "BL" ]:
                        subsequence.append(accel.BLElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PM" ]:
                        subsequence.append(accel.PMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "BCM" ]:
                        subsequence.append(accel.BCMElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PORT" ]:
                        dtype = "" if row.device_type == None else row.device_type
                        subsystem = "" if row.subsystem == None else row.subsystem                      
                        subsequence.append(accel.PortElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                                system=row.system, subsystem=subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "DC", "DC0" ]:

                        inst = "D{:d}".format(int(row.position))

                        elem = accel.CorrElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        elem.channels.hkick_cset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_CSET".format(self.prefix, elem=elem)
                        elem.channels.hkick_rset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RSET".format(self.prefix, elem=elem)
                        elem.channels.hkick_read = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RD".format(self.prefix, elem=elem)
                        elem.channels.vkick_cset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_CSET".format(self.prefix, elem=elem)
                        elem.channels.vkick_rset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RSET".format(self.prefix, elem=elem)
                        elem.channels.vkick_read = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RD".format(self.prefix, elem=elem)

                        subsequence.append(elem)

                    elif row.device in [ "DH", "CH" ]:

                        inst = "D{:d}".format(int(row.position))

                        elem = accel.BendElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        #elem.channels.hkick_cset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_CSET".format(self.prefix, elem=elem)
                        #elem.channels.hkick_rset = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RSET".format(self.prefix, elem=elem)
                        #elem.channels.hkick_read = "{}{elem.system}_{elem.subsystem}:DCH_{elem.inst}:ANG_RD".format(self.prefix, elem=elem)
                        #elem.channels.vkick_cset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_CSET".format(self.prefix, elem=elem)
                        #elem.channels.vkick_rset = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RSET".format(self.prefix, elem=elem)
                        #elem.channels.vkick_read = "{}{elem.system}_{elem.subsystem}:DCV_{elem.inst}:ANG_RD".format(self.prefix, elem=elem)

                        subsequence.append(elem)


                    elif row.device in [ "QH", "QV" ]:
                        
                        inst = "D{:d}".format(int(row.position))
                        
                        elem = accel.QuadElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type, inst=inst)

                        elem.channels.gradient_cset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:GRAD_CSET".format(self.prefix, elem=elem)
                        elem.channels.gradient_rset = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:GRAD_RSET".format(self.prefix, elem=elem)
                        elem.channels.gradient_read = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}:GRAD_RD".format(self.prefix, elem=elem)

                        subsequence.append(elem)

                    elif row.device in [ "S" ]:
                        subsequence.append(accel.HexElement(row.center_position, row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "SLH" ]:
                        # use dift to represent slit for now
                        subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.device in [ "dump" ]:
                        subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.device in [ "STRIP" ]:
                        elem = get_prev_element((accel.ChgStripElement))
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
                        subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "solenoid-entry", "solenoid-exit" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            row.center_position -= drift_delta
                            drift_delta = 0.0
                        subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "coil-out", "coil-out (assumed)", "coil out", "coil out + leads" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))                

                    elif row.element_name in [ "BPM-box", "diagnostic box", "vacuum box" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name == "stripper module":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        try:
                            get_prev_element((accel.ChgStripElement)).length += row.eff_length
                        except:
                            subsequence.append(accel.ChgStripElement(row.center_position, row.eff_length, row.diameter, "CHARGE STRIPPER", desc=row.element_name))

                    elif row.element_name == "lithium film stripper":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elem = get_prev_element((accel.ChgStripElement))
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
                    subsequence.append(accel.DriftElement(row.center_position, row.eff_length, row.diameter, desc=desc))

            except Exception as e:
                raise Exception("AccelFactory: {}: row {}: {}".format(str(e), ridx+1, row))

        return accelerator



class _LayoutRow(object):
    """
    LayoutRow contains the data from a single row of the layout sheet in the XLF.
    """

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
        self.diameter = self._cell_to_float(row[_XLF_LAYOUT_DIAMETER_IDX])
        self.eff_length = self._cell_to_float(row[_XLF_LAYOUT_EFFECTIVE_LENGTH_IDX])
        self.center_position = self._cell_to_float(row[_XLF_LAYOUT_CENTER_POSITION_IDX])


    def __str__(self):
        return type(self).__name__+str(self.__dict__)
