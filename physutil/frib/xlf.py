# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys, os.path, re, json, xlrd

from ..config import FactoryWithConfig

from ..add import pasv, diag, mag, cs, rf, seq, accel



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



class AccelFactory(FactoryWithConfig):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.

    :param xlfpath: File path to Expanded Lattice File (.xlsx)
    :type xlfpath: string
    :param diameter: Default diameter to use for elements (mm)
    :type diameter: number
    :rtype Accelerator
    """

    _CONFIG_OPT_LENGTH = "length"

    _CONFIG_OPT_DIAMETER = "diameter"

    _CONFIG_OPT_BETA = "beta"

    _CONFIG_OPT_VOLTAGE = "voltage"
                        
    _CONFIG_OPT_FREQUENCY = "frequency"

    _CONFIG_OPT_CHAN_PHASE = "channel_phase"
                        
    _CONFIG_OPT_CHAN_AMPLITUDE = "channel_amplitude"


    def __init__(self, xlfpath, config=None):
        super(AccelFactory, self).__init__(config)
        self.xlfpath = xlfpath


    def build(self):
        
        if not os.path.isfile(self.xlfpath):
            raise Exception("AccelFactory: Expanded Lattice File not found: '{}'".format(self.xlfpath))
  
        wkbk = xlrd.open_workbook(self.xlfpath)

        if XLF_LAYOUT_SHEET_NAME not in wkbk.sheet_names():
            raise Exception("AccelFactory: Expanded Lattice File layout not found: '{}'".format(XLF_LAYOUT_SHEET_NAME))

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
                raise Exception("AccelFactory: previous element not found")
            elif not isinstance(elements[-1], allow_types):
                raise Exception("AccelFactory: previous element type invalid")
            return elements[-1]

        for ridx in xrange(ridx, layout.nrows):
            row = _LayoutRow(layout.row(ridx))

            # apply default values
            if (row.diameter == None) and self.config.has_default(self._CONFIG_OPT_DIAMETER):
                row.diameter = self.config.getfloat_default(self._CONFIG_OPT_DIAMETER)

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

                    if (drift_delta != 0.0) and (row.eff_length != 0.0):
                        # these 'named' elements do not support non-zero drift delta
                        raise Exception("Unsupported drift delta on element: {}".format(row.element_name))

                    elif row.device in [ "GV", "FVS", "FAV"  ]:
                        elements.append(pasv.ValveElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "CAV1", "CAV2", "CAV3", "CAV4", "CAV5", "CAV6", "CAV7", "CAV8" ]:
                        m = re.match("(b\\d{2}) cavity", row.element_name)
                        if not m:
                            raise Exception("Unrecognized element name for cavity: '{}'".format(row.element_name))

                        dtype = "CAV_" + m.group(1).upper()

                        cav = rf.CavityElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype)

                        if self.config.has_option(dtype, self._CONFIG_OPT_LENGTH):
                            drift_delta = (cav.length - self.config.getfloat(dtype, self._CONFIG_OPT_LENGTH)) / 2.0
                            get_prev_element().length += drift_delta
                            cav.length -= drift_delta * 2.0

                        if self.config.has_option(dtype, self._CONFIG_OPT_BETA):
                            cav.beta = self.config.getfloat(dtype, self._CONFIG_OPT_BETA)
                        else:
                            raise Exception("Cavity parameter '{}' not found".format(self._CONFIG_OPT_BETA))

                        if self.config.has_option(dtype, self._CONFIG_OPT_VOLTAGE):
                            cav.voltage = self.config.getfloat(dtype, self._CONFIG_OPT_VOLTAGE)
                        else:
                            raise Exception("Cavity parameter '{}' not found".format(self._CONFIG_OPT_VOLTAGE))
                        
                        if self.config.has_option(dtype, self._CONFIG_OPT_FREQUENCY):
                            cav.frequency = self.config.getfloat(dtype, self._CONFIG_OPT_FREQUENCY)
                        else:
                            raise Exception("Cavity parameter '{}' not found".format(self._CONFIG_OPT_FREQUENCY))

                        if self.config.has_option(dtype, self._CONFIG_OPT_CHAN_PHASE):
                            cav.channels.phase = self.config.get(dtype, self._CONFIG_OPT_CHAN_PHASE).format(elem=cav)
                        else:
                            raise Exception("Cavity parameter '{}' not found".format(self._CONFIG_OPT_CHAN_PHASE))

                        if self.config.has_option(dtype, self._CONFIG_OPT_CHAN_AMPLITUDE):
                            cav.channels.amplitude = self.config.get(dtype, self._CONFIG_OPT_CHAN_AMPLITUDE).format(elem=cav)
                        else:
                            raise Exception("Cavity parameter '{}' not found".format(self._CONFIG_OPT_CHAN_AMPLITUDE))

                        elements.append(cav)

                    elif row.device in [ "SOL1", "SOL2", "SOL3" ]:
                        dtype = "SOL_" + row.device_type 

                        sol = mag.SolElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype)

                        if self.config.has_option(dtype, self._CONFIG_OPT_LENGTH):
                            drift_delta = (sol.length - self.config.getfloat(dtype, self._CONFIG_OPT_LENGTH)) / 2.0
                            get_prev_element().length += drift_delta
                            sol.length -= drift_delta * 2.0

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

                    elif row.device in [ "DC", "DH", "DC0", "CH" ]:
                        elements.append(mag.CorrElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "QH", "QV" ]:
                        elements.append(mag.QuadElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "S" ]:
                        elements.append(mag.HexElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

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
                        try:
                            get_prev_element((cs.CSElement)).length += row.eff_length
                        except:
                            elements.append(cs.CSElement(row.eff_length, row.diameter, "CHARGE STRIPPER", desc=row.element_name))

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
                raise Exception("AccelFactory: {}: row {}: {}".format(str(e), ridx+1, row))

        return accel.Accelerator(sequences, self.xlfpath)



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
