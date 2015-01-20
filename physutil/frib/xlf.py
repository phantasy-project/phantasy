# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys, os.path, xlrd


class AccelFactory(object):

    XLF_LAYOUT_SHEET_START = 8

    XLF_LAYOUT_SHEET_NAME = "LatticeLayout"

    def __init__(self, xlfpath):
        self.xlfpath = xlfpath

    def create(self):

        if not os.path.isfile(self.xlfpath):
            raise Exception("XLF: not found: {}".format(self.xlfpath))

        wkbk = xlrd.open_workbook(self.xlfpath)

        return self._read_layout(wkbk)


    def _read_layout(self, wkbk):

        if self.XLF_LAYOUT_SHEET_NAME not in wkbk.sheet_names():
            raise Exception("Expanded Lattice File layout sheet not found: {}".format(self.XLF_LAYOUT_SHEET_NAME))

        sheet = wkbk.sheet_by_name(self.XLF_LAYOUT_SHEET_NAME)

        # skip front-end, perhaps this should be read too?
        for ridx in xrange(self.XLF_LAYOUT_SHEET_START, sheet.nrows):
            row = _LayoutRow(sheet.row(ridx))
            if row.system == "LS1": break

        print(ridx)
        elements = []

        seqname = None
        sequences = []

        subseqname = None
        subsequences = []

        for ridx in xrange(ridx, sheet.nrows):
            row = _LayoutRow(sheet.row(ridx))

            if row.elementLength == None:
                continue

            if subseqname == None:
                if row.subsystem != None:
                    subsysname = row.subsystem
                else:
                    raise Exception()

            elif (row.subsystem != None) and (row.subsystem != subseqname):
                subsequences.append(SeqElement(elements, name=subseqname))
                elements = []


            if seqname == None:
                if row.system != None:
                    seqname = row.system
                else:
                    raise Exception()

            elif (row.system != None) and (row.system != seqname):
                sequences.append(SeqElement(subsequences, name=seqname))
                subsequences = []

            if row.system == None:
                if row.elementName in [ "bellow", "bellows" ]:
                    elements.append(DriftElement(row.elementLength))
                else:
                    raise Exception("Unsupported layout data (Row: {}): {}".format(ridx+1,row))


                elements.append()

            else:
                if row.device == "GV":
                    elements.append(ValveElement(row.elementLength))

                else:
                    raise Exception("Unsupported layout data (Row: {}): {}".format(ridx+1,row))


        return Accelerator(sequences)


class _LayoutRow(object):

    XLF_LAYOUT_SYSTEM_IDX = 0

    XLF_LAYOUT_SUBSYSTEM_IDX = 1

    XLF_LAYOUT_DEVICE_IDX = 2

    XLF_LAYOUT_POSITION_IDX = 3

    XLF_LAYOUT_NAME_IDX = 4

    XLF_LAYOUT_DEVICE_TYPE_IDX = 5

    XLF_LAYOUT_ELEMENT_NAME_IDX = 6

    XLF_LAYOUT_DIAMETER_IDX = 7

    XLF_LAYOUT_EFFECTIVE_LENGTH = 10

    def __init__(self, row):
        self.system = self._read_string(row[self.XLF_LAYOUT_SYSTEM_IDX])
        self.subsystem = self._read_string(row[self.XLF_LAYOUT_SUBSYSTEM_IDX])
        self.position = self._read_float(row[self.XLF_LAYOUT_POSITION_IDX])
        self.name = self._read_string(row[self.XLF_LAYOUT_NAME_IDX])
        self.device = self._read_string(row[self.XLF_LAYOUT_DEVICE_IDX])
        self.deviceType = self._read_string(row[self.XLF_LAYOUT_DEVICE_TYPE_IDX])
        self.elementName = self._read_string(row[self.XLF_LAYOUT_ELEMENT_NAME_IDX])
        self.diameter = self._read_float(row[self.XLF_LAYOUT_DIAMETER_IDX])
        self.elementLength = self._read_float(row[self.XLF_LAYOUT_EFFECTIVE_LENGTH])


    def _read_string(self, cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            return cell.value
        else:
            return None


    def _read_float(self, cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            try:
                return float(cell.value)
            except:
                return None
        elif cell.ctype == xlrd.XL_CELL_NUMBER:
            return cell.value
        else:
            return None

    def __str__(self):
        return "{{ system:'{}', subsystem:'{}', elementName:'{}'".format(self.system, self.subsystem, self.elementName)
