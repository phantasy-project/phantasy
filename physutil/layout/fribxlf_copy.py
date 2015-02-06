# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys, os.path, re, json, xlrd

from ..config import FactoryWithConfig

from ..add import pasv, diag, mag, cs, rf, seq, accel



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

_CONFIG_DIAMETER = "diameter"

_CONFIG_SOL_INFO = "sol_info"

_CONFIG_CAV_INFO = "cav_info"



def build_accel(xlfpath, confpath):
    """
    Convenience method for building ADD from Expanded Lattice File.
    """

    accel_factory = AccelFactory(xlfpath)

    with open(confpath, "r") as fp:
        config = json.load(fp)

        if _CONFIG_DIAMETER in config:
            accel_factory.diamter = config[_CONFIG_DIAMETER]

        if _CONFIG_CAV_INFO in config:
            for (dtype, cav_info) in config[_CONFIG_CAV_INFO].iteritems():
                accel_facotry.add_cav(dtype, **cav_info)

        if _CONFIG_SOL_INFO in config:
            for (dtype, sol_info) in config[_CONFIG_SOL_INFO].iteritems():
                accel_factory.add_sol_info(dtype, **sol_info)

    return accel_factory.build()


class AccelFactory(object):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.

    :param xlfpath: File path to Expanded Lattice File (.xlsx)
    :type xlfpath: string
    :param diameter: Default diameter to use for elements (mm)
    :type diameter: number
    :rtype Accelerator
    """

    def __init__(self, xlfpath="", diameter=40.0):
        super(AccelFactory, self).__init__(config)
        self.xlfpath = xlfpath
        self.diameter = diameter
        self._cav_info = {}
        self._sol_info = {}


    @property
    def xlfpath(self):
        return self._xlfpath

    @xlfpath.setter
    def xlfpath(self, xlfpath):
        if not isinstance(cavity_info, str):
            raise TypeError("AccelFactory: 'xlfpath' property must be type a string")
        self._xlfpath = xlfpath


    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, _diameter):
        if not isinstance(cavity_info, (int, float)):
            raise TypeError("AccelFactory: 'diameter' property must be type a number")
        self._diameter = _diameter


    def get_sol_info(self, dtype):
        return self._sol_info[dtype]

    def has_sol_info(self, dtype):
        return (dtype in self._sol_info)

    def add_sol_info(self, dtype, *, length=None, **kw):
        self._sol_info[dtype] = _SolInfo(length)


    def get_cav_info(self, dtype):
        return self._sol_info[dtype]

    def has_cav_info(self, dtype):
        return (dtype in self._sol_info)

    def add_cav_info(self, dtype, *, beta, voltage, frequency, length=None, **kw):
        self._sol_info[dtype] = _SolInfo(beta, voltage, frequency, length)


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

        accelerator = accel.Accelerator(self.xlfpath)

        sequence = None

        subsequence = None

        drift_delta = 0.0

        def get_prev_element(allow_types=(pasv.DriftElement,)):
            if len(subsequence.elements) == 0:
                raise Exception("AccelFactory: previous element not found")
            elif not isinstance(elements[-1], allow_types):
                raise Exception("AccelFactory: previous element type invalid")
            return subsequence.elements[-1]

        for ridx in xrange(ridx, layout.nrows):
            row = _LayoutRow(layout.row(ridx))

            # skip rows without length
            if row.eff_length == None:
                continue

            # apply default values
            if row.diameter == None:
                row.diameter = self.diameter

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


            if subseqence == None:
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
                        subsequence.append(pasv.ValveElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                            system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "CAV1", "CAV2", "CAV3", "CAV4", "CAV5", "CAV6", "CAV7", "CAV8" ]:
                        m = re.match("(b\\d{2}) cavity", row.element_name)
                        if not m:
                            raise Exception("Unrecognized element name for cavity: '{}'".format(row.element_name))

                        dtype = m.group(1).upper()

                        cav = rf.CavityElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype)

                        if self.has_cav_info(dtype):
                            cav_info = self.get_cav_info(dtype)
                            cav.beta = cav_info.beta
                            cav.voltage = cav_info.voltage
                            cav.frequency = cav_info.frequency
                            if cav_info.has_length():
                                drift_delta = (cav.length - cav_info.length) / 2.0
                                get_prev_element().length += drift_delta
                                cav.length -= drift_delta * 2.0
                        else:
                            raise Exception("Cavity information not found: {}".format(cav.name))

                        subseqence.append(cav)

                    elif row.device in [ "SOL1", "SOL2", "SOL3" ]:
                        dtype = "SOL_" + row.device_type 

                        sol = mag.SolElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype)

                        if self.has_sol_info(dtype):
                            sol_info = self.get_sol_info(dtype)
                            if sol_info.has_length():
                                drift_delta = (sol.length - sol_info.length) / 2.0
                                get_prev_element().length += drift_delta
                                sol.length -= drift_delta * 2.0

                        subsequence.append(sol)

                    elif row.device in [ "BLM" ]:
                        subsequence.append(diag.BLMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device))

                    elif row.device in [ "BPM" ]:
                        subsequence.append(diag.BPMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "BL" ]:
                        subsequence.append(diag.BLElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PM" ]:
                        subsequence.append(diag.PMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device == "BCM":
                        subsequence.append(diag.BCMElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "PORT" ]:
                        dtype = "" if row.device_type == None else row.device_type
                        subsystem = "" if row.subsystem == None else row.subsystem                      
                        subsequence.append(pasv.PortElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=subsystem, device=row.device, dtype=dtype))

                    elif row.device in [ "DC", "DH", "DC0", "CH" ]:
                        subsequence.append(mag.CorrElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "QH", "QV" ]:
                        subsequence.append(mag.QuadElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "S" ]:
                        subsequence.append(mag.HexElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

                    elif row.device in [ "SLH" ]:
                        # use dift to represent slit for now
                        subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.device in [ "dump" ]:
                         # use dift to represent dump for now
                        subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    else:
                        raise Exception("Unsupported layout with device: '{}'".format(row.device))

                elif row.element_name != None:

                    if row.element_name in [ "bellow", "bellows", "bellow+tube", "2 bellows + tube" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            drift_delta = 0.0
                        subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "solenoid-entry", "solenoid-exit" ]:
                        if drift_delta != 0.0:
                            row.eff_length += drift_delta
                            drift_delta = 0.0
                        subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name in [ "coil-out", "coil-out (assumed)", "coil out", "coil out + leads" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))                

                    elif row.element_name in [ "BPM-box", "diagnostic box", "vacuum box" ]:
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                    elif row.element_name == "stripper module":
                        if drift_delta != 0.0:
                            raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                        try:
                            get_prev_element((cs.CSElement)).length += row.eff_length
                        except:
                            subsequence.append(cs.CSElement(row.eff_length, row.diameter, "CHARGE STRIPPER", desc=row.element_name))

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
                    subsequence.append(pasv.DriftElement(row.eff_length, row.diameter, desc=desc))

            except Exception as e:
                raise Exception("AccelFactory: {}: row {}: {}".format(str(e), ridx+1, row))

        return accel.Accelerator(sequences, self.xlfpath)


class _CavInfo(object):

    def __init__(self, beta, frequency, voltage, length=None, **kw):
        self.beta = beta
        self.voltage = voltage
        self.frequency = frequency
        self.length = length

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, beta):
        if not isinstance(beta, (int, float)):
            raise TypeError("_CavInfo: 'beta' property must be type a number")
        self._beta = beta

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        if not isinstance(voltage, (int, float)):
            raise TypeError("_CavInfo: 'voltage' property must be type a number")
        self._voltage = voltage

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("_CavInfo: 'frequency' property must be type a number")
        self._frequency = frequency

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if (length != None) and not isinstance(length, (int, float)):
            raise TypeError("_CavInfo: 'length' property must be type a number or None")
        self._length = length

    def has_length():
        return isinstance(self.length, (int, float))


class _SolInfo(object):

    def __init__(self, length=None):
        self.length = length

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if (length != None) and not isinstance(length, (int, float)):
            raise TypeError("_CavInfo: 'length' property must be type a number or None")
        self._length = length

    def has_length():
        return isinstance(self.length, (int, float))



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
