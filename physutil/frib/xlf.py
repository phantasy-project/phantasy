# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys, os.path, re, json, xlrd

#from ..add import accelerator as accel

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



def read_add(xlfpath, cdfpath=None, diameter=None):
    """
    Read the Accelerator Design Description from FRIB Expanded Lattice File.

    :param xlfpath: File path to Expanded Lattice File (.xlsx)
    :type xlfpath: string
    :param diameter: Default diameter to use for elements (mm)
    :type diameter: number
    :rtype Accelerator
    """

    if not os.path.isfile(xlfpath):
        raise Exception("Expanded Lattice File not found: '{}'".format(xlfpath))

    if (cdfpath != None) and not os.path.isfile(cdfpath):
        raise Exception("Cavity data file not found: '{}'".format(cdfpath))

    with open(cdfpath, "r") as f: cdf = json.load(f)
    
    wkbk = xlrd.open_workbook(xlfpath)

    if XLF_LAYOUT_SHEET_NAME not in wkbk.sheet_names():
        raise Exception("Expanded Lattice File layout not found: '{}'".format(XLF_LAYOUT_SHEET_NAME))

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

    for ridx in xrange(ridx, layout.nrows):
        row = _LayoutRow(layout.row(ridx))

        # apply default values
        if row.diameter == None:
            ##row.diameter = diameter
            row.diameter = 40

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
                if row.device in [ "GV", "FVS", "FAV"  ]:
                    elements.append(pasv.ValveElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                        system=row.system, subsystem=row.subsystem, device=row.device))

                elif row.device in [ "CAV1", "CAV2", "CAV3", "CAV4", "CAV5", "CAV6", "CAV7", "CAV8" ]:
                    m = re.match("(b\\d{2}) cavity", row.element_name)
                    if not m:
                        raise Exception("Unrecognized element name for cavity: '{}'".format(row.element_name))

                    dtype = m.group(1).upper()

                    length = row.eff_length

                    if dtype in cdf:
                        if "length" in cdf[dtype]:
                            length = cdf[dtype]["length"]
                            if length != row.eff_length:
                                delta = (row.eff_length - length) / 2.0
                                if len(elements) == 0:
                                    raise Exception("cavity: no preceeding element found")
                                elif not isinstance(elements[-1], pasv.DriftElement):
                                    raise Exception("cavity: preceeding element not drift")
                                else:
                                    elements[-1].length += delta
                                    drift_delta = delta

                    cav = rf.CavityElement(length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype)

                    if dtype in cdf:
                        if "beta" in cdf[dtype]:
                            cav.beta = cdf[dtype]["beta"]

                        if "voltage" in cdf[dtype]:
                            cav.voltage = cdf[dtype]["voltage"]

                        if "frequency" in cdf[dtype]:
                            cav.frequency = cdf[dtype]["frequency"]

                    elements.append(cav)

                elif row.device in [ "SOL1", "SOL2", "SOL3" ]:
                    dtype = row.device_type
                    length = row.eff_length
                    if row.device_type in cdf:
                        if "length" in cdf[dtype]:
                            length = cdf[dtype]["length"]
                            if length != row.eff_length:
                                delta = (row.eff_length - length) / 2.0
                                if len(elements) == 0:
                                    raise Exception("solenoid: no preceeding element found")
                                elif not isinstance(elements[-1], pasv.DriftElement):
                                    raise Exception("solenoid: preceeding element not drift")
                                else:
                                    elements[-1].length += delta
                                    drift_delta = delta

                    elements.append(mag.SolElement(length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=row.device_type))

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

                elif row.device in [ "DC", "DH", "DC0", "CH" ]: #  DC0, CH could be typo in lattice file?
                    elements.append(mag.CorrElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype))

                elif row.device in [ "QH", "QV" ]: # Horizontal VS verticle
                    elements.append(mag.QuadElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype))

                elif row.device in [ "S" ]:
                    elements.append(mag.HexElement(row.eff_length, row.diameter, row.name, desc=row.element_name,
                                                    system=row.system, subsystem=row.subsystem, device=row.device, dtype=dtype))

                elif row.device in [ "SLH" ]:
                    # use dift to represent slit for now
                    if drift_delta != 0.0:
                        raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
                    elements.append(pasv.DriftElement(row.eff_length, row.diameter, desc=row.element_name))

                elif row.device == "dump":
                     # use dift to represent dump for now
                    if drift_delta != 0.0:
                        raise Exception("Unsupported drift delta on element: {}".format(row.element_name))
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

                # elif row.element_name == "BPM-box":
                #     if len(elements) == 0:
                #         raise Exception("BPM-box: with no preceeding element")
                #
                #     elem = elements[-1]
                #     if not isinstance(elem, diag.BPMElement):
                #         raise Exception("BPM-box: does not follow BPM element")
                #
                #     if elem.length != 0.0:
                #         raise Exception("BPM-box: diagnostic element has non-zero length")
                #
                #     elem.length = row.eff_length

                # elif row.element_name == "diagnostic box":
                #     if len(elements) == 0:
                #         raise Exception("diagnostic box: with no preceeding element")
                #
                #     elem = elements[-1]
                #     if not isinstance(elem, (diag.BPMElement, diag.BLElement, diag.PMElement, pasv.PortElement)):
                #         raise Exception("diagnostic box: does not follow BPM, BL, PM or PORT")
                #
                #     if elem.length != 0.0:
                #         raise Exception("diagnostic box: diagnostic element has non-zero length")
                #
                #     elem.length = row.eff_length

                # elif row.element_name == "vacuum box":
                #     if row.eff_length > 0.0:
                #         if len(elements) == 0:
                #             raise Exception("vacuum box: with no preceeding element")
                #
                #         elem = elements[-1]
                #         if not isinstance(elem, pasv.PortElement):
                #             raise Exception("vacuum box: does not follow PORT")
                #
                #         if elem.length != 0.0:
                #             raise Exception("vacuum box: diagnostic element has non-zero length")
                #
                #         elem.length = row.eff_length

                elif row.element_name == "stripper module":
                    if len(elements) == 0:
                        elements.append(cs.CSElement(row.eff_length, row.diameter, "CHARGE_STRIPPER", desc=row.element_name))

                    elif not isinstance(elements[-1], (cs.CSElement)):
                        elements.append(cs.CSElement(row.eff_length, row.diameter, "CHARGE_STRIPPER", desc=row.element_name))

                    else:
                        elements[-1].length += row.eff_length

                elif row.element_name == "lithium film stripper":
                    if len(elements) == 0:
                        raise Exception("lithium film stripper: no preceeding elements")

                    elif not isinstance(elements[-1], (cs.CSElement)):
                        raise Exception("lithium film stripper: must follow stripper module")

                    else:
                        elem = elements[-1]
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
