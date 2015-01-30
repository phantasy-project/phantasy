# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys, os.path, re, json, xlrd

#from ..add import accelerator as accel

from ..data.config import Config

from ..add import pasv, diag, mag, cs, rf, seq, accel
#from ..add import 


XLF_LAYOUT_SHEET_START = 8

XLF_LAYOUT_SHEET_NAME = "LatticeLayout"

XLF_LAYOUT_SYSTEM_IDX = 0

XLF_LAYOUT_SUBSYSTEM_IDX = 1

XLF_LAYOUT_DEVICE_IDX = 2

XLF_LAYOUT_POSITION_IDX = 3

XLF_LAYOUT_NAME_IDX = 4

XLF_LAYOUT_DEVICE_TYPE_IDX = 5

XLF_LAYOUT_ELEMENT_NAME_IDX = 6

XLF_LAYOUT_DIAMETER_IDX = 7

XLF_LAYOUT_EFFECTIVE_LENGTH_IDX = 10



class AccelFactory(object):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.

    :param xlfpath: File path to Expanded Lattice File (.xlsx)
    :type xlfpath: string
    :param diameter: Default diameter to use for elements (mm)
    :type diameter: number
    :rtype Accelerator
    """

    _CONFIG_XLF = "xlf"

    _CONFIG_DEVICES = "devices"

    _CONFIG_XLF_DEFAULTS = "defaults"

    _CONFIG_XLF_DIAMETER = "diameter"

    def __init__(self, xlfpath, config=None):
        self.xlfpath = xlfpath
        if config != None:
            self.config = config
        else:
            self.config = OrderedDict()

    @property
    def config(self, config):
        return self._config

    @config.setter
    def config(self, config):
        self._config = OrderedDict(config)
        
        if self._CONFIG_DEVICES in self._config:
            if not isinstance(self._config[self._CONFIG_DEVICES], dict):
                raise TypeError("ADDFactory: '{}' config property not type 'dict'".foramt(self._CONFIG_DEVICES))
        else:
            self._config[self._CONFIG_DEVICES] = OrderedDict()

        if self._CONFIG_XLF_DEFAULTS in self._config:
            if not isinstance(self._config[self._CONFIG_XLF_DEFAULTS], dict):
                raise TypeError("ADDFactory: '{}' config property not type 'dict'".foramt(self._CONFIG_XLF_DEFAULTS))
        else:
            self._config[self._CONFIG_XLF_DEFAULTS] = OrderedDict()


    def get_config_prop(self, property, dtype=None):
        """
        Get the value of a configuration property.
        """
        if dtype != None:
            if dtype in self.config[self._CONFIG_DEVICES]:
                if prop in self.config[self._CONFIG_DEVICES][dtype]:
                    return self.config[self._CONFIG_DEVICES][dtype][prop]

        if prop in self.config[self._CONFIG_XLF_DEFAULTS]
            return self.config[self._CONFIG_XLF_DEFAULTS][prop]
            
        return None


    def set_config_prop(self, prop, value, dtype=None):
        """
        Set the value of a configuration property.
        """
        if dtype != None:
            if dtype not in self.config[self._CONFIG_DEVICES]:
                self.config[self._CONFIG_DEVICES][dtype] = OrderedDict()
            self.config[self._CONFIG_DEVICES][dtype][prop] = value
        else:
            self.config[self._CONFIG_XLF_DEFAULTS][prop] = value


    def build(self):
        
        if not os.path.isfile(xlfpath):
            raise Exception("ADDFactory: Expanded Lattice File not found: '{}'".format(xlfpath))
  
        wkbk = xlrd.open_workbook(xlfpath)

        if XLF_LAYOUT_SHEET_NAME not in wkbk.sheet_names():
            raise Exception("ADDFactory: Expanded Lattice File layout not found: '{}'".format(XLF_LAYOUT_SHEET_NAME))

        layout = wkbk.sheet_by_name(XLF_LAYOUT_SHEET_NAME)

        # skip front-end, perhaps this should be read too?
        for ridx in xrange(XLF_LAYOUT_SHEET_START, layout.nrows):
            row = _LayoutRow(layout.row(ridx))
            if row.system == "LS1": break

        elements = []

        seqname = None
        sequences = []

        subseqname = None
        subsequences = []

        drift_delta = 0.0

        def get_prev_element(allow_types=(pasv.DriftElement,)):
            if len(elements) == 0:
                raise Exception("ADDFactory: previous element not found")
            elif not isinstance(elements[-1], allow_types):
                raise Exception("ADDFactory: previous element type invalid")
            return elements[-1]

        for ridx in xrange(ridx, layout.nrows):
            row = _LayoutRow(layout.row(ridx))

            # apply default values
            if row.diameter == None:
                row.diameter = get_config_prop(diameter, row.device, row.device_type)

            if row.eff_length == None:
                continue

            # unit conversion
            row.diameter *= 0.001


            if subseqname == None:
                if row.subsystem != None:
                    subseqname = row.subsystem
                else:
                    raise Exception("XLF: Initial layout data must specify subsystem (row:{}): {}".format(ridx+1,row))

            elif (row.subsystem != None) and (row.subsystem != subseqname):
                subsequences.append(seq.SeqElement(elements, name=subseqname))
                subseqname = row.subsystem
                elements = []


            if seqname == None:
                if row.system != None:
                    seqname = row.system
                else:
                    raise Exception("XLF: Initial layout data must specifiy system (row:{}): {}".format(ridx+1,row))

            elif (row.system != None) and (row.system != seqname):
                sequences.append(seq.SeqElement(subsequences, name=seqname))
                seqname = row.system
                subsequences = []


            try:
                if row.device != None:

                    if drift_delta != 0.0:
                        # these 'named' elements do not support non-zero drift delta
                        raise Exception("Unsupported drift delta on element: {}".format(row.element_name))

                    elif row.device in [ "GV", "FVS", "FAV"  ]:
                        elements.append(pasv.ValveElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "CAV1", "CAV2", "CAV3", "CAV4", "CAV5", "CAV6", "CAV7", "CAV8" ]:
                        m = re.match("(b\\d{2}) cavity", row.element_name)
                        if not m:
                            raise Exception("Unrecognized element name for cavity: '{}'".format(row.element_name))

                        cav = rf.CavityElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device, dtype=m.group(1).upper())



                        cav.settings.phase = get_config_prop("setting_phase", ).format(cav)
                        cav.settings.amplitude = get_config_prop("setting_amplitude").format(cav)



                        length = get_config_prop("length", device, dtype)
                        if length != None:    
                            drift_delta = (cav.length - length) / 2.0
                            get_prev_element().length += drift_delta
                            cav.length = length

                        beta = get_config_prop("beta", cav.device, cav.dtype)
                        if beta != None:
                            cav.beta = beta

                        voltage = get_config_prop("voltage", cav.device, cav.dtype)
                        if voltage != None:
                            cav.voltage = voltage
                        
                        frequency = get_config_prop("frequency", cav.device, cav.dtype)
                        if frequency != None:
                            cav.frequency = frequency

                        elements.append(cav)

                    elif row.device in [ "SOL1", "SOL2", "SOL3" ]:
                        sol = mag.SolElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type)

                        length = get_config_prop("length", device, dtype)
                        if length != None:
                            drift_delta = (sol.length - length) / 2.0
                            get_prev_element().length += drift_delta
                            sol.length = length

                        elements.append(sol)

                    elif row.device in [ "BLM" ]:
                        elements.append(diag.BLMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "BPM" ]:
                        elements.append(diag.BPMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "BL" ]:
                        elements.append(diag.BLElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PM" ]:
                        elements.append(diag.PMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device == "BCM":
                        elements.append(diag.BCMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PORT" ]:
                        dtype = "" if row.device_type == None else row.device_type
                        subsystem = "" if row.subsystem == None else row.subsystem                      
                        elements.append(pasv.PortElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "DC", "DH" ]:
                        elements.append(mag.CorrElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "QH", "QV" ]:
                        elements.append(mag.QuadElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "S" ]:
                        elements.append(mag.HexElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "SLH" ]:
                        # use dift to represent slit for now
                        elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.device in [ "dump" ]:
                         # use dift to represent dump for now
                        elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    else:
                        raise Exception("Unsupported layout with device: '{}'".format(row.device))

                elif row.element_name != None:

                    if row.element_name in [ "bellow", "bellows", "bellow+tube", "2 bellows + tube" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            drift_delta = 0.0
                        elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "solenoid-entry", "solenoid-exit" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            drift_delta = 0.0
                        elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "coil-out", "coil-out (assumed)", "coil out", "coil out + leads" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))                

                    elif row.element_name in [ "BPM-box", "diagnostic box", "vacuum box" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name == "stripper module":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elem = get_prev_element((cs.CSElement))
                        elem.length += row.eff_length

                    elif row.element_name == "lithium film stripper":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        elem = get_prev_element((cs.CSElement))
                        elem.name = row.name
                        elem.desc = row.element_name
                        elem.system = row.system
                        elem.subsystem = row.subsystem
                        elem.device = "LFS" # NOT OFFICIAL (MISSING IN XLF)

                    else:
                        raise Exception("Unsupported layout with name: '{}'".format(row.element_name))

                elif row.eff_length != 0.0:
                    if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            drift_delta = 0.0
                    desc = "drift_{}".format(ridx+1) if row.element_name == None else row.element_name
                    elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=desc))

            except Exception as e:
                raise Exception("XLF: {}: row {}: {}".format(str(e), ridx+1, row))

        return accel.Accelerator(sequences, xlfpath)



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


    def __init__(self, row, diameter=None):
        self.system = self._cell_to_string(row[XLF_LAYOUT_SYSTEM_IDX])
        self.subsystem = self._cell_to_string(row[XLF_LAYOUT_SUBSYSTEM_IDX])
        self.position = self._cell_to_float(row[XLF_LAYOUT_POSITION_IDX])
        self.name = self._cell_to_string(row[XLF_LAYOUT_NAME_IDX])
        self.device = self._cell_to_string(row[XLF_LAYOUT_DEVICE_IDX])
        self.device_type = self._cell_to_string(row[XLF_LAYOUT_DEVICE_TYPE_IDX])
        self.element_name = self._cell_to_string(row[XLF_LAYOUT_ELEMENT_NAME_IDX])
        self.diameter = self._cell_to_float(row[XLF_LAYOUT_DIAMETER_IDX])
        self.eff_length = self._cell_to_float(row[XLF_LAYOUT_EFFECTIVE_LENGTH_IDX])


    def __str__(self):
        return type(self).__name__+str(self.__dict__)
